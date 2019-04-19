import matplotlib.pyplot as plt
import numpy as np
from classy import Class

#Universal params #

kmax = 1
kmin = -4
numks = 20
ks_arr = np.logspace(kmin, kmax, numks)

#Class stuff

params = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'A_s' : 2.3e-9,
    'h' : 0.6711,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

lmax=2500
l = np.array(range(2,lmax+1))
factor = l*(l+1)/(2*np.pi)

# Theory Cls

cosmo = Class()
cosmo.set(params)
cosmo.compute()
fullcl = cosmo.raw_cl(lmax)

TT=fullcl['tt'][2:]
EE=fullcl['ee'][2:]
TE=fullcl['te'][2:]

clfull = np.array([[TT,TE],[TE,EE]], dtype = float)
#plt.loglog(l, factor*clfull[0,0])
#plt.show()

np.save("Fish_data/clfull_%i_log" %numks, clfull)

dAMP = 0.05
nell = 2499
dcl = np.zeros((numks,nell,3))
time = 0
for i in np.arange(numks) : 
    cosmop = Class(); cosmop.set(params) ; cosmop.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP}) ; cosmop.compute() ; cosmop.empty()
    cosmom = Class(); cosmom.set(params) ; cosmom.set({'k_amp' : ks_arr[i], 'dAmp_k' : -dAMP}) ; cosmom.compute() ; cosmom.empty()
#    plt.loglog(factor*cosmop.raw_cl(lmax)['tt'][2:], label =  ks_arr[i])
#    plt.legend()
    dcl[i,:,0] = ( (np.array(cosmop.raw_cl(lmax)['tt'][2:]) - np.array(cosmom.raw_cl(lmax)['tt'][2:]))/(2*dAMP))
    dcl[i,:,1] = ( (np.array(cosmop.raw_cl(lmax)['ee'][2:]) - np.array(cosmom.raw_cl(lmax)['ee'][2:]))/(2*dAMP))
    dcl[i,:,2] = ( (np.array(cosmop.raw_cl(lmax)['te'][2:]) - np.array(cosmom.raw_cl(lmax)['te'][2:]))/(2*dAMP))
    time = time + 1
    print "K NUMBER", time
#plt.show()

dctt = dcl[:,:,0]
dcee = dcl[:,:,1]
dcte = dcl[:,:,2]

dctt = np.array(dctt)
dcee  = np.array(dcee)
dcte = np.array(dcte)

np.save("Fish_data/dcfull_%i_log" %numks, dcl)

