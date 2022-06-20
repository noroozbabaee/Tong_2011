# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce the data needed for Figure 11 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig11_sim.py
import opencor as oc
import numpy as np
# The prefix of the saved output file name
prefilename = 'Fig11'
sub =['A','B','C','D','E']
varName = np.array(["Time", "Force", "I_tot", "v", "cai"])
simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011_newversion.sedml'
simulation = oc.open_simulation(simfile)
data = simulation.data()

# Set constant values
start = 0
end = 20000
pointInterval = 0.1
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)
I_st = [-0.018, -0.04,  -0.18, -1.2]
ca = [0.0000116, 0.000116, 0.000116, 0.000156]
v_init = [-53, -53, -50, -40]
gna = [0.12, 0.1, 0.06, 0.00]
k0 = [6, 6, 7, 6]

for i in range(len(I_st)):
    # Reset states variables
    simulation.reset(True)
    data.constants()['interface/I_CaL/s_clamp'] = 1
    data.constants()['interface/parameters/gna'] = gna[i]
    data.constants()['interface/test_start'] = 1000
    data.constants()['interface/test_end'] = 10000
    data.constants()['interface/I_test'] = I_st[i]
    data.constants()['interface/Ca_Concentrations/ca_var'] = 1
    data.constants()['interface/membrane_potential/v_var'] = 1
    data.constants()['interface/Ca_Concentrations/cai_init'] = ca[1]
    data.constants()['interface/membrane_potential/v_init'] = -55
    data.constants()['interface/parameters/ko'] = k0[i]
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    rows = end * 10 + 1
    vars = np.reshape(varName, (1,5))
    # Grab some algebraic results
    r = np.zeros((rows, len(varName)))
    r[:, 0] = results.voi().values()
    r[:, 1] = results.algebraic()['interface/Ca_dependent_Force/Force'].values()
    r[:, 2] = results.algebraic()['interface/membrane_potential/I_tot'].values()
    r[:, 3] = results.algebraic()['interface/membrane_potential/v'].values()
    r[:, 4] = results.algebraic()['interface/Ca_Concentrations/cai'].values()

    filename = '%s_%s.csv' % (prefilename, sub[i])
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
