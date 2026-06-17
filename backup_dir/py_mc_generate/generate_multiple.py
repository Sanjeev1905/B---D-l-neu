import subprocess

for x in range(0, 180):
	command = "python3 generate_mc_full_range.py && mkdir np_samples_full_range"+str(x)+" && mv sm_B2Kstarll_mumu *np_mumu_* np_samples_full_range"+str(x)
	subprocess.call(command, shell=True)
