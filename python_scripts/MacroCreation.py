import glob

def macro_creation(n_particles: int, macro_path: str, thickness:int, f_position:int, g_position: int):
    # Open the file in write mode to add the initial commands and the loops
    with open(macro_path, 'w') as file:
        # Write the initial verbose and initialization commands

        file.write('/run/initialize\n')
        file.write('/control/verbose 1\n')
        file.write('/event/verbose 0\n')

        file.write('/tracking/storeTrajectory 0\n')

        # Write the commmand to change the gun position
        file.write(f'/gun/position 0 0 {f_position} mm\n')

        # # Write the command to set the thickness
        file.write(f'/ICESPICE/Detector/Thickness {thickness}\n')
    
        # # Write the command to set the position
        file.write(f'/ICESPICE/Detector/Position {g_position}\n')

        # Loop through energies from 100 keV to 2000 keV in steps of 100 keV
        for energy in range(100, 2100, 100):

            # Write the command to set the energy
            file.write(f'/gun/energy {energy} keV\n')
            
            # Write the command to set the filename of the output root file
            file.write(f'/analysis/setFileName ICESPICE_PIPS{thickness}_f{f_position}mm_g{abs(g_position)}mm_{energy}.csv\n')
            
            # Write the command to run the simulation
            file.write(f'/run/beamOn {n_particles}\n')

def all_macros():
    # Loop through the positions from -20 to -55 in steps of -5
    for detector in [100, 300, 500, 1000]:
        for f_position in [50]:
            for g_position in range(-20,-55, -5): # -20 mm to -50 mm in steps of -5 mm
                n_particles = 50000
                # path = f'./build/MACRO_ICESPICE_PIPS{detector}_f{f_position}mm_g{abs(g_position)}mm.mac'
                path = f'./build/MACRO_ICESPICE_PIPS{detector}_f{f_position}mm_g{abs(g_position)}mm.mac'

                macro_creation(n_particles, macro_path=path, thickness=detector, f_position=f_position, g_position=g_position)

all_macros()

# create a bash script to run all the macros
with open('./build/run_all.sh', 'w') as file:
    file.write('#!/bin/bash\n')

    # look for all files that start with MACRO_ICESPICE
    for macro_file in glob.glob('./build/MACRO_ICESPICE*.mac'):
        # get rid of the build/ part of the path
        macro_file = macro_file[8:]
        file.write(f'./ICESPICE {macro_file}\n')