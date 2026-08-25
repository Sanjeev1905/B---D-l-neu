import ROOT
import math


# ============================================================
# Input / output
# ============================================================

input_file = "reco_000_047_600.root"
output_file = "param_000_047_600.root"

tree_name = "antiB0"


# ============================================================
# Open input
# ============================================================

fin = ROOT.TFile.Open(input_file)
tree = fin.Get(tree_name)

if not tree:
    raise RuntimeError(f"Could not find tree: {tree_name}")


# ============================================================
# Output
# ============================================================

fout = ROOT.TFile(output_file, "RECREATE")

outtree = ROOT.TTree(
    tree_name,
    "B -> D* l nu angular variables"
)

q2  = array = ROOT.std.vector("double")()
ctd = ROOT.std.vector("double")()
ctl = ROOT.std.vector("double")()
chi = ROOT.std.vector("double")()

outtree.Branch("q2", q2)
outtree.Branch("ctd", ctd)
outtree.Branch("ctl", ctl)
outtree.Branch("chi", chi)


# ============================================================
# EvtGen-like EvtDecayAngle
#
# EvtDecayAngle(P,Q,D)
#
# P = parent
# Q = intermediate particle
# D = daughter
#
# This is exactly the invariant expression used by EvtGen.
# ============================================================

def evt_decay_angle(P, Q, D):

    pd = P.Dot(D)
    pq = P.Dot(Q)
    qd = Q.Dot(D)

    mp2 = P.M2()
    mq2 = Q.M2()
    md2 = D.M2()

    denominator = math.sqrt(
        (pq * pq - mq2 * mp2) *
        (qd * qd - mq2 * md2)
    )

    if denominator == 0:
        return float("nan")

    cost = (
        pd * mq2 - pq * qd
    ) / denominator

    # Protect against tiny numerical deviations
    return max(-1.0, min(1.0, cost))


# ============================================================
# EvtGen-like EvtDecayAngleChi
#
# This follows EvtGen's actual implementation:
#
# 1. Boost all particles to parent rest frame
# 2. D = d1 + d2
# 3. Remove the D-direction component from d1 and h1
# 4. Construct d1' = D x d1_perp
# 5. chi = atan2(d1' . h1_perp, d1_perp . h1_perp)
#
# EvtGen returns chi in [0, 2*pi].
# ============================================================

def evt_decay_angle_chi(P, d1, d2, h1, h2):

    # --------------------------------------------------------
    # Boost to parent rest frame
    # --------------------------------------------------------

    boost = -P.BoostVector()

    d1p = ROOT.TLorentzVector(d1)
    d2p = ROOT.TLorentzVector(d2)
    h1p = ROOT.TLorentzVector(h1)
    h2p = ROOT.TLorentzVector(h2)

    d1p.Boost(boost)
    d2p.Boost(boost)
    h1p.Boost(boost)
    h2p.Boost(boost)

    # --------------------------------------------------------
    # D = d1 + d2
    # --------------------------------------------------------

    D = d1p + d2p

    Dvec = D.Vect()

    # --------------------------------------------------------
    # Remove component of d1 along D
    #
    # d1_perp =
    # d1 - (D . d1 / D . D) D
    #
    # This is exactly what EvtGen does.
    # --------------------------------------------------------

    DdotD = Dvec.Dot(Dvec)

    if DdotD == 0:
        return float("nan")

    d1vec = d1p.Vect()
    h1vec = h1p.Vect()

    d1_perp = (
        d1vec
        - (Dvec.Dot(d1vec) / DdotD) * Dvec
    )

    h1_perp = (
        h1vec
        - (Dvec.Dot(h1vec) / DdotD) * Dvec
    )

    # --------------------------------------------------------
    # d1' = D x d1_perp
    # --------------------------------------------------------

    d1_prime = Dvec.Cross(d1_perp)

    d1_perp_mag = d1_perp.Mag()
    d1_prime_mag = d1_prime.Mag()

    if d1_perp_mag == 0 or d1_prime_mag == 0:
        return float("nan")

    d1_perp *= 1.0 / d1_perp_mag
    d1_prime *= 1.0 / d1_prime_mag

    # --------------------------------------------------------
    # EvtGen:
    #
    # x = d1_perp . h1_perp
    # y = d1_prime . h1_perp
    # --------------------------------------------------------

    x = d1_perp.Dot(h1_perp)
    y = d1_prime.Dot(h1_perp)

    angle = math.atan2(y, x)

    # EvtGen converts [-pi, pi] -> [0, 2pi]
    if angle < 0:
        angle += 2.0 * math.pi

    return angle


