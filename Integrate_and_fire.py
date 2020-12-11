import math
import matplotlib.pyplot as plt


## Constants given by the text ##

E_l = -65
R_m = 10
V_th = -50 
tau_m = 10
V_reset = -65
V_max = 0



## Empty lists to graph results
Voltage = []
input = []
time = []

## Initial voltage ##
V = E_l

## Total time, in milliseconds
ms = 500

## Initial electrode current ##
I = 0

## Time step ##
delta_t = .01




## These are functions to test out the input
## uncomment out the ones you wish to test

def input_func(time):
       return (1/3*math.cos(1/25*time)+math.sin(2/75*time))+1
      # return math.exp(math.cos(1/20*time)-1/2*math.sin(1/30*time))
      # return math.cos(1/100*time)+math.sin(2/50*time)+1
      # return 2

for T in range(0,(int)(ms*(1/delta_t))):
    if( V>1000 or V<-1000):        ## Check for overflow 
        continue

    # Evaluate input current
    I = input_func(T*delta_t)

    # Implement function for spikes, occurring when V crosses V_th threshold
    if(V >= V_th):
        V = V_max
        Voltage.append(V_max)
        V = V_reset
        Voltage.append(V_reset)
        time.append((T*delta_t)+delta_t)
        time.append((T*delta_t)+2*delta_t)
        input.append(input_func(T*delta_t+delta_t))
        input.append(input_func(T*delta_t+2*delta_t))
        T=T+2
        

    ## Calculate voltage using forward euler method
    V = V + ((1/tau_m)*(E_l-V+R_m*I))*delta_t

    # Save function values in list to plot points
    Voltage.append(V)
    input.append(I)
    time.append(T*delta_t)
    
                                ## Plotting the points ## 


fig, axs = plt.subplots(2, 1)
axs[0].plot(time, Voltage,'tab:green')
axs[0].set_title('Voltage')
axs[0].set_title('Voltage')
axs[0].set_ylabel('Voltage (mV)')
axs[0].set_xlabel('Time (milliseconds)')
axs[0].grid(True)

axs[1].plot(time, input,'tab:orange')
axs[1].set_title('Input current')
axs[1].set_xlabel('Time (milliseconds)')
axs[1].set_ylabel('Ie (nA)')
fig.tight_layout()
plt.show()


    
