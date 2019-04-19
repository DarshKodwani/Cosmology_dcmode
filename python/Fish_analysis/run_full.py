import os
import sys 

if len(sys.argv)!=6 :
    print "Usage: run_full.py numks fsky tracer (T or TE) mode (G or D) noise (N or Y)"
    exit(1)

numks = int(sys.argv[1])
fsky = float(sys.argv[2])
tracer = str(sys.argv[3])
mode = str(sys.argv[4])
noise = str(sys.argv[5])

os.system('python cl_gen.py %i %s'  %(numks, mode))
os.system('python fisher.py %i %.2f %s %s %s' %(numks, fsky, tracer, mode, noise) )



