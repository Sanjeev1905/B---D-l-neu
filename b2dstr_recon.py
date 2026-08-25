import basf2 as b2
import modularAnalysis as ma
import variables.utils as vu
from variables import variables as vm
import vertex as vx

analysis_gt = ma.getAnalysisGlobaltag()
# b2.B2INFO(f'Appending analysis GT: {analysis_gt}')
b2.conditions.append_globaltag("Legacy_CollisionAxisCMS")
b2.conditions.append_globaltag(analysis_gt)

main = b2.Path()
outVars = []

tag = "mu"
inRootFile = f"np_000_047_600.root"
outRootFile = f"reco_000_047_600.root"
#inRootFile = f"dstarlnu_hp.root"
#outRootFile = f"dstarlnu_hp_h.root"
#inRootFile = f"/group/belle2/users2022/purwar/B2Dslnu/dataFiles/B2Ds{tag}nu_SM_1k_wBkg.root"
#outRootFile = f"b2ds{tag}nu_gen_SM_1k.root"
#inRootFile = f"/group/belle2/users2022/purwar/B2Dslnu/dataFiles/B2Ds{tag}nu_SM2_1k_wBkg.root"
#outRootFile = f"b2ds{tag}nu_gen_SM2_1k.root"
# inRootFile = f"/group/belle2/users2022/purwar/B2Dslnu/dataFiles/B2Ds{tag}nu_NPs3_1k_wBkg.root"
# outRootFile = f"b2ds{tag}nu_gen_NPs3_1k.root"

FSPs = ["K-:sl","pi+:sl",f"anti-nu_{tag}:sl",f"{tag}-:sl"]
nonFSPs = ["D0:sl","D*+:sl","anti-B0:sl"]


decayStr = "anti-B0:sl -> [D*+:sl -> [D0:sl -> K-:sl pi+:sl] pi+:slow]" + f' {tag}-:sl anti-nu_{tag}:sl'
print("Decay String: "+ decayStr)

printSummaryOfList=True

ma.inputMdst(environmentType='default', filename=inRootFile, path=main)

for pl in FSPs:
    ma.fillParticleListFromMC(pl, cut='', path=main)
if printSummaryOfList:
    ma.summaryOfLists(FSPs, path=main)

ma.copyList("pi+:slow","pi+:sl",path=main)

decayList = ["D0:sl -> K-:sl pi+:sl","D*+:sl -> D0:sl pi+:slow","anti-B0:sl -> D*+:sl" + f" {tag}-:sl anti-nu_{tag}:sl"]
print('Decay List: {}'.format(decayList))

for i,d in enumerate(decayList):
    ma.reconstructMCDecay(d, '', path=main)
    if printSummaryOfList:
        ma.summaryOfLists(nonFSPs[i], path=main)

listVars1 = ['M','InvM','dr','dz','dM','mcPDG','pt','E','p','px','py','pz']
listVars2 = listVars1 + ['isSignal','Q']
listVars3 = listVars2 + ['Mbc','deltaE']

outVars += vu.create_aliases_for_selected(listVars1+['kaonID','pionID'], f"anti-B0:sl -> [D*+:sl -> [D0:sl -> ^K-:sl ^pi+:sl] ^pi+:slow] {tag}-:sl ^anti-nu_{tag}:sl", prefix=['Km_sl','pip_sl','pip_slow','nu_sl'])
outVars += vu.create_aliases_for_selected(listVars2, f"anti-B0:sl -> [^D*+:sl -> [^D0:sl -> K-:sl pi+:sl] pi+:slow] ^{tag}-:sl anti-nu_{tag}:sl", prefix=['Dsp_sl','D0_sl','lm_sl'])

outVars += listVars3
outVars += ['chiProb','mcErrors']

ma.variablesToNtuple(nonFSPs[-1], outVars, path=main, treename = 'antiB0', filename=outRootFile)

b2.process(main)
