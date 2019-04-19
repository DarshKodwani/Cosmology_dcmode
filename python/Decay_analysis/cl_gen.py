import matplotlib.pyplot as plt
import numpy as np
from classy import Class

#Universal params #

kmax = 1
kmin = -4
numks = 20
ks_arr = np.logspace(kmin, kmax, numks)

#Class stuff

params_grow_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'A_s' : 2.3e-9,
    'h' : 0.6711,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

params_decay = {
    'output' : 'tCl pCl tpCl mPk', 
    'lensing' : 'no', 
    'A_s' : 2.3e-9, 
    'h' : 0.6711, 
    'omega_b' : 0.022068, 
    'omega_cdm' : 0.12029,
    'ic' : 'addcs',
    'f_addcs' : .1,
    'n_addcs' : 1., 
    'alpha_addcs' : 0.,
    'phi_addcs' : 0.785 }

lmax=2500
l = np.array(range(2,lmax+1))
factor = l*(l+1)/(2*np.pi)

#Fiducial Cls

cosmo_fid = Class()
cosmo_fid.set(params_grow_fid)
cosmo_fid.compute()
cl_fid = cosmo_fid.raw_cl(lmax)

TT = cl_fid['tt'][2:]
EE = cl_fid['ee'][2:]
TE = cl_fid['te'][2:]

cl_mat = np.array([ [TT,TE], [TE, EE]], dtype = float)

np.save("Fish_data/clfid_%i" %numks, cl_mat)

dAMP = 0.05
nell = 2499
dcl_g = np.zeros((numks, nell, 3))
dcl_d = np.zeros((numks, nell, 3))
time = 0 

for i in np.arange(numks) : 
    cosmop_g = Class(); cosmop_g.set(params_grow_fid) ; cosmop_g.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP}) ; cosmop_g.compute() ; cosmop_g.empty()
    cosmom_g = Class(); cosmom_g.set(params_grow_fid) ; cosmom_g.set({'k_amp' : ks_arr[i], 'dAmp_k' : -dAMP}) ; cosmom_g.compute() ; cosmom_g.empty()
#    plt.loglog(factor*cosmop_g.raw_cl(lmax)['tt'][2:], label =  ks_arr[i])
#    plt.legend()
    dcl_g[i,:,0] = ( (np.array(cosmop_g.raw_cl(lmax)['tt'][2:]) - np.array(cosmom_g.raw_cl(lmax)['tt'][2:]))/(2*dAMP))
    dcl_g[i,:,1] = ( (np.array(cosmop_g.raw_cl(lmax)['ee'][2:]) - np.array(cosmom_g.raw_cl(lmax)['ee'][2:]))/(2*dAMP))
    dcl_g[i,:,2] = ( (np.array(cosmop_g.raw_cl(lmax)['te'][2:]) - np.array(cosmom_g.raw_cl(lmax)['te'][2:]))/(2*dAMP))
    cosmop_d = Class(); cosmop_d.set(params_decay) ; cosmop_d.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP}) ; cosmop_d.compute() ; cosmop_d.empty()
    cosmom_d = Class(); cosmom_d.set(params_decay) ; cosmom_d.set({'k_amp' : ks_arr[i], 'dAmp_k' : -dAMP}) ; cosmom_d.compute() ; cosmom_d.empty()
    dcl_d[i,:,0] = ( (np.array(cosmop_d.raw_cl(lmax)['tt'][2:]) - np.array(cosmom_d.raw_cl(lmax)['tt'][2:]))/(2*dAMP))
    dcl_d[i,:,1] = ( (np.array(cosmop_d.raw_cl(lmax)['ee'][2:]) - np.array(cosmom_d.raw_cl(lmax)['ee'][2:]))/(2*dAMP))
    dcl_d[i,:,2] = ( (np.array(cosmop_d.raw_cl(lmax)['te'][2:]) - np.array(cosmom_d.raw_cl(lmax)['te'][2:]))/(2*dAMP))
    time = time + 1
    print "K NUMBER", time
#plt.show()

np.save("Fish_data/dcl_d_%i" %numks, dcl_d)
np.save("Fish_data/dcl_g_%i" %numks, dcl_g)
