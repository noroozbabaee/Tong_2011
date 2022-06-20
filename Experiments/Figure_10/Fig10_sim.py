# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig10_sim.py
import opencor as oc

import numpy as np
# The prefix of the saved output file name
prefilename = 'Fig10'
# Load the simulation file
Fig_AC = 1
Fig_B = 1
Fig_DE = 0
Fig_FG = 0
sub =['A_C', 'B', 'D_E', 'F_G']

if Fig_AC:
    varName = np.array([ "Time", "css", "ctc", "icl", "c",  "v", "cai" ])
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011_newVersion.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 10000
    pointInterval = 0.1
    # Reset states variables
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    cai = [ 100e-6, 250e-6, 500e-6]
    for i in range(len(cai)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants()['interface/membrane_potential/v_init'] = 190
        data.constants() [ 'interface/Ca_Concentrations/ca_var' ] = 0
        data.constants() [ 'interface/membrane_potential/v_var' ] = 1
        data.constants() [ 'interface/Ca_Concentrations/time_clamp_sta' ] = 0
        data.constants() [ 'interface/Ca_Concentrations/time_clamp_end' ] = end
        data.constants()['interface/Ca_Concentrations/cai_init'] = cai[i]
        data.constants()['interface/Ca_Concentrations/cai_hold'] = cai[i]
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        rows = end * 10 + 1
        vars = np.reshape(varName, (1, 7))
        # Grab some algebraic (state variable) results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic()['interface/I_Cl/css'].values()
        r [ :, 2 ] = results.algebraic()['interface/I_Cl/ctc'].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/I_Cl/icl'].values()
        r [ :, 4 ] = results.states() [ 'interface/I_Cl/c'].values()
        r [ :, 5 ] = results.algebraic() [ 'interface/membrane_potential/v'].values()
        r [ :, 6 ] = results.algebraic() [ 'interface/Ca_Concentrations/cai'].values()
        filename = '%s_%s_%s.csv' % (prefilename,sub[0],i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close

if Fig_B :
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011_newVersion.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 50000
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    v_cons = [-60, -30, 0, 30]
    varName = np.array([ "Time", "css",  "cai","v" ])
    for i in range(len(v_cons)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants()['interface/membrane_potential/v_init'] = 100
        data.constants() [ 'interface/Ca_Concentrations/cai_init' ] = 0.000116
        data.constants() [ 'interface/Ca_Concentrations/ca_var' ] = 1
        data.constants() [ 'interface/membrane_potential/v_var' ] = 0
        data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 0
        data.constants() [ 'interface/membrane_potential/time_clamp_end' ] = end
        data.constants() [ 'interface/membrane_potential/v_hold1'] = v_cons[i]
        data.constants() [ 'interface/membrane_potential/v_clamp' ] = v_cons[i]
        data.constants() [ 'interface/membrane_potential/v_hold2' ] = v_cons[i]
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Data to save
        rows = end * 10 + 1
        vars = np.reshape(varName, (1,4))
        # Grab a some algebraic variable results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic()['interface/I_Cl/css'].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/Ca_Concentrations/cai'].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
        filename = '%s_%s_%s.csv' % (prefilename,sub[1],i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close

if Fig_DE:
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011_newVersion.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 400
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    varName = np.array([ "Time", "css", "ctc", "icl", "c", "v", "ical" ])
    vars = np.reshape(varName, (1,7))
    rows = end * 10 + 1
    v_clamp = [ 50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50 ]
    for i in range(len(v_clamp)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants() [ 'interface/membrane_potential/v_var' ] = 0
        data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 100
        data.constants() [ 'interface/membrane_potential/time_clamp_end' ] = 200
        data.constants() [ 'interface/membrane_potential/a_correction' ] = 0
        data.constants() [ 'interface/Ca_Concentrations/cai_init' ] = 0.000116
        data.constants() [ 'interface/membrane_potential/v_hold1' ] = -60
        data.constants() [ 'interface/membrane_potential/v_clamp' ] = v_clamp [ i ]
        data.constants() [ 'interface/membrane_potential/v_hold2' ] = -60
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() [ 'interface/I_Cl/css' ].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/I_Cl/ctc' ].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/I_Cl/icl' ].values()
        r [ :, 4 ] = results.states() [ 'interface/I_Cl/c' ].values()
        r [ :, 5 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
        r [ :, 6 ] = results.algebraic() [ 'interface/I_CaL/ical' ].values()
        filename = '%s_%s_%s.csv' % (prefilename, sub[2], i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close
if Fig_FG:
    simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Tong_2011_newVersion.sedml'
    simulation = oc.open_simulation(simfile)
    data = simulation.data()
    # Set constant values
    start = 0
    end = 400
    pointInterval = 0.1
    data.set_starting_point(start)
    data.set_ending_point(end)
    data.set_point_interval(pointInterval)
    varName = np.array([ "Time", "css", "ctc", "icl", "c", "v", "ical" ])
    vars = np.reshape(varName, (1,7))
    rows = end * 10 + 1
    v_clamp = [  40, 20, 0,  -20,  -40, -60, -80, -100 ]
    for i in range(len(v_clamp)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants() [ 'interface/membrane_potential/v_var' ] = 0
        data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 100
        data.constants() [ 'interface/membrane_potential/time_clamp_end' ] = 200
        data.constants() [ 'interface/membrane_potential/a_correction' ] = 0
        data.constants() [ 'interface/Ca_Concentrations/cai_init' ] = 0.000116
        data.constants() [ 'interface/membrane_potential/v_hold1' ] = -60
        data.constants() [ 'interface/membrane_potential/v_clamp' ] = 0
        data.constants() [ 'interface/membrane_potential/v_hold2' ] = v_clamp[i]
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Grab a some algebraic variable results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic() [ 'interface/I_Cl/css' ].values()
        r [ :, 2 ] = results.algebraic() [ 'interface/I_Cl/ctc' ].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/I_Cl/icl' ].values()
        r [ :, 4 ] = results.states() [ 'interface/I_Cl/c' ].values()
        r [ :, 5 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
        r [ :, 6 ] = results.algebraic() [ 'interface/I_CaL/ical' ].values()
        filename = '%s_%s_%s.csv' % (prefilename, sub[3], i)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close
