"""Linux-only trusted wrappers for ADR-0007; callers retain authority/evidence.

Never execute these builders as root Python: sudo applies only to installed
Bubblewrap. Target runs with no capabilities and the invoking nonzero host UID, in new
network/PID/IPC/UTS and mount namespaces. No system policy is modified. Additional
trusted-fixture enforcement probes are mandatory before any legacy target.
"""
import os
from pathlib import Path, PurePosixPath


def sandbox(root, cwd, *, build=False, wall_seconds=None):
    """Construct namespace/mount arguments; root is an owned private audit tree.

Only build directory is host-writable during compilation; validation has no
writable host mounts. /tmp is a disposable namespace-local tmpfs. /proc and /dev
are namespace-local. Each writable tmpfs is capped at 16 MiB. Captured standard
streams live outside sandbox mounts. These are address-space/file limits, not a
claim of aggregate cgroup memory accounting.
"""
    maximum = 300 if build else 10
    wall_seconds = maximum if wall_seconds is None else wall_seconds
    if type(wall_seconds) is not int or not 1 <= wall_seconds <= maximum:
        raise ValueError('invalid wall budget')
    root = Path(root)
    if (os.getuid() == 0 or root.is_symlink() or not root.is_dir() or root.stat().st_uid != os.getuid()
            or root.stat().st_mode & 0o077 or cwd not in ('/A','/B','/build')):
        raise ValueError('untrusted private root or cwd')
    for name in ('deps','source','inputs','A','B','probes','build'):
        if (root/name).is_symlink() or not (root/name).is_dir():
            raise ValueError('invalid sandbox mount')
    args = ['/usr/bin/sudo','-n','/usr/bin/timeout','--signal=KILL',
            str(wall_seconds),'/usr/bin/bwrap','--unshare-net','--unshare-pid','--unshare-ipc','--unshare-uts',
            '--cap-drop','ALL','--cap-add','CAP_SETUID','--cap-add','CAP_SETGID',
            '--cap-add','CAP_SETPCAP','--cap-add','CAP_DAC_OVERRIDE','--die-with-parent','--new-session',
            '--clearenv','--setenv','PATH','/usr/bin:/bin','--setenv','LC_ALL','C',
            '--setenv','OPENBLAS_NUM_THREADS','1','--setenv','OMP_NUM_THREADS','1',
            '--setenv','CMAKE_PREFIX_PATH','/deps/usr',
            '--setenv','LD_LIBRARY_PATH','/deps/usr/lib/x86_64-linux-gnu',
            '--ro-bind','/usr','/usr','--ro-bind','/bin','/bin',
            '--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64',
            '--dir','/etc','--chmod','0755','/etc',
            '--ro-bind','/etc/alternatives','/etc/alternatives',
            '--ro-bind','/etc/ld.so.cache','/etc/ld.so.cache','--proc','/proc','--dev','/dev','--size','16777216','--tmpfs','/tmp','--chmod','1777','/tmp',
            '--size','16777216','--tmpfs','/dev/shm','--chmod','1777','/dev/shm']
    for name in ('deps','source','inputs','A','B','probes'):
        args += ['--ro-bind',str(root/name),'/'+name]
    args += ['--bind' if build else '--ro-bind',str(root/'build'),'/build','--chdir',cwd,'--',
             '/usr/bin/setpriv','--reuid',str(os.getuid()),'--regid',str(os.getgid()),
             '--clear-groups','--bounding-set=-all','--inh-caps=-all','--ambient-caps=-all',
             '--no-new-privs','--']
    return args


def guarded_target(argv, *, cpu=5, memory=268435456):
    """Deny forks, subsequent exec and networking under installed strace 6.8.

strace 6.8 starts tracing after the initial target exec; no occurrence delay
may be used for exec injection. Every observed execve, every
execveat and all process/thread creation calls fail EPERM. strace kill-on-exit
retains PTRACE_O_EXITKILL; no detach, injection-count limit or follow-forks escape
is used. Logs include tracer lines on stderr and must be retained verbatim.
The restriction changes attempted syscall behavior; it is audit instrumentation,
not a claim about ordinary legacy execution. Only Linux x86_64 is tested here.
"""
    if (not isinstance(argv, list) or not argv or not isinstance(argv[0],str)
            or not argv[0].startswith(('/build/','/probes/'))
            or '..' in PurePosixPath(argv[0]).parts
            or any(not isinstance(a,str) or '\x00' in a for a in argv)
            or type(cpu) is not int or not 1 <= cpu <= 5
            or type(memory) is not int or not 1 <= memory <= 268435456):
        raise ValueError('invalid target/limits')
    return ['/usr/bin/prlimit',f'--as={memory}',f'--cpu={cpu}','--core=0',
            '--fsize=1048576','--nofile=128','--','/usr/bin/strace',
            '--kill-on-exit','--inject=execve:error=EPERM',
            '--inject=execveat,fork,vfork,clone,clone3,unshare,setns,ptrace,io_uring_setup:error=EPERM',
            '--inject=%network:error=EPERM','-e','trace=%process,%network,%file','--',*argv]
