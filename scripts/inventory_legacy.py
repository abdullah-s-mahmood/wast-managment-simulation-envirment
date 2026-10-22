#!/usr/bin/env python3
"""Private, read-only tar inventory. Never extracts, follows links or runs content.

Findings prohibit acceptance. Detection is bounded, not proof of absent secrets.
The manifest contains member paths and MUST remain in restricted local storage.
"""
import argparse,gzip,hashlib,json,re,tarfile,time
from pathlib import Path,PurePosixPath

DEFAULTS=json.loads((Path(__file__).resolve().parents[1]/'docs/audit/intake_limits.json').read_text())
SECRET=re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{20,}|\bAKIA[A-Z0-9]{16}|\bgithub_pat_[A-Za-z0-9_]{20,}')

class LimitError(ValueError):pass

class Bounded:
    """Count all expanded bytes, including skipped payloads and extended headers."""
    def __init__(self,stream,limits,start):self.stream,self.limits,self.start,self.count=stream,limits,start,0
    def read(self,size=-1):
        if time.monotonic()-self.start>self.limits['max_seconds']:raise LimitError('time_limit')
        if size<0 or self.count+size>self.limits['max_expanded_bytes']:raise LimitError('expanded_limit')
        data=self.stream.read(size);self.count+=len(data);return data

def role(name):
    parts={p.lower() for p in PurePosixPath(name).parts};suffix=PurePosixPath(name).suffix.lower()
    for labels,kind in [({'results','output','outputs','build'},'generated_output'),
                        ({'cache','__pycache__','.cache'},'cache'),
                        ({'vendor','third_party','node_modules','dependencies'},'dependency'),
                        ({'tests','test'},'test'),({'data','datasets'},'dataset')]:
        if parts&labels:return kind
    return {'.h':'header','.hpp':'header','.py':'source','.cpp':'source','.c':'source',
            '.cc':'source','.rs':'source','.json':'configuration','.yaml':'configuration',
            '.yml':'configuration','.toml':'configuration','.csv':'dataset'}.get(suffix,'document_or_unknown')

def inspect(path,limits):
    """Return deterministic ordered manifest with incomplete status on any limit/error.

Per-member hashes cover regular-file bytes only. Binary/signature checks process
chunks with overlap; findings record codes, never content snippets. Classification
is a path/suffix heuristic, not dependency or scientific interpretation.
"""
    if set(limits)!=set(DEFAULTS) or any(type(v)is not int or v<=0 for v in limits.values()):
        raise ValueError('invalid resource policy')
    result={'schema_version':1,'complete':False,'members':[],'findings':[],'archive_sha256':None,'compressed_bytes':None,'expanded_bytes_read':0}
    start=time.monotonic();seen=set();folded=set();bounded=None
    try:
        before=path.stat();result['compressed_bytes']=before.st_size
        if before.st_size>limits['max_compressed_bytes']:raise LimitError('compressed_limit')
        with path.open('rb') as raw:
            result['archive_sha256']=hashlib.file_digest(raw,'sha256').hexdigest();raw.seek(0)
            with gzip.GzipFile(fileobj=raw) as expanded:
                bounded=Bounded(expanded,limits,start)
                with tarfile.open(fileobj=bounded,mode='r|',bufsize=10240) as archive:
                    for index,member in enumerate(archive):
                        if index>=limits['max_members']:raise LimitError('member_count_limit')
                        name=member.name;pure=PurePosixPath(name)
                        unsafe=(not name or pure.is_absolute() or '\\' in name or ':' in name
                                or any(x in ('..','') for x in name.split('/'))
                                or any(ord(c)<32 for c in name))
                        if unsafe:raise LimitError('unsafe_member_path')
                        key=str(pure)
                        if key in seen or key.casefold() in folded:raise LimitError('duplicate_or_case_collision')
                        seen.add(key);folded.add(key.casefold())
                        if not(member.isfile() or member.isdir()):
                            result['rejected_member']={'path':key,'type_hex':member.type.hex(),'link_target':member.linkname}
                            raise LimitError('link_or_special_member')
                        if member.size>limits['max_member_bytes']:raise LimitError('member_size_limit')
                        flags=[];digest=None
                        if member.isfile():
                            sha=hashlib.sha256();tail=b'';binary=False
                            stream=archive.extractfile(member) # in-memory stream, never filesystem extraction
                            while True:
                                chunk=stream.read(65536)
                                if not chunk:break
                                sha.update(chunk);probe=tail+chunk
                                if SECRET.search(probe) and 'potential_secret' not in flags:flags.append('potential_secret')
                                if b'\0' in chunk:binary=True
                                if sha.digest_size and not tail:
                                    if chunk.startswith((b'\x7fELF',b'MZ')):flags.append('executable_signature')
                                    if chunk.startswith((b'PK\x03\x04',b'\x1f\x8b',b'7z\xbc\xaf')):flags.append('nested_archive')
                                tail=probe[-256:]
                            digest=sha.hexdigest()
                            if binary:flags.append('binary_content')
                            if member.mode&0o111:flags.append('executable_permission')
                        result['members'].append({'path':key,'bytes':member.size,'sha256':digest,
                            'content_type':'binary' if member.isfile() and binary else 'text_or_directory',
                            'role':'binary' if member.isfile() and binary and role(key)=='document_or_unknown' else role(key),'language_hint':pure.suffix.lower() or 'unknown',
                            'kind':'file' if member.isfile() else 'directory','flags':flags,
                            'provenance':'archive_sha256 + path; owner-authorized local audit only'})
                        for flag in flags:result['findings'].append({'member_index':index,'code':flag})
                # Drain gzip for CRC/truncation/trailing data and resource accounting.
                while bounded.read(65536):pass
        after=path.stat()
        if (before.st_size,before.st_mtime_ns,before.st_ino)!=(after.st_size,after.st_mtime_ns,after.st_ino):
            raise LimitError('archive_changed')
        result['complete']=True
    except (OSError,EOFError,tarfile.TarError,ValueError) as error:
        result['findings'].append({'member_index':None,'code':str(error) if isinstance(error,LimitError) else 'corrupt_or_unreadable_archive'})
    if bounded:result['expanded_bytes_read']=bounded.count
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path);parser.add_argument('--limits',type=Path,required=True)
    args=parser.parse_args()
    result=inspect(args.archive,json.loads(args.limits.read_text()))
    print(json.dumps(result,sort_keys=True,indent=2))
    raise SystemExit(0 if result['complete'] and not result['findings'] else 1)
