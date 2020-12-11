import math
import matplotlib.pyplot as plt


## Constants given by the Dayan and Abbot ##
g_l = .003      
g_k = .36
g_na = 1.2
E_l = -54.387
E_k = -77
E_na= 50   

A = 10                     ## Surface area
c_m = .02                  ## Membrane capacitance


## Rate functions given by Dayan and Abbot ##

alpha_n = lambda V: (.01*(V+55))/(1-(math.exp(-.1*(V+55))))
beta_n = lambda V:.125*math.exp(-.0125*(V+65))

alpha_m = lambda V:.1*(V+40)/(1-math.exp(-.1*(V+40)))
beta_m = lambda V:4*math.exp(-.0556*(V+65))

alpha_h = lambda V:.07*math.exp(-.05*(V+65))
beta_h = lambda V:1/(1+math.exp(-.1*(V+35)))

n_inf = lambda V:alpha_n(V)/(alpha_n(V)+beta_n(V))
tau_n = lambda V: 1/(alpha_n(V)+beta_n(V))

m_inf = lambda V:alpha_m(V)/(alpha_m(V)+beta_m(V))
tau_m = lambda V: 1/(alpha_m(V)+beta_m(V))

h_inf = lambda V:alpha_h(V)/(alpha_h(V)+beta_h(V))
tau_h = lambda V: 1/(alpha_h(V)+beta_h(V))


## Empty lists to graph results
Voltage = []
sodium_channel = []
potassium_channel = []
membrane_current = []
M = []
N = []
H = []
time = []

## Initial voltage ##
V=-70

# Initial values of m, n and h
n=.4
h=.6
m=.1


## Total time, in milliseconds
ms = 20

## Initial Electrode current ##
I = 0

## Time step ##
delta_t = .01

for T in range(0,(int)(ms*(1/delta_t))):
    if(V==-55 or V==-65 or V==-40 or V>1000 or V<-1000):        ## Check for overflow or division by 0
        continue


    ## Compute gating variables m,n,h
                                                                ## Calculate dm/dt, dn/dt and dh/dt using forward euler method: 
    n = n + ((n_inf(V)-n)/tau_n(V))*delta_t                     ## y(t + Δt) = y(t) + f(y(t))* Δt
    N.append(n)

    h = h + ((h_inf(V)-h)/tau_h(V))*delta_t
    H.append(h)

    m = m + ((m_inf(V)-m)/tau_m(V))*delta_t
    M.append(m)
    
   # n = n_inf(V)+(n-n_inf(V))*math.exp(-delta_t/tau_n(V))
   # h = h_inf(V)+(h-h_inf(V))*math.exp(-delta_t/tau_h(V))      # Another way of calculating m, n, h 
   # m = m_inf(V)+(m-m_inf(V))*math.exp(-delta_t/tau_m(V))

    
    

    ## Calculate sodium conductance
    G_na = g_na*m**3*h
    sodium_channel.append(100*G_na)

    ## Calculate potassium conductance
    G_k = g_k*n**4
    potassium_channel.append(100*G_k)

    ## Calculate membrane potential
    i_m = (g_l*(V-E_l)+(G_k*(V-E_k))+(G_na*(V-E_na)))
    membrane_current.append(i_m)

    ## Calculate voltage using forward euler method
    V = V+((-i_m/c_m+((I/A)/c_m)))*delta_t
    Voltage.append(V)

    ## input current between time 5ms and 10ms
    if(T>500 and T<1000):
        I=1
    else:
        I=0
    
    time.append(T*delta_t)
    
                                ## Plotting the points ## 
## plot n ##

fig, axs = plt.subplots(2, 3)
axs[0, 0].plot(time, N,'tab:green')
axs[0, 0].set_ylabel('n')
axs[0, 0].set_xlabel('Time (ms)')
axs[0, 0].set_ylim(0,1)

## plot m ##
axs[0, 1].plot(time, M, 'tab:orange')
axs[0, 1].set_ylim(0,1)
axs[0, 1].set_ylabel('m')
axs[0, 1].set_xlabel('Time (ms)')

## plot h ##
axs[0, 2].plot(time, H, 'tab:purple')
axs[0, 2].set_ylim(0,1)
axs[0, 2].set_ylabel('h')
axs[0, 2].set_xlabel('Time (ms)')

## plot Voltage
axs[1, 0].plot(time, Voltage, 'tab:cyan')
axs[1, 0].set_title('Voltage')
axs[1, 0].set_ylabel('(mV)')
axs[1, 0].set_xlabel('Time (ms)')
axs[1, 0].set_ylim(-100,100)

##plot membrane current
axs[1, 1].plot(time, membrane_current, 'tab:blue')
axs[1, 1].set_title('Membrane Current')
axs[1, 1].set_xlabel('Time (ms)')
axs[1, 1].set_ylabel('im (µA/mm^2)')
#axs[1, 1].set_ylim(-10,10)

# plot sodium and potassium conductance
axs[1, 2].plot(time, sodium_channel, 'tab:blue')
axs[1, 2].plot(time, potassium_channel, 'tab:red')
axs[1, 2].set_title('Na & K conductance')
axs[1, 2].set_xlabel('Time (ms)')
axs[1, 2].set_ylabel('Conductance (mS/cm^2)')
axs[1, 2].set_ylim(-10,50)


fig.tight_layout()

plt.show()
    