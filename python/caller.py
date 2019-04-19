import pylab as pl
import classy


print classy.__file__



def run_class(param, lmax=2000):

    cosmo = classy.Class()
    cosmo.set(param)
    cosmo.compute()
    
    cls = cosmo.lensed_cl(lmax)

    cosmo.struct_cleanup()
    cosmo.empty()

    return cls


if __name__=='__main__':
    # Define your cosmology (what is not specified will be set to CLASS default parameters)
    params = {
        'output': 'tCl lCl',
        'l_max_scalars': 2000,
        'lensing': 'yes',
        'A_s': 2.3e-9,
        'n_s': 0.9624, 
        'h': 0.6711,
        'omega_b': 0.022068,
        'omega_cdm': 0.12029,
        }
    cls_fid=run_class(params)
    
    # decay mode 1 #
    dcparam={
        'ic' : 'ad&addcs',
        'f_addcs': 1.,
        'n_addcs': 1.,
        'alpha_addcs': 0.,
        'phi_addcs': 0.785,
        }
    dcparam.update(params)
    cls_dc1=run_class(dcparam)
    
    
    # decay mode 2 #
    dcparam={
        'ic' : 'ad&addcs',
        'f_addcs': 0.2,
        'n_addcs': 1.,
        'alpha_addcs': 0.,
        'phi_addcs': 0.785,
        }
    dcparam.update(params)
    cls_dc2=run_class(dcparam)
    
    
    # 
    pl.loglog(cls_fid['ell'], cls_fid['ell']*(cls_fid['ell']+1)*cls_fid['tt'], 'b-')
    pl.loglog(cls_dc1['ell'], cls_dc1['ell']*(cls_dc1['ell']+1)*cls_dc1['tt'], 'r-')
    pl.loglog(cls_dc2['ell'], cls_dc2['ell']*(cls_dc2['ell']+1)*cls_dc2['tt'], 'k-')
    
    pl.show()
