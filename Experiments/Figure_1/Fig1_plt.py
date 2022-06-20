# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 1 from original paper, the python file 'Fig1_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig1'

# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 3, 2
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace=.3, wspace=.3)
axs = axs.ravel()
var_name = ['Time','fss','dss','f1tc','f2tc','dtc','ical','v','I_Ca_tot']
# Set ylable
tit = ['Steady state','Steady state','Time constant (ms)','Time constant (ms)','I (normalised)','I (normalised)']
# Set Color
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]

filename = '%s.csv' % (prefilename)
data = pd.read_csv(filename)
print('filename', filename)
data = pd.read_csv(filename)
time = data [ var_name[0] ]
fss_data = data [var_name[1]]
dss_data = data [var_name[2]]
f1tc_data = data [var_name[3]]
f2tc_data = data [var_name[4]]
dtc_data = data [var_name[5]]
ical_data = data [var_name[6]]
v_data = data [var_name[7]]
axs[0].plot( v_data, pow(dss_data,2), 'b')
axs[1].plot( v_data, fss_data, 'b')
axs[2].plot( v_data, dtc_data, 'b')
axs[3].plot( v_data, f1tc_data, 'b',  v_data, f2tc_data, 'b')

I_V = []
prefilename = 'Fig1_5'
filename5 = '%s_%s.csv' % (prefilename, 5)
data5 = pd.read_csv(filename5)
max_ical_data5 = max(abs(data5 ['ical']))
for i in range(11):
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    time = data ['Time']
    ical_data = data ['ical']
    max_ical_data = max(data ['ical'])
    print(' max_ical_data ', max_ical_data5)
    if  5<=i<11:
         axs [4].plot( time, ical_data/max_ical_data5, color=cycle [i % 4])
    if max_ical_data  < 0:
        MAX_I_V = (min(ical_data / max_ical_data5))
    else:
        MAX_I_V = (max(ical_data / max_ical_data5))
    I_V.append(MAX_I_V )

V = [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50]
print(I_V)
axs[5].plot(V, I_V, '-b')


# To add the extracted data from original paper to your plot, modify the path to have access to the
# "Extracted_data"
prefilename = 'Fig1'
for i in range(6):
    prefilename = 'Extracted_Data/Fig1'
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    if i == 3 :
        x_name2 = 'x'
        y_name2 = 'Curve2'
        y_data2 = data [ y_name2 ]
        x_data2 = data [ x_name2 ]
        axs [ i ].plot(x_data2, y_data2, 'k^')
    elif i== 4:
        for j in range(1,6):
            filename = 'Extracted_Data/Fig1_4.csv'
            data = pd.read_csv(filename)
            x_name = 'x'
            y_name = 'Curve%s' %(j)
            x_data = data [ x_name ]
            y_data = data [ y_name ]
            axs [ i ].plot(x_data, y_data, '^')

    x_name = 'x'
    y_name = 'Curve1'
    x_data = data [ x_name ]
    y_data = data [ y_name ]

    axs [ i ].set_ylabel('%s' % (tit [ i ]), fontsize=labelfontsize)
    if i!=4:
       axs [ i ].set_xlim([ -80, 50 ])
       axs [ i ].set_xlabel('V (mV)', fontsize=labelfontsize)
    else:
        axs [ i ].set_xlim([ 0, 60 ])
        axs [ i ].set_xlabel('Time (ms)', fontsize=labelfontsize)
    axs [ i ].plot(x_data, y_data, 'k^')


figfiles = 'Figure_1.png'
plt.savefig(figfiles)
plt.show()