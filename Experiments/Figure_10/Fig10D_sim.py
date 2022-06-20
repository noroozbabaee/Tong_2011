# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig1_sim.py
import opencor as oc
import matplotlib.pyplot as plt
import numpy as np
# The prefix of the saved output file name


prefilename = 'Fig10_D'
# Load the simulation file

simfile = 'Tong_2011_newVersion.sedml'
simulation = oc.open_simulation(simfile)
data = simulation.data()

# Reset states variables and parameters

# Set constant values
start = 0
end = 400
pointInterval = 0.1
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)
varName = np.array([ "Time", "css", "ctc", "icl", "c",  "v", "cai", "I_tot", "I_inward"])
#simulation.reset(True)
vars = np.reshape(varName, (1, 9))
rows = end * 10 + 1
v_clamp = [50, 40, 30, 20, 10, 0, -10, -20, -30, -40, -50]

# v_clamp = [ -20, -15,-10,-5, 0,5, 10]
for i in range(len(v_clamp)):
    data.constants() [ 'interface/I_test_swt' ] = 1
    data.constants() [ 'interface/test_start' ] = 100
    data.constants() [ 'interface/test_end' ] = 200
    data.constants() [ 'interface/I_test' ] = -1

    data.constants() [ 'interface/Ca_Concentrations/cai_hold_swtch'] = 0
    data.constants() [ 'interface/membrane_potential/v_var'] = 0
    data.constants() [ 'interface/membrane_potential/time_clamp_strt'] = 100
    data.constants() [ 'interface/membrane_potential/time_clamp_stp'] = 200
    data.constants() [ 'interface/membrane_potential/a_correction'] = 0
    data.constants() [ 'interface/Ca_Concentrations/cai_init'] = 0.000116

    data.constants() [ 'interface/membrane_potential/v_hold'] = -60
    data.constants() [ 'interface/membrane_potential/v_clamp'] = v_clamp [ i ]
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    # Grab a some algebraic variable results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic() [ 'interface/I_Cl/css' ].values()
    r [ :, 2 ] = results.algebraic() [ 'interface/I_Cl/ctc' ].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/I_Cl/icl' ].values()
    r [ :, 4 ] = results.states() [ 'interface/I_Cl/c' ].values()
    r [ :, 5 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
    r [ :, 6 ] = results.algebraic() [ 'interface/membrane_potential/v' ].values()
    r [ :, 7 ] = results.algebraic() [ 'interface/membrane_potential/I_tot' ].values()
    r [ :, 8 ] = results.algebraic() [ 'interface/membrane_potential/I_inward' ].values()
    filename = '%s_%s.csv' % (prefilename,  i)
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
