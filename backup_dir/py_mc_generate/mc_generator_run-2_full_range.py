# can update the number of events from here

import random
import subprocess
import os
from pathlib import Path

def getSeed():
    seed = random.randint(1, 1234567890)
    return seed

particles = ["B0", "anti-B0"]

for parent_dir in os.listdir("."):

    if not parent_dir.startswith("np_mumu"):
        continue

    for subdir, dirs, files in os.walk(parent_dir):

        for dec_file in files:

            if dec_file.endswith(".dec"):

                seed = getSeed()
                fileStem = Path(str(dec_file)).stem
                filepath = os.path.join(subdir, dec_file)

                if "anti-B0" in fileStem:
                    particle = "anti-B0"
                else:
                    particle = "B0"

                # run generator
                command = (
                    "../../cpp/mc_generator/run_bb_kstarll "
                    "-n 50000 "
                    "-u " + str(filepath) +
                    " -o " + "c9_" + particle + "_" +
                    str(fileStem) + "_lab.root -s " +
                    str(seed)
                )

                command2 = (
                    "mv " +
                    "c9_" + particle + "_" +
                    str(fileStem) + "_lab.root " +
                    str(subdir) + "/"
                )

                subprocess.call(command, shell=True)
                subprocess.call(command2, shell=True)

            else:
                continue

#######################
