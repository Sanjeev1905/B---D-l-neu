#!/usr/bin/env python3
# BF of B to D* mu nu ~ `5%`

import basf2 as b2
import modularAnalysis as ma
import sys
import stdV0s
import variables.collections as vc
import variables.utils as vu
import variables.collections as vc
from variables import variables as vm
# from variables_module import Variables
import argparse
import glob
import os
import vertex as vx



# analysis_gt = ma.getAnalysisGlobaltag()
# b2.conditions.append_globaltag("Legacy_CollisionAxisCMS")
# b2.conditions.append_globaltag(analysis_gt)

main = b2.create_path()

isSignal = True
tag = "mu"
# If input file, we enter in testing mode
inRootFile = "np_10k.root"
outRootFile = "np_10k_var.root"

#input
ma.inputMdst(environmentType="default",filename=inRootFile, path=main)

# add alias
vm.addAlias('goodTrack_slow','passesCut(abs(dr) < 2 and abs(dz)< 4 and useCMSFrame(p) < 0.40 and thetaInCDCAcceptance)')  # good slow tracks
vm.addAlias('goodTracks','passesCut(abs(dr)< 2 and abs(dz)< 4 and thetaInCDCAcceptance)') 
# # kaon, pion and muon cuts
vm.addAlias('goodKaons','passesCut(goodTracks and kaonID > 0.1 )')  # good kaons:sl
vm.addAlias('goodPions','passesCut(goodTracks and pionID > 0.1 )')
vm.addAlias('goodPions_slow','passesCut(goodTrack_slow and pionID > 0.1)')
# vm.addAlias('goodMuons','passesCut(goodTracks and muonID > 0.9)')
vm.addAlias('goodMuons','passesCut(goodTracks and muonID>0.9 and inKLMAcceptance and useCMSFrame(p) >0.6 )')  # good muons:sl


# supress Bhabha scattering
# ma.appyEventCuts('[nTracks >= 3]', path=main)


# ma.fillParticleList("K-:sl", cut= "goodKaons  ", path=main)
# ma.fillParticleList("pi+:sl", cut= "goodPions ", path=main)
# ma.fillParticleList(f"{tag}-:sl", cut="goodTracks and goodMMuons", path=main)
# ma.fillParticleList("pi+:slow",cut="goodPions",path=main)
ma.fillParticleList("K-:sl", cut= "goodKaons", path=main)
ma.fillParticleList("pi+:sl", cut= "goodPions", path=main)
ma.fillParticleList(f"{tag}-:sl", cut="goodTracks and goodMuons", path=main)
ma.fillParticleList("pi+:slow",cut="goodPions_slow",path=main)

# cuts for roe
trackBasedCuts = 'thetaInCDCAcceptance and pt>0.1 and dr<5 and abs(dz)<10'
eclBasedCuts = 'thetaInCDCAcceptance and E > 0.05'

# slow pions listed
# ma.copyList("pi+:slow", "pi+:sl",cut="p < 0.40", path=main) # slow pion cut to be explored further

ma.buildEventKinematics(inputListNames = None, path = main)

ma.reconstructDecay("D0:sl -> K-:sl pi+:sl",  cut="1.835 < M < 1.885", path=main) 
# ma.reconstructDecay('D0:sl -> K-:sl pi+:sl', cut="", path=main)

ma.matchMCTruth("D0:sl", path=main)

ma.reconstructDecay("D*+:sl -> D0:sl pi+:slow",  cut="0.141 < massDifference(0) < 0.156 ", path=main)
# ma.reconstructDecay("D*+:sl -> D0:sl pi+:slow",  cut=" ", path=main)

ma.matchMCTruth("D*+:sl", path=main)

reco_str = '?nu'

# if charged_lepton=='e-': reco_str += '?addbrems'

ma.reconstructDecay(
    f"anti-B0:sl -> D*+:sl {tag}-:sl {reco_str}",  cut="", path=main
    # f"anti-B0:sl -> D*+:sl {tag}-:sl {reco_str}",  cut="Mbc > 5.27 and abs(deltaE) < 0.5", path=main
)

ma.matchMCTruth("anti-B0:sl", path=main)

# vx.treeFit(
#     "anti-B0:sl", conf_level=0.001, updateAllDaughters=False, ipConstraint=True, path=main
# )
  
if isSignal:
    ma.applyCuts("anti-B0:sl", "isSignalAcceptMissing == 1", path=main)


# https://software.belle2.org/latest-light/sphinx/online_book/basf2/roe.html
ma.buildRestOfEvent("anti-B0:sl", fillWithMostLikely=True, path=main) 

# ma.appendROEMask("anti-B0:sl", "myMask",trackBasedCuts, eclBasedCuts, path=main)

# tree fit
# vx.treeFit("anti-B0:sl", conf_level=0.001, path=main)

# Setting all vars
missing_mass_vars= ['missingMomentumOfEvent', 'missingMass2OfEvent', 'genMissingMass2OfEvent', 'recMissM2', 'recQ2BhSimple', 'recQ2Bh'] # ,'weQ2lnu'
event_variables  = ['Ecms', 'EcmsMC']

standard_vars    = vc.kinematics + vc.mc_kinematics 
standard_vars   += vu.create_aliases( vc.kinematics,    "useCMSFrame({variable})" , "CMS")
standard_vars   += vu.create_aliases( vc.mc_kinematics, "useCMSFrame({variable})" , "CMS")
standard_vars    = vu.create_aliases_for_selected(standard_vars, f"^anti-B0:sl -> [^D*+:sl -> [^D0:sl -> K-:sl pi+:sl] pi+:sl] ^{tag}-:sl")


mc_truth         = vc.mc_truth  + ['isSignalAcceptMissingMassive', 'isSignalAcceptMissing', 'genMotherID', 'genMotherPDG', 'mcInitial']
mc_truth         += vu.create_aliases_for_selected(mc_truth, f"^anti-B0:sl -> [^D*+:sl -> [^D0:sl -> K-:sl pi+:sl] pi+:sl] ^{tag}-:sl")

final_state_vars = ['dr', 'dz', 'theta', 'phi', 'p']
final_state_vars = vu.create_aliases_for_selected(final_state_vars, f"anti-B0:sl -> [D*+:sl -> [D0:sl -> ^K-:sl ^pi+:sl] ^pi+:sl] ^{tag}-:sl")

roe_kinematics = vu.create_aliases( ["roePx()", "roePy()", "roePz()", "roeE()", "roeM()", "roeMbc()"], 
                                   "useCMSFrame({variable})" , "CMS")
roe_kinematics += vu.create_aliases( ["roePx(myMask)", "roePy(myMask)", "roePz(myMask)", "roeE(myMask)", "roeM(myMask)", "roeMbc(myMask)"], 
                                   "useCMSFrame({variable})" , "CMS")

all_vars         = standard_vars + mc_truth + final_state_vars  + event_variables 




ma.variablesToNtuple(
    "anti-B0:sl",
    variables=all_vars,
    filename=outRootFile,
    treename="all_vars",
    path=main,
)

b2.process(main)
print(b2.statistics)
