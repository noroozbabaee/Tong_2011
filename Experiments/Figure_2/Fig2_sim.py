# FOR the case of variavle voltage use the following definition
#        var v: mV {init: v_init, pub: out};
#        ode(v, time) = - I_tot;
#
# FOR the case of step-manner voltage use the following definition
#        var v: mV {pub: out};
#        v = sel
#             case (time <= time_clamp_sta) and (v_var == 0{dimensionless}):
#                 v_hold;
#             case (time > time_clamp_sta) and (time <= time_clamp_end) and (v_var == 0{dimensionless}):
#                 v_clamp;
#             otherwise:
#                 v_hold;
#         endsel;

# To reproduce the data needed for Figure 2 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig2_sim.py
import opencor as oc
import numpy as np
Fig_2CD= 1
Fig_2AB = 1
if  Fig_2AB:
    prefilename = 'Fig2'
    # Load the simulation file
    from pathlib import Path
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011.sedml'

    simulation = oc.open_simulation(simfile)
    data = simulation.data()

    # Reset states variables and parameters
    simulation.reset(True)
    # Set constant values
    start = 0
    end = 5000
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    data.constants()['interface/membrane_potential/v_init'] = -90
    data.constants() [ 'interface/parameters/kmca' ] = 0.001
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    varName = np.array(["Time", "hss", "mss", "htc", "mtc", "ina", "v"])
    vars = np.reshape(varName, (1,7))
    rows = end * 10 + 1
    # Access simulation results
    results = simulation.results()
    # Grab a some algebraic variable results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic()['interface/I_Na/hss'].values()
    r [ :, 2 ] = results.algebraic()['interface/I_Na/mss'].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/I_Na/htc' ].values()
    r [ :, 4 ] = results.algebraic() [ 'interface/I_Na/mtc' ].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/I_Na/ina' ].values()
    r [ :, 6 ] = results.states() [ 'interface/membrane_potential/v' ].values()
    filename = '%s.csv' % (prefilename)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
if Fig_2CD:
    prefilename = 'Fig2_3'
    # Load the simulation file
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()

    # Set constant values
    start = 0
    end = 50
    pointInterval = 0.001
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_clamp =[50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50]
    for i in range(11):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants()['interface/membrane_potential/v_hold'] = -90
        data.constants() [ 'interface/parameters/kmca' ] = 0.001
        data.constants() [ 'interface/membrane_potential/v_var' ] = 0
        data.constants() [ 'interface/membrane_potential/v_clamp'] = v_clamp[i]
        data.constants() [ 'interface/membrane_potential/time_clamp_end'] = end
        data.constants() [ 'interface/membrane_potential/time_clamp_sta'] = 10
        simulation.run()

        # Data to save
        varName = np.array([ "Time", "ina", "v" ])
        vars = np.reshape(varName, (1,3))
        rows = end * 1000 + 1
        # Access simulation results
        results = simulation.results()
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() [ 'interface/I_Na/ina'].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
        # Save the simulation result
        filename = '%s_%s.csv' % (prefilename, i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close



