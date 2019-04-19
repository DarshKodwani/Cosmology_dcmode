import numpy as np
import matplotlib.pyplot as plt

#Universal params#

kmax = 1e1
kmin = 1e-4
numks = 200
ks_arr = np.linspace(kmin, kmax, numks)

#Cls

dclfull = np.load("Fish_data/dcfull_%i_lin.npy" %numks) #[numks, nell, (TT,EE,TE)]
clmat = np.load("Fish_data/clfull_%i_lin.npy" %numks) #[(TT,EE,TE), nell]
planck_noise = np.load("Fish_data/planck_noise.npy") #[TT, EE], nell#

ls = np.arange(2, len(clmat[0,0])+2)
factor = ls*(ls+1)/(2*np.pi)

dctt = dclfull[:,:,0]

tt_cov = clmat[0,0] + planck_noise[0,:]

#plt.loglog(ls, clmat[0,0], label = 's')
#plt.loglog(ls, planck_noise[0,:], label = 'n')
#plt.legend()
#plt.show()
#quit()
### Fisher matrix ###

full_fish = np.zeros((numks, numks))
fsky = 1.
fish_factor = fsky*(ls+0.5)
fish_sum = []
ci = 0 

for i in np.arange(numks) : 
    print "K NUMBER", i
    dTTi = dctt[i,:]
    cj = 0 
    for j in np.arange(numks) : 
        dTTj = dctt[j,:]
#        for ell in ls : 
#            temp = fish_factor[ell]*dTTi[ell]*dTTj[ell]/tt_cov[ell]**2
#            fish_sum.append(temp)
#        full_fish[ci, cj] = np.sum(fish_sum)
        full_fish[ci, cj] = np.sum(fish_factor*(dTTi*dTTj/tt_cov**2))
        cj += 1
    ci += 1

np.save("Fish_data/TT_fish_%i_lin.npy" %numks, full_fish)

