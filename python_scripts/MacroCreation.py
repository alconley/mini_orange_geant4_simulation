# Define the file path for the macro
macro_path = './ICESPICE.mac'

n_particles = 10000

# Open the file in write mode to add the initial commands and the loops
with open(macro_path, 'w') as file:
    # Write the initial verbose and initialization commands
    file.write('/control/verbose 1\n')
    file.write('/run/verbose 0\n')
    file.write('/event/verbose 0\n')
    file.write('/run/initialize\n')
    
    # Loop through the different thicknesses of our PIPS detectors
    for thickness in [100, 300, 500, 1000]:
        # Write the command to set the thickness
        file.write(f'/ICESPICE/Detector/Thickness {thickness}\n')
        
        # Loop through the positions from -20 to -60 in steps of 5
        for position in range(-20, -65, -5):
            # Write the command to set the position
            file.write(f'/ICESPICE/Detector/Position {position}\n')
            
            # Loop through energies from 50 keV to 2000 keV in steps of 50 keV
            for energy in range(50, 2050, 50):
                # Write the command to set the energy
                file.write(f'/ICESPICE/source/Energy {energy}\n')
                
                # Write the command to set the filename of the output root file
                file.write(f'/analysis/setFileName ICESPICE_PIPS{thickness}_f50mm_g{position}mm_{energy}keV.root\n')
                
                # Write the command to run the simulation
                file.write(f'/run/beamOn {n_particles}\n')