# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce Figure 6 from original paper, the python file 'Fig8_sim.py' should be run.

import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing
import numpy as np
# Figure name
prefilename = 'Fig8'

# Set figure dimension (width, height) in inches.
fw, fh = 15, 10

# Set subplots
subpRow, subpCol = 3, 2
ax, lns = {}, {}

# This gives list with the colors from the cycle, which you can use to iterate over.
cycle = plt.rcParams [ 'axes.prop_cycle' ].by_key() [ 'color' ]
# Set ylable
ylab = ['V_0.5(mV)','Gating Charge (e)','Steady State','Steady State','Time Constant (ms)','I (normalised)']
# Set subplots
lfontsize, labelfontsize = 10, 15  # legend, label fontsize
fig, axs = plt.subplots(subpRow, subpCol, figsize=(fw, fh), facecolor='w', edgecolor='k')
fig.subplots_adjust(hspace = .3, wspace=.3)
axs = axs.ravel()
ca_i = [ 0.000005,0.00001, 0.00005, 0.00008, 0.0001, 0.0005, 0.0008, 0.001, 0.005, 0.008, 0.01, 0.05, 0.1, 0.5, 0.8, 1.0, 5.0, 8, 10, 50, 80, 100]
xassz = []
xassvh = []
xabssz = []
xabssvh = []
iBk_tot = []

for j in range(len(ca_i)):
    varName = np.array(["Time", "xass_z", "xass_vh", "xatc", "xass", "iBKa","xa", "v", "xabss_z", "xabss_vh",
                        "xabtc", "xabss", "iBKab","xab"])
    filename = '%s_%s.csv' % (prefilename, j)
    data = pd.read_csv(filename)
    v_data = data [varName[7]]
    xassz_data = max(data [ varName [ 1 ] ])
    xassz.append(xassz_data)
    xassvh_data = max(data [ varName [ 2 ] ])
    xassvh.append(xassvh_data)
    xabssz_data = max(data [ varName [ 8 ] ])
    xabssz.append(xabssz_data)
    xabssvh_data = max(data [ varName [ 9 ] ])
    xabssvh.append(xabssvh_data)
    xass_data = data [varName[4]]
    xatc_data = data [varName[3]]
    xabss_data = data[varName [11]]
    xabtc_data = data[varName [10]]
    xab_data = data [ varName [13 ] ]
    if j in [0,7,10,13]:
        axs [ 2 ].plot(v_data, xass_data, 'k')
        axs [ 3 ].plot(v_data, xabss_data, 'k')
    axs [ 4 ].semilogy(v_data, xatc_data, 'k')
    axs [ 4 ].semilogy(v_data, xabtc_data, '-k')
    if j == 1 or j == 6:
        iBka_data = (data [ varName [ 5 ] ])
        iBkab_data = (data [ varName [ 12 ] ])
        iBk = 0.7 * iBka_data + 0.3 * iBkab_data
        axs [ 5 ].plot(v_data, iBk/8.2, 'k')
        axs [ 5 ].set_ylim([ 0, 1 ])
ca_i = np.array(ca_i)*1000
axs[0].semilogx(ca_i, xassvh, 'k', ca_i, xabssvh, '--k')
axs[1].semilogx(ca_i, xassz, 'k',  ca_i, xabssz, '--k')
for i in range(6):
    if 0 <= i < 2:
        axs [ i ].set_xlim([ 0.01, 100 ])
        axs [ i ].set_xlabel('Ca_i [10-6 M)', fontsize=12)
    if 2 <= i < 5: axs [ i ].set_xlim([ -100, 350 ])
    if 5 <= i < 6: axs [ i ].set_xlim([ -60, 60 ])

    axs [ i ].set_xlabel('V (mV)', fontsize=labelfontsize)
    axs [ i ].set_ylabel('%s' % (ylab [ i ]), fontsize=labelfontsize)


figfiles = 'Figure_8.png'
plt.savefig(figfiles)
plt.show()
