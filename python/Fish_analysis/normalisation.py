import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import quad

kscale = 3e-3 # SCALE BEYOND WHICH WE NORMALISE!

def load_cltf(fname):
    F=open(fname, 'rb')
    tt_size, l_size, q_size = np.fromfile(F, dtype=np.intc, count=3)
    l = np.fromfile(F, dtype=np.intc, count=l_size)
    q = np.fromfile(F, dtype=np.float64, count=q_size)
    data=np.fromfile(F, dtype=np.float64).reshape(tt_size, l_size, q_size)
    return l, q, data

gl, gq, gt = load_cltf('/Users/kodwani/Documents/Codes_glamdring/class_dcmode/decaycltransfer_ad.dat')
dl, dq, dt = load_cltf('/Users/kodwani/Documents/Codes_glamdring/class_dcmode/decaycltransfer_addcs.dat')

sgT = gt[0,:,:] + gt[2,:,:] + gt[3,:,:]
sdT = dt[0,:,:] + dt[2,:,:] + dt[3,:,:]
pgT = gt[1,:,:] + gt[4,:,:] 
pdT = dt[1,:,:] + dt[4,:,:]

sgT2 = sgT**2
sdT2 = sdT**2
pgT2 = pgT**2
pdT2 = pdT**2

snormg_l = []
snormd_l = []
pnormg_l = []
pnormd_l = []

for l in np.arange(len(gl)) : 
    k_index_g = []
    k_index_d = []
    for i in np.arange(len(gq)) : 
        if kscale < gq[i] : 
            k_index_g.append(i)
        if kscale < dq[i] : 
            k_index_d.append(i)
#        print(i)
    temp_int_sg = np.trapz(sgT2[l, k_index_g[0]:k_index_g[-1]], gq[k_index_g[0]:k_index_g[-1]])
    temp_int_sd = np.trapz(sdT2[l, k_index_d[0]:k_index_d[-1]], dq[k_index_d[0]:k_index_d[-1]])
    snormg_l.append(temp_int_sg)
    snormd_l.append(temp_int_sd)

    temp_int_pg = np.trapz(pgT2[l, k_index_g[0]:k_index_g[-1]], gq[k_index_g[0]:k_index_g[-1]])
    temp_int_pd = np.trapz(pdT2[l, k_index_d[0]:k_index_d[-1]], dq[k_index_d[0]:k_index_d[-1]])
    pnormg_l.append(temp_int_pg)
    pnormd_l.append(temp_int_pd)

snorm_l = np.array(snormg_l)/np.array(snormd_l)
pnorm_l = np.array(pnormg_l)/np.array(pnormd_l)
snorm_l = np.sqrt(snorm_l)
pnorm_l = np.sqrt(pnorm_l)

np.save("Data/renorm_temp", snorm_l)
np.save("Data/renorm_pol", pnorm_l)
np.save("Data/renorm_ls", gl)


plt.plot(gl, snorm_l)
plt.xlabel("ell")
plt.title("Renormalizing function")
plt.savefig("plots/Renorm_function.pdf")
plt.show()
quit()


ell_index = 60
#print(gl[ell_index])
#print(snorm_l[ell_index])
plt.loglog(gq, sgT2[ell_index, :], label = 'G', alpha = 1)
plt.loglog(gq, sdT2[ell_index, :], label = 'D', alpha = 0.4)
#plt.loglog(gq, (snorm_l[ell_index]**2)*sdT2[ell_index, :], label = 'D_R', alpha = 0.4, ls = '--')
plt.title("ell = %i, horizon k = %.2E" %(gl[ell_index], kscale))
plt.legend()
plt.savefig("plots/test_not_renorm_transfer.pdf")
plt.show()
