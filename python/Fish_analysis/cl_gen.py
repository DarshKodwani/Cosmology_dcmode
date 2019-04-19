import matplotlib.pyplot as plt
import numpy as np
from classy import Class
import sys
from scipy.interpolate import interp1d

if len(sys.argv)!=3 :
    print("Usage: cl_gen.py numks mode (D or G)")
    exit(1)

numks = int(sys.argv[1])
mode = str(sys.argv[2])
renorm = True

Trenorm_data = np.load("Data/renorm_temp.npy")
Prenorm_data = np.load("Data/renorm_pol.npy")
lsrenorm_data = np.load("Data/renorm_ls.npy")
Trenorm = interp1d(lsrenorm_data, Trenorm_data)
Prenorm = interp1d(lsrenorm_data, Prenorm_data)

def split(a, n):
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in xrange(n))

lmax = 2500
A_grow = 2.3e-9
epsilon_decay = 0.01*A_grow
#epsilon_decay = 0.
dAMP_grow = A_grow/100.
dAMP_decay = epsilon_decay/100
#dAMP_decay = A_grow/100.

params_grow_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'A_s' : A_grow,
    'h' : 0.6711,
    'ic' : 'ad',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

params_decay_fid = { 
    'output': 'tCl pCl tpCl',
    'lensing': 'no',
    'n_addcs': 1.,
    'alpha_addcs': 0.,
    'phi_addcs': 0.,
    'h' : 0.6711,
    'ic' : 'addcs',
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029 }

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
Trenorm = Trenorm(ls)
Prenorm = Prenorm(ls)
cl_fid_array = np.array([ls, TT, EE, TE])
cosmo_fid.empty()

"""
plt.plot(ls, ls*(ls+1)*TT/(2*np.pi), label = "TT_fid")
plt.plot(ls, ls*(ls+1)*EE/(2*np.pi), label = "EE_fid")
plt.plot(ls, ls*(ls+1)*TE/(2*np.pi), label = "TE_fid")
plt.legend()
plt.show()
quit()
"""

if mode == "G" :
    np.save("Data/G_Data/clfid", cl_fid_array)
elif mode == "D" :
    np.save("Data/D_Data/clfid", cl_fid_array)

# k_array used

dk_amp = 0.1
ks_arr = pps_fid['k [1/Mpc]']
print(ks_arr)

num_kbins = numks
ks_binned_idx = split(np.arange(len(ks_arr)), num_kbins)
ks_binned = []
for i in ks_binned_idx : 
    ks_binned.append(i[-1] - 1)
print(ks_binned)

ks = np.array([ks_arr, ks_binned])

print("Min and Max values for k bins")
print(ks_arr[ks_binned[0]], ks_arr[ks_binned[-1]])
for i in ks_binned :
    print("Log binning is")
    print(np.log(ks_arr[i]) - np.log(ks_arr[i-1]))
    
if mode == "G" :
    np.save("Data/G_Data/karr_numks%i" %num_kbins, ks)
elif mode == "D" :
    np.save("Data/D_Data/karr_numks%i" %num_kbins, ks)

#Derivatives of cls

dcls = np.zeros((num_kbins, len(ls), 3))
ci = 0

if mode == "G" : 
    for i in ks_binned : 
        cosmop = Class()
        cosmop.set(params_grow_fid)
        cosmop.set({'k_amp' : ks_arr[i], 'dAmp_k' : dAMP_grow}) 
        cosmop.compute()
        clp = cosmop.raw_cl(lmax) 
        cosmop.empty()
        
        cosmom = Class() 
        cosmom.set(params_grow_fid) 
        cosmom.set({'k_amp' : ks_arr[i], 'dAmp_k' : -dAMP_grow}) 
        cosmom.compute() 
        clm = cosmom.raw_cl(lmax) 
        cosmom.empty()
        
        tempdcl_tt = (clp['tt'][2:] - clm['tt'][2:])/(2*dAMP_grow)
        tempdcl_ee = (clp['ee'][2:] - clm['ee'][2:])/(2*dAMP_grow)
        tempdcl_te = (clp['te'][2:] - clm['te'][2:])/(2*dAMP_grow)
        dcls[ci,:,0] = tempdcl_tt
        dcls[ci,:,1] = tempdcl_ee
        dcls[ci,:,2] = tempdcl_te
        ci += 1

elif mode == "D" : 
    if renorm == True : 
        print("Renormalised transfer function used")
        renorm_factor_TT = Trenorm**2
        renorm_factor_EE = Prenorm**2
        renorm_factor_TE = Trenorm*Prenorm
    elif renorm == False : 
        renorm_factor_TT = 1.
        renorm_factor_EE = 1.
        renorm_factor_TE = 1.
    for i in ks_binned : 
        cosmop = Class()
        cosmop.set(params_decay_fid)
        cosmop.set({'k_amp' : ks_arr[i], 'dAmp_k' : epsilon_decay + dAMP_decay}) 
        cosmop.compute()
        clp = cosmop.raw_cl(lmax)
#        plt.loglog(ls, ls*(ls+1)*clp)
#        plt.show()
        cosmop.empty()
        
        cosmom = Class() 
        cosmom.set(params_decay_fid) 
        cosmom.set({'k_amp' : ks_arr[i], 'dAmp_k' : epsilon_decay - dAMP_decay}) 
        cosmom.compute() 
        clm = cosmom.raw_cl(lmax) 
        cosmom.empty()
        
        tempdcl_tt = renorm_factor_TT*(clp['tt'][2:] - clm['tt'][2:])/(2*dAMP_decay)
        tempdcl_ee = renorm_factor_EE*(clp['ee'][2:] - clm['ee'][2:])/(2*dAMP_decay)
        tempdcl_te = renorm_factor_TE*(clp['te'][2:] - clm['te'][2:])/(2*dAMP_decay)
        plt.loglog(ls, tempdcl_tt, label = "tempdcl k = %.5E" %ks_arr[i] )
        dcls[ci,:,0] = tempdcl_tt
        dcls[ci,:,1] = tempdcl_ee
        dcls[ci,:,2] = tempdcl_te
        ci += 1
#plt.legend()
#plt.show()
#quit()
#plt.legend()
#plt.show()

if mode == "G" : 
    if renorm == False :
        np.save("Data/G_Data/dcls_numks%i" %num_kbins, dcls)
    elif renorm == True : 
        np.save("Data/G_Data/dcls_numks%i_R" %num_kbins, dcls)

elif mode == "D" : 
    if renorm == False : 
        np.save("Data/D_Data/dcls_numks%i" %num_kbins, dcls)
    elif renorm == True : 
        np.save("Data/D_Data/dcls_numks%i_R" %num_kbins, dcls)

if mode == "G" : 
    if renorm == False : 
        plt.savefig("plots/G_plots/cls.pdf")
    elif renorm == True : 
        plt.savefig("plots/G_plots/cls_R.pdf")

elif mode == "D" : 
    if renorm == False : 
        plt.savefig("plots/D_plots/cls.pdf")
    elif renorm == True : 
        plt.savefig("plots/D_plots/cls_R.pdf")
        
