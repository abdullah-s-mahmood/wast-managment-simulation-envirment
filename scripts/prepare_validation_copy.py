#!/usr/bin/env python3
"""Private hash-bound copies for ADR-0007; no execution or source reuse.

Library helper only. Caller must verify owner authority, the exact reviewed plan,
private destination and process CPU/address-space limits before calling. Bytes
are staged in bounded memory and written only after complete TAR/gzip parsing,
full before/after hash verification and membership/hash checks. No extract/all,
link following or archive-selected output paths are used.
"""
import gzip
import hashlib
import os
from pathlib import Path, PurePosixPath
import tarfile
import time

from scripts import inventory_legacy as inventory

MAX_COPY_BYTES = 4 * 1024 * 1024  # Audit text/input staging ceiling, not a model parameter.


def prepare(archive_path, manifest, destinations, private_root, limits):
    """Copy selected IDs to caller-assigned safe relative paths; return hashes.

`destinations` maps immutable entry IDs to relative output names, never link
metadata. Destination must not exist; failed publication may leave partial private
files and must never be retried by overwriting them. The accepted inventory must
be complete and integrity-verified. This function does not grant execution rights.
"""
    if (not inventory.verify_manifest(manifest) or manifest.get('schema_version') != 2
            or manifest.get('complete') is not True or manifest.get('identity_verified') is not True):
        raise ValueError('unverified inventory')
    if (not isinstance(limits,dict) or set(limits)!=set(inventory.DEFAULTS)
            or any(type(v) is not int or v<=0 for v in limits.values())):
        raise ValueError('invalid resource policy')
    if not destinations or not isinstance(destinations, dict):
        raise ValueError('empty copy selection')
    members = {m['entry_id']:m for m in manifest['members']}
    names = set()
    for entry, output in destinations.items():
        m = members.get(entry)
        if (m is None or m['kind'] != 'file' or m['quarantined']
                or m['bytes'] < 0 or not m['sha256']):
            raise ValueError('unapproved member')
        if (not isinstance(output, str) or not output or '\\' in output
                or PurePosixPath(output).is_absolute()
                or any(x in ('', '.', '..') for x in output.split('/'))
                or output.casefold() in names):
            raise ValueError('unsafe destination')
        names.add(output.casefold())
    if sum(members[x]['bytes'] for x in destinations) > MAX_COPY_BYTES:
        raise ValueError('copy staging limit')
    root = Path(private_root)
    if root.exists() or root.is_symlink():
        raise ValueError('destination exists')
    if (root.parent.is_symlink() or root.parent.stat().st_uid != os.getuid()
            or root.parent.stat().st_mode & 0o077):
        raise ValueError('private parent required')
    start = time.monotonic()
    staged = {}
    with Path(archive_path).open('rb') as raw:
        before = os.fstat(raw.fileno())
        if (before.st_size > limits['max_compressed_bytes']
                or before.st_size != manifest['compressed_bytes']
                or inventory.full_hash(raw, limits, start) != manifest['archive_sha256']):
            raise ValueError('archive identity mismatch')
        raw.seek(0)

        class GuardedInfo(tarfile.TarInfo):
            def _proc_pax(self, archive):
                if self.size > limits['max_metadata_bytes']:
                    raise inventory.LimitError('metadata_size_limit')
                return super()._proc_pax(archive)
            def _proc_gnulong(self, archive):
                if self.size > limits['max_metadata_bytes']:
                    raise inventory.LimitError('metadata_size_limit')
                return super()._proc_gnulong(archive)
            def _proc_sparse(self, archive):
                raise inventory.LimitError('unsupported_sparse_encoding')

        with gzip.GzipFile(fileobj=raw) as expanded:
            bounded = inventory.Bounded(expanded, limits, start)
            with tarfile.open(fileobj=bounded, mode='r|', tarinfo=GuardedInfo) as archive:
                count = 0
                for index, member in enumerate(archive):
                    inventory.deadline(limits, start)
                    if index >= limits['max_members'] or member.size > limits['max_member_bytes']:
                        raise inventory.LimitError('member_limit')
                    if member.issparse():
                        raise inventory.LimitError('unsupported_sparse_encoding')
                    if index >= len(manifest['members']):
                        raise ValueError('membership mismatch')
                    expected = manifest['members'][index]
                    if member.name != expected['path'] or member.size != expected['bytes']:
                        raise ValueError('membership mismatch')
                    count += 1
                    entry = f'entry-{index:08d}'
                    if entry not in destinations:
                        continue
                    if not member.isfile():
                        raise ValueError('selected member is not regular')
                    # Never call extractfile on an unselected member or any link.
                    payload = archive.extractfile(member)
                    data = payload.read(expected['bytes'] + 1)
                    if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
                        raise ValueError('selected payload mismatch')
                    staged[entry] = data
                end = archive.offset
                if any(bounded.suffix_at(end)):
                    raise ValueError('nonzero trailer')
            while True:
                chunk = bounded.read(65536)
                if not chunk:
                    break
                if any(chunk):
                    raise ValueError('nonzero trailer')
            if bounded.count < end + 1024:
                raise ValueError('missing tar terminator')
        if count != len(manifest['members']) or set(staged) != set(destinations):
            raise ValueError('incomplete selection')
        if inventory.full_hash(raw, limits, start) != manifest['archive_sha256']:
            raise ValueError('archive changed')
        stamp = lambda s:(s.st_size, s.st_mtime_ns, s.st_ino, s.st_dev)
        if stamp(before) != stamp(os.fstat(raw.fileno())) or stamp(before) != stamp(Path(archive_path).stat()):
            raise ValueError('archive changed')
    root.mkdir(mode=0o700)
    receipts = {}
    for entry, data in staged.items():
        path = root / destinations[entry]
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o400)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        receipts[entry] = {'destination':destinations[entry], 'sha256':hashlib.sha256(data).hexdigest(),
                           'bytes':len(data)}
    return receipts
