import matplotlib.pyplot as plt
import numpy as np
from classy import Class
import sys

if len(sys.argv)!=2 :
    print "Usage: noise.py mode (D or G)"
    exit(1)

mode = sys.argv[1]

amintorad = np.pi/(60*180) #rad = amintorad*amin
muKtoK = 1e-12

Planck_100 = {'freq' : 100, 'beam_size' : 9.5*amintorad, 'sigmatt' : 6.82*amintorad, 'sigmaee' : 10.9120*amintorad}
Planck_143 = {'freq' : 143, 'beam_size' : 7.1*amintorad, 'sigmatt' : 6.0016*amintorad, 'sigmaee' : 11.4576*amintorad}
Planck_217 = {'freq' : 217, 'beam_size' : 5.*amintorad, 'sigmatt' : 13.0944*amintorad, 'sigmaee' : 26.7644*amintorad}
Planck_353 = {'freq' : 353, 'beam_size' : 5.*amintorad, 'sigmatt' : 40.1016*amintorad, 'sigmaee' : 81.2944*amintorad}

planck_noise = [Planck_100, Planck_143, Planck_217, Planck_353]
fig = plt.figure(figsize=(10, 10))
ax0 = fig.add_axes([0.1, 0.5, 0.8, 0.4])
ax1 = fig.add_axes([0.1, 0.1, 0.8, 0.4])
ax = [ax0, ax1]

observables = ['tt', 'ee']

lmax = 2500
ls = np.arange(2,lmax+1)
factor = ls*(ls+1)/(2*np.pi)

params_grow = {
    'output' : 'tCl pCl tpCl mPk', 
    'lensing' : 'no', 
    'A_s' : 2.3e-9,
    'h' : 0.6711, 
    'omega_b' : 0.022068,
    'omega_cdm' : 0.12029}
cosmo = Class()
cosmo.set(params_grow)
cosmo.compute()
fullcl_grow = cosmo.raw_cl(lmax)
cosmo.empty()

noise_full = np.zeros((len(observables), len(ls)))
n = 0   
for a in observables : 
    sigma = 'sigma' + a

    def noise_one(l, theta_beam, sigma) : 
        return (sigma**2)*np.exp(l*(l+1)*(theta_beam**2)/(8*np.log(2)))

    def full_noise(l, noise_list) :
        temp = []
        for j in noise_list : 
            temp.append( (j[sigma]**2)*np.exp(-l*(l+1)*(j['beam_size']**2)/(8*np.log(2))))
        return np.sum(temp, axis = 0)

    noise_full[n,:] = muKtoK*full_noise(ls, planck_noise)

    for j in planck_noise : 
        ax[n].plot(ls, muKtoK*factor*noise_one(ls, j['beam_size'], j[sigma]), '--', label = 'Channel frequency %i GHz' %j['freq']) 
        ax[n].set_yscale('log')
    
    ax[n].plot(ls, muKtoK*factor*full_noise(ls, planck_noise), label = 'Full noise ' )
    ax[n].plot(ls, factor*fullcl_grow[a][2:], label = 'Signal ' )
    ax[n].set_yscale('log')
    ax[n].set_xlabel(r"$\ell$", fontsize = 18)
    ax[n].set_ylabel(r"$\ell(\ell+1)C_{\ell}^{%s}/{2 \pi}$" %a, fontsize = 18)
    ax[n].tick_params(axis = 'both', which = 'major', labelsize = 15)
    n = n + 1
    
#np.save("Data/noise_full" %mode, noise_full)
ax[0].legend(loc = "lower right", fontsize = '16')
#plt.savefig("Noise_TTEE.pdf")
plt.loglog(ls, factor*noise_full[0,:])
plt.show()
