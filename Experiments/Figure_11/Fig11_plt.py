# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 11 from original paper, the python file 'Fig11_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig11'
figfile = 'Figure_11_origin'
# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 2, 2
ax, lns = {}, {}
# Set ylabel
ylab = ['Steady state','Time constant (ms)','I (normalised)','I (normalised)']
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .2, wspace=.2)
axs = axs.ravel()
var_name = ['Time','Force', 'I_tot', 'v', 'cai']
# y_name =['fss'];
x_base =[0.4, 0.6]
sub = ['A','B','C','D']
I_st =[ -0.18, -0.13, -0.1, -0.5]
for i in range(len(I_st)):
    filename = '%s_%s.csv' % (prefilename, sub[i])
    data = pd.read_csv(filename)

    time = data [ var_name[0] ]
    Force_data = data [var_name[1]]
    I_tot_data = data [var_name[2]]
    v_data = data [var_name[3]]
    cai_data = data [var_name[4]]
    axs[i].plot( time, v_data, color=cycle [ i %5 ])
    axs[i].set_ylabel('%s' % ylab[i], fontsize = labelfontsize)
    axs[i].set_xlabel('Time (s)', fontsize = labelfontsize)
plt.show()
