import numpy as np
import matplotlib.pyplot as plt
from classy import Class

A_grow = float(2.3e-9)
lmax = int(2500)

params_fid = {'output' : 'tCl pCl tpCl', 'A_s' : A_grow, 'ic' : 'addcs'}

cosmo_fid = Class() ; cosmo_fid.set(params_fid) ; cosmo_fid.compute()
pps_fid = cosmo_fid.get_primordial()
cls_fid = cosmo_fid.raw_cl(lmax)
cosmo_fid.empty()

ks = pps_fid['k [1/Mpc]']
ls = cls_fid['ell'][2:]
TT = cls_fid['tt'][2:]
EE = cls_fid['ee'][2:]
TE = cls_fid['te'][2:]
plt.loglog(ls, ls*(ls+1)*TT)
plt.show()


