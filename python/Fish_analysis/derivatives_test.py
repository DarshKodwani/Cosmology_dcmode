import matplotlib.pyplot as plt
import numpy as np
from classy import Class


dAmp_list = np.array([0.01,0.1,1,10])*1e-9
#k_list = np.array([0.1,0.01])
#dAmp_list = np.array([0.01,0.1])

params_grow_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'A_s' : 2.3e-9,
    'h' : 0.6711,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

lmax = 2500

cosmo_fid = Class()
cosmo_fid.set(params_grow_fid)
cosmo_fid.compute()
pps_fid = cosmo_fid.get_primordial()
ks = pps_fid['k [1/Mpc]']
ks_ls = np.array([ks[3], ks[30]])

for k in ks_ls : 
    dcl = np.zeros((len(dAmp_list), lmax-1))
    ind = 0
    fig, ax = plt.subplots(2,1)
    for amp in dAmp_list : 
        cosmop = Class() ; cosmop.set(params_grow_fid) ; cosmop.set({'k_amp' : k, 'dAmp_k' : amp}), cosmop.compute(), ; cosmop.empty() ; clp = cosmop.raw_cl(lmax)
        cosmom = Class() ; cosmom.set(params_grow_fid) ; cosmom.set({'k_amp' : k, 'dAmp_k' : -amp}), cosmom.compute(), ; cosmom.empty() ; clm = cosmom.raw_cl(lmax)
        ls = clp['ell'][2:]
        factor_cl = ls*(ls+1)/(2*np.pi)
        ax[0].loglog(ls, factor_cl*clp['tt'][2:], label = r"$\epsilon$ +ve %.3E" %amp)
        ax[0].loglog(ls, factor_cl*clm['tt'][2:], label = r"$\epsilon$ -ve %.3E" %amp)
        ax[0].set_title("Cls with power added at k = %.3f" %k, fontsize = "small")
        ax[0].set_xlabel(r"$\ell$", fontsize = "small")
        ax[0].set_ylabel(r"$\frac{\ell(\ell+1) C_\ell}{2 \pi}$", fontsize = "small")
        tempdcl = (clp['tt'][2:] - clm['tt'][2:])/(2*amp)
        ax[1].loglog(ls, tempdcl, label = r"$\epsilon$ = %.3f" %amp)
        ax[1].set_xlabel(r"$\ell$", fontsize = "small")
        ax[1].set_ylabel(r"$\frac{C_\ell(\epsilon) - C_\ell(-\epsilon)}{2 \epsilon}$", fontsize = "small")
        ax[1].set_title(r"Numerical derivatives for k = %.3E " %k, fontsize = "small")
        dcl[ind, :] = tempdcl
        ind += 1
        print ind

    ax[0].legend(loc = 'upper right', fontsize = "small")
    ax[1].legend(fontsize = "small")
    plt.show()
    plt.savefig("plots/numerical_deriv_check_ktest_%.3f.pdf" %k)

