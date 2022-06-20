# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 6 from original paper, the python file 'Fig6_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig12'
figfile = 'Figure_12_origin'

# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 3, 2
ax, lns = {}, {}
# Set ylab
ylab = ['V (mv)', 'V (mv)', 'Ca (nM)', 'Ca (nM)', 'Ist (PA/PF)', 'Ist (PA/PF)']
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.3)
axs = axs.ravel()
var_name = ['Time','I_st', 'v', 'cai']
# y_name =['fss'];
x_base =[0.4, 0.6]
sub = ['A','B']
for i in range(len(sub)):
    filename = '%s_%s.csv' % (prefilename, sub[i])
    data = pd.read_csv(filename)
    time = data [ var_name[0] ]
    Ist_data = data [var_name[1]]
    v_data = data [var_name[2]]
    cai_data = data [var_name[3]]
    if i==0:
        axs [ 0].plot(time, v_data, 'k')  # y_data = data [ var [ i ] ]
        axs [ 2 ].plot(time, cai_data, 'b')
        axs [ 4 ].plot( time, Ist_data, 'b')
    if i==1:
        axs [ 1].plot(time, v_data, 'k')  # y_data = data [ var [ i ] ]
        axs [ 3 ].plot(time, cai_data, 'b')
        axs [ 5 ].plot( time, Ist_data, 'b')
for i in range(6):
    axs[i].set_xlabel('Time (ms)', fontsize = labelfontsize)
    axs[i].set_ylabel('%s' % ylab[i], fontsize=labelfontsize)
plt.show()

