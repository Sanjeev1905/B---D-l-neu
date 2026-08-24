import os
import subprocess
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--start", type=int, required=True)
parser.add_argument("--end", type=int, required=True)

args = parser.parse_args()

seed_values = []

for sample in range(args.start, args.end + 1):
    # Base directory containing the decay files
    base_directory = "decfiles_b2dstar_np_240826/decfile" + str(sample)
    # Directory where the event data will be stored
    events_directory = "datafiles_b2dstar_np_240826/rootfile" + str(sample)
    
    # adding seed with random number generator
    num = random.randint(100, 1000000)
    
    seed = num +100000
    #seed_values.append(seed)
    
    # saving the seed in a txt file
    #seed_file = f"seeds_{args.start}_{args.end}.txt"
    
    #with open(seed_file, "w") as f:
    #	 f.write(f" {seed} ")

    # Command to run the event generation
    # command_template = "basf2 --random-seed {seed} generate_events.py -- 100 {dec_file} {root_file}"
    command_template = (
        "basf2 --random-seed {seed} genmc_MC15ri_b.py -- "
        "10 {dec_file} {root_file}"
    )

    
    # Create the base events_data directory if it doesn't exist
    if not os.path.exists(events_directory):
        os.makedirs(events_directory)

    # Initialize a counter to track progress
    total_directories = 0
    processed_directories = 0

    # First, count the total number of directories to process
    for g_L_dir in os.listdir(base_directory):
        g_L_path = os.path.join(base_directory, g_L_dir)

        if os.path.isdir(g_L_path):
            for g_R_dir in os.listdir(g_L_path):
                g_R_path = os.path.join(g_L_path, g_R_dir)

                # if os.path.isdir(g_R_path):
                #     for dec_file in os.listdir(g_R_path):
                #         if dec_file.endswith(".dec"):
                #             total_directories += 1

    # Traverse through the directory structure and process files
    for g_L_dir in os.listdir(base_directory):
        g_L_path = os.path.join(base_directory, g_L_dir)

        if os.path.isdir(g_L_path):
            for g_R_dir in os.listdir(g_L_path):
                g_R_path = os.path.join(g_L_path, g_R_dir)

                if os.path.isdir(g_R_path):
                    for dec_file in os.listdir(g_R_path):
                        if dec_file.endswith(".dec"):
                            # Full path to the .dec file
                            dec_file_path = os.path.join(g_R_path, dec_file)

                            # Extract g_L, g_R, and g_P values from the filename
                            parts = dec_file.replace("decay_", "").replace(".dec", "").split("_")
                            g_L, g_R, g_P = parts[0], parts[1], parts[2]

                            # Keep only gR=0 and gP=0
                            # if abs(float(g_R)) > 1e-6 or abs(float(g_P)) > 1e-6:
                            #     continue

                            # Create the subdirectory for this set of parameters
                            event_subdir = os.path.join(events_directory, f"events_{g_L}_{g_R}_{g_P}")
                            os.makedirs(event_subdir, exist_ok=True)

                            # File paths for the root and text files
                            root_file_path = os.path.join(event_subdir, f"decay_{g_L}_{g_R}_{g_P}.root")
                            text_file_path = os.path.join(event_subdir, f"params_{g_L}_{g_R}_{g_P}.txt")

                            # Prepare the command for generating the root file
                            # command = command_template.format(dec_file=dec_file_path, root_file=root_file_path, seed = seed)
                            # command = command_template.format(
                            #             "basf2 --random-seed {seed} generate_events.py -- "
                            #             "100 {dec_file} {root_file}"
                            #         )
                            command = command_template.format(
                                seed=seed,
                                dec_file=dec_file_path,
                                root_file=root_file_path
                            )

                            # Retry logic for event generation
                            success = False
                            while not success:
                                result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                                if "*** Break *** segmentation violation" not in result.stderr:
                                    success = True
                                    
                                 

                            # Copy the .dec file to the new subdirectory & check command
                            print(command)
                            
                            subprocess.run(f"cp {dec_file_path} {event_subdir}", shell=True)

                            # Write the g_L, g_R, and g_P values to the text file
                            with open(text_file_path, "w") as f:
                                f.write(f"{g_L} {g_R} {g_P} {seed}\n {command}\n")

                            # Increment the processed directories counter
                            processed_directories += 1

                            # Print progress
                            print(f"Processed {processed_directories} of {total_directories} directories")
                            
                            

