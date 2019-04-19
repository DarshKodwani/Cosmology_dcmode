import matplotlib.pyplot as plt
import numpy as np 

def mycorr(fish):
    cov = np.linalg.inv(fish)
    corr = np.zeros([len(np.diag(cov)), len(np.diag(cov))])
    for i in np.arange(len(np.diag(cov))) : 
        for j in np.arange(len(np.diag(cov))) : 
            corr[i, j] = cov[i,j]/np.sqrt(cov[i,i]*cov[j,j])
    return corr 

kmax = 1
kmin = -4
numks = 20
ks_arr = np.logspace(kmin, kmax, numks)
TEdata = np.load("fish_%i_log.npy" %numks)
Tdata = np.load("TT_fish_%i_log.npy" %numks)

#print(np.where(Tdata==1)[0])
#print(np.linalg.inv(Tdata))
quit()
covar_T = np.linalg.inv(Tdata)
covar_TE = np.linalg.inv(TEdata)


