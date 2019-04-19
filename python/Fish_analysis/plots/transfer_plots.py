import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import quad
from matplotlib.font_manager import FontProperties
from matplotlib import cm
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

kscale = 1e-3 # SCALE BEYOND WHICH WE NORMALISE!

def load_cltf(fname):
    F=open(fname, 'rb')
    tt_size, l_size, q_size = np.fromfile(F, dtype=np.intc, count=3)
    l = np.fromfile(F, dtype=np.intc, count=l_size)
    q = np.fromfile(F, dtype=np.float64, count=q_size)
    data=np.fromfile(F, dtype=np.float64).reshape(tt_size, l_size, q_size)
    return l, q, data

gl, gq, gt = load_cltf('/users/dkodwani/Decaying_mode/class_dcmode/decaycltransfer_ad.dat')
dl, dq, dt = load_cltf('/users/dkodwani/Decaying_mode/class_dcmode/decaycltransfer_addcs.dat')

sgT = gt[0,:,:] + gt[2,:,:] + gt[3,:,:]
sdT = dt[0,:,:] + dt[2,:,:] + dt[3,:,:]
pgT = gt[1,:,:] + gt[4,:,:] 
pdT = dt[1,:,:] + dt[4,:,:]

sgT2 = sgT**2
sdT2 = sdT**2
pgT2 = pgT**2
pdT2 = pdT**2

ell_1 = 0
ell_2 = 50

plt.figure(figsize = (10,10))
plt.loglog(gq, sgT2[ell_1,:], label = r'$(\Delta^{TT}_G(\ell = %i))^2$' %gl[ell_1], color = 'red', alpha = 0.5)
plt.loglog(gq, sdT2[ell_1,:], label = r'$(\Delta^{TT}_D(\ell = %i))^2$' %dl[ell_1], color = 'red',  ls = '--', alpha = 0.5)
plt.loglog(gq, sgT2[ell_2,:], label = r'$(\Delta^{TT}_G(\ell = %i))^2$' %gl[ell_2], color = 'blue', alpha = 0.5)
plt.loglog(gq, sdT2[ell_2,:], label = r'$(\Delta^{TT}_D( \ell = %i))^2$' %dl[ell_2], color = 'blue', ls = '--', alpha = 0.5)
plt.xlabel("k Mpc$^{-1}$", fontsize = 22)
plt.ylim(1e-14, 10)
plt.xlim([1e-5,2e-1])
plt.tick_params('both', labelsize = 20)
plt.legend(fontsize = 16)
plt.savefig("transfers.pdf")
plt.show()
