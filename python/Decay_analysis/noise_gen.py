import matplotlib.pyplot as plt
import numpy as np
from classy import Class

amintorad = np.pi/(60*180) #rad = amintorad*amin
muKtoK = 1e-12

Planck_100 = {'freq' : 100, 'beam_size' : 9.5*amintorad, 'sigmatt' : 6.82*amintorad, 'sigmaee' : 10.9120*amintorad}
Planck_143 = {'freq' : 143, 'beam_size' : 7.1*amintorad, 'sigmatt' : 6.0016*amintorad, 'sigmaee' : 11.4576*amintorad}
Planck_217 = {'freq' : 217, 'beam_size' : 5.*amintorad, 'sigmatt' : 13.0944*amintorad, 'sigmaee' : 26.7644*amintorad}
Planck_353 = {'freq' : 353, 'beam_size' : 5.*amintorad, 'sigmatt' : 40.1016*amintorad, 'sigmaee' : 81.2944*amintorad}

planck_noise = [Planck_100, Planck_143, Planck_217, Planck_353]
observables = ['tt', 'ee']
lmax = 2500
ls = np.arange(2,lmax+1)
factor = ls*(ls+1)/(2*np.pi)

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
    n = n + 1
 
np.save("Fish_data/planck_noise", noise_full)
#plt.semilogy(ls, factor*noise_full[0,:], label = 'T')
#plt.semilogy(ls, factor*noise_full[1,:], label = 'E')
#plt.legend()
#plt.show()
