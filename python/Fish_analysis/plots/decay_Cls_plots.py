import numpy as np
import matplotlib.pyplot as plt
from classy import Class
import matplotlib
from matplotlib import cm
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

params_grow = {
    'output' : 'tCl pCl tpCl mPk', 
    'lensing' : 'no', 
    'A_s' : 2.3e-9,
    'h' : 0.6711, 
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029}

params_decay = {
    'output' : 'tCl pCl tpCl mPk', 
    'lensing' : 'no', 
    'A_s' : 2.3e-9, 
    'h' : 0.6711, 
    'omega_b' : 0.022068, 
    'omega_cdm' : 0.12029,
    'ic' : 'ad&addcs',
    'f_addcs' : .1,
    'n_addcs' : 1., 
    'alpha_addcs' : 0.,
    'phi_addcs' : 0.}
#    'phi_addcs' : 0.785 }

lmax = 2500
l = np.array(range(2,lmax+1))
factor = l*(l+1)/(2*np.pi)

cosmo = Class()
cosmo.set(params_grow)
cosmo.compute()
fullcl_grow = cosmo.raw_cl(lmax)
cosmo.empty()

frac_decay = np.linspace(0.1,1,4)

fig, ax = plt.subplots(1, 3, tight_layout = True, figsize=(15,5))

ax[0].plot(l, factor*fullcl_grow['tt'][2:], label = "Growing only")
ax[0].set_ylabel('$\ell(\ell+1)C^{TT}_\ell [K^2]$', fontsize = 15)
ax[0].set_xlabel('$\ell$', fontsize = 15)
ax[0].set_title('Temperature', fontsize = 15)
ax[0].set_yscale('log')
ax[0].set_xscale('log')
ax[0].set_xlim([2,2200])
ax[0].tick_params(axis='both', which='major', labelsize=15)

ax[1].plot(l, factor*fullcl_grow['ee'][2:], label = "Growing")
ax[1].set_ylabel('$\ell(\ell+1)C^{EE}_\ell [K^2]$', fontsize = 15)
ax[1].set_xlabel('$\ell$', fontsize = 15)
ax[1].set_title('Polarization', fontsize = 15)
ax[1].set_yscale('log')
ax[1].set_xscale('log')
ax[1].set_xlim([2,2200])
ax[1].tick_params(axis='both', which='major', labelsize=15)

ax[2].plot(l, factor*fullcl_grow['te'][2:], label = "Growing")
ax[2].set_ylabel('$\ell(\ell+1)C^{TE}_\ell [K^2]$', fontsize = 15)
ax[2].set_xlabel('$\ell$', fontsize = 15)
ax[2].set_title('Polarization + Temperature', fontsize = 15)
ax[2].set_yscale('log')
ax[2].set_xscale('log')
ax[2].set_xlim([2,2200])
ax[2].tick_params(axis='both', which='major', labelsize=15)

for j in frac_decay :
    cosmo = Class(); cosmo.set(params_decay) ; cosmo.set({'f_addcs' : j}) ; cosmo.compute() ; cosmo.empty()
    ax[0].plot(l, factor*cosmo.raw_cl(lmax)['tt'][2:], label = "Decay with $f_{GD}$ = %1.2f" %j)
    ax[1].plot(l, factor*cosmo.raw_cl(lmax)['ee'][2:], label = "Decay with $f_{GD}$ = %1.2f" %j)
    ax[2].plot(l, factor*cosmo.raw_cl(lmax)['te'][2:], label = "Decay with $f_{GD}$ = %1.2f" %j)

ax[0].legend(fontsize = 12)    
plt.subplots_adjust(wspace = 0.01)
plt.savefig("decay_cls.pdf")
plt.show()