# ============================================================
# Event loop
# ============================================================

nentries = tree.GetEntries()

print("Number of events:", nentries)

for i in range(nentries):

    tree.GetEntry(i)

    # --------------------------------------------------------
    # Construct four-vectors from your ntuple
    # --------------------------------------------------------

    Dstar = ROOT.TLorentzVector(
        tree.Dsp_sl_px,
        tree.Dsp_sl_py,
        tree.Dsp_sl_pz,
        tree.Dsp_sl_E
    )

    D0 = ROOT.TLorentzVector(
        tree.D0_sl_px,
        tree.D0_sl_py,
        tree.D0_sl_pz,
        tree.D0_sl_E
    )

    pion = ROOT.TLorentzVector(
        tree.pip_slow_px,
        tree.pip_slow_py,
        tree.pip_slow_pz,
        tree.pip_slow_E
    )

    lepton = ROOT.TLorentzVector(
        tree.lm_sl_px,
        tree.lm_sl_py,
        tree.lm_sl_pz,
        tree.lm_sl_E
    )

    neutrino = ROOT.TLorentzVector(
        tree.nu_sl_px,
        tree.nu_sl_py,
        tree.nu_sl_pz,
        tree.nu_sl_E
    )


    # ========================================================
    # Construct B and q
    # ========================================================

    q = lepton + neutrino

    B = Dstar + q


    # ========================================================
    # 1. q^2
    #
    # Same as:
    #
    # EvtVector4R q = l1 + l2;
    # double q2 = q.mass2();
    # ========================================================

    q2_value = q.M2()


    # ========================================================
    # 2. cos(theta_D*)
    #
    # Same as:
    #
    # EvtDecayAngle(b, dstar, k)
    #
    # b     = B
    # dstar = D*
    # k     = D0
    # ========================================================

    ctd_value = evt_decay_angle(
        B,
        Dstar,
        D0
    )


    # ========================================================
    # 3. cos(theta_l)
    #
    # Same as:
    #
    # EvtDecayAngle(b, q, l1)
    #
    # b  = B
    # q  = l + nu
    # l1 = charged lepton
    # ========================================================

    ctl_value = evt_decay_angle(
        B,
        q,
        lepton
    )


    # ========================================================
    # 4. chi
    #
    # Same as:
    #
    # EvtDecayAngleChi(
    #     b,
    #     k,
    #     pi,
    #     l1,
    #     l2
    # )
    #
    # k  = D0
    # pi = slow pion
    # l1 = lepton
    # l2 = neutrino
    # ========================================================

    chi_value = evt_decay_angle_chi(
        B,
        D0,
        pion,
        lepton,
        neutrino
    )


    # ========================================================
    # Store
    # ========================================================

    q2.clear()
    ctd.clear()
    ctl.clear()
    chi.clear()

    q2.push_back(q2_value)
    ctd.push_back(ctd_value)
    ctl.push_back(ctl_value)
    chi.push_back(chi_value)

    outtree.Fill()


# ============================================================
# Write
# ============================================================

fout.cd()
outtree.Write()

fout.Close()
fin.Close()


print()
print("==============================================")
print("Finished")
print("==============================================")
print("Input :", input_file)
print("Output:", output_file)
print("Tree  :", tree_name)
print()
print("Variables:")
print("  q2")
print("  ctd")
print("  ctl")
print("  chi")
print("==============================================")