# To reproduce the data needed for Figure 7 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig7_sim.py

import opencor as oc
import numpy as np
Fig_A = 1
Fig_BCD = 1
if Fig_A:
    prefilename = 'Fig7'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Reset states variables and parameters
    simulation.reset(True)
    # Set constant values
    start = 0
    end = 20000
    pointInterval = 0.5
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    data.constants()['interface/membrane_potential/v_init'] = -90
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    varName = np.array(["Time", "sss", "xss", "stc", "xtc","ika", "v"])
    vars = np.reshape(varName, (1,7))
    rows = end * 2 + 1
    # Grab some variable results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic()['interface/I_Ka/sss'].values()
    r [ :, 2 ] = results.algebraic()['interface/I_Ka/xss'].values()
    r [ :, 3 ] = results.algebraic() ['interface/I_Ka/stc'].values()
    r [ :, 4 ] = results.algebraic() ['interface/I_Ka/xtc'].values()
    r [ :, 5 ] = results.algebraic() ['interface/I_Ka/ika'].values()
    r [ :, 6 ] = results.states() ['interface/membrane_potential/v'].values()
    filename = '%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close

if Fig_BCD:
    prefilename = 'Fig7_BCD'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 10000
    pointInterval = 0.5
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_clamp = [-40,-30,-20,-10, 0, 10,20,30, 40,50 ]
    for i in range(len(v_clamp)):
        data.constants() [ 'interface/membrane_potential/v_hold' ] = -80
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants() [ 'interface/parameters/kmca' ] = 0.001
        data.constants() [ 'interface/membrane_potential/v_clamp' ] = v_clamp [ i ]
        data.constants() [ 'interface/membrane_potential/time_clamp_end' ] = end
        data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 10
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        varName = np.array(["Time", "ika", "v", " stc"])
        vars = np.reshape(varName, (1, 4))
        rows = end * 2 + 1
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() ['interface/I_Ka/ika'].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v'].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/I_Ka/stc' ].values()
        # Save the simulation result of the last run
        filename = '%s_%s.csv' % (prefilename, i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close

