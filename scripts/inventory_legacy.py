#!/usr/bin/env python3
"""Inventory TAR/GZIP privately without extraction or link dereferencing.

Completion describes parsing and accounting only. Quarantine, reuse authorization
and scientific validation remain separate. Manifest paths/targets are private.
"""
import argparse
import codecs
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import tarfile
import time
import zlib

ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = json.loads((ROOT/'docs/audit/intake_limits.json').read_text())
SECRET = re.compile(rb'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{20,}|\bAKIA[A-Z0-9]{16}|\bgithub_pat_[A-Za-z0-9_]{20,}')


class LimitError(ValueError):
    """A resource/identity/integrity boundary prevents inventory completion."""


def deadline(limits, start):
    if time.monotonic()-start > limits['max_seconds']:
        raise LimitError('time_limit')


class Bounded:
    """Account for every expanded byte, including TAR headers, padding and skips."""
    def __init__(self, stream, limits, start):
        self.stream, self.limits, self.start = stream, limits, start
        self.count, self.tail = 0, b''

    def read(self, size=-1):
        deadline(self.limits, self.start)
        remaining = self.limits['max_expanded_bytes']-self.count
        if size < 0:
            raise LimitError('unbounded_read')
        # One-byte lookahead distinguishes an exact budget ending at EOF.
        data = self.stream.read(min(size, remaining+1))
        if len(data) > remaining:
            raise LimitError('expanded_limit')
        self.count += len(data)
        self.tail = (self.tail+data)[-65536:]
        return data

    def suffix_at(self, offset):
        start = self.count-len(self.tail)
        if not start <= offset <= self.count:
            raise LimitError('unverified_tar_terminator')
        return self.tail[offset-start:]


def role(name):
    """Path/suffix hints only; no inferred scientific or dependency semantics."""
    parts = {p.lower() for p in PurePosixPath(name).parts}
    for labels, kind in [({'results','output','outputs','build'},'generated_output'),
                         ({'cache','__pycache__','.cache'},'cache'),
                         ({'vendor','third_party','node_modules','dependencies'},'dependency'),
                         ({'tests','test'},'test'), ({'data','datasets'},'dataset')]:
        if parts & labels:
            return kind
    return {'.h':'header','.hpp':'header','.py':'source','.cpp':'source','.c':'source',
            '.cc':'source','.rs':'source','.json':'configuration','.yaml':'configuration',
            '.yml':'configuration','.toml':'configuration','.csv':'dataset'}.get(
                PurePosixPath(name).suffix.lower(),'document_or_unknown')


def path_flags(name):
    parts = name.split('/')
    return ['unsafe_member_path'] if (
        not name or PurePosixPath(name).is_absolute() or '\\' in name or ':' in name
        or any(p in ('..','') for p in parts) or any(ord(c)<32 for c in name)) else []


def canonical_digest(value):
    """Canonical UTF-8 JSON integrity digest; not an authenticity signature."""
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()


def verify_manifest(result):
    copied = dict(result)
    digest = copied.pop('manifest_sha256', None)
    return digest == canonical_digest(copied)


def full_hash(stream, limits, start):
    stream.seek(0)
    digest = hashlib.sha256()
    while True:
        deadline(limits, start)
        chunk = stream.read(65536)
        if not chunk:
            break
        digest.update(chunk)
    return digest.hexdigest()


