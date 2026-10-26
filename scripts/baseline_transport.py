"""Bounded data-only transport for private baseline outputs; never execute files.

Used after target termination in an isolated namespace. Caller must ensure no
concurrent writers. No TAR/extract semantics, links, special files or archive-
selected host paths. Complete transport does not mean a successful simulation.
"""
import base64
import hashlib
import json
import os
from pathlib import Path,PurePosixPath
import stat

MAX_BYTES=67108864
MAX_FILE_BYTES=16777216
MAX_ENTRIES=64
MAX_TRANSPORT_BYTES=90000000


def safe_name(name):
    """Portable nonempty relative name with bounded UTF-8 metadata."""
    return (isinstance(name,str) and 0<len(name.encode('utf-8'))<=1024
            and not PurePosixPath(name).is_absolute() and '\\' not in name
            and all(p not in ('','.','..') for p in name.split('/')))


def pack(root,process):
    """Collect at most 64 regular files/64 MiB, rejecting links and changes."""
    root=Path(root);files=[];seen=set();total=0
    if root.is_symlink() or not root.is_dir():raise ValueError('invalid export root')
    for index,path in enumerate(root.rglob('*')):
        if index>=MAX_ENTRIES:raise ValueError('export count limit')
        info=path.lstat();name=str(path.relative_to(root))
        if not safe_name(name) or name.casefold() in seen:raise ValueError('export name collision')
        seen.add(name.casefold())
        if stat.S_ISDIR(info.st_mode):continue
        if not stat.S_ISREG(info.st_mode) or info.st_nlink!=1:raise ValueError('export link/special')
        if info.st_size>MAX_FILE_BYTES:raise ValueError('export member size')
        total+=info.st_size
        if total>MAX_BYTES:raise ValueError('export total size')
        fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW)
        with os.fdopen(fd,'rb') as stream:
            opened=os.fstat(stream.fileno());data=stream.read(MAX_FILE_BYTES+1);after=os.fstat(stream.fileno())
        stamp=lambda s:(s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)
        if stamp(info)!=stamp(opened) or stamp(opened)!=stamp(after) or len(data)!=info.st_size:
            raise ValueError('export changed while reading')
        files.append({'path':name,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),
                      'base64':base64.b64encode(data).decode('ascii')})
    return {'schema_version':1,'complete':True,'process':process,'files':files}


def decode(packet,destination):
    """Validate complete data/hash/path scope before exclusively publishing files.

Returns process metadata; callers independently validate process exit and actual
baseline artifacts. Private parent must be owned and mode 0700. Invalid packets
publish nothing; failed filesystem publication may leave partial private evidence.
"""
    root=Path(destination)
    if (root.exists() or root.is_symlink() or root.parent.is_symlink()
            or root.parent.stat().st_uid!=os.getuid() or root.parent.stat().st_mode & 0o077):
        raise ValueError('new private destination required')
    if (not isinstance(packet,dict) or set(packet)!={'schema_version','complete','process','files'}
            or type(packet['schema_version']) is not int or packet['schema_version']!=1
            or packet['complete'] is not True or not isinstance(packet['process'],dict)
            or not isinstance(packet['files'],list) or len(packet['files'])>MAX_ENTRIES):
        raise ValueError('invalid transport schema')
    staged={};folded=set();prefixes={};total=0
    for record in packet['files']:
        if not isinstance(record,dict) or set(record)!={'path','bytes','sha256','base64'}:
            raise ValueError('invalid member record')
        name=record['path'];size=record['bytes']
        if (not safe_name(name) or name.casefold() in folded or type(size) is not int
                or not 0<=size<=MAX_FILE_BYTES or not isinstance(record['base64'],str)
                or len(record['base64'])>4*((MAX_FILE_BYTES+2)//3)):
            raise ValueError('invalid transport member')
        for prefix in [PurePosixPath(name),*PurePosixPath(name).parents]:
            if str(prefix)=='.':continue
            key=str(prefix).casefold()
            if key in prefixes and prefixes[key]!=str(prefix):raise ValueError('case-colliding directory')
            prefixes[key]=str(prefix)
        total+=size
        if total>MAX_BYTES:raise ValueError('transport total size')
        folded.add(name.casefold())
        try:data=base64.b64decode(record['base64'],validate=True)
        except (ValueError,TypeError):raise ValueError('invalid encoded content') from None
        if len(data)!=size or hashlib.sha256(data).hexdigest()!=record['sha256']:
            raise ValueError('transport hash/size mismatch')
        staged[name]=data
    # A file cannot also be another file's directory.
    if any(str(parent) in staged for name in staged for parent in PurePosixPath(name).parents if str(parent)!='.'):
        raise ValueError('transport path conflict')
    root.mkdir(mode=0o700)
    for name,data in staged.items():
        path=root/name;path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o400)
        with os.fdopen(fd,'wb') as stream:stream.write(data)
    return packet['process']
