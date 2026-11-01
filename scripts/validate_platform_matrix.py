#!/usr/bin/env python3
"""Validate target planning independently of verified platform/runtime support."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from scripts.validate_baseline_result import strict_json

DEPENDENCIES={'git','python','cpp_compiler','cmake','build_driver','sumo','ns3'}
TARGETS={'LINUX_UBUNTU2404_X86_64','WIN11_WSL2_UBUNTU2404_X86_64','WIN11_MSYS2_X86_64'}
SCOPES={'host_probe','governance','dependency_smoke','adapter_integration','deterministic_replay'}


def host_probe():
    """Report sanitized host observations; never infer Windows/WSL from Linux success."""
    system=platform.system();machine=platform.machine();kernel=platform.release()
    release=platform.freedesktop_os_release() if system=='Linux' else {}
    target='UNCLASSIFIED_HOST'
    if (system=='Linux' and machine=='x86_64' and release.get('ID')=='ubuntu'
            and release.get('VERSION_ID')=='24.04' and not re.search('microsoft|wsl',kernel,re.I)):
        target='LINUX_UBUNTU2404_X86_64'
    return {'schema_version':1,'platform_id':target,'scope':'host_probe','status':'PASS',
            'command':['python','scripts/validate_platform_matrix.py','probe'],
            'exit_code':0,'observed_at_utc':datetime.now(timezone.utc).isoformat(),'observed':{'system':system,'machine':machine,'kernel':kernel,
             'distribution_id':release.get('ID','UNAVAILABLE'),'distribution_version':release.get('VERSION_ID','UNAVAILABLE'),
             'python':platform.python_version()},'support_claim':'HOST_OBSERVATION_ONLY',
            'accepted_dependency_versions':[],'simulator_support_verified':False}


def validate(data,root):
    """Require routes and tuple/scope-specific evidence; passing a plan is not support.

Future runtime gates stay open. Version selection/installation and adapter tests
belong to subsequent sprints, not source-audit tool versions or this schema.
    """
    if (not isinstance(data,dict) or type(data.get('schema_version')) is not int or data['schema_version']!=1
            or data.get('claim')!='TARGET_PLAN_NOT_VERIFIED_RUNTIME'
            or data.get('accepted_dependency_versions')!=[]):raise ValueError('unsupported matrix/claim/version')
    rows=data.get('platforms')
    if not isinstance(rows,list) or {r['id'] for r in rows}!=TARGETS or len(rows)!=len(TARGETS):raise ValueError('missing/duplicate/unsupported target')
    receipts={}
    for evidence in data.get('evidence',[]):
        eid=evidence['id'];path=evidence['artifact']
        if eid in receipts or not re.fullmatch(r'docs/platforms/[A-Za-z0-9_-]+\.json',path):raise ValueError('unsafe/duplicate receipt')
        raw=(Path(root)/path).read_bytes()
        if len(raw)>1048576 or hashlib.sha256(raw).hexdigest()!=evidence['sha256']:raise ValueError('receipt hash/budget')
        receipt=strict_json(raw)
        if (receipt.get('scope') not in SCOPES or receipt.get('status')!='PASS'
                or type(receipt.get('exit_code')) is not int or receipt['exit_code']!=0
                or not isinstance(receipt.get('command'),list) or not receipt['command']):raise ValueError('unperformed evidence')
        observed=receipt.get('observed',{})
        if (type(receipt.get('schema_version')) is not int or receipt['schema_version']!=1
                or receipt.get('platform_id')!='LINUX_UBUNTU2404_X86_64'
                or receipt.get('scope')!='host_probe' or receipt.get('support_claim')!='HOST_OBSERVATION_ONLY'
                or receipt.get('simulator_support_verified') is not False
                or receipt.get('accepted_dependency_versions')!=[]
                or tuple(observed.get(k) for k in ('system','machine','distribution_id','distribution_version'))!=('Linux','x86_64','ubuntu','24.04')
                or not isinstance(observed.get('kernel'),str) or re.search('microsoft|wsl',observed['kernel'],re.I)):
            raise ValueError('receipt observation/target mismatch; Windows requires independent future evidence schema')
        receipts[eid]=receipt
    expected={'LINUX_UBUNTU2404_X86_64':('Linux','Ubuntu 24.04','linux','required'),
              'WIN11_WSL2_UBUNTU2404_X86_64':('Windows 11','Ubuntu 24.04','wsl2_linux_guest','required'),
              'WIN11_MSYS2_X86_64':('Windows 11','Windows 11 / MSYS2 MinGW64','native_msys2','best_effort')}
    for row in rows:
        if tuple(row.get(k) for k in ('host_os','runtime_os','runtime_kind','support_level'))!=expected[row['id']]:raise ValueError('platform tuple disagreement')
        if row.get('support_level') not in ('required','best_effort') or row.get('simulator_support_verified') is not False:raise ValueError('runtime support promotion')
        if row['id']=='WIN11_MSYS2_X86_64':
            if row['support_level']!='best_effort' or row['runtime_kind']!='native_msys2':raise ValueError('native Windows scope')
        elif row['support_level']!='required':raise ValueError('required target downgraded')
        if row['architecture']!='x86_64':raise ValueError('unplanned architecture')
        if row['id']=='WIN11_WSL2_UBUNTU2404_X86_64' and row['runtime_kind']!='wsl2_linux_guest':raise ValueError('WSL/native parity assumption')
        routes=row.get('dependencies')
        if not isinstance(routes,list) or len(routes)!=len(DEPENDENCIES) or {r['id'] for r in routes}!=DEPENDENCIES:raise ValueError('missing/duplicate dependency route')
        for route in routes:
            if (not isinstance(route.get('install_route'),str) or not route['install_route'].strip()
                    or not isinstance(route.get('verification'),list) or not route['verification']
                    or not all(isinstance(x,str) and x.strip() for x in route['verification'])
                    or not route.get('source_url','').startswith('https://')
                    or route.get('version_pin') is not None or route.get('verification_status')!='NOT_RUN'):
                raise ValueError('unsupported route/version/installed claim')
        gates=row.get('gates')
        if not isinstance(gates,dict) or set(gates)!=SCOPES:raise ValueError('missing platform gates')
        for scope,gate in gates.items():
            if gate['status']=='NOT_RUN':
                if gate.get('evidence_id') is not None:raise ValueError('not-run evidence masquerade')
            elif gate['status']=='PASS':
                receipt=receipts.get(gate.get('evidence_id'))
                if not receipt or receipt['platform_id']!=row['id'] or receipt['scope']!=scope:raise ValueError('cross-platform/scope evidence substitution')
                if scope!='host_probe':raise ValueError('runtime/governance evidence requires later qualified matrix revision')
            else:raise ValueError('invalid gate state')
    return {'status':'VALID_PLATFORM_PLAN_UNVERIFIED_RUNTIME','targets':len(rows),
            'required_targets':sum(r['support_level']=='required' for r in rows),
            'verified_simulator_targets':0,'later_platform_gates':'OPEN','dependency_versions':'UNSELECTED'}


def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='mode',required=True)
    sub.add_parser('probe');check=sub.add_parser('check');check.add_argument('matrix',type=Path);check.add_argument('--repository',type=Path,default=ROOT)
    args=parser.parse_args()
    try:result=host_probe() if args.mode=='probe' else validate(strict_json(args.matrix.read_bytes()),args.repository)
    except (OSError,ValueError,TypeError,KeyError,AttributeError):
        print('INVALID_PLATFORM_PLAN_OR_EVIDENCE',file=sys.stderr);return 1
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':raise SystemExit(main())
