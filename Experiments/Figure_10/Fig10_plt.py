# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 6 from original paper, the python file 'Fig6_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig10'

# Set figure dimension (width, height) in inches.
fw, fh = 16, 8
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
ylab = ['Steady state','Time constant (ms)','I (normalised)','I (normalised)']
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# To add the extracted data from original paper to your plot, modify the path to have access to the
# "Extracted_data"
I_V = []
prefilename = 'Fig10'
Fig_F_G = 1
Fig_D_E = 0
sub =['A_C','B','D_E','F_G']
varName = np.array([ "Time", "css", "ctc", "icl", "c",  "v", "cai"])

cai = [100, 250, 500]
for i in range(len(cai)):
    filename = '%s_%s_%s.csv' % (prefilename, sub [ 0 ], i)
    print(filename)
    data = pd.read_csv(filename)
    time = data [ varName [ 0 ] ]
    css_data = data [ varName [ 1 ] ]
    ctc_data = data [ varName [ 2 ] ]
    icl_data = data [ varName [ 3 ] ]
    c_data = data [ varName [ 4 ] ]
    v_data = data [ varName [ 5 ] ]
    cai_data = data [ varName [ 6 ] ]
    axs [ 0 ].plot(v_data, css_data, color=cycle [ i % 8 ])
    axs [ 1 ].plot(v_data, ctc_data, 'y')
    var_Name = np.array([ "Time", "css", "cai","v" ])
    for i in range(4):
        filename = '%s_%s_%s.csv' % (prefilename, sub [ 1 ], i)
        print(filename)
        data = pd.read_csv(filename)
        time = data [ var_Name [ 0 ] ]
        css_data = data [ var_Name [ 1 ] ]
        cai_data = data [ var_Name [ 2 ] ]
        v_data = data [ var_Name [ 3 ] ]
        # axs [ 1 ].plot(cai_data, css_data, color=cycle [ i % 8 ])

for i in range(7):
    filename = '%s_%s_%s.csv' % (prefilename, sub[2], i)
    varName = np.array([ "Time", "css", "ctc", "icl", "c", "v", "ical" ])
    data = pd.read_csv(filename)
    time = data [ varName [ 0 ] ]
    css_data = data [ varName [ 1 ] ]
    ctc_data = data [ varName [ 2 ] ]
    icl_data = data [ varName [ 3 ] ]
    c_data = data [ varName [ 4 ] ]
    v_data = data [ varName [ 5 ] ]
    ical_data = data [ varName [ 6 ] ]

    I_cl_tot = icl_data + ical_data
    axs [ 2 ].plot(time, I_cl_tot, color=cycle [ i % 8 ])

for i in range(8):
    filename = '%s_%s_%s.csv' % (prefilename, sub[3], i)
    varName = np.array([ "Time", "css", "ctc", "icl", "c", "v", "ical" ])
    data = pd.read_csv(filename)
    time = data [ varName [ 0 ] ]
    css_data = data [ varName [ 1 ] ]
    ctc_data = data [ varName [ 2 ] ]
    icl_data = data [ varName [ 3 ] ]
    c_data = data [ varName [ 4 ] ]
    v_data = data [ varName [ 5 ] ]
    ical_data = data [ varName [ 6 ] ]

    I_cl_tot = icl_data + ical_data
    axs [ 3 ].plot(time, I_cl_tot, color=cycle [ i % 8 ])

for i in range(4):
    axs [ i ].set_ylabel('%s' % (ylab [ i ]), fontsize=labelfontsize)
    axs [ i ].set_xlabel('Time (ms)', fontsize=labelfontsize)
    axs [ i ].set_xlim([0, 400])
    if i == 0 or i == 1:
        axs[i].set_xlim([ -50, 50 ])
        axs [ i ].set_xlabel('V (mv)', fontsize=labelfontsize)



plt.show()