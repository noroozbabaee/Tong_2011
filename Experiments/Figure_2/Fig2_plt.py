# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 2 from original paper, the python file 'Fig2_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig2'

# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 2, 2
ax, lns = {}, {}

# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.3)
axs = axs.ravel()
var_name = np.array(["Time", "hss", "mss", "htc", "mtc", "ina", "v"])
filename = '%s.csv' % (prefilename)
data = pd.read_csv(filename)
data = pd.read_csv(filename)
time = data [ var_name[0] ]
hss_data = data [var_name[1]]
mss_data = data [var_name[2]]
htc_data = data [var_name[3]]
mtc_data = data [var_name[4]]
ina_data = data [var_name[5]]
v_data = data [var_name[6]]

axs[0].plot( v_data, hss_data, 'b', v_data, pow(mss_data,3), 'r')
axs[1].semilogy( v_data, htc_data, 'b', v_data, mtc_data, 'r')

# Set ylable
ylab = ['Steady state','Time constant (ms)', 'I (normalised)','I (normalised)']
I_V = []
for i in range(11):
    prefilename = 'Fig2_3'
    filename5 = '%s_%s.csv' % (prefilename, 5)
    data5 = pd.read_csv(filename5)
    print('filename', filename5)
    ina_data5 = data5['ina']
    max_ina_data5 = max(abs(data5['ina']))
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    print('filename', filename)
    time = data['Time']
    ina_data = data['ina']
    max_ina_data = max(data['ina'])
    print('max_ina_data', max_ina_data5)
    if 5 <= i < 11:
         axs[2].plot(time, ina_data/max_ina_data5, color=cycle[i % 4])
    if max_ina_data < 0:
        MAX_I_V = (min(ina_data / max_ina_data5))
    else:
        MAX_I_V = (max(ina_data / max_ina_data5))
    I_V.append(MAX_I_V)

V = [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50]
print(I_V)
axs[3].plot(V, I_V, '-b')

# To add the extracted data from original paper to your plot, modify the path to have access to the
# "Extracted_data"
prefilename = 'Fig2'
for i in range(4):
    prefilename = 'Extracted_Data/Fig2'
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    if i == 3:
        x_name = 'x'
        y_name = 'Curve1'
        x_data = data [ x_name ]
        y_data = data [ y_name ]
        axs [ i ].plot(x_data, y_data, '^')
    elif i== 2:
        for j in range(1,6):
            data = pd.read_csv(filename)
            x_name = 'x'
            y_name = 'Curve%s' %(j)
            x_data = data [ x_name ]
            y_data = data [ y_name ]
            axs [ i ].plot(x_data, y_data, '^')
    else:
        x_name = 'x'
        y_name = 'Curve1'
        x_data = data [ x_name ]
        y_data = data [ y_name ]
        y_name2 = 'Curve2'
        y_data2 = data [ y_name2 ]
        axs [ i ].plot(x_data, y_data, 'k^')
        axs [ i ].plot(x_data, y_data2, 'k^')
    axs [ i ].set_ylabel('%s' % (ylab[ i ]), fontsize=labelfontsize)
    if i!=2:
       axs [ i ].set_xlim([-80, 50])
       axs [ i ].set_xlabel('V (mV)', fontsize=labelfontsize)
    else:
        axs [ i ].set_ylim([-1, 0])
        axs [ i ].set_xlim([0, 50])
        axs [ i ].set_xlabel('Time (ms)', fontsize=labelfontsize)


figfiles = 'Figure_2.png'
plt.savefig(figfiles)
plt.show()