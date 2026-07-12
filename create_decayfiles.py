import os
import numpy as np

# Define the ranges
g_L_values = np.linspace(0.0, 0.08, 9)
g_R_values = np.linspace(0.00, 0.105, 8)
g_P_values = np.linspace(-0.6, 0.0, 7)



# Template for the line to be modified
template_line = "1   D*+    mu-   anti-nu_mu   BTODSTARLNUNP 0 0 {g_L:.3f} 0 1 {g_R:.3f} 0 2 0 {g_P:.3f} 3 0 {neg_g_P:.3f};\n"


for sample in range (0, 226):
    # Base directory to save files
    parent_dir = "decfiles_b2dstar_np_070726" 
    base_directory = os.path.join(parent_dir, "decfile" + str(sample))


    # Create base directory if it doesn't exist
    if not os.path.exists(base_directory):
        os.makedirs(base_directory)

    # Iterate over all values of g_L, g_R, and g_P
    for g_L in g_L_values:
        g_L_directory = os.path.join(base_directory, f"decay_{g_L:.3f}")
        os.makedirs(g_L_directory, exist_ok=True)

        for g_R in g_R_values:
            g_R_directory = os.path.join(g_L_directory, f"decay_{g_L:.3f}_{g_R:.3f}")
            os.makedirs(g_R_directory, exist_ok=True)

            for g_P in g_P_values:
                filename = os.path.join(g_R_directory, f"decay_{g_L:.3f}_{g_R:.3f}_{g_P:.3f}.dec")
                
                # Read the original .dec file
                with open("BB_dstarlnu_np.dec", "r") as f:
                    content = f.readlines()

                # Modify the specific line with the new values of g_L, g_R, and g_P
                modified_content = []
                for line in content:
                    if "1   D*+    mu-   anti-nu_mu   BTODSTARLNUNP" in line:
                        # Calculate negative g_P
                        neg_g_P = -g_P
                        modified_line = template_line.format(g_L=g_L, g_R=g_R, g_P=g_P, neg_g_P=neg_g_P)
                        modified_content.append(modified_line)
                    else:
                        modified_content.append(line)
                
                # Write the modified content to the new file
                with open(filename, "w") as f:
                    f.writelines(modified_content)
