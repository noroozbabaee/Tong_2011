# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 6 from original paper, the python file 'Fig5_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig5'
# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 3, 2
ax, lns = {}, {}
# Set ylable
ylab = ['Steady state','Steady state','Time constant (ms)','Time constant (ms)','I (normalised)','I (normalised)']
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.3)
axs = axs.ravel()
varName = np.array([ "Time", "qss", "rss", "qtc", "r1tc", "r2tc", "ik1", "v" ])
# Load Data
filename = '%s.csv' % (prefilename)
data = pd.read_csv(filename)
time = data [ varName[0] ]
qss_data = data [varName[1]]
rss_data = data [varName[2]]
qtc_data = data [varName[3]]
r1tc_data = data [varName[4]]
r2tc_data = data [varName[5]]
ik1_data = data [varName[6]]
v_data = data [varName[7]]
axs[0].plot( v_data, pow(qss_data,2), 'b', v_data, rss_data, '--b')
axs[1].plot(v_data, qtc_data, 'b')
axs[2].semilogy(v_data, r1tc_data/1000, 'b',  v_data, r2tc_data/1000, '--b')


I_V = []
prefilename = 'Fig5_5'
V =  [-40,-30,-20,-10,0, 10 ]
for i in range(len(V)):
    filename5 = '%s_%s.csv' % (prefilename, 5)
    data5 = pd.read_csv(filename5)
    ik1_data5 = data5 ['ik1']
    max_ik1_data5 = max(abs(data5 ['ik1']))
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    time = data ['Time']
    ik1_data = data ['ik1']
    max_ik1_data = max(data['ik1'])
    axs [ 4 ].plot(time / 1000, ik1_data/max_ik1_data5 , color=cycle [ i % 4 ])
    axs [ 5 ].plot(time / 1000, ik1_data / max_ik1_data5, color=cycle [ i % 4 ])
    axs [ 4 ].set_xlim([ 0, 10 ])
    axs [ 5 ].set_xlim([ 0, 0.5 ])
    MAX_I_V = (min(ik1_data / max_ik1_data5))
    I_V.append(MAX_I_V )

prefilename = 'Fig5_4'
V_max = [-30, -20, -10, 0, 10,20,30,40,45,-30, -20, -10, 0, 10,20,30,40,45]
V =  [ -30, -20, -10, 0, 10,20,30,40,45]
I_max = []
for j in range(2):
    for i in range(len(V)):
        filename = '%s_%s_%s.csv' % (prefilename, j,i)
        data = pd.read_csv(filename)
        ik1_data = data ['v']
        max_ik1_data1 = max((data ['ik1']))
        v_max = np.reshape(V_max, (1,-1))
        if max_ik1_data1 < 0:
            MAX_I_V = (min(data ['ik1']))
        else:
            MAX_I_V = (max(data ['ik1']))
        I_max.append(max_ik1_data1 )
axs [ 3 ].plot(V_max, np.array(I_max)/12.2, '^r')

# To add the extracted data from original paper to your plot, modify the path to have access to the
# "Extracted_data"
prefilename = 'Extracted_Data/Fig5'
for i in range(6):
    filename = '%s_%s.csv' % (prefilename,  i+1)
    data = pd.read_csv(filename)
    data = pd.read_csv(filename)
    y_d = data [ 'Curve1' ]
    x_d = data [ 'x' ]
    axs [ i ].plot(x_d, y_d, 'k*')
    axs [ i ].set_xlim([ -70, 60 ])
    axs [ i ].set_xlabel('V (mV)', fontsize=labelfontsize)
    axs [ i ].set_ylabel('%s' % (ylab [ i ]), fontsize=labelfontsize)
    if i == 0 or i == 3:
        y_d_2 = data [ 'Curve2' ]
        axs [ 0 ].plot(x_d, y_d_2, 'k*')
    elif i == 1:
         axs [ 1 ].semilogy(x_d, y_d, 'k*')
    elif i == 2:
        y_d_2 = data [ 'Curve2' ]
        axs [ i ].semilogy(x_d, y_d, 'k*', x_d, y_d_2, 'k*')
    elif i == 4 or i == 5 :
         for j in range(1, 6):
            x_name = 'x'
            y_name = 'Curve%s' % (j)
            x_data = data [ x_name ]
            y_data = data [ y_name ]
            axs [ i ].plot(x_data, y_data, '^')
            if i == 4:axs [ i ].set_xlim([ 0, 10 ])
            if i == 5:axs [ i ].set_xlim([ 0, 0.4 ])
            axs [ i ].set_xlabel('Time (s)', fontsize=12)
            axs [ i ].set_ylim([ 0, 1.2 ])

    axs [i].set_xlabel('V (mV)', fontsize=labelfontsize)
    axs [i].set_ylabel('%s' % (ylab[i]),fontsize=labelfontsize)


figfiles = 'Figure_5.png'
plt.savefig(figfiles)
plt.show()
