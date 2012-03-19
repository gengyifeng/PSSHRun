#!/usr/bin/env python
import os,sys,os.path
nccopy="/home/yifeng/Workspace/C/pnco/lib/netcdf4/bin/nccopy"
args="-k 3"
indir="/home/yifeng/Workspace/Python/PSSHRun/data"
outdir="/home/yifeng/Workspace/Python/PSSHRun/output"
if __name__=='__main__':
    if os.path.exists(outdir):
        print "output directory exists"
        sys.exit(0)
    else:
        os.mkdir(outdir)
    for root,dirs,files in os.walk(indir):
        for file in files:
            if file[-2:]=='nc':
                in_file=os.path.join(root,file)
                out_file=os.path.join(outdir,file);
                os.system(nccopy+" "+args+" "+in_file+" "+out_file)


