import math
import numpy as np
import matplotlib.pyplot as plt





tau_1 = .20
tau_2 = 1.6
C = 10
K = -40
threshold = -55
u_rest = -70
spike_arrival_times = -10000
def PSP(t):
        return (C*t)*math.exp((-t*.01)/tau_1)
def AHP(t):
    if((t*.01)>=.75 ):
        return  K*math.exp((-t*.01)/tau_2)
    else:
        return 0
def input_(t,T):
    if(T>500 and T<3500):
        return 16*math.sin(T*.01)
    return 0
ms = 100

delta_t = .01
Voltage = []
input_list = []
time = []


u = u_rest
u_prev = u


for T in range(0,(int)(ms*(1/delta_t))):
     input =T*.005
     time.append(T*delta_t) 
     u_prev = u
     u = PSP(T-spike_arrival_times)+AHP(T-spike_arrival_times)+input_((T-spike_arrival_times),T)+u_rest
     if(u_prev<=threshold and u>threshold):
        spike_arrival_times=T
     Voltage.append(u)   
     input_list.append(input_(T-spike_arrival_times,T))
     

fig, axs = plt.subplots(2, 1)
axs[0].set_title('SRM0 Model')
axs[0].plot(time, Voltage)
axs[1].set_xlabel('Time')
axs[1].set_ylabel('Input current')
axs[0].set_ylabel('Voltage')
axs[1].plot(time,input_list)
plt.show()


plt.plot(time,input_list)


plt.show()


