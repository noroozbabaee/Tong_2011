# Author : Leyla Noroozbabaee
# Date: 12/04/2022
# FOR the case of time dependent state variable such as membrane potential the following definition is applied.
#        var v: mV {init: v_init, pub: out};
#        ode(v, time) = - I_tot;
#
# FOR the case of step-wise changes in state variable such as membrane potential the following definition is applied
#        var v: mV {pub: out};
#        v = sel
#             case (time <= time_clamp_sta) and (v_var == 0{dimensionless}):
#                 v_hold;
#             case (time > time_clamp_sta) and (time <= time_clamp_end) and (v_var == 0{dimensionless}):
#                 v_clamp;
#             otherwise:
#                 v_hold;
#         endsel;

# To reproduce the data needed for Figure 5 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig5_sim.py

import opencor as oc
import numpy as np
Fig_D = 1
Fig_ABC = 1
Fig_EF = 1
if Fig_ABC:
    prefilename = 'Fig5'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Reset states variables and parameters
    simulation.reset(True)
    # Set constant values
    start = 0
    end = 1000
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    # simulation.reset(True)
    data.constants()['interface/membrane_potential/v_init'] = -80
    data.constants() ['interface/parameters/kmca'] = 0.001
    data.constants() [ 'interface/I_h/a_correction' ] = 1
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    varName = np.array(["Time", "qss", "rss", "qtc", "r1tc","r2tc", "ik1", "v"])
    vars = np.reshape(varName, (1,8))
    rows = end * 10 + 1
    # Grab some algebraic results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic()['interface/I_K1/qss'].values()
    r [ :, 2 ] = results.algebraic()['interface/I_K1/rss'].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/I_K1/qtc'].values()
    r [ :, 4 ] = results.algebraic() [ 'interface/I_K1/r1tc'].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/I_K1/r2tc'].values()
    r [ :, 6 ] = results.algebraic() [ 'interface/I_K1/ik1'].values()
    r [ :, 7 ] = results.states() [ 'interface/membrane_potential/v' ].values()
    filename = '%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close


if Fig_EF:
    prefilename = 'Fig5_4'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 10000
    pointInterval = 1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_clamp = [-30, -20, -10, 0, 10, 20, 30, 40,45]
    v_hold = [-380, -40]
    # Reset states variables and parameters
    simulation.reset(True)
    for j in range(len(v_hold)):
        data.constants()['interface/membrane_potential/v_hold'] = v_hold[j]
        for i in range(len(v_clamp)):
            data.constants() [ 'interface/membrane_potential/v_clamp' ] = v_clamp [ i ]
            data.constants() [ 'interface/membrane_potential/time_clamp_end' ] = end
            data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 40
            data.constants() [ 'interface/parameters/ki' ] = 110
            data.constants() [ 'interface/parameters/ko' ] = 4
            simulation.run()
            # Access simulation results
            results = simulation.results()
            # Data to save
            varName = np.array([ "Time", "ik1", "v","max" ])
            vars = np.reshape(varName, (1, 4))
            rows = end * 1 + 1
            # Grab some algebraic results
            r = np.zeros((rows, len(varName)))
            r [ :, 0 ] = results.voi().values()
            r [ :, 1 ] = results.algebraic() [ 'interface/I_K1/ik1' ].values()
            r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
            r [ :, 3 ] = max(r [ :, 1 ])
            # Save the simulation result of the last run
            filename = '%s_%s_%s.csv' % (prefilename, j,i)
            np.savetxt(filename, vars, fmt='%s', delimiter=",")
            with open(filename, "ab") as f:
                np.savetxt(f, r, delimiter=",")
            f.close

if Fig_D:
    prefilename = 'Fig5_5'
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
    time_clamp = 40
    v_clamp = [-40,-30,-20,-10,0, 10 ]
    for i in range(len(v_clamp)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants() [ 'interface/membrane_potential/v_hold' ] = -80
        data.constants() [ 'interface/parameters/kmca' ] = 0.001
        data.constants() [ 'interface/membrane_potential/v_clamp' ] = v_clamp [ i ]
        data.constants() [ 'interface/membrane_potential/time_clamp_end' ] = end
        data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 40
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        varName = np.array([ "Time", "ik1", "v" ])
        vars = np.reshape(varName, (1, 3))
        rows = end * 2 + 1
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() ['interface/I_K1/ik1'].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v'].values()
        # Save the simulation result of the last run
        filename = '%s_%s.csv' % (prefilename, i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close

