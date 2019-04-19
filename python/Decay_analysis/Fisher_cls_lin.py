import matplotlib.pyplot as plt
import numpy as np

#Universal params#

kmax = 1e1
kmin = 1e-4
numks = 200
ks_arr = np.linspace(kmin, kmax, numks)

#Cls

dclfull = np.load("Fish_data/dcfull_%i_lin.npy" %numks) #[numks, nell, (TT,EE,TE)]
clmat = np.load("Fish_data/clfull_%i_lin.npy" %numks) #[(TT,EE,TE), nell]
planck_noise = np.load("Fish_data/planck_noise.npy") #[TT, EE], nell

ls = np.arange(2, len(clmat[0,0])+2)
factor = ls*(ls+1)/(2*np.pi)

dctt = dclfull[:,:,0]
dcee = dclfull[:,:,1]
dcte = dclfull[:,:,2]

clmat[0,0] = clmat[0,0] + planck_noise[0,:]
clmat[1,1] = clmat[1,1] + planck_noise[1,:]

#plt.loglog(ls, factor*clmat[0,0], label = 's')
#plt.loglog(ls, factor*planck_noise[0,:], label = 'n')
#plt.legend()
#plt.show()
#quit()

### Fisher matrix ###

full_fish = np.zeros((numks, numks))
fsky = 1.

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
        for l in np.arange(len(clmat[0,0])) : 
            icov = np.linalg.inv(clmat[:,:,l])
            fish_sum = 0.5*(2*ls[l] + 1)*fsky*np.trace(np.dot(icov, np.dot(clmati[:,:,l], np.dot(icov, clmatj[:,:,l]))))
            full_fish[ci,cj] += fish_sum
        cj += 1
    ci += 1 

np.save("Fish_data/fish_%i_lin" %numks, full_fish)
