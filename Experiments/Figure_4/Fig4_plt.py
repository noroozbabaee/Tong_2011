# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 6 from original paper, the python file 'Fig6_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig4'

# Set figure dimension (width, height) in inches.
fw, fh = 15, 15
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
var_name = np.array([ "Time", "yss", "ya", "yb", "ytc", "ih", "v" ])
filename = '%s.csv' % (prefilename)
data = pd.read_csv(filename)
print('filename', filename)
data = pd.read_csv(filename)
time = data [ var_name[0] ]
yss_data = data [var_name[1]]
ya_data = data [var_name[2]]
yb_data = data [var_name[3]]
ytc_data = data [var_name[4]]
ih_data = data [var_name[5]]
v_data = data [var_name[6]]
axs[0].plot(v_data, yss_data, 'b')
axs[1].plot(v_data, ytc_data/350, 'b')
axs [ 1 ].set_xlim([ -150, 0 ])
axs [ 1 ].set_ylim([ 0,5 ])
# Set ylable
ylab= ['Steady state','Time constant (ms)', 'I (normalised)','I (normalised)']
I_V = []
for i in range(9):
    prefilename = 'Fig4_3'
    filename5 = '%s_%s.csv' % (prefilename, 1)
    data5 = pd.read_csv(filename5)
    ih_data5 = data5 ['ih']
    max_ih_data5 = max(abs(data5 ['ih']))
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    time = data ['Time']
    ih_data = data ['ih']
    max_ih_data = max(data ['ih'])
    if 0 <= i < 10:
        axs [2].plot( time/100, ih_data/1.8, color=cycle [i % 4])
        axs [2].set_xlim([ 0,3 ])

    if max_ih_data  < 0:
        MAX_I_V = (min(ih_data/1.8))
    else:
        MAX_I_V = (max(ih_data/1.8))
    I_V.append(MAX_I_V )

V = [-130, -110, -90, -80, -70, -60, -50, -40, -30]
axs[3].plot(V, I_V, '-b')
axs[3].set_ylim([ -3, 1 ])
axs[3].set_xlim([ -150, 0 ])

# # To add the extracted data from original paper to your plot, modify the path to have access to the
# # "Extracted_data"
prefilename = 'Extracted_Data/Fig4'
for i in range(4):
    filename = '%s_%s.csv' % (prefilename,  i+1)
    data = pd.read_csv(filename)
    y_d = data [ 'Curve1' ]
    x_d = data [ 'x' ]
    axs [ i ].plot(x_d, y_d, 'k*')
    axs [i].set_xlim([ -150, 0 ])
    axs [i].set_xlabel('V (mV)', fontsize=labelfontsize)
    axs [i].set_ylabel('%s' % (ylab[i]),fontsize=labelfontsize)
    if i == 2:
        y_d_2 = data [ 'Curve2' ]
        y_d_3 = data [ 'Curve3' ]
        axs [ i ].plot(x_d, y_d_2, '*', x_d, y_d_3,'*', color=cycle [ i%4  ])
        axs [ i ].set_xlim([ 0,3 ])
        axs [ i ].set_xlabel('Time (ms)', fontsize=labelfontsize)
        axs [ i ].set_ylim([ -1, 0 ])

figfiles = 'Figure_4.png'
plt.savefig(figfiles)
plt.show()
