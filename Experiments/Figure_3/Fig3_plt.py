# Author: Leyla Noroozbabaee
# Date: 12/12/2021

# To reproduce Figure 3 from original paper, the python file 'Fig3_sim.py' should be run at the prompt in the OpenCOR Python console.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig3'
# Set figure dimension (width, height) in inches.
fw, fh = 15, 10
# Set subplots
subpRow, subpCol = 3, 2
ax, lns = {}, {}
# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.3)
axs = axs.ravel()
var_name = np.array(["Time", "bss", "gss", "btc", "gtc", "icat", "v"])
# Load Data
filename = '%s.csv' % (prefilename)
data = pd.read_csv(filename)
data = pd.read_csv(filename)
time = data [ var_name[0] ]
bss_data = data [var_name[1]]
gss_data = data [var_name[2]]
btc_data = data [var_name[3]]
gtc_data = data [var_name[4]]
icat_data = data [var_name[5]]
v_data = data [var_name[6]]
axs[1].plot( v_data, pow(bss_data, 2), 'b')
axs[0].plot( v_data, gss_data, 'b')
axs[3].plot( v_data, gtc_data, 'b')

# Set ylable
ylab = ['Steady state','Steady state','Time-topeak (ms)','Time constant (ms)','I (normalised)','I (normalised)']
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]

I_V = []
Time_Max = []
V = [20, 10, 0, -10, -20,-30,-35, -40, -45,-50]
prefilename = 'Fig3_2'
for i in range(len(V)):
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    time = data ['Time']
    btc_data = np.array(data ['btc'])
    max_btc = max(btc_data)
    Time_Max.append(pow(max_btc,2))

axs [ 2 ].plot(V, Time_Max, '*b')


prefilename = 'Fig3_4'
V = [-60, -50, -40, -30, -20, -10, 0, 10, 20]
filename5 = '%s_%s.csv' % (prefilename, 8)
data5 = pd.read_csv(filename5)
icat_data5 = data5 [ 'icat' ]
max_icat_data5 = max(abs(data5 [ 'icat' ]))
for i in range(len(V)):
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    time = data ['Time']
    icat_data = np.array(data ['icat'])
    axs [4].plot( time, icat_data/0.20810 , color=cycle [i % 4])
    MAX_I_V = (min(icat_data / max_icat_data5))
    I_V.append(MAX_I_V)
axs[5].plot(V, I_V, '-b')
for i in range(5):
    axs [i].set_xlabel('V (mV)', fontsize=labelfontsize)
    axs [ i ].set_ylabel('%s' % (ylab [ i ]), fontsize=labelfontsize)
    if i == 4: axs [i].set_xlabel('Time (ms)', fontsize=labelfontsize)

# To add the extracted data from original paper to your plot, modify the path to have access to the
# "Extracted_data"

# prefilename = 'Extracted_Data/Fig3'
#
# for i in range(5):
#
#     if i== 4:
#         for j in range(1,5):
#             filename = 'Extracted_Data/Fig3_55.csv'
#             data = pd.read_csv(filename)
#             x_name = 'x'
#             y_name = 'Curve%s' %(j)
#             x_data = data [ x_name ]
#             y_data = data [ y_name ]
#             axs [ i ].plot(x_data, y_data, '^')
#     else:
#         filename = '%s_%s.csv' % (prefilename, i + 1)
#         data = pd.read_csv(filename)
#         y_d = data [ 'Curve1' ]
#         x_d = data [ 'x' ]
#         axs [ i ].plot(x_d, y_d, 'k*')
#         axs [i].set_xlim([ -100, 50 ])
#         axs [i].set_xlabel('V (mV)', fontsize=labelfontsize)
#         axs [ i ].set_ylabel('%s' % (ylab [ i ]), fontsize=labelfontsize)
figfiles = 'Figure_3.png' 
plt.savefig(figfiles)
plt.show()
