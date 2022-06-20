# Author : Leyla Noroozbabaee
# Date: 12/20/2022

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

# To reproduce the data needed for Figure 6 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig6_sim.py
import opencor as oc
import matplotlib.pyplot as plt
import numpy as np

Fig_ABC = 0
Fig_D = 0
Fig_EF = 1
if Fig_ABC:
    prefilename = 'Fig6'
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
    varName = np.array(["Time", "pss", "kss", "ptc", "k1tc","k2tc", "ik2", "v"])
    vars = np.reshape(varName, (1,8))
    rows = end * 2 + 1
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic()['interface/I_K2/pss'].values()
    r [ :, 2 ] = results.algebraic()['interface/I_K2/kss'].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/I_K2/ptc'].values()
    r [ :, 4 ] = results.algebraic() [ 'interface/I_K2/k1tc'].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/I_K2/k2tc'].values()
    r [ :, 6 ] = results.algebraic() [ 'interface/I_K2/ik2'].values()
    r [ :, 7 ] = results.states() [ 'interface/membrane_potential/v' ].values()
    filename = '%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
if Fig_D:
    prefilename = 'Fig6_4'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    start = 0
    end = 100
    pointInterval = 0.01
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_hold = [-80, -40]
    simulation.reset(True)
    for j in range(len(v_hold)):
        data.constants()['interface/membrane_potential/v_init'] = v_hold[j]
        data.constants() [ 'interface/parameters/ki' ] = 110
        data.constants() [ 'interface/parameters/ko' ] = 5
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        varName = np.array([ "Time", "ik2", "v" ])
        vars = np.reshape(varName, (1, 3))
        rows = end * 100 + 1
        # Grab some algebraic (state variable) results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() [ 'interface/I_K2/ik2' ].values()
        r [ :, 2 ] = results.states() [ 'interface/membrane_potential/v' ].values()
        # Save the simulation result
        filename = '%s_%s.csv' % (prefilename, j)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close

if Fig_EF:
    prefilename = 'Fig6_5'
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
        varName = np.array([ "Time", "ik2", "v" ])
        vars = np.reshape(varName, (1, 3))
        rows = end * 2 + 1
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() ['interface/I_K2/ik2'].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v'].values()
        # Save the simulation result
        filename = '%s_%s.csv' % (prefilename, i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close

