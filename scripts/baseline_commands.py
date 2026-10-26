"""Namespace command construction for owner-approved ADR-0009, Linux x86_64."""
from pathlib import Path
import os
from scripts.private_validation_commands import sandbox


def baseline_sandbox(root,mode):
    """Use 120s outer watchdog, read-only host mounts, 64MiB output tmpfs.

Supervisor/target inherit one CPU affinity, 1GiB address space and bounded regular
stdout capture. Setup is privileged; all compiler/supervisor/target code is nonroot.
"""
    if mode not in ('baseline','fixture','security','memory','cpu','file','wall','quota'):
        raise ValueError('unsupported baseline mode')
    root=Path(root)
    for name in ('baseline_supervisor.py','baseline_transport.py'):
        if (root/'probes'/name).is_symlink() or not (root/'probes'/name).is_file():
            raise ValueError('supervisor staging missing')
    args=sandbox(root,'/A');args[args.index('/usr/bin/bwrap')-1]='120'
    index=args.index('--chdir')
    args[index:index]=['--size','67108864','--tmpfs','/outputs','--chmod','1777','/outputs']
    cpu=min(os.sched_getaffinity(0))
    return args+['/usr/bin/taskset','-c',str(cpu),'/usr/bin/prlimit','--as=1073741824',
                 '--cpu=60','--fsize=100000000','--core=0','--','/usr/bin/python3','-I','-B',
                 '/probes/baseline_supervisor.py','--mode',mode]
