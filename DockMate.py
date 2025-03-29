import os
import subprocess
from openbabel import openbabel, pybel
from concurrent.futures import ThreadPoolExecutor

def convert_ligand_to_pdbqt(input_ligand, output_pdbqt):
    mol = next(pybel.readfile(input_ligand.split('.')[-1], input_ligand))
    mol.addh()  # Add hydrogens
    mol.make3D()
    mol.write("pdbqt", output_pdbqt, overwrite=True)
    print(f"Ligand converted: {output_pdbqt}")

def prepare_protein(pdb_file, output_pdbqt):
    script = f"""
    source ~/.bashrc
    prepare_receptor4.py -r {pdb_file} -o {output_pdbqt} -A hydrogens
    """
    subprocess.run(script, shell=True, executable='/bin/bash')
    print(f"Protein prepared: {output_pdbqt}")

def run_p2rank(pdb_file):
    p2rank_cmd = f"p2rank predict {pdb_file}"
    subprocess.run(p2rank_cmd, shell=True)
    pockets_file = pdb_file.replace(".pdb", "_predictions.csv")
    return pockets_file

def extract_pocket_info(pockets_file):
    with open(pockets_file, "r") as f:
        lines = f.readlines()
        if len(lines) > 1:
            top_pocket = lines[1].split(',')  # Assuming CSV format
            center_x, center_y, center_z = float(top_pocket[1]), float(top_pocket[2]), float(top_pocket[3])
            size_x, size_y, size_z = float(top_pocket[4]), float(top_pocket[5]), float(top_pocket[6])
            return center_x, center_y, center_z, size_x, size_y, size_z
    return 0.0, 0.0, 0.0, 20.0, 20.0, 20.0  # Default values if no pockets found

def create_config_file(center_x, center_y, center_z, size_x, size_y, size_z, output_file="config.txt"):
    config_content = f"""
    center_x = {center_x}
    center_y = {center_y}
    center_z = {center_z}
    size_x = {size_x}
    size_y = {size_y}
    size_z = {size_z}
    exhaustiveness = 8
    """
    with open(output_file, "w") as f:
        f.write(config_content.strip())
    print(f"Config file created: {output_file}")

def run_docking(protein_pdbqt, ligand_pdbqt, config_file, output_pdbqt):
    vina_cmd = f"vina --receptor {protein_pdbqt} --ligand {ligand_pdbqt} --config {config_file} --out {output_pdbqt}"
    subprocess.run(vina_cmd, shell=True)
    print(f"Docking completed: {output_pdbqt}")

def process_ligand(ligand_file, ligand_folder, protein_pdbqt, config_file):
    ligand_path = os.path.join(ligand_folder, ligand_file)
    ligand_pdbqt = ligand_file.rsplit('.', 1)[0] + ".pdbqt"
    convert_ligand_to_pdbqt(ligand_path, ligand_pdbqt)
    output_docked_pdbqt = ligand_file.rsplit('.', 1)[0] + "_docked.pdbqt"
    run_docking(protein_pdbqt, ligand_pdbqt, config_file, output_docked_pdbqt)

def process_ligand_folder(ligand_folder, protein_pdbqt, config_file):
    ligands = [f for f in os.listdir(ligand_folder) if f.endswith(".pdb") or f.endswith(".sdf")]
    
    with ThreadPoolExecutor() as executor:
        executor.map(lambda ligand: process_ligand(ligand, ligand_folder, protein_pdbqt, config_file), ligands)

if __name__ == "__main__":
    ligand_folder = "ligands"  # Folder containing all ligand files
    protein_file = "protein.pdb"
    protein_pdbqt = "protein.pdbqt"
    
    prepare_protein(protein_file, protein_pdbqt)
    pockets_file = run_p2rank(protein_file)
    center_x, center_y, center_z, size_x, size_y, size_z = extract_pocket_info(pockets_file)
    create_config_file(center_x, center_y, center_z, size_x, size_y, size_z)
    
    process_ligand_folder(ligand_folder, protein_pdbqt, "config.txt")
