#!/usr/bin/env python

import paramiko
import os
import sys
import getpass
import getopt
import re
import thread
class SSHRunCommand:
    def __init__(self,host,command,port=22,mode='k',username=None,password=None,**kwargs):
        self.host=host
        self.port=port
        self.command=command
        self.mode=mode
        if username==None:
            self.username=getpass.getuser()
        else:
            self.username=username
        self.password=password
    def sshWithPass(self):
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host,port=self.port,username=self.username,password=self.password)
        stdin,stdout,stderr=ssh.exec_command(self.command)
        sys.stderr.write(stderr.read())
        sys.stdout.write(stdout.read())
        ssh.close()
    def sshWithKey(self):
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        privateKeyFile=os.path.expanduser('~/.ssh/id_rsa');
        myKey=paramiko.RSAKey.from_private_key_file(privateKeyFile)
        ssh.connect(self.host,port=self.port,username=self.username,pkey=myKey)
        stdin,stdout,stderr=ssh.exec_command(self.command)
        sys.stderr.write(stderr.read())
        sys.stdout.write(stdout.read())
        ssh.close()
    def sshSimple(self):
#        subprocess.check_call("ssh "+self.host+" "+self.command,shell=True,stdout=open('/dev/null','w'),stderr=subprocess.STDOUT)
        os.system("ssh "+self.username+"@"+self.host+" -p "+str(self.port)+" "+self.command)

def usage():
    print "sshrun [--help] [-h --host] [-m --mode] [-c --cmd] [-u --user] [-p --pass] [-p --port] \n\
mode='k' connect with rsa keyfile \n\
mode='p' connect with username and password \n\
mode='s' connect with native ssh command "
def main(argv):
    try:
        opts,args=getopt.getopt(argv,"c:h:m:u:p:v",['help','cmd=','host=','mode=','user=','pass=','port='])
    except getopt.GetoptError,err:
        print str(err)
        usage()
        sys.exit(2)
#    output=None
#    verbose=False
    mode='k'
    port=22
    user=None
    for o,a in opts:
        if o =='--help':
            usage()
            sys.exit()
        elif o in('-h','--host'):
            host=a
        elif o in('-c','--cmd'):
            cmd=a
        elif o in('-m','--mode'):
            mode=a
        elif o in('-u','--user'):
            user=a
        elif o in('-p','--pass'):
            password=a
        elif o =='--port':
            port=a
        else:
            assert False,"unhandled option"
    if mode=='k':
        SSHRunCommand(host,command=cmd,port=port).sshWithKey()
    elif mode=='p':
        SSHRunCommand(host,command=cmd,port=port,username=user,password=password).sshWithPass()
    elif mode=='s':
        if user!=None:
            SSHRunCommand(host,username=user,command=cmd,port=port).sshSimple()
        else:
            SSHRunCommand(host,command=cmd,port=port).sshSimple()
            

if __name__=='__main__':
    main(sys.argv[1:])
