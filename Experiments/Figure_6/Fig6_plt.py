# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 6 from original paper, the python file 'Fig6_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig6'
# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 3, 2
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]

# Set ylable
ylab = ['Steady state','Time constant (ms)','Time constant (ms)','I (normalised)','I (normalised)','I (normalised)']

# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.3)
axs = axs.ravel()
varName = np.array(["Time", "pss", "kss", "ptc", "k1tc","k2tc", "ik2", "v"])
filename = '%s.csv' % (prefilename)
data = pd.read_csv(filename)
time = data [ varName[0] ]
pss_data = data [varName[1]]
kss_data = data [varName[2]]
ptc_data = data [varName[3]]
k1tc_data = data [varName[4]]
k2tc_data = data [varName[5]]
ik2_data = data [varName[6]]
v_data = data [varName[7]]
axs[0].plot( v_data, pow(pss_data,2), 'b', v_data, kss_data, '--b')
axs[1].plot(v_data, ptc_data, 'b')
axs[2].semilogy(v_data, k1tc_data/1000, 'b',  v_data, k2tc_data/1000, '--b')

I_V = []
prefilename = 'Fig6_5'
V =  [-40,-30,-20,-10,0, 10 ]
for i in range(len(V)):
    filename5 = '%s_%s.csv' % (prefilename, 5)
    data5 = pd.read_csv(filename5)
    ik2_data5 = data5 ['ik2']
    max_ik2_data5 = max(abs(data5 ['ik2']))
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    time = data ['Time']
    ik2_data = data ['ik2']
    max_ik2_data = max(data['ik2'])
    axs [ 4 ].plot(time / 1000, ik2_data/max_ik2_data5 , color=cycle [ i % 4 ])
    axs [ 5 ].plot(time / 1000, ik2_data / max_ik2_data5, color=cycle [ i % 4 ])
    axs [ 4 ].set_xlim([ 0, 10 ])
    axs [ 5 ].set_xlim([ 0, 0.5 ])
    axs [3].plot( V[i], max_ik2_data/5, '^')
    MAX_I_V = (min(ik2_data / max_ik2_data5))
    I_V.append(MAX_I_V )

# To add the extracted data from original paper, modify the path to have access to the folder
# "Extracted_data"
prefilename = 'Extracted_Data/Fig6'
for i in range(6):
    filename = '%s_%s.csv' % (prefilename,  i+1)
    data = pd.read_csv(filename)
    axs [ i ].set_xlim([ -70, 60 ])
    if i == 1 or i==3 :
        y_d = data [ 'Curve1' ]
        x_d = data [ 'x' ]
        axs [ i ].plot(x_d, y_d, 'k*')
    elif i == 4 or i == 5 :
         for j in range(1, 6):
            x_name = 'x'
            y_name = 'Curve%s' % (j)
            x_data = data [ x_name ]
            y_data = data [ y_name ]

            if i == 4:
                axs [ i ].set_xlim([ 0, 10 ])
                axs [ i ].plot(x_data - 0.233, y_data, '^')
            if i == 5:
                axs [ i ].set_xlim([ 0, 0.4 ])
                axs [ i ].plot(x_data, y_data, '^')
            axs [ i ].set_xlabel('Time (s)', fontsize=12)
            axs [ i ].set_ylim([ 0, 1.2 ])
         axs [i].set_xlabel('V (mV)', fontsize=labelfontsize)
         axs [i].set_ylabel('%s' % (ylab[i]),fontsize=labelfontsize)
    else:
        y_d = data [ 'Curve1' ]
        x_d = data [ 'x' ]
        y_d_2 = data [ 'Curve2' ]
        axs [ i ].plot(x_d, y_d_2, 'k*')
        axs [ i ].plot(x_d, y_d, 'k*')
        axs [ i ].set_xlabel('V (mV)', fontsize=labelfontsize)
        axs [ i ].set_ylabel('%s' % (ylab [ i ]), fontsize=labelfontsize)
    axs [i].set_xlabel('V (mV)', fontsize=labelfontsize)
    axs [i].set_ylabel('%s' % (ylab[i]),fontsize=labelfontsize)

figfiles = 'Figure_6.png'
plt.savefig(figfiles)
plt.show()
