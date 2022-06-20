# Author: Leyla Noroozbabaee
# Date: 12/12/2021
# To reproduce the data needed for Figure 9 in associated original paper,
# execute this script in the Python console in OpenCOR. This can be done
# with the following commands at the prompt in the OpenCOR Python console:
#
#     In [1]: cd path/to/folder_this_file_is_in
#     In [2]: run Fig9_sim.py
import opencor as oc
import numpy as np


prefilename = 'Fig9'
# Load the simulation file
simfile = 'C:/Users/lnor300/Documents/CellML/12_Labors/Tong_2011_V1/Simulations/VoltageVAR_Tong_2011.sedml'
simulation = oc.open_simulation(simfile)
data = simulation.data()
# Set constant values
start = 0
end = 300
pointInterval = 0.01
data.set_starting_point(start)
data.set_ending_point(end)
data.set_point_interval(pointInterval)
sub =['A','B']
varName = np.array([ "Time", "ik1", "ik2", "iBKa", "iBKab", "ika", "ib", "v", "I_K_tot", "xabtc"])
vars = np.reshape(varName, (1, 10))
rows = end * 100 + 1
v_hold =[-40,-80]
v_clamp = [  70,60,50,40,30,20,10,0,-10,-20,-30,-40 ]
for i in range(len(v_hold)):
    for j in range(len(v_clamp)):
        # Reset states variables and parameters
        simulation.reset(True)
        data.constants() [ 'interface/membrane_potential/v_hold' ] = v_hold [ i ]
        data.constants() [ 'interface/membrane_potential/v_clamp' ] = v_clamp [ j ]
        data.constants() [ 'interface/membrane_potential/time_clamp_end' ] = 250
        data.constants() [ 'interface/membrane_potential/time_clamp_sta' ] = 20
        simulation.run()
        # Access simulation results
        results = simulation.results()
        # Grab some algebraic results
        r = np.zeros((rows, len(varName)))
        r [ :, 0 ] = results.voi().values()
        r [ :, 1 ] = results.algebraic()['interface/I_K1/ik1'].values()
        r [ :, 2 ] = results.algebraic()['interface/I_K2/ik2'].values()
        r [ :, 3 ] = results.algebraic() [ 'interface/I_BKa/iBKa'].values()
        r [ :, 4 ] = results.algebraic() [ 'interface/I_BKab/iBKab'].values()
        r [ :, 5 ] = results.algebraic() [ 'interface/I_Ka/ika'].values()
        r [ :, 6 ] = results.algebraic() [ 'interface/I_b/ib'].values()
        r [ :, 7 ] = results.algebraic() [ 'interface/membrane_potential/v'].values()
        r [ :, 8 ] = results.algebraic() [ 'interface/membrane_potential/I_K_tot'].values()
        r [ :, 9 ] = results.algebraic() [ 'interface/I_BKab/xabtc'].values()
        filename = '%s_%s_%s.csv' % (prefilename,sub[i],  j)
        np.savetxt(filename, vars, fmt='%s', delimiter=",")
        with open(filename, "ab") as f:
            np.savetxt(f, r, delimiter=",")
        f.close
