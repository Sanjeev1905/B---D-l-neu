import ROOT
import variables

input_file = "../data/sm_01_50k.root"
output_file = "../data/sm_50k_diamond.root"
tree_name = "all_vars"

rdf = ROOT.RDataFrame(tree_name, input_file)

# Declare C++ functions
variables.define_all()

# ============================================================
# Diamond-frame B
# ============================================================

rdf = variables.apply_diamond_frame(
    rdf,
    bmass=5.27963,
    numass=0.0,
    npoints=4,
    phi_start=0.0,
    clip_cost=True,
    name="diamond",
    truth=False,
    lepton="muon"
)

# ============================================================
# Physics variables
# ============================================================

rdf = variables.apply_q2(
    rdf,
    name="diamond",
    truth=False
)

rdf = variables.apply_costhetal(
    rdf,
    name="diamond",
    truth=False
)

rdf = variables.apply_costhetal_lucien(
    rdf,
    name="diamond",
    truth=False
)

rdf = variables.apply_costhetal_alexei(
    rdf,
    name="diamond",
    truth=False
)

rdf = variables.apply_costhetadst(
    rdf,
    name="diamond",
    truth=False
)

rdf = variables.apply_chi(
    rdf,
    name="diamond",
    truth=False
)

rdf = variables.apply_chi_alt(
    rdf,
    name="diamond",
    truth=False
)

# ============================================================
# ONLY save these final variables
# ============================================================

final_variables = [
    # Diamond-frame B four-vector
    "Bdiamond_CMS_px",
    "Bdiamond_CMS_py",
    "Bdiamond_CMS_pz",
    "Bdiamond_CMS_E",

    # Physics variables
    "q2_diamond",
    "costhetal_diamond",
    "costhetallucien_diamond",
    "costhetalalexei_diamond",
    "costhetadst_diamond",
    "helicitychi_diamond",
    "helicitychialt_diamond",
]

# ============================================================
# Snapshot only selected branches
# ============================================================

rdf.Snapshot(
    tree_name,
    output_file,
    final_variables
)

print("Diamond Frame calculation completed.")
print(f"Output: {output_file}")