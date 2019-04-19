import matplotlib.pyplot as plt
import numpy as np

#### Importing Cls ####

dclfull = np.load("Fish_data/dcfull.npy") #[numks, nell, (TT,EE,TE)]
clmat = np.load("Fish_data/clfull.npy") #[(TT,EE,TE),nell]

dctt = dclfull[:,:,0]
dcee = dclfull[:,:,1]
dcte = dclfull[:,:,2]

# Defining detector noise                                                                                                                                                                               
#Using the defintiion of detector noise used in "Forecasting isocurvature models with CMB lensing information" by Santos et al (2012). See Eq A9 in this paper.                                            # Defining the noise paramaters - all quantities taken from the paper given above Table VII - we only take the 143 GHz channel                                                                            
arcmin_rad = 3437.75 
thetaarcmin = 7.1
thetaarcmin100 = 9.5
thetaarcmin217 = 5.0
thetaarcmin353 = 5.0
thetarad = thetaarcmin/arcmin_rad
thetarad100 = thetaarcmin100/arcmin_rad
thetarad217 = thetaarcmin217/arcmin_rad
thetarad353 = thetaarcmin353/arcmin_rad

sigmaT = 6.0016*(10**(-6))
sigmaT100 = 6.82*(10**(-6))
sigmaT217 = 13.0944*(10**(-6))
sigmaT353 = 40.1016*(10**(-6))

#sigmaT = 6.0016
#sigmaT100 = 6.82
#sigmaT217 = 13.0944
#sigmaT353 = 40.1016


sigmaP = 11.4576*(10**(-6))
sigmaP100 = 10.9120*(10**(-6))
sigmaP217 = 26.7644*(10**(-6))
sigmaP353 = 81.2944*(10**(-6))

#sigmaP = 11.4576
#sigmaP100 = 10.9120
#sigmaP217 = 26.7644
#sigmaP353 = 81.2944

def dnoise(l):
    return ((thetaarcmin*sigmaT)**2)*np.exp(l*(l+1)*thetarad**2/(8*np.log(2)))                      

def dnoiseP(l):                                                                                   
    return ((thetaarcmin*sigmaP)**2)*np.exp(l*(l+1)*thetarad**2/(8*np.log(2)))                      

def dnoise_full(l):
    return ( ((thetaarcmin*sigmaT)**(-2))*np.exp(-l*(l+1)*(thetarad**2)/(8*np.log(2)))
    + ((thetaarcmin100*sigmaT100)**(-2))*np.exp(-l*(l+1)*(thetarad100**2)/(8*np.log(2)))
    + ((thetaarcmin217*sigmaT217)**(-2))*np.exp(-l*(l+1)*(thetarad217**2)/(8*np.log(2)))
    + ((thetaarcmin353*sigmaT353)**(-2))*np.exp(-l*(l+1)*(thetarad353**2)/(8*np.log(2))))**(-1)

def dnoiseP_full(l):
    return (  ((thetaarcmin*sigmaP)**(-2))*np.exp(-l*(l+1)*(thetarad**2)/(8*np.log(2)))
    + ((thetaarcmin100*sigmaP)**(-2))*np.exp(-l*(l+1)*(thetarad100**2)/(8*np.log(2)))
    + ((thetaarcmin217*sigmaP217)**(-2))*np.exp(-l*(l+1)*(thetarad217**2)/(8*np.log(2)))
    + ((thetaarcmin353*sigmaP353)**(-2))*np.exp(-l*(l+1)*(thetarad353**2)/(8*np.log(2))))**(-1)

#### Fisher matrix ####

numks = 30
ks_arr = np.logspace(-4, 1, numks)
dks = 10**(-5)
dAMP = 5*10**(-1)
lmax = 2500

nell = 2499
dcl = np.zeros((numks,nell,3))
icov = np.zeros((nell, 3, 3, nell))

# Computing the covariance #
#icovdet = -TE**6 + EE*(TE**4)*TT - (EE**2)*(TE**2)*(TT**2) + (EE**3)*(TT**3)
#icovtttt = (EE**3)*TT
#icovttte = EE*(TE**3) - (EE**2)*TE*TT 
#icovttee = -TE**4
#icovtett = EE*(TE**3) - (EE**2)*TE*TT 
#icovtete = -TE**4 + (EE**2)*(TT**2)
#icovteee = (TE**3)*TT - EE*TE*(TT**2)
#icoveett = -TE**4
#icoveete = (TE**3)*TT - EE*TE*(TT**2)
#icoveeee = EE*(TT**3)

full_fish = np.zeros((numks,numks))

#ci = 0
#for i in np.arange(numks) : 
#    fish_sum = []
#    dTTi = dctt[i,:]
#    dEEi = dcee[i,:]
#    dTEi = dcte[i,:]
#    cj = 0
#    for j in np.arange(numks) : 
#            dTTj = dctt[j,:]
#            dEEj = dcee[j,:]
#            dTEj = dcte[j,:]
#            for l in range(2,lmax-1) :
#                fsky=0.5
#                fish_factor = fsky*((2*l+1)/2.)*( dTTi[l]*EE2[l]*dTTj[l]/( (TE2[l] - EE[l]*TT[l])**2) 
#                                              + 2*dTTi[l]*TE2[l]*dTEj[l]/( (TE2[l] - EE[l]*TT[l])**2) 
#                                              - 4*dTTi[l]*EE[l]*TE[l]*dEEj[l]/( (TE2[l] - EE[l]*TT[l])**2)
#                                              + dTEi[l]*TT2[l]*dTEj[l]/( (TE2[l] - EE[l]*TT[l])**2) 
#                                              - 4*dTEi[l]*TE[l]*TT[l]*dEEj[l]/( (TE2[l] - EE[l]*TT[l])**2)
#                                              + 2*dEEi[l]*(TE2[l]+EE[l]*TT[l])*EE[l]/( (TE2[l] - EE[l]*TT[l])))
#                fish_sum.append(fish_factor)
#            full_fish[ci,cj] = np.sum(fish_sum)
#            cj += 1
#    ci += 1

fsky=1.
ci = 0
for i in np.arange(numks) : 
    fish_sum = 0
    dTTi = dctt[i,:]
    dEEi = dcee[i,:]
    dTEi = dcte[i,:]
    dclmati = np.array([[dTTi, dTEi],[dTEi, dEEi]])
    cj = 0
    for j in np.arange(i,numks) : 
            dTTj = dctt[j,:]
            dEEj = dcee[j,:]
            dTEj = dcte[j,:]
            dclmatj = np.array([[dTTj, dTEj], [dTEj, dEEj]])
            for ell in range(0,lmax-1) : 
                invcov = np.linalg.inv(clmat[:,:,ell])
                fish_sum = 0.5*(2*ell+1)*fsky*np.trace(np.dot(invcov, np.dot(dclmati[:,:,ell], np.dot(invcov, dclmatj[:,:,ell]))))
            full_fish[ci,cj] += fish_sum
            if j!=i: 
                full_fish[cj,ci] = full_fish[ci,cj]
            cj += 1
    ci += 1

plt.imshow(full_fish)
plt.savefig('fish1_temp.pdf')

plt.figure()
CS = plt.contour(ks_arr, ks_arr, full_fish, 1000)
cbar = plt.colorbar(CS)
plt.title('Fisher information $I(k_1, k_2)$')
plt.yscale('log')
plt.xscale('log')
plt.savefig('fish2_temp.pdf')
