# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 9 from original paper, the python file 'Fig9_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig9'
# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 2,2
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.3)
axs = axs.ravel()

I_V = []
prefilename = 'Fig9'
varName = np.array([ "Time", "ik1", "ik2", "iBKa", "iBKab", "ika", "ib", "v", "I_K_tot" ,"xabtc"])
sub =['A','B','C']
v_clamp = [  70,60,50,40,30,20,10,0,-10,-20,-30,-40 ]
v_hold = [ -40,-80 ]
Max_I_K = []
Max_Inactv = []
for i in range(len(v_hold)):
    for j in range(len(v_clamp)):
        filename = '%s_%s_%s.csv' % (prefilename, sub [ i ], j)
        print(filename)
        data = pd.read_csv(filename)
        time = data [ varName[0] ]
        ik1_data = data [varName[1]]
        ik2_data = data [varName[2]]
        iBKa_data = data [varName[3]]
        iBKab_data = data [varName[4]]
        ika_data = data [varName[5]]
        ib_data = data [varName[6]]
        v_data = data [varName[7]]
        I_K = data [ varName [8]]
        xabtc = data [ varName [9] ]
        Max_I = max(I_K)
        Max_I_K.append(Max_I)
        max_inact = max(xabtc)
        Max_Inactv.append( max_inact)
        I_K_tot = + ik1_data + ik2_data + ika_data + 0.7*iBKa_data + 0.3*iBKab_data + ib_data
        axs [ 3 ].plot(time, iBKab_data, 'g')
        axs [ 3-i ].plot(time, I_K ,  color=cycle [ j % 8 ])
        if j==4 and i==1:
            ik_TEA = ika_data
            axs [ 0 ].plot(time, I_K, 'k', time, ik_TEA, '-k')
axs [ 1 ].plot(v_clamp*2, np.array(Max_I_K)/20.49, '*k')
for i in range(4):
    axs [ i ].set_xlabel('Time (ms)', fontsize=labelfontsize)
    axs [ i ].set_ylabel('I (normalised)', fontsize=labelfontsize)
plt.show()

prefilename = 'Figure_9'
