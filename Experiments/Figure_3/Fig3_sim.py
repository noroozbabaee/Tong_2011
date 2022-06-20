# Author : Leyla Noroozbabaee
# Date: 12/2/2022

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

# To reproduce the data needed for Figure 3 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig3_sim.py


import opencor as oc
import numpy as np

Fig_AC = 1
Fig3_DE = 1
Fig3_B = 1
if Fig_AC:
    prefilename = 'Fig3'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Reset states variables and parameters
    simulation.reset(True)
    # Set constant values
    start = 0
    end = 10000
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    data.constants()['interface/membrane_potential/v_init'] = -100
    data.constants()['interface/parameters/kmca'] = 0.001
    data.constants() [ 'interface/parameters/ecat' ] = 42
    # Run simulation
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    varName = np.array(["Time", "bss", "gss", "btc", "gtc", "icat", "v"])
    vars = np.reshape(varName, (1,7))
    rows = end * 10 + 1
    # Grab some algebraic results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic()['interface/I_CaT/bss'].values()
    r [ :, 2 ] = results.algebraic()['interface/I_CaT/gss'].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/I_CaT/btc' ].values()
    r [ :, 4 ] = results.algebraic() [ 'interface/I_CaT/gtc' ].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/I_CaT/icat' ].values()
    r [ :, 6 ] = results.states() [ 'interface/membrane_potential/v' ].values()
    filename = '%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
if Fig3_DE:
    prefilename = 'Fig3_4'
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 100
    pointInterval = 0.001
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_clamp = [-60, -50, -40, -30, -20, -10, 0, 10, 20]
    for i in range(len(v_clamp)):
        simulation.reset(True)
        data.constants()['interface/membrane_potential/v_hold'] = -80
        data.constants()['interface/parameters/kmca'] = 0.001
        data.constants()['interface/membrane_potential/v_var'] = 0
        data.constants()['interface/membrane_potential/v_clamp'] = v_clamp[i]
        data.constants()['interface/membrane_potential/time_clamp_end'] = end
        data.constants()['interface/membrane_potential/time_clamp_sta'] = 10
        data.constants()['interface/parameters/ecat'] = 25
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        varName = np.array(["Time", "icat", "v"])
        vars = np.reshape(varName, (1, 3))
        rows = end * 1000 + 1
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() [ 'interface/I_CaT/icat' ].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
        # Save the simulation result of the last run
        filename = '%s_%s.csv' % (prefilename, i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close
if Fig3_B:
    import os
    os.system('clear')
    prefilename = 'Fig3_2'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 100
    pointInterval = 0.001
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_clamp = [20, 10, 0, -10, -20, -30, -35, -40, -45, -50]
    for i in range(len(v_clamp)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants() [ 'interface/membrane_potential/v_hold'] = -100
        data.constants() [ 'interface/parameters/kmca'] = 0.001
        data.constants()['interface/membrane_potential/v_clamp'] = v_clamp[i]
        data.constants()['interface/membrane_potential/time_clamp_end'] = end
        data.constants()['interface/membrane_potential/time_clamp_sta'] = 13
        data.constants() [ 'interface/parameters/ecat' ] = 25
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        varName = np.array(["Time", "icat", "v", "btc"])
        vars = np.reshape(varName, (1, 4))
        rows = end * 1000 + 1
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic()['interface/I_CaT/icat'].values()
        r [ :, 2 ] = results.algebraic()['interface/membrane_potential/v'].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/I_CaT/btc' ].values()
        filename = '%s_%s.csv' % (prefilename, i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close
