import os
import numpy as np
import pandas as pd
import uproot
from sklearn.preprocessing import MinMaxScaler
# data is not suffled, need to suffel
# Directories for input and output
# input_dir = "/mnt/data/work/ml_hawaii/test_b2dstar/datafiles_b2star_np_230626/decfile" + str(sample)   

output_dir = "/mnt/data/work/ml_hawaii/test_b2dstar/B2Dslnu_070726/generated_voxel_images"   

os.makedirs(output_dir, exist_ok=True)
EVENTS_PER_IMAGE = 50000

# Parameters for binning
num_bins = 50  # Number of bins for each axis (modifiable)

# Function to apply Min-Max scaling and binning
def process_data(df):
    # Apply Min-Max scaling to q2 and chi
    scaler = MinMaxScaler()
    df[["q2", "chi"]] = scaler.fit_transform(df[["q2", "chi"]])

    # Bin ctd, ctl, and chi
    df["X"] = np.digitize(df["ctd"], bins=np.linspace(-1, 1, num_bins)) - 1
    df["Y"] = np.digitize(df["chi"], bins=np.linspace(0, 1, num_bins)) - 1
    df["Z"] = np.digitize(df["ctl"], bins=np.linspace(-1, 1, num_bins)) - 1

    return df

def generate_voxel_grid(df):
    # Create an empty voxel grid
    voxelgrid_np = np.zeros((num_bins, num_bins, num_bins))
    counts = np.zeros((num_bins, num_bins, num_bins))  # To store counts for averaging

    # Process data
    df_processed = process_data(df)

    # Accumulate q2 values and counts for averaging
    for X, Y, Z, Q2 in zip(df_processed["X"], df_processed["Y"], df_processed["Z"], df_processed["q2"]):
        if 0 <= X < num_bins and 0 <= Y < num_bins and 0 <= Z < num_bins:
            voxelgrid_np[X, Y, Z] += Q2
            counts[X, Y, Z] += 1

    # Calculate averages (avoid division by zero)
    with np.errstate(divide='ignore', invalid='ignore'):
        voxelgrid_np = np.where(counts > 0, voxelgrid_np / counts, 0)

    return voxelgrid_np

# output_dir = "/mnt/data/work/ml_hawaii/test_b2dstar/generated_voxel_images"   
# os.makedirs(output_dir, exist_ok+True)

# Process each root file and generate voxel grid
for sample in range(0, 99):
    input_dir = "/mnt/data/work/ml_hawaii/test_b2dstar/B2Dslnu_070726/datafiles_b2dstar_np_100726_test/rootfile" + str(sample)   

    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".root"):
                input_file_path = os.path.join(root, file)

                # Extract parameter values from the directory structure
                param_dir = os.path.basename(root)
                if param_dir.startswith("events_"):
                    try:
                        g_L, g_R, g_P = map(float, param_dir.replace("events_", "").split("_"))  # Remove 'events_' prefix and split
                    except ValueError:
                        print(f"Skipping directory {param_dir}: not in expected format events_gL_gR_gP")
                        continue

                    # Open the .root file and access the 'ntp' tree
                    with uproot.open(input_file_path) as infile:
                        if "ntp" in infile:
                            tree = infile["ntp"]

                            # Load branches into a DataFrame
                            df = pd.DataFrame({
                                "ctd": tree["ctd"].array(library="np"),
                                "chi": tree["chi"].array(library="np"),
                                "ctl": tree["ctl"].array(library="np"),
                                "q2": tree["q2"].array(library="np"),
                            })

                            # Generate voxel grid
                            df_shuffled = df.sample(frac=1).reset_index(drop=True) # suffled the data
                            # voxel_image = generate_voxel_grid(df_shuffled)

                            n_images = len(df_shuffled) // EVENTS_PER_IMAGE

                            for i in range(n_images):
                                start = i * EVENTS_PER_IMAGE
                                stop = (i +  1) * EVENTS_PER_IMAGE
                                # df_chunk = df_shuffled.iloc[start:stop]
                                voxel_image = generate_voxel_grid(df_shuffled)

                                output_file_name = f"{g_L:.3f}_{g_R:.3f}_{g_P:.3f}_s{sample}_i{i:03d}.npy"
                                output_file_path = os.path.join(output_dir, output_file_name)
                                np.save(output_file_path, voxel_image)
                                print(f"Saved voxel image for {file} with parameters {param_dir} in {output_dir}")
                else:
                    print(f"Skipping directory {param_dir}: does not start with 'events_'")

                                

                            # Save the voxel image as a .npy file with parameter-based name
                            # output_file_name = f"{g_L:.3f}_{g_R:.3f}_{g_P:.3f}" + str(sample)".npy"
                            # output_file_path = os.path.join(output_dir, output_file_name)
                            # np.save(output_file_path, voxel_image)

                            # print(f"Saved voxel image for {file} with parameters {param_dir} in {output_dir}")
                # else:
                #     print(f"Skipping directory {param_dir}: does not start with 'events_'")
