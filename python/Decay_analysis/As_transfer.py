import matplotlib.pyplot as plt
import numpy as np
from classy import Class

params = { 
    'output': 'tCl pCl tpCl dCl vCl',
    'lensing': 'no',
    'A_s' : 2.3e-9,
    'n_s' : 1,
    'h' : 0.6711,
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029}

lmax = 2500

#Theory Cls
"""
As_list = np.linspace(2., 3., 11)

for j in As_list : 
    cosmo = Class()
    cosmo.set(params) ; cosmo.set({'A_s' : j})
    cosmo.compute()
    fullcl = cosmo.raw_cl(lmax)
    cosmo.struct_cleanup()
    cosmo.empty()
    plt.loglog(fullcl['ell'][2:], factor*fullcl['tt'][2:], label = "As = %0f" %j)
    
plt.legend()
plt.show()
"""
#Fisher for As

As_fid = 2.3e-9
dAs = As_fid*10**(-2)
#ns_fid = 0.96
#dns = ns_fid*10**(-2)
#h_fid =0.6711
#dh = h_fid*10**(-2)
fsky = 1.

cosmo_fid = Class()
cosmo_fid.set(params) 
cosmo_fid.set({'output':'tCl,pCl,lCl,dTk,vTk','ic':'ad,addcs','z_pk':'0.0,1.0,2.0,4.0,7.0,13.0, 1000.0'})
cosmo_fid.compute()
transfers = cosmo_fid.get_transfer()
tr_ad = transfers['ad']
tr_addcs = transfers['addcs']
plt.plot(tr_ad['k (h/Mpc)'], tr_ad['t_tot'], label = 'grow')
plt.plot(tr_addcs['k (h/Mpc)'], tr_addcs['t_tot'], label = 'decay')
plt.legend()
plt.show()
quit()

fid_cl = cosmo_fid.raw_cl(lmax)
cosmo_fid.struct_cleanup()
cosmo_fid.empty()

cosmo_p = Class()
cosmo_p.set(params) 
cosmo_p.set({'A_s' : As_fid + dAs}) 
cosmo_p.compute()
p_cl = cosmo_p.raw_cl(lmax)
cosmo_p.struct_cleanup()
cosmo_p.empty()

cosmo_m = Class()
cosmo_m.set(params) 
cosmo_m.set({'A_s' : As_fid - dAs}) 
cosmo_m.compute()
m_cl = cosmo_m.raw_cl(lmax)
cosmo_m.struct_cleanup()
cosmo_m.empty()

dcl_tt = (p_cl['tt'][2:] - m_cl['tt'][2:])/(2*dAs)

factor = fid_cl['ell'][2:]*(fid_cl['ell'][2:]+1)/(2*np.pi)
#plt.loglog(fid_cl['ell'][2:], factor*dcl_tt)
plt.loglog(fid_cl['ell'][2:], factor*fid_cl['tt'][2:])
plt.show()
quit()


fish_temp = dcl_tt**2/(fid_cl['tt'][2:]**2)
prefac = fsky*(2*fid_cl['ell'][2:] + 1)/2.
fish = sum(prefac*fish_temp)
print np.sqrt(1/fish)
