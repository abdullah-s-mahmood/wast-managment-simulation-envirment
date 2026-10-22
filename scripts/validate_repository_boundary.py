#!/usr/bin/env python3
"""Fail-closed bootstrap inventory check; not a complete secret or plagiarism detector."""
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {'governance', 'governance_source', 'test_source', 'reserved_layout'}
FORBIDDEN_PARTS = {'legacy', 'results', 'runs', 'output', 'outputs', 'build', 'cache',
                   '__pycache__', '.venv', 'secrets', '.git'}
FORBIDDEN_SUFFIXES = {'.exe', '.dll', '.so', '.o', '.a', '.bin', '.pyc', '.pcap',
                      '.trace', '.log', '.pem', '.key'}
PATTERNS = (
    ('private key', re.compile(r'-----BEGIN (?:[A-Z]+ )?PRIVATE KEY-----')),
    ('credential token', re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})\b')),
    ('machine-local path', re.compile(r'(?:/(?:home|Users)/[^\s/]+|[A-Za-z]:\\Users\\[^\s\\]+)')),
)


def safe_path(value):
    return (isinstance(value, str) and bool(value) and '\\' not in value
            and not PurePosixPath(value).is_absolute()
            and all(part not in ('', '.', '..') for part in value.split('/')))


def validate(root, manifest, paths):
    errors = []
    if (not isinstance(manifest, dict) or set(manifest) != {'schema_version', 'groups'}
            or type(manifest.get('schema_version')) is not int
            or manifest['schema_version'] != 1 or not isinstance(manifest.get('groups'), dict)):
        return ['invalid inventory schema/version']
    approved = set()
    for category, entries in manifest['groups'].items():
        if category not in CATEGORIES or not isinstance(entries, list):
            errors.append('invalid inventory category/list')
            continue
        for entry in entries:
            if not safe_path(entry) or entry in approved:
                errors.append('invalid or duplicate approved path')
                continue
            approved.add(entry)
    if errors:
        return errors
    if len(paths) != len(set(paths)):
        errors.append('duplicate inventory path')
    for name in sorted(set(paths)):
        if not safe_path(name):
            errors.append('unsafe inventory path')
            continue
        if name not in approved:
            errors.append(f'unapproved path: {name}')
            continue
        relative = PurePosixPath(name)
        if (set(relative.parts) & FORBIDDEN_PARTS or relative.suffix.lower() in FORBIDDEN_SUFFIXES
                or relative.name == '.env' or relative.name.startswith('.env.')):
            errors.append(f'forbidden artifact: {name}')
            continue
        path = root / name
        if any(parent.is_symlink() for parent in [path, *path.parents] if parent != root):
            errors.append(f'symlink not permitted: {name}')
            continue
        try:
            data = path.read_bytes()
            text = data.decode('utf-8')
        except (OSError, UnicodeError):
            errors.append(f'unreadable/non-text artifact: {name}')
            continue
        if b'\x00' in data:
            errors.append(f'binary artifact: {name}')
        for kind, pattern in PATTERNS:
            if pattern.search(text):
                errors.append(f'{kind} detected: {name}')  # Never echo matched content.
    for name in sorted(approved - set(paths)):
        errors.append(f'approved path missing from inventory: {name}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--manifest', default='docs/REPOSITORY_INVENTORY.json')
    args = parser.parse_args()
    try:
        if not safe_path(args.manifest):
            raise ValueError('manifest must be repository-relative')
        manifest = json.loads((args.root / args.manifest).read_text(encoding='utf-8'))
        listing = subprocess.run(['git', '-C', str(args.root), 'ls-files', '-z',
                                  '--cached', '--others', '--exclude-standard'],
                                 check=True, capture_output=True)
        paths = listing.stdout.decode('utf-8').rstrip('\x00').split('\x00') if listing.stdout else []
        errors = validate(args.root, manifest, paths)
    except (OSError, UnicodeError, ValueError, subprocess.CalledProcessError):
        print('FAIL: cannot read inventory/manifest or enumerate Git files', file=sys.stderr)
        return 1
    for error in errors:
        print('FAIL: ' + error, file=sys.stderr)
    if errors:
        return 1
    print(f'PASS: {len(paths)} approved text artifacts; no prohibited artifact/signature detected.')
    print('NOTE: bounded inventory/signature checks do not prove provenance or absence of all secrets.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
