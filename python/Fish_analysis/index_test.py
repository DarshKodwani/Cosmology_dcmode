import numpy as np

cl = np.array([1.,2.,3.])
invcl = 1/cl
dcl = np.zeros((2,3))
dcl[0,:] = cl*1.1
dcl[1,:] = cl*1.2
fish = np.zeros((2,2))
ls = np.array([1.,2.,3.])
factor_fish = (ls+0.5)

for i in np.arange(2) : 
    dcli = dcl[i,:] 
    for j in np.arange(2) : 
        dclj = dcl[j,:]
#        fish[i,j] = sum(factor_fish*dcli*invcl*dclj*invcl)
        fish_temp = []
        for ell in np.arange(len(ls)) : 
            fish_temp.append(factor_fish[ell]*dcli[ell]*invcl[ell]*dclj[ell]*invcl[ell])
        fish[i,j] = sum(fish_temp)

print fish
