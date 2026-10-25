/* Independently authored enforcement fixture, not legacy code.
 * Modes exercise UID/caps, read-only mounts, denied process/network syscalls,
 * 256 MiB address space, CPU, 1 MiB file and 10-second watchdog boundaries.
 * CPU/file/wall modes deliberately terminate by the enforced limit.
 */
#define _GNU_SOURCE
#include <sys/syscall.h>
#include <sys/socket.h>
#include <sys/resource.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#define REQUIRE(x) do {if(!(x)){fprintf(stderr,"FAIL line=%d errno=%d\n",__LINE__,errno);return 90;}}while(0)
#define DENIED(x) do {errno=0;long v=(x);REQUIRE(v==-1 && errno==EPERM);}while(0)
int main(int argc,char **argv){
 const char *mode=argc>1?argv[1]:"security";
 if(!strcmp(mode,"cpu")){volatile unsigned long n=0;while(1)n++;}
 if(!strcmp(mode,"wall")){sleep(30);return 99;}
 if(!strcmp(mode,"memory")){void *p=malloc(512UL*1024*1024);REQUIRE(p==NULL);puts("MEMORY_DENIED");return 0;}
 if(!strcmp(mode,"file")){int fd=open("/tmp/large",O_CREAT|O_WRONLY,0600);REQUIRE(fd>=0);char b[65536]={0};while(write(fd,b,sizeof b)>0){}return 99;}
 REQUIRE(getuid()!=0 && geteuid()==getuid() && getgroups(0,NULL)==0);
 REQUIRE(prctl(PR_GET_NO_NEW_PRIVS,0,0,0,0)==1);
 FILE *f=fopen("/proc/self/status","r");REQUIRE(f);char line[1024];int caps=0;
 while(fgets(line,sizeof line,f)) { if(!strncmp(line,"CapEff:",7)){REQUIRE(strtoull(line+7,NULL,16)==0);caps=1;} }
 fclose(f);REQUIRE(caps);
 struct rlimit lim;REQUIRE(getrlimit(RLIMIT_AS,&lim)==0 && lim.rlim_max==268435456);
 REQUIRE(getrlimit(RLIMIT_CPU,&lim)==0 && lim.rlim_max==5);
 const char *paths[]={"/A/forbidden","/build/forbidden","/source/forbidden","/inputs/forbidden","/usr/forbidden"};
 for(unsigned i=0;i<sizeof paths/sizeof paths[0];i++){errno=0;int fd=open(paths[i],O_CREAT|O_WRONLY,0600);REQUIRE(fd==-1 && errno==EROFS);}
 DENIED(socket(AF_INET,SOCK_STREAM,0));
 DENIED(syscall(SYS_fork));DENIED(syscall(SYS_vfork));
 DENIED(syscall(SYS_clone,SIGCHLD,0,0,0,0));DENIED(syscall(SYS_clone3,0,0));
 char *args[]={"/usr/bin/true",NULL};char *env[]={NULL};
 DENIED(execve(args[0],args,env));DENIED(execve(args[0],args,env));
 int fd=open(args[0],O_RDONLY);REQUIRE(fd>=0);DENIED(syscall(SYS_execveat,fd,"",args,env,AT_EMPTY_PATH));close(fd);
 REQUIRE(access("/home",F_OK)==-1);
 puts("SECURITY_PROBE_PASSED");return 0;
}
