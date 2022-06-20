# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig12_sim.py
import opencor as oc
import numpy as np
# The prefix of the saved output file name
prefilename = 'Fig12'
# Load the simulation file
sub =['A','B']
varName = np.array(["Time",  "I_st", "v", "cai"])
simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/Fig12_Tong_2011.sedml'
# simfile = 'Fig12_Tong_2011.sedml'
simulation = oc.open_simulation(simfile)
data = simulation.data()
# Set constant values
start = 0
end = 10000
pointInterval = 1
# Reset states variables
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)
A = [1, 0]
B = [0, 1]
ca = [0.000116,0.00016]
v_init =[-53, -43]
for i in range(len(ca)):
    simulation.reset(True)
    data.constants() [ 'interface/membrane_potential/A'] = A[i]
    data.constants() [ 'interface/membrane_potential/B'] = B[i]
    data.constants() [ 'interface/Ca_Concentrations/cai_init'] = ca [i]
    data.constants() [ 'interface/membrane_potential/v_init' ] = v_init[i]
    simulation.run()
    # Access simulation results
    results = simulation.results()
    # Data to save
    varName = np.array([ "Time", "I_st", "v", "cai" ])
    rows = end * 1 + 1
    vars = np.reshape(varName, (1, 4))
    # Grab a some algebraic variable results
    r = np.zeros((rows, len(varName)))
    r [ :, 0 ] = results.voi().values()
    r [ :, 1 ] = results.algebraic() [ 'interface/I_st'].values()
    r [ :, 2 ] = results.algebraic() [ 'interface/membrane_potential/v'].values()
    r [ :, 3 ] = results.algebraic() [ 'interface/Ca_Concentrations/cai'].values()

    filename = '%s_%s.csv' % (prefilename, sub[i])
    np.savetxt(filename, vars, fmt='%s', delimiter=",")
    with open(filename, "ab") as f:
        np.savetxt(f, r, delimiter=",")
    f.close
