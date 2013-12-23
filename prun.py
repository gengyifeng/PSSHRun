#!/usr/bin/env python
import subprocess
import re
import os,sys
import time
#cmd='uptime'
def runFromHosts():
    hostFile=open('hosts','r')
    re_obj=re.compile(r"\s")
    list=[]
    hlist=[]
    finish=set()
    starttime=time.clock()
    cmd=" ".join(sys.argv[1:])
    for line in hostFile.readlines():
        host=re_obj.split(line)[0]
#        process=subprocess.Popen("python sshrun.py -h"+ host+" -c \'"+cmd+"\'",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        process=subprocess.Popen("python sshrun.py -h"+ host+" -c \'"+cmd+"\'",stdout=open('stdout.log','aw'),stderr=open("stderr.log",'aw'),shell=True)
#        process=subprocess.Popen("python sshrun.py -h"+ host+" -c \'"+cmd+"\'",shell=True,close_fds=True)
#        process=subprocess.Popen("python test.py",stdout=open("stdout.log",'w'),stderr=open("stderr.log",'w'),shell=True)
        hlist.append(host)
        list.append(process)
#        stdout,stderr=process.communicate()
#        print re_obj.split(line)[0]+": "+ str(status)
    
    while len(finish)!=len(list):
        for i in range(len(list)):
            status=list[i].poll()
            if (i in finish) or (status==None):
                continue;
            if status==0:
                print "Success: "+hlist[i]
            else:
                print "Failed : " +hlist[i]+"'s returncode = "+str(status)
            finish.add(i)
    endtime = time.clock()
    print "runtime: "+ str(endtime-starttime)
if __name__=='__main__':
    runFromHosts()
