# Author: Leyla Noroozbabaee
# Date: 12/01/2021
# To reproduce Figure 7 from original paper, the python file 'Fig7_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
# Figure name
prefilename = 'Fig7'
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
fig.subplots_adjust(hspace=.3, wspace=.3)
axs = axs.ravel()
ylab = [ 'Steady state', 'Time to peak (ms)', 'I (normalised)', 'I (normalised)' ]
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Load Data Figure 7(A)
filename = '%s.csv' % prefilename
data = pd.read_csv(filename)
varName = np.array(["Time", "sss", "xss", "stc", "xtc","ika", "v"])
time = data[varName[0]]
sss_data = data [varName[1]]
xss_data = data [varName[2]]
v_data = data [varName[6]]
axs[0].plot( v_data, pow(sss_data,1), 'b', v_data, xss_data, '--b')
I_V_Max= []
T_to_P = []
# Load Data
prefilename = 'Fig7_BCD'
V = [ -40, -30, -20, -10, 0, 10, 20, 30, 40, 50]
filename5 = '%s_%s.csv' % (prefilename, 5)
data5 = pd.read_csv(filename5)
ika_data5 = data5['ika']
max_ika_data5 = max(abs(data5['ika']))
for i in range(len(V)):
    filename = '%s_%s.csv' % (prefilename, i)
    data = pd.read_csv(filename)
    time = data ['Time']
    ika_data = data ['ika']
    max_ika_data = max(data['ika'])
    stc_data = max(data[' stc'])
    T_to_P.append(stc_data)
    MAX_I_V= (max(ika_data / max_ika_data5))
    I_V_Max.append(MAX_I_V)
    if 0 <= i < 6:
        axs[2].plot(time / 1000, ika_data/max_ika_data5, color=cycle[i % 4])
axs[1].plot(V, T_to_P, color=cycle[i % 4])
axs[3].plot(V, np.array(I_V_Max)/2.217, '-b')

for k in range(4):
    axs [ k ].set_xlim([ -70, 50 ])
    axs [ k ].set_xlabel('V (mV)', fontsize=labelfontsize)
    axs [ k ].set_ylabel('%s' % (ylab [ k ]), fontsize=labelfontsize)
    if k != 2:
        axs [ 2 ].set_xlim([0, 0.15])
        axs [ 2 ].set_xlabel('Time (ms)', fontsize=labelfontsize)
        axs [ 2 ].set_ylabel('%s' % (ylab[2]), fontsize=labelfontsize)

figfiles = 'Figure_7.png'
plt.savefig(figfiles)
plt.show()
