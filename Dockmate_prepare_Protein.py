import os
import subprocess
from Bio import PDB

MGLTOOLS_PATH = r"Requirements\MGLTools-1.5.7\python.exe" 
PREPARE_RECEPTOR_SCRIPT = r"Requirements\MGLTools-1.5.7\Lib\site-packages\AutoDockTools\Utilities24\prepare_receptor4.py"

def prepare_pdbqt(input_pdb, output_pdbqt):
    """Remove non-protein molecules, add polar hydrogens, Kollman charges, and prepare PDBQT using MGLTools."""
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("protein", input_pdb)

    class CleanProtein(PDB.Select):
        def accept_residue(self, residue):
            return residue.id[0] == " "  # Keep only protein residues

    cleaned_pdb = "temp_cleaned.pdb"  # Temporary file
    io = PDB.PDBIO()
    io.set_structure(structure)
    io.save(cleaned_pdb, CleanProtein())

    # Convert to PDBQT with Kollman charges and polar hydrogens
    command = f"{MGLTOOLS_PATH} {PREPARE_RECEPTOR_SCRIPT} -r {cleaned_pdb} -o {output_pdbqt} -A checkhydrogens -U waters"
    subprocess.run(command, shell=True)
    
    # Remove temporary file
    os.remove(cleaned_pdb)
    print(f"Protein prepared and saved as {output_pdbqt}")

def prepare_Protein(pdb_file):
    if not os.path.exists(pdb_file):
        print(f"Error: File not found! Path: {pdb_file}")
        return
    pdbqt_file = pdb_file.replace(".pdb", ".pdbqt")
    prepare_pdbqt(pdb_file, pdbqt_file)
