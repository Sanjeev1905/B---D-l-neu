import uproot as ur
from otherfunctions import *
import time
import os
startTime = time.time()

integrated_luminosity = [250] # /ab
#nevents =  [24613]
nevents = [2460]
samples = range(47, 125)
#samples = [56, 10, 200]

for sample in samples:
    # loop through subdirectories to produce templates for each value of \delta C9
    base_dir = "../mc_generator/np_mumu" + str(sample)
    subdirs = [d for d in os.listdir(base_dir)if os.path.isdir(os.path.join(base_dir, d))]
    print(len(subdirs))
    subdirs.remove("sm_B2Kstarll_mumu")
    for subdir in subdirs:
        particle_np_file = ur.open("../mc_generator/np_mumu"+str(sample)+"/"+subdir+"/c9_B0_np_B2Kstarll_B0_"+subdir[3:]+"_lab.root:ntp")
        anti_particle_np_file = ur.open("../mc_generator/np_mumu"+str(sample)+"/"+subdir+"/c9_anti-B0_np_B2Kstarll_anti-B0_"+subdir[3:]+"_lab.root:ntp")

        df = import_data_and_prepare_for_cnn_images(particle_np_file, anti_particle_np_file)
        df_shuffled = df.sample(frac=1)

        delta_C9 = c9_val_getter("../mc_generator/np_mumu"+str(sample)+"/"+subdir+"/")

        for NEVTS, LINT in zip(nevents, integrated_luminosity):
            df_images_shuffled = generateImages(df_shuffled, NEVTS, float(delta_C9))
            df_images_shuffled_recast = df_images_shuffled.astype({'delta_C9':'float16'})
            writeToNPY(df_images_shuffled_recast, delta_C9, sample)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