def inspect(path, limits, *, expected_sha256=None, expected_size=None):
    """Return v2 ordered manifest; quarantine never grants reuse or execution.

All parsed members get unique entry IDs. Regular payloads are hashed in chunks,
including quarantined paths. Links/special members are metadata only; their
content/targets are never opened. Parser corruption, identity changes or resource
exhaustion stop the inventory with explicit incomplete status and retained prefix.
Memory/CPU hard limits must enclose library calls; the Linux CLI enforces them.
"""
    if (not isinstance(limits,dict) or set(limits)!=set(DEFAULTS)
            or any(type(v) is not int or v<=0 for v in limits.values())):
        raise ValueError('invalid resource policy')
    result = dict(schema_version=2,complete=False,inventory_status='incomplete',
                  security_findings_present=False,security_clearance='not_granted',
                  quarantine_count=0,source_reuse_authorization='prohibited',
                  scientific_model_validation='unvalidated',members=[],findings=[],
                  archive_sha256=None,archive_sha256_after=None,identity_verified=False,
                  compressed_bytes=None,expanded_bytes_read=0,resource_policy=dict(limits))
    start, seen, folded, bounded = time.monotonic(), {}, {}, None
    try:
        with Path(path).open('rb') as raw:
            before = os.fstat(raw.fileno())
            result['compressed_bytes'] = before.st_size
            if before.st_size > limits['max_compressed_bytes']:
                raise LimitError('compressed_limit')
            result['archive_sha256'] = full_hash(raw,limits,start)
            if ((expected_size is not None and before.st_size != expected_size)
                    or (expected_sha256 is not None and result['archive_sha256'] != expected_sha256)):
                raise LimitError('baseline_identity_mismatch')
            raw.seek(0)

            class GuardedInfo(tarfile.TarInfo):
                def _proc_pax(self, archive):
                    if self.size > limits['max_metadata_bytes']:
                        raise LimitError('metadata_size_limit')
                    return super()._proc_pax(archive)
                def _proc_gnulong(self, archive):
                    if self.size > limits['max_metadata_bytes']:
                        raise LimitError('metadata_size_limit')
                    return super()._proc_gnulong(archive)
                def _proc_sparse(self, archive):
                    raise LimitError('unsupported_sparse_encoding')

            with gzip.GzipFile(fileobj=raw) as expanded:
                bounded = Bounded(expanded,limits,start)
                # Stream mode avoids filesystem semantics. Errorlevel does not
                # control parsing: errors are caught below, never retried as success.
                with tarfile.open(fileobj=bounded,mode='r|',bufsize=10240,tarinfo=GuardedInfo) as archive:
                    for index, member in enumerate(archive):
                        deadline(limits,start)
                        if index >= limits['max_members']:
                            raise LimitError('member_count_limit')
                        if member.size > limits['max_member_bytes']:
                            raise LimitError('member_size_limit')
                        if member.issparse():
                            raise LimitError('unsupported_sparse_encoding')
                        name = member.name
                        key = str(PurePosixPath(name))
                        flags = path_flags(name)
                        kind = ('file' if member.isfile() else 'directory' if member.isdir()
                                else 'symlink' if member.issym() else 'hardlink' if member.islnk() else 'special')
                        record = dict(entry_id=f'entry-{index:08d}',path=name,bytes=member.size,
                                      type_hex=member.type.hex(),kind=kind,sha256=None,
                                      content_type='not_read',role=role(name),
                                      language_hint=PurePosixPath(name).suffix.lower() or 'unknown',
                                      flags=flags,quarantined=False,
                                      provenance='archive_sha256 + entry_id + path; local audit only')
                        # Mark all colliding entries, including earlier occurrences.
                        for mapping, lookup, code in ((seen,key,'duplicate_member_path'),
                                                       (folded,key.casefold(),'case_collision')):
                            if lookup in mapping:
                                for prior in mapping[lookup]:
                                    if code not in prior['flags']:
                                        prior['flags'].append(code)
                                flags.append(code)
                            mapping.setdefault(lookup,[]).append(record)
                        if member.issym() or member.islnk():
                            record['link_target'] = member.linkname
                            flags.append('link_quarantined')
                            base = posixpath.dirname(name) if member.issym() else ''
                            resolved = posixpath.normpath(posixpath.join(base,member.linkname))
                            root = name.split('/')[0]
                            if (path_flags(member.linkname) or
                                    not(resolved==root or resolved.startswith(root+'/'))):
                                flags.append('unsafe_link_target')
                        elif not(member.isfile() or member.isdir()):
                            flags.append('special_member_quarantined')
                        if member.isfile():
                            sha, tail, first, binary = hashlib.sha256(), b'', True, False
                            decoder = codecs.getincrementaldecoder('utf-8')('strict')
                            # Only regular bytes: extractfile is an in-memory
                            # payload stream, never extract/extractall or link access.
                            payload = archive.extractfile(member)
                            while True:
                                deadline(limits,start)
                                chunk = payload.read(65536)
                                if not chunk:
                                    break
                                sha.update(chunk)
                                probe = tail+chunk
                                if ('potential_secret' not in flags
                                        and any(marker in probe for marker in (b'-----BEGIN ',b'ghp_',b'gho_',b'ghu_',b'ghs_',b'ghr_',b'AKIA',b'github_pat_'))
                                        and SECRET.search(probe)):
                                    flags.append('potential_secret')
                                binary |= b'\0' in chunk
                                if decoder is not None:
                                    try:
                                        decoder.decode(chunk)
                                    except UnicodeDecodeError:
                                        binary, decoder = True, None
                                if first:
                                    if chunk.startswith((b'\x7fELF',b'MZ')):
                                        flags.append('executable_signature')
                                    if chunk.startswith((b'PK\x03\x04',b'\x1f\x8b',b'7z\xbc\xaf')):
                                        flags.append('nested_archive')
                                first, tail = False, probe[-256:]
                            if decoder is not None:
                                try:
                                    decoder.decode(b'',final=True)
                                except UnicodeDecodeError:
                                    binary = True
                            record['sha256'] = sha.hexdigest()
                            record['content_type'] = 'binary' if binary else 'text_or_unknown'
                            if binary:
                                flags.append('binary_content')
                                if record['role']=='document_or_unknown':
                                    record['role']='binary'
                            if member.mode & 0o111:
                                flags.append('executable_permission')
                        result['members'].append(record)
                    end_offset = archive.offset
                    suffix = bounded.suffix_at(end_offset)
                    if any(suffix):
                        raise LimitError('nonzero_tar_trailer')
                # Require two zero TAR terminators and validate the complete gzip
                # CRC/footer. Never ignore a second concatenated TAR after EOF.
                while True:
                    chunk = bounded.read(65536)
                    if not chunk:
                        break
                    if any(chunk):
                        raise LimitError('nonzero_tar_trailer')
                if bounded.count < end_offset+1024:
                    raise LimitError('missing_tar_terminator')
            result['archive_sha256_after'] = full_hash(raw,limits,start)
            after = os.fstat(raw.fileno())
            current = Path(path).stat()
            stamp = lambda s:(s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)
            if (stamp(before)!=stamp(after) or stamp(after)!=stamp(current)
                    or result['archive_sha256']!=result['archive_sha256_after']):
                raise LimitError('archive_changed')
            result['identity_verified'] = True
            result['complete'], result['inventory_status'] = True, 'completed'
    except (OSError,EOFError,tarfile.TarError,ValueError,zlib.error,RecursionError,MemoryError) as error:
        result['findings'].append(dict(member_index=None,code=str(error) if isinstance(error,LimitError) else 'corrupt_or_unreadable_archive'))
    if bounded:
        result['expanded_bytes_read'] = bounded.count
    for index, record in enumerate(result['members']):
        record['flags'] = sorted(set(record['flags']))
        record['quarantined'] = bool(record['flags'])
        result['quarantine_count'] += int(record['quarantined'])
        result['findings'].extend(dict(member_index=index,code=flag) for flag in record['flags'])
    result['security_findings_present'] = bool(result['findings'])
    result['manifest_sha256'] = canonical_digest(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive',type=Path)
    parser.add_argument('--limits',type=Path,required=True)
    parser.add_argument('--expected-sha256')
    parser.add_argument('--expected-size',type=int)
    args = parser.parse_args()
    try:
        limits = json.loads(args.limits.read_text())
        if not isinstance(limits,dict) or set(limits)!=set(DEFAULTS) or any(type(x) is not int or x<=0 for x in limits.values()):
            raise ValueError('invalid resource policy')
        # Only Linux CLI is currently supported/tested for hostile inputs.
        import resource
        resource.setrlimit(resource.RLIMIT_AS,(limits['max_memory_bytes'],limits['max_memory_bytes']))
        resource.setrlimit(resource.RLIMIT_CPU,(limits['max_cpu_seconds'],limits['max_cpu_seconds']))
        result = inspect(args.archive,limits,expected_sha256=args.expected_sha256,expected_size=args.expected_size)
    except (OSError,ValueError,ImportError):
        parser.exit(1,'FAIL: unreadable/unsupported resource policy or platform\n')
    print(json.dumps(result,sort_keys=True,indent=2))
    return 0 if result['complete'] else 1


if __name__=='__main__':
    raise SystemExit(main())
