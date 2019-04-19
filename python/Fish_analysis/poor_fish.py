import matplotlib.pyplot as plt
import numpy as np
from classy import Class

def split(a, n):
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))

#Universal params #

kmax = 0
kmin = -4
numks = 3
ks_arr = np.logspace(kmin, kmax, numks)

#Class stuff

A_Grow = 2.3e-9
params_grow_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'A_s' : A_Grow,
    'h' : 0.6711,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }
fsky = 1.
lmax = 2500
numks = 10

#Fid Cls

cosmo_fid = Class()
cosmo_fid.set(params_grow_fid)
cosmo_fid.compute()
pps_fid = cosmo_fid.get_primordial()
cl_fid = cosmo_fid.raw_cl(lmax)
TT = cl_fid['tt'][2:]
EE = cl_fid['ee'][2:]
TE = cl_fid['te'][2:]
ls = cl_fid['ell'][2:]
cls_factor = ls*(ls+1)/(2*np.pi)
cl_fid_array = np.array([ls, TT, EE, TE])
fish_factor = ls+0.5

dAMP = 1e-11
dk_amp = 0.1
ks_arr = pps_fid['k [1/Mpc]']
print ks_arr

num_kbins = numks
ks_binned_idx = split(np.arange(len(ks_arr)), num_kbins)
ks_binned = []
for i in ks_binned_idx : 
    ks_binned.append(i[-1] - 1)
print ks_binned

ks = np.array([ks_arr, ks_binned])

#Numerical derivatives, dcl

dAMP = A_Grow*0.1
dcl = np.zeros((numks, len(ls), 3))
time = 0 
fish = np.zeros((numks, numks))

for i in np.arange(numks) : 
    cosmopi = Class() ; cosmopi.set(params_grow_fid) ; cosmopi.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP}) ; cosmopi.compute() ; cosmopi.empty() 
    cosmomi = Class() ; cosmomi.set(params_grow_fid) ; cosmomi.set({'k_amp' : ks_arr[i], 'dAmp_k' : -dAMP}) ; cosmomi.compute() ; cosmomi.empty() 
    dTTi = cosmopi.raw_cl(lmax)['tt'][2:]
    plt.loglog(ls, dTTi)

plt.show()


quit()

for i in np.arange(numks) : 
    cosmopi = Class() ; cosmopi.set(params_grow_fid) ; cosmopi.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP}) ; cosmopi.compute() ; cosmopi.empty() 
    cosmomi = Class() ; cosmomi.set(params_grow_fid) ; cosmomi.set({'k_amp' : ks_arr[i], 'dAmp_k' : -dAMP}) ; cosmomi.compute() ; cosmomi.empty() 
    dTTi = cosmopi.raw_cl(lmax)['tt'][2:] - cosmomi.raw_cl(lmax)['tt'][2:]
    for j in np.arange(numks) : 
        cosmopj = Class() ; cosmopj.set(params_grow_fid) ; cosmopj.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP}) ; cosmopj.compute() ; cosmopj.empty() 
        cosmomj = Class() ; cosmomj.set(params_grow_fid) ; cosmomj.set({'k_amp' : ks_arr[i], 'dAmp_k' : -dAMP}) ; cosmomj.compute() ; cosmomj.empty() 
        dTTj = cosmopj.raw_cl(lmax)['tt'][2:] - cosmomj.raw_cl(lmax)['tt'][2:]        
        fish[i,j] = fsky*sum(fish_factor*dTTj*(1/TT)*dTTi*(1/TT))
#        fish_temp = []
#        for ell in np.arange(len(ls)) : 
#            fish_temp.append(fish_factor[ell]*dTTi[ell]*dTTj[ell]/(TT[ell]**2))
#        fish[i,j] = fsky*np.sum(fish_temp)
    print "K NUMBER!", time 
    time = time + 1

print "FISHER", fish


