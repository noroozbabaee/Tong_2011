# Author : Leyla Noroozbabaee
# Date: 12/02/2022

# FOR the case of time dependent state variable such as membrane potential the following definition was used.
#        var v: mV {init: v_init, pub: out};
#        ode(v, time) = - I_tot;
#
# FOR the case of step-wise changes in state variable such as membrane potential the following definition
#        var v: mV {pub: out};
#        v = sel
#             case (time <= time_clamp_sta) and (v_var == 0{dimensionless}):
#                 v_hold;
#             case (time > time_clamp_sta) and (time <= time_clamp_end) and (v_var == 0{dimensionless}):
#                 v_clamp;
#             otherwise:
#                 v_hold;
#         endsel;

# To reproduce the data needed for Figure 1 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig1_sim.py

import opencor as oc
import numpy as np

Fig_ABCD = 1
Fig_EF = 1
if Fig_ABCD:
    prefilename = 'Fig1'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011/Simulations/Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Reset states variables and parameters
    simulation.reset(True)
    # Set constant values
    start = 0
    end = 6000
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    data.constants()['interface/membrane_potential/v_init'] = -100
    data.constants() [ 'interface/parameters/kmca' ] = 0.001
    data.constants() [ 'interface/parameters/ecal' ] = 45
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    varName = np.array(["Time", "fss", "dss", "f1tc", "f2tc", "dtc", "ical", "v", "I_Ca_tot"])
    vars = np.reshape(varName, (1,9))
    rows = end * 10 + 1
    # Grab some algebraic results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic()['interface/I_CaL/fss'].values()
    r [ :, 2 ] = results.algebraic()['interface/I_CaL/dss'].values()
    r [ :, 3 ] = results.constants() [ 'interface/I_CaL/f1tc' ].values()
    r [ :, 4 ] = results.algebraic() [ 'interface/I_CaL/f2tc' ].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/I_CaL/dtc' ].values()
    r [ :, 6 ] = results.algebraic() [ 'interface/I_CaL/ical'].values()
    r [ :, 7 ] = results.states() [ 'interface/membrane_potential/v' ].values()
    r [ :, 8 ] = results.algebraic() [ 'interface/membrane_potential/I_Ca_tot' ].values()
    filename = '%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
if Fig_EF:
    prefilename = 'Fig1_5'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set the time interval and total time for the simulation
    start = 0
    end = 60
    pointInterval = 0.01
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_clamp =[50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50]
    for i in range(11):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants()['interface/membrane_potential/v_hold'] = -60
        data.constants()['interface/membrane_potential/v_var'] = 0
        data.constants()['interface/parameters/kmca'] = 0.001
        data.constants() [ 'interface/membrane_potential/v_clamp' ] = v_clamp[i]
        data.constants() [ 'interface/membrane_potential/time_clamp_end']= end
        data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 6
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        varName = np.array(["Time", "ical", "I_tot","I_Ca_tot","v"])
        vars = np.reshape(varName, (1,5))
        rows = end * 100 + 1

        # Grab some algebraic variable results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() [ 'interface/I_CaL/ical'].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/I_tot'].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/membrane_potential/I_Ca_tot'].values()
        r [ :, 4 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
        # Save the simulation result
        filename = '%s_%s.csv' % (prefilename, i )
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close
