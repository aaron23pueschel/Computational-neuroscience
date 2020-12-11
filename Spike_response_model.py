import scipy.integrate as integrate
from scipy.integrate import quad
import numpy as np
from numpy import sqrt, sin, cos, pi, exp
C=.1
t_hat = 0
refr = 2
m_reset = 0
h_reset = .26
n1_reset = .58
n2_reset = .21
g_l = .01
m_eq = .0194
h_eq = .8684
n1_eq = .00057
n2_eq = .00025

tau_m = 8.0
tau_h = 8.0
tau_n1 = 100.0
tau_n2 = .75

g_na = .01
g_k = .01
g_l =.01



g_1 = lambda m,h : g_na*m**3*h
g_2 = lambda n1:g_k*n1**4
g_3 = lambda n2:g_k*n2**2
g_4 = g_l

m = lambda t:(m_reset-m_eq)*np.exp(-(t-t_hat-refr)/tau_m)+m_eq
h = lambda t:(h_reset-h_eq)*np.exp(-(t-t_hat-refr)/tau_h)+h_eq
n1 = lambda t:(n1_reset-n1_eq)*np.exp(-(t-t_hat-refr)/tau_n1)+n1_eq
n2 = lambda t:(n2_reset-n2_eq)*np.exp(-(t-t_hat-refr)/tau_n2)+n2_eq

def input_func(time):
      # return (5*math.cos(1/25*time)+math.sin(2/75*time))+1
      # return math.exp(math.cos(1/20*time)-1/2*math.sin(1/30*time))
      # return math.cos(1/100*time)+math.sin(2/50*time)+1
       return 2

def integrand(t):
   return (1/(g_1(m(t-t_hat),h(t-t_hat))+g_2(n1(t-t_hat))+g_3(n2(t-t_hat))+g_4))
def kernel_k(t,s):
    return (1/C)*H(t-t_hat-refr-s)*np.exp(-1*quad(integrand,t-s,t)[0])*input_func(t-s)
def K(t):
    #return kernel_k(1,2)
    return quad(lambda x: kernel_k(t, x), 0, np.inf)[0]
def H(x):
    if(x>=0):
        return 1
    return 0
def tau_x(t):
    sum = 0
    


ms = 1




import math
import matplotlib.pyplot as plt

delta_t = .01
Voltage = []
time = []
for T in range(0,(int)(ms*(1/delta_t))):
     Voltage.append(K(T))
     time.append(T*delta_t)
                                


plt.plot(time,Voltage)
print(Voltage)
#axs[1].plot(time, input,'tab:orange')
#axs[1].set_title('Input current')
#axs[1].set_xlabel('Time (milliseconds)')
#axs[1].set_ylabel('Ie (nA)')
#fig.tight_layout()
plt.show()


    
