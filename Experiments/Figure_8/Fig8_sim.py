# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce the data needed for Figure 8 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig8_sim.py
import opencor as oc
import matplotlib.pyplot as plt
import numpy as np
# The prefix of the saved output file name

prefilename = 'Fig8'
# Load the simulation file
simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/CaVAR_Tong_2011.sedml'
simulation = oc.open_simulation(simfile)
data = simulation.data()
# Set constant values
start = 0
end = 5000
pointInterval = 0.1
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)
ca_i = [0.000005, 0.00001, 0.00005, 0.00008, 0.0001, 0.0005, 0.0008, 0.001, 0.005, 0.008, 0.01, 0.05, 0.1, 0.5, 0.8, 1.0, 5.0, 8, 10, 50, 80, 100]
for j in range(len(ca_i)):
    # Reset states variables and parameters
    simulation.reset(True)
    data.constants()['interface/membrane_potential/v_init'] = 260
    data.constants() [ 'interface/Ca_Concentrations/cai' ] = ca_i [ j ]
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    varName = np.array(["Time", "xass_z", "xass_vh", "xatc", "xass", "iBKa","xa", "v", "xabss_z", "xabss_vh",
                        "xabtc", "xabss", "iBKab","xab"])
    vars = np.reshape(varName, (1,14))
    rows = end * 10 + 1
    # Grab some algebraic results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.constants()['interface/I_BKa/xass_z'].values()
    r [ :, 2 ] = results.constants()['interface/I_BKa/xass_vh'].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/I_BKa/xatc'].values()
    r [ :, 4 ] = results.algebraic() [ 'interface/I_BKa/xass'].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/I_BKa/iBKa'].values()
    r [ :, 6 ] = results.states() ['interface/I_BKa/xa'].values()
    r [ :, 7] = results.states() ['interface/membrane_potential/v' ].values()
    r [ :, 8 ] = results.constants() [ 'interface/I_BKab/xabss_z' ].values()
    r [ :, 9 ] = results.constants() [ 'interface/I_BKab/xabss_vh' ].values()
    r [ :, 10 ] = results.algebraic() [ 'interface/I_BKab/xabtc' ].values()
    r [ :, 11] = results.algebraic() [ 'interface/I_BKab/xabss' ].values()
    r [ :, 12] = results.algebraic() [ 'interface/I_BKab/iBKab' ].values()
    r [ :, 13] = results.states() [ 'interface/I_BKab/xab' ].values()
    filename = '%s_%s.csv' % (prefilename, j)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
