import math
import matplotlib.pyplot as plt
from random import seed
from random import gauss
import pandas as pd
import numpy as np
import scipy as sci




def main():
    
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
    ms = 100000

    ## Initial Electrode current ##
    I = 0

    ## Time step ##
    delta_t = .01
    list_I = []
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
    
        if(T%20==0):
            seed(T)
            I = gauss(0, 1)
            list_I.append(I)
        else:
            list_I.append(I)
        time.append(T*delta_t)
    
                                    ## Plotting the points ## 
    ## plot n ##
    data = {'Input':list_I,'Voltage':Voltage}
    df = pd.DataFrame(data)
    return df


def generate_n():
    df = pd.read_csv('outputfile.csv')
    df = pd.DataFrame(df)
    count = 0
    l = []
    t = []
    for i in range(0,1000000) :
        if(df['Voltage'][i]>=0):
            l.append(i)
            while(df['Voltage'][i]>=0):
                i+=1
    vec_of_vecs = []
    for j in l:
        vec = []
        for k in range(j-100,j+1000):
            vec.append(df['Voltage'][k])
        vec_of_vecs.append(vec)
    avg = []
    out = []
    count = 0
    for i in range(len(vec_of_vecs[1])):
        sum = 0
        for j in range(len(vec_of_vecs)):
            sum+=vec_of_vecs[j][i]
        count+=1
        avg.append(sum/len(l))
        out.append(count)
    data = {'Kernel_n':avg}
    df = pd.DataFrame(data)   
    df.to_csv('Kernel_n.csv')
    plt.plot(out,avg)
    plt.show()



def max_(list_of_lists):
    max = 0
    maxint = 0
    for i in range(0,len(list_of_lists)):
        if (len(list_of_lists[i])>max):
            max = len(list_of_lists[i])
            maxint = i
    return list_of_lists[maxint]


generate_n()