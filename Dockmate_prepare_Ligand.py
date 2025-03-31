import os
import glob
import subprocess


OPENBABEL_PATH = r"Requirements\OpenBabel-3.1.1\obabel.exe"
MGLTOOLS_PATH = r"Requirements\MGLTools-1.5.7\python.exe"
PREPARE_LIGAND_SCRIPT = r"Requirements\MGLTools-1.5.7\Lib\site-packages\AutoDockTools\Utilities24\prepare_ligand4.py"


def convert_sdf_to_pdb(sdf_file, pdb_file):
    # """Convert SDF to PDB using Open Babel."""
    command = f"{OPENBABEL_PATH} {sdf_file} -O {pdb_file}"
    subprocess.run(command, shell=True)
    print(f"Converted {sdf_file} to {pdb_file}")


def prepare_ligand_pdbqt(input_pdb, output_pdbqt):
    # Get absolute paths and directories
    full_pdb_path = os.path.abspath(input_pdb)
    input_dir = os.path.dirname(full_pdb_path)
    input_filename = os.path.basename(full_pdb_path)
    full_output_path = os.path.abspath(output_pdbqt)  
    
    # Store current directory
    original_dir = os.getcwd()
    
    try:
        # Change to input directory
        os.chdir(input_dir)
        
        # Use full paths for the Python executable and script
        mgl_full_path = os.path.join(original_dir, MGLTOOLS_PATH)
        script_full_path = os.path.join(original_dir, PREPARE_LIGAND_SCRIPT)
        
        # Run command using the local filename (not the full path)
        command = f"\"{mgl_full_path}\" \"{script_full_path}\" -l \"{input_filename}\" -o \"{full_output_path}\" -A hydrogens"

        subprocess.run(command, shell=True, capture_output=True, text=True)

    finally:
        # Change back to original directory
        os.chdir(original_dir)

    print(f"{input_pdb} saved as {output_pdbqt}")




def process_ligands(folder_path):
    # Process all ligands in the specified folder.
    os.makedirs(os.path.join(folder_path, "processed_ligands"), exist_ok=True)  

    sdf_files = glob.glob(os.path.join(folder_path, "*.sdf"))
    # Convert all SDF files to PDB
    for sdf in sdf_files:
        pdb_file = sdf.replace(".sdf", ".pdb")
        convert_sdf_to_pdb(sdf, pdb_file)
    # Recompute PDB file list after conversion
    pdb_files = glob.glob(os.path.join(folder_path, "*.pdb"))   
    # Convert all PDB files to PDBQT
    for pdb in pdb_files:
        pdbqt_file = os.path.join(folder_path, "processed_ligands", os.path.basename(pdb).replace(".pdb", ".pdbqt"))
        prepare_ligand_pdbqt(pdb, pdbqt_file)




def prepare_Ligand(Ligand_folder):
    folder_path = Ligand_folder.strip()
    if not os.path.exists(folder_path):
        print("Error: Folder not found!")
        return
    process_ligands(folder_path)
