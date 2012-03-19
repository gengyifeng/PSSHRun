#!/usr/bin/env python
import os,sys,re,time,subprocess
import paramiko
def runFromHosts():
    hostFile=open('hosts','r')
    re_obj=re.compile(r"\s")
    list=[]
    hlist=[]
    finish=set()
    starttime=time.clock()
    cmd=sys.argv[1]
    for line in hostFile.readlines():
        host=re_obj.split(line)[0]
        homePath=sys.argv[1]
        remotePath=sys.argv[2]
        cmd="scp "+homePath+" "+host+":"+remotePath
        process=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
        list.append(process)
        hlist.append(host)

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
def usage():
    print "usage:\"./pscp.py homePath remotePath\""
if __name__=='__main__':
    if len(sys.argv)<3:
        usage()
    else:
        runFromHosts()    
