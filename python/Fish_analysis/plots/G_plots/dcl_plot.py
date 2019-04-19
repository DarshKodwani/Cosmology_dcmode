import numpy as np
import matplotlib.pyplot as plt

dcl = np.load("../Data/dcls_numks20.npy")

ls = np.arange(len(dcl[0,:,0]))[2:]

plt.figure()
for i in np.arange(len(dcl[:,0,0])) : 
    plt.loglog(ls, dcl[i,:,2][2:])

plt.legend()
plt.show()
