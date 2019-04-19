import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.integrate import quad

def load_cltf(fname):
    F=open(fname, 'rb')
    tt_size, l_size, q_size = np.fromfile(F, dtype=np.intc, count=3)
    l = np.fromfile(F, dtype=np.intc, count=l_size)
    q = np.fromfile(F, dtype=np.float64, count=q_size)
    data=np.fromfile(F, dtype=np.float64).reshape(tt_size, l_size, q_size)
    return l, q, data

if __name__=='__main__':
    root='/users/dkodwani/Decaying_mode/class_dcmode'
    folder='/'
    gname=['decaycltransfer_ad.dat', 'decaycltransfer_ad.dat']
    folder='/'
    dname=['decaycltransfer_addcs.dat', 'decaycltransfer_addcs.dat']

    gl, gq, gt = load_cltf(root+folder+gname[0])
    dl, dq, dt = load_cltf(root+folder+dname[0])
    scalarg_T = gt[0,:,:] + gt[2,:,:] + gt[3,:,:]
    scalard_T = dt[0,:,:] + dt[2,:,:] + dt[3,:,:]
    scalarg2_T = scalarg_T**2
    scalard2_T = scalard_T**2

    normg_l = []
    normd_l = []
    k_index_g = []
    k_index_d = []

    for l in np.arange(len(gl)) :
        for i in np.arange(len(gq)) : 
            if 1e-3 < gq[i] :
                k_index_g.append(i)
            if 1e-3 < dq[i] :
                k_index_d.append(i)
        temp_int_g = np.trapz(scalarg2_T[l, k_index_g[0]:k_index_g[-1]], gq[k_index_g[0]:k_index_g[-1]])
        temp_int_d = np.trapz(scalard2_T[l, k_index_d[0]:k_index_d[-1]], dq[k_index_d[0]:k_index_d[-1]])
        normg_l.append(temp_int_g)
        normd_l.append(temp_int_d)
    norm_l = np.array(normg_l)/np.array(normd_l)
    
    l_check_index = 2
    l_check = gl[l_check_index]
#    plt.semilogx(gq, scalarg2_T[l_check_index,:], label = "gt")
#    plt.semilogx(gq, norm_l[l_check_index]*scalard2_T[l_check_index,:], label = "dt")
    plt.xlabel(r"$k$ (Mpc$^{-1}$)")
    plt.ylabel(r"$T^2(l =%i)$" %l_check)
#    plt.xlim(1e-4, 1e0)
    plt.legend()
#    plt.savefig("Normalising_check_%i.pdf" %l_check)
#    plt.loglog(gl, normg_l, label='Growing mode')
#    plt.loglog(gl, norm_l*normd_l, label='Decaying mode')
    plt.loglog(gl, norm_l**2, label='Normalising factor')
    plt.xlabel(r"$\ell$")
    plt.ylabel(r"$\int^{10^{-3}} \ dk \ T_\ell^2(k)$")
    plt.legend()
    plt.savefig("Inegral_T2.pdf")
    plt.show()
    

#    ell = 70
#    plt.semilogx(gq, scalarg_T[ell,:], label="growing T l=%i" %gl[ell] )
#    plt.semilogx(gq, scalard_T[ell,:], label="decaying T l=%i" %gl[ell] )
#    plt.legend()
#    plt.show()
