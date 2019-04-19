import numpy as np
import pylab as pl
from scipy.interpolate import interp1d
from scipy.integrate import quad

#camb_g_l5= np.loadtxt("/Users/darshkodwani/Desktop/CAMB-0.1.6.1/pycamb/grow_trnsf_l5.txt",unpack=True)
#camb_d_l5= np.loadtxt("/Users/darshkodwani/Desktop/CAMB-0.1.6.1/pycamb/decay_trnsf_l5.txt",unpack=True)
#camb_ks = np.loadtxt("/Users/darshkodwani/Desktop/CAMB-0.1.6.1/pycamb/list_ks.txt",unpack=True)

def load_cltf(fname):

    F=open(fname, 'rb')

    tt_size, l_size, q_size = np.fromfile(F, dtype=np.intc, count=3)

    l = np.fromfile(F, dtype=np.intc, count=l_size)
    q = np.fromfile(F, dtype=np.float64, count=q_size)

    data=np.fromfile(F, dtype=np.float64).reshape(tt_size, l_size, q_size)

    return l, q, data

if __name__=='__main__':
    #
    root='/users/dkodwani/Decaying_mode/class_dcmode'

    # scalar #
    folder='/'
    gname=['decaycltransfer_ad.dat', 'decaycltransfer_ad.dat']

    folder='/'
    dname=['decaycltransfer_addcs.dat', 'decaycltransfer_addcs.dat']

    # tesnor #
    #folder='output/'
    #fname=['decay_tensor/cltransfer_ad.dat', 'decay_tensor/cltransfer_ten.dat', \
    #       'decay_tensor/cltransfer_addct.dat']



    # for scalar, the first few common outputs are [t2, e, t0, t1, b ...]
    # for tensor, the common outputs are [t2, e, b ]


    gl, gq, gt=load_cltf(root+folder+gname[0])
    dl, dq, dt=load_cltf(root+folder+dname[0])
    print gt.shape
    print 'gl=', dl
    print 'gq=', gq
    

    #tt_idx = -1
#    llist=[0, 1, 2, 3, 4, 5, 10, 20, 50]    
    llist = [2]
    
    fig_size = pl.rcParams["figure.figsize"]
    fig_size[0] = 12
    fig_size[1] = 12
    """
    for li in llist:
        pl.loglog(dq,( gt[0,li,:] + gt[2,li,:] + gt[3,li,:] )**2, 'b', label = 'Growing')   # t0, t2, t3
        pl.loglog(dq,( dt[0,li,:] + dt[2,li,:] + dt[3,li,:] )**2, 'r', label = 'Decaying')
    pl.xlabel(r"k (Mpc$^{-1}$)", fontsize = 25)
    pl.ylabel(r"$\Delta_{%i}(k)^2$" %gl[li], fontsize = 25)
    pl.xlim(10**(-5),10**(0))
    pl.ylim(10**(-13),10**(-1))
    pl.tick_params(axis = 'both', which = 'major', labelsize = 20)
    pl.legend(fontsize = 20)
    pl.savefig("T_lowl.pdf")
    """


#    pl.show()
    
#    T_tot = (gt[0,3,:] + gt[2,3,:] + gt[3,3,:])**2
#    T_interp = interp1d(gq, T_tot)
#    pl.loglog(gq, T_tot, label = 'tot')
#    pl.loglog(gq, T_interp(gq), label = 'interp')
#    pl.legend()
#    pl.show()
#    quit()
    
    def power(k,kp,ns,As) :
        return As*(k/kp)**(ns-1)

    def cls(l, k, kp, As, ns) : 
        cltemp = []
        for ell in np.arange(np.size(l)) - 1 : 
            T_tot = (gt[0,ell,:] + gt[2,ell,:] + gt[3,ell,:])**2
            T_interp = interp1d(k, T_tot)
            cl_int_l = quad(lambda x : T_interp(np.exp(x))*power(np.exp(x),kp,ns,As)*np.log(10), min(np.log(k)), max(np.log(k)))[0]
            cltemp.append(cl_int_l)
        cls_interp = interp1d(l, cltemp)
        pl.loglog(l, l*(l+1)*cls_interp(l), label = 'cls_interp')
        pl.show()

    cls(gl[10:], gq, 0.05, 0.96, 2.215e-9)
#    pl.show()

#    cls_growing = cls(gl[0:5], gq, 0.05, 0.96, 2.215e-9)
#    pl.semilogy(gl[0:5], cls_growing(gl[0:5]))
#    pl.show()
