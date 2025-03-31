import os
import subprocess

vina_path = r"Requirements\Vina\vina.exe"  # Path to Vina executable

def perform_Docking(receptor_file, ligand_folder, output_folder, 
                    center_x, center_y, center_z, 
                    size_x, size_y, size_z, 
                    num_modes=9, energy_range=3.0, exhaustiveness=8):
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Loop through all ligand files in the folder
    for ligand_file in os.listdir(ligand_folder):
        if ligand_file.endswith(".pdbqt"):  # Process only .pdbqt files
            ligand_path = os.path.join(ligand_folder, ligand_file)
            output_name = os.path.splitext(ligand_file)[0]  # Get ligand name without extension

            output_pdbqt = os.path.join(output_folder, f"{output_name}_docked.pdbqt")
            log_file = os.path.join(output_folder, f"{output_name}_log.txt")

            # Run Vina docking command
            command = [
                vina_path,
                "--receptor", receptor_file,
                "--ligand", ligand_path,
                "--center_x", str(center_x), "--center_y", str(center_y), "--center_z", str(center_z),
                "--size_x", str(size_x), "--size_y", str(size_y), "--size_z", str(size_z),
                "--out", output_pdbqt,
                "--log", log_file,
                "--num_modes", str(num_modes),
                "--energy_range", str(energy_range),
                "--exhaustiveness", str(exhaustiveness)
            ]

            print(f"Running docking for {ligand_file}...")
            subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Batch docking completed!")
