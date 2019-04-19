import matplotlib.pyplot as plt
import numpy as np

#Universal params#

kmax = 1
kmin = -4
numks = 20
ks_arr = np.logspace(kmin, kmax, numks)
mode = "d"

#Cls

dcl = np.load("Fish_data/dcl_%s_%i.npy" %(mode,numks)) #[numks, nell, (TT,EE,TE)]
clmat = np.load("Fish_data/clfid_%i.npy" %numks) #[(TT,EE,TE), nell]
planck_noise = np.load("Fish_data/planck_noise.npy") #[TT, EE], nell

ls = np.arange(2, len(clmat[0,0])+2)
factor = ls*(ls+1)/(2*np.pi)

dctt = dcl[:,:,0]
dcee = dcl[:,:,1]
dcte = dcl[:,:,2]

clmat[0,0] = clmat[0,0] + planck_noise[0,:]
clmat[1,1] = clmat[1,1] + planck_noise[1,:]

#plt.loglog(ls, factor*clmat[0,0], label = 's')
#plt.loglog(ls, factor*planck_noise[0,:], label = 'n')
#plt.legend()
#plt.show()
#quit()

### Fisher matrix ###

full_fish = np.zeros((numks, numks))
TT_fish = np.zeros((numks, numks))
fsky = 1.
fish_factor = fsky*(ls+0.5)
tt_cov = clmat[0,0] + planck_noise[0,:]

ci = 0 
for i in np.arange(numks) : 
    print "K NUMBER", i
    dTTi = dctt[i,:]
    dEEi = dcee[i,:]
    dTEi = dcte[i,:]
    clmati = np.array([[dTTi, dTEi], [dTEi, dEEi]])
    cj = 0
    for j in np.arange(numks) : 
        dTTj = dctt[j,:]
        dEEj = dcee[j,:]
        dTEj = dcte[j,:]
        clmatj = np.array([[dTTj, dTEj], [dTEj, dEEj]])
        TT_fish[ci, cj] = np.sum(fish_factor*(dTTi*dTTj/tt_cov**2))
        for l in np.arange(len(clmat[0,0])) : 
            icov = np.linalg.inv(clmat[:,:,l])
            fish_sum = 0.5*(2*ls[l]+1)**np.trace(np.dot(icov, np.dot(clmati[:,:,l], np.dot(icov, clmatj[:,:,l]))))
            full_fish[ci,cj] += fish_sum
        cj += 1 
    ci += 1 

np.save("Fish_data/full_fish_%s_%i" %(mode, numks), full_fish)
np.save("Fish_data/TT_fish_%s_%i" %(mode, numks), TT_fish)
