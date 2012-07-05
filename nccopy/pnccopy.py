#!/usr/bin/env python
import os,sys,os.path
import subprocess
#nccopy="/home/yifeng/Workspace/C/pnco/lib/netcdf4/bin/nccopy"
nccopy="nccopy"
def usage():
    print "Usage: ./pnccopy.py [-k kind] [-d n] [-s] [-u] [-c chunkspec] [-m bufsize] input output \
            Attention: input and output should be last two arguments."
def main(argv):
    if len(argv)<2:
        usage()
        sys.exit(1)
    else:
        args=' '.join(argv[:-2])
    input =argv[-2]
    output = argv[-1]
    if os.path.isfile(input):
        os.system(nccopy+" "+args+" "+input+" "+output)
        sys.exit(0);
    if os.path.exists(output):
        print "output directory:"+output+" exists"
        sys.exit(1)
    else:
        os.mkdir(output)
    flist=[]
    list=[]
    finish=set()
    for root,dirs,files in os.walk(input):
        for file in files:
            if file[-2:]=='nc':
                in_file=os.path.join(root,file)
                out_file=os.path.join(output,file);
		#os.system(nccopy+" "+args+" "+in_file+" "+out_file)
		cmd=nccopy+" "+args+" "+in_file+" "+out_file
	        process=subprocess.Popen(cmd,shell=True,close_fds=True)
		list.append(process)
		flist.append(file)
    while len(finish)!=len(list):
     	for i in range(len(list)):
            status=list[i].poll()
       	    if (i in finish) or (status==None):
                continue;
            if status==0:
                print "Success: "+flist[i]
            else:
                print "Failed : " +flist[i]+"'s returncode = "+str(status)
            finish.add(i)
 
if __name__=='__main__':
    main(sys.argv[1:]) 
