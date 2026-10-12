import os
import numpy as np

# Coupling parameter ranges
g_L_values = np.linspace(0.0, 0.08, 9)
g_R_values = np.linspace(0.00, 0.105, 8)
g_P_values = np.linspace(-0.6, 0.0, 7)

# Input decay file
input_dec_file = "../stering/hp_dec.dec"

# Output directory: all files will be saved here
output_dir = (
    "/home/belle2/sanjeeva/B2dstrlnu/"
    "diamond_frame/myAnalysis/evtgen_dataprod/decfiles"
)
os.makedirs(output_dir, exist_ok=True)

# Template for the modified decay line
template_line = (
    "1   D*+sig    mu-   anti-nu_mu   BTODSTARLNUNP "
    "0 0 {g_L:.3f} 0 1 {g_R:.3f} 0 2 0 {g_P:.3f} "
    "3 0 {neg_g_P:.3f};\n"
)

# Read the original decay file once
with open(input_dec_file, "r") as f:
    original_content = f.readlines()

# Find the active decay line
target_indices = [
    i for i, line in enumerate(original_content)
    if (
        "D*+sig" in line
        and "mu-" in line
        and "anti-nu_mu" in line
        and "BTODSTARLNUNP" in line
        and not line.lstrip().startswith("#")
    )
]

if len(target_indices) != 1:
    raise RuntimeError(
        f"Expected exactly one matching active decay line, "
        f"found {len(target_indices)}"
    )

target_index = target_indices[0]

# Generate every possible combination
count = 0

for g_L in g_L_values:
    for g_R in g_R_values:
        for g_P in g_P_values:

            # Calculate negative g_P
            neg_g_P = -g_P

            # Create modified decay line
            modified_line = template_line.format(
                g_L=g_L,
                g_R=g_R,
                g_P=g_P,
                neg_g_P=neg_g_P
            )

            # Replace only the target line
            modified_content = original_content.copy()
            modified_content[target_index] = modified_line

            # Filename identifying the coupling parameters
            filename = (
                f"decay_{g_L:.3f}_{g_R:.3f}_{g_P:.3f}.dec"
            )

            output_path = os.path.join(output_dir, filename)

            # Write the new decay file
            with open(output_path, "w") as f:
                f.writelines(modified_content)

            count += 1

print(f"Generated {count} decay files.")
print(f"All files saved in: {output_dir}")