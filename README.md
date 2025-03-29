# DockMate

**DockMate** is an automated molecular docking pipeline designed for high-throughput virtual screening of ligand-protein interactions. It streamlines the process of preparing molecular structures, predicting binding pockets, and performing docking simulations using AutoDock Vina.

## Features
- **Ligand Preparation:** Converts ligand files (.pdb, .sdf) to PDBQT format with hydrogen addition and 3D structure generation.
- **Protein Preparation:** Prepares receptor proteins using `prepare_receptor4.py`.
- **Binding Site Prediction:** Utilizes `p2rank` to predict binding pockets.
- **Automated Docking:** Runs molecular docking simulations using AutoDock Vina.
- **Parallel Processing:** Supports multi-threaded ligand screening for efficiency.

## Requirements
- Python 3.x
- OpenBabel (`pybel` module)
- AutoDock Tools & AutoDock Vina
- p2rank
- Bash shell (for script execution)

## Usage
1. **Prepare the protein structure:**
   ```bash
   python DockMate.py
   ```
2. **Ensure your ligands are stored in the `ligands/` directory.**
3. **Docking results will be saved as PDBQT files.**
