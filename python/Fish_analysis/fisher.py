import matplotlib.pyplot as plt
import numpy as np
from classy import Class
import sys

if len(sys.argv)!=6 :
    print "Usage: fisher.py numks fsky tracer (T or TE) mode (D or G) Noise (N or Y)"
    exit(1)

numks = int(sys.argv[1])
fsky = float(sys.argv[2])
tracer = sys.argv[3]
mode = sys.argv[4]
Noise_planck = sys.argv[5]

renorm = True

if Noise_planck == 'N' :
    noise = False
if Noise_planck == 'Y' :
    noise = True

#Importing cls, dcls, ks, noise

cls_fid = np.load("Data/%s_Data/clfid.npy" %mode)

ls = cls_fid[0,2:]
TT = cls_fid[1,2:]
EE = cls_fid[2,2:]
TE = cls_fid[3,2:]

if renorm == True and mode == "D": 
    dcls_full = np.load("Data/%s_Data/dcls_numks%i_R.npy" %(mode, numks))
else :
    dcls_full = np.load("Data/%s_Data/dcls_numks%i.npy" %(mode, numks))

dclTT = dcls_full[:,2:,0]
dclEE = dcls_full[:,2:,1]
dclTE = dcls_full[:,2:,2]

#plt.loglog(ls, dclTT[0])
#plt.show()

k_arr = np.load("Data/%s_Data/karr_numks%i.npy" %(mode, numks))
ks_full = k_arr[0]
ks_bins = k_arr[1]
ks_power = ks_full[ks_bins]
if numks != len(ks_bins) : 
    print "Number of kbins is not consistent between fisher and cl_gen!"
    exit(1)

if noise == True :
    noise_full = np.load("Data/noise_full.npy")
    TT = TT + noise_full[0,:][2:]
    EE = EE + noise_full[1,:][2:]

#Computing Fisher

time = 0 
fish = np.zeros((numks, numks))
fish_factor = ls + 0.5

if tracer == "T" : 
    for i in np.arange(numks) : 
        dTTi = dclTT[i,:]
        for j in np.arange(i, numks) : 
            dTTj = dclTT[j,:]
            fish[i,j] = sum(fsky*fish_factor*dTTi*dTTj/(TT**2))
#            fish_temp = []
#            for ell in np.arange(len(ls)) :
#                fish_temp.append(fsky*fish_factor[ell]*dTTi[ell]*dTTj[ell]/(TT[ell]**2))
#            fish[i,j] = sum(fish_temp)
            if i != j : 
                fish[j,i] = fish[i,j] 
            print time 
            time = time + 1

#With polarisation
clmat = np.array([[TT, TE], [TE, EE]])

if tracer == "TE" : 
    for i in np.arange(numks) : 
        dTTi = dclTT[i,:]
        dEEi = dclEE[i,:]
        dTEi = dclTE[i,:]
        dclmati = np.array([[dTTi, dTEi], [dTEi, dEEi]])
        for j in np.arange(i, numks) : 
            dTTj = dclTT[j,:]
            dEEj = dclEE[j,:]
            dTEj = dclTE[j,:]
            dclmatj = np.array([[dTTj, dTEj], [dTEj, dEEj]])
            fishtemp = []
            for ell in np.arange(len(ls)) :
                iclmat = np.linalg.inv(clmat[:,:,ell])
                temp = np.trace( np.dot(iclmat[:,:], np.dot(dclmati[:,:,ell], np.dot(iclmat[:,:], dclmatj[:,:,ell]))))
                fishtemp.append(temp)
            fish[i,j] = sum(fishtemp*fish_factor*fsky)
            if i!=j : 
                fish[j,i] = fish[i,j]
            print time 
            time = time + 1

if noise == True : 
    if renorm == False : 
        np.save("Data/%s_Data/fish_numks%i_fsky%.2f_%s_noiseY" %(mode, numks, fsky, tracer), fish)
    elif renorm == True : 
        np.save("Data/%s_Data/fish_numks%i_fsky%.2f_%s_noiseY_R" %(mode, numks, fsky, tracer), fish)

elif noise == False : 
    if renorm == False : 
        np.save("Data/%s_Data/fish_numks%i_fsky%.2f_%s_noiseN" %(mode, numks, fsky, tracer), fish)
    if renorm == True : 
        np.save("Data/%s_Data/fish_numks%i_fsky%.2f_%s_noiseN_R" %(mode, numks, fsky, tracer), fish)

#CS = plt.contour(ks_power, ks_power, fish, 1000)
#cbar = plt.colorbar(CS)
#plt.yscale('log')
#plt.xscale('log')
#plt.show()

#print(max(np.diag(fish)))
#plt.imshow(fish)
print "EVALS OF FISHER", np.linalg.eigvals(fish)
fig ,ax = plt.subplots(nrows = 1, ncols = 2, figsize =(16, 6))
cov = np.linalg.inv(fish)
print "SIGMAS", np.diag(cov)
ax[1].loglog(ks_power, np.diag(cov), label = 'cov')
ax[0].loglog(ks_power, np.diag(fish), label = 'fish')
#plt.legend()
#plt.show()
