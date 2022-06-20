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

# To reproduce the data needed for Figure 4 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig4_sim.py

import opencor as oc
import numpy as np

Fig_AB = 1
Fig_CD = 1
if Fig_AB:
    prefilename = 'Fig4'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 10000
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    # Reset states variables and parameters
    simulation.reset(True)
    data.constants()['interface/I_h/a_correction'] = 1
    data.constants()['interface/membrane_potential/v_init'] = -110
    data.constants()['interface/parameters/kmca'] = 0.001
    # Run Simulation
    simulation.run()
    # Data to save
    varName = np.array(["Time", "yss", "ya", "yb", "ytc", "ih", "v" ])
    vars = np.reshape(varName, (1,7))
    rows = end * 10 + 1
    # Access simulation results
    results = simulation.results()
    # Grab some algebraic results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic()['interface/I_h/yss'].values()
    r [ :, 2 ] = results.algebraic()['interface/I_h/ya'].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/I_h/yb' ].values()
    r [ :, 4 ] = results.algebraic() [ 'interface/I_h/ytc' ].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/I_h/ih' ].values()
    r [ :, 6 ] = results.states() [ 'interface/membrane_potential/v' ].values()
    filename = '%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
if Fig_CD:
    prefilename = 'Fig4_3'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 300
    pointInterval = 0.001
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_clamp = [-130, -110, -90, -80, -70, -60, -50, -40, -30]
    for i in range(len(v_clamp)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants()[ 'interface/membrane_potential/v_init' ] = -150
        data.constants()['interface/membrane_potential/v_hold'] = -30
        data.constants() ['interface/parameters/kmca' ] = 0.001
        data.constants()['interface/membrane_potential/v_clamp'] = v_clamp[i]
        data.constants()['interface/membrane_potential/time_clamp_end'] = end
        data.constants()['interface/membrane_potential/time_clamp_sta'] = 100
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        varName = np.array([ "Time", "ih", "v" ])
        vars = np.reshape(varName, (1, 3))
        rows = end * 1000 + 1
        # Grab some algebraic (states) results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() [ 'interface/I_h/ih' ].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
        # Save the simulation result
        filename = '%s_%s.csv' % (prefilename, i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close
