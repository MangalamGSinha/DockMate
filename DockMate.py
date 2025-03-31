import os
from Requirements.Dockmate_prepare_Ligand import prepare_Ligand
from Requirements.Dockmate_prepare_Protein import prepare_Protein
from Requirements.Dockmate_perform_Docking import perform_Docking


def parse_config(config_file):
    config = {}
    
    try:
        with open(config_file, 'r') as f:
            for line in f:
                # Skip empty lines and comments
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Split each line by the '=' character and strip whitespace
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Handle specific parameter types
                    if key == 'protein':
                        config['protein'] = value
                    elif key == 'ligand_folder':
                        config['ligand_folder'] = value
                    elif key == 'pocket_center_x_y_z':
                        coords = value.split()
                        if len(coords) == 3:
                            config['pocket_center'] = [float(coords[0]), float(coords[1]), float(coords[2])]
                        else:
                            raise ValueError(f"Expected 3 pocket coordinates, got {len(coords)}")
                    elif key == 'pocket_size':
                        sizes = value.split()
                        if len(sizes) == 3:
                            config['pocket_size'] = [float(sizes[0]), float(sizes[1]), float(sizes[2])]
                        else:
                            raise ValueError(f"Expected 3 pocket size values, got {len(sizes)}")
                    elif key == 'output_folder':
                        config['output_folder'] = str(value)
                    elif key == 'num_modes':
                        config['num_modes'] = int(value)
                    elif key == 'energy_range':
                        config['energy_range'] = float(value)
                    elif key == 'exhaustiveness':
                        config['exhaustiveness'] = int(value)
                    else:
                        # Store any additional parameters as strings
                        config[key] = value
                else:
                    print(f"Warning: Ignoring malformed line: {line}")
        
        # Validate that required parameters are present
        required_params = ['protein', 'ligand_folder', 'pocket_center', 'pocket_size']
        missing_params = [param for param in required_params if param not in config]
        if missing_params:
            raise ValueError(f"Missing required parameters: {', '.join(missing_params)}")
            
        return config
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {config_file}")
    except Exception as e:
        raise Exception(f"Error parsing config file: {str(e)}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Dockmate: A molecular docking tool")
    parser.add_argument("-config", required=True, help="Path to configuration file")
    args = parser.parse_args()
    
    try:
        config = parse_config(args.config)
        print("Configuration loaded successfully:")
        for key, value in config.items():
            print(f"  {key}: {value}")

        print("Preparing Ligands")
        prepare_Ligand(config['ligand_folder'])  # Process ligands in the specified folder

        print("Preparing Protein")
        prepare_Protein(config['protein'])  # Prepare the protein


        print("Performing Docking")
        perform_Docking(
            receptor_file=config['protein'].replace(".pdb", ".pdbqt"),  # Assuming the output from prepare_Protein is .pdbqt
            ligand_folder=os.path.join(config['ligand_folder'], "processed_ligands"),  # Processed ligands folder
            output_folder=config.get('output_folder','docking_results'),  # Output folder for docking results
            center_x=config['pocket_center'][0],
            center_y=config['pocket_center'][1],
            center_z=config['pocket_center'][2],
            size_x=config['pocket_size'][0],
            size_y=config['pocket_size'][1],
            size_z=config['pocket_size'][2],
            num_modes=config.get('num_modes', 9),  # Default to 9 if not specified
            energy_range=config.get('energy_range', 3.0),  # Default to 3.0 if not specified
            exhaustiveness=config.get('exhaustiveness', 8)  # Default to 8 if not specified
        )
        print("Docking completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())