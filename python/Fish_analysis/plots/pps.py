import numpy as np 
import matplotlib.pyplot as plt
from classy import Class
from decimal import Decimal
from matplotlib.font_manager import FontProperties
from matplotlib import cm
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

def split(a, n):
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))

#kmax = 0
#kmin = -5
#numks = 10
#ks_arr = np.logspace(kmin, kmax, numks)
lmax = 2500
A_grow = 2.3e-9
params_grow_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'A_s' : A_grow,
    'n_s' : 1,
    'h' : 0.6711,
    'dk_amp' : 0.1,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

cosmo = Class()
cosmo.set(params_grow_fid)
cosmo.compute()
pps_fid = cosmo.get_primordial()
cosmo.empty()
fig = plt.subplots(figsize = (16,10))
plt.loglog(pps_fid['k [1/Mpc]'], pps_fid['P_scalar(k)'], label = 'fiducial')
#plt.show()
dAMP = 0.01*A_grow

ks_arr = pps_fid['k [1/Mpc]']
num_bins = 20
ks_binned_idx = split(np.arange(len(ks_arr)), num_bins)
ks_binned = []
for i in ks_binned_idx : 
    ks_binned.append(i[-1] -1 )
print ks_binned

for i in ks_binned : 
    cosmoi = Class() ; cosmoi.set(params_grow_fid) ; cosmoi.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP}) ; cosmoi.compute() ; ppsi = cosmoi.get_primordial() ; cosmoi.empty()
#    plt.loglog(ppsi['k [1/Mpc]'], ppsi['P_scalar(k)'], label = 'PPS for power added at k = %.2ef with amplitude %.2ef' %(ks_arr[i], dAMP), alpha = 0.4, ls = '--')
    plt.loglog(ppsi['k [1/Mpc]'], ppsi['P_scalar(k)'], label = r'k = %.2e' %ks_arr[i], alpha = 0.6, ls = '--')

plt.legend(loc='upper center', bbox_to_anchor=(-.09, 1.), fontsize = 15, frameon=False)
plt.xlabel(r"k Mpc$^{-1}$", fontsize = 20)
plt.tick_params('both', labelsize = 20)
plt.savefig("pps.pdf")
plt.show()
