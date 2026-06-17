# Generates EvtGen .dec files for B2Kstarll physics using A. Sibidanov's new generator BTOSLLNP
# Currently only tested on KEKCC

import numpy as np
import subprocess

# generate range of WC values
step_values = np.linspace(-2.0, 0.0, 21)
values = np.array(step_values)

# append known WC values of interst
values = np.append(values, [-0.87, -0.40])

other_values = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1]

vals = np.append(values, other_values)

#for num1, num2 in zip(values[::2], values[1::2]):
#	interp = (num1 + num2)/2
#	vals.append(interp)

#leptons = ["ee", "mumu"]

leptons = ["mumu"]

flavors = ["B0", "anti-B0"]

sample = 56

parent_dir = "np_mumu" + str(sample)

subprocess.call("mkdir -p " + parent_dir, shell=True)

# generate decay files line by line
for lepton in leptons:
	command = "mkdir -p " + parent_dir + "/sm_B2Kstarll_" + lepton
	subprocess.call(command, shell=True)
	for flavor in flavors:
		if flavor == "B0":
			line = "1.000 anti-B0 B0                           VSS;\n"
		elif flavor == "anti-B0":
			line = "1.000 B0 anti-B0                           VSS;\n"
		else:
			print("ERROR!  B-MESON FLAVOR NOT GIVEN!\n")

		if lepton == "mumu":
			lines = ["# need to turn off mixing to prevent B0 from becoming an anti-B0\n", 
				"Define dm_incohMix_B0 0.0\n", 
				"\n",
				"Decay Upsilon(4S)\n",
				line,
				"Enddecay\n\n",
				"Decay anti-B0\n", 
				"1.000 anti-K*0 mu+ mu- BTOSLLNP;\n", 
				"Enddecay\n", 
				"\n", 
				"Decay B0\n", 
				"1.000 K*0 mu+ mu- BTOSLLNP;\n", 
				"Enddecay\n", 
				"\n",
				"Decay anti-K*0\n",
				"1.000 K- pi+ VSS;\n",
				"Enddecay\n",
				"\n",
				"Decay K*0\n",
				"1.000 K+ pi- VSS;\n",
				"Enddecay\n",
				"\n",
				"End"]
		elif lepton == "ee":
			lines = ["# need to turn off mixing to prevent B0 from becoming an anti-B0\n", 
				"Define dm_incohMix_B0 0.0\n", 
				"\n", 
				"Decay Upsilon(4S)\n",
				line,
				"Enddecay\n\n",
				"Decay anti-B0\n", 
				"1.000 anti-K*0 e+ e- BTOSLLNP;\n", 
				"Enddecay\n", 
				"\n", 
				"Decay B0\n", 
				"1.000 K*0 e+ e- BTOSLLNP;\n",
				"Enddecay\n", 
				"\n",
				"Decay anti-K*0\n",
				"1.000 K- pi+ VSS;\n",
				"Enddecay\n",
				"\n",
				"Decay K*0\n",
				"1.000 K+ pi- VSS;\n",
				"Enddecay\n",
				"\n",
				"End"]

		f_sm = open("sm_B2Kstarll_"+flavor+"_"+lepton+".dec", "w+")
	
		for line in lines:
			f_sm.write(line)

		f_sm.close()

		command2 = (
    			"mv sm_B2Kstarll_" + flavor + "_" + lepton +
   			 ".dec " + parent_dir + "/sm_B2Kstarll_" + lepton
			)
		subprocess.call(command2, shell=True)

for lepton in leptons:
	for value in vals:
		# convert WC value to folder and file name string; p = point/decimal point
		left = int(str(value).split(".")[0])
		right = str(value).split(".")[1]

		if left > 0:
			wc_label =  str(left)+"p"+right
		elif left < 0 or left == 0:
			wc_label =  "n"+str(abs(left))+"p"+right
		else:
			wc_label = str(left)+"p"+right
		command3 = "mkdir -p " + parent_dir + "/np_"+lepton+"_"+wc_label
		subprocess.call(command3, shell=True)
		for flavor in flavors:
			if flavor == "B0":
				line = "1.000 anti-B0 B0                           VSS;\n"
			elif flavor == "anti-B0":
				line = "1.000 B0 anti-B0                           VSS;\n"
			else:
				print("ERROR!  B-MESON FLAVOR NOT GIVEN!\n")

			if lepton == "mumu":
				lines = ["# delta C_9 = "+str(value)+"\n",
					"# need to turn off mixing to prevent B0 from becoming an anti-B0\n", 
					"Define dm_incohMix_B0 0.0\n", 
					"\n",
					"Decay Upsilon(4S)\n",
					line,
					"Enddecay\n\n",   
					"Decay anti-B0\n", 
					"1.000 anti-K*0 mu+ mu- BTOSLLNP 0 1 "+str(value)+" 0.0;\n", 
					"Enddecay\n", 
					"\n",   
					"Decay B0\n", 
					"1.000 K*0 mu+ mu- BTOSLLNP 0 1 "+str(value)+" 0.0;\n", 
					"Enddecay\n", 
					"\n",
					"Decay anti-K*0\n",
					"1.000 K- pi+ VSS;\n",
					"Enddecay\n",
					"\n",
					"Decay K*0\n",
					"1.000 K+ pi- VSS;\n",
					"Enddecay\n",
					"\n",   
					"End"]
			elif lepton == "ee":
				lines = ["# delta C_9 = "+str(value)+"\n",
					"# need to turn off mixing to prevent B0 from becoming an anti-B0\n",
					"Define dm_incohMix_B0 0.0\n",
					"\n",
					"Decay Upsilon(4S)\n",
					line,
					"Enddecay\n\n",
					"Decay anti-B0\n",
					"1.000 anti-K*0 e+ e- BTOSLLNP 0 1 "+str(value)+" 0.0;\n",
					"Enddecay\n",
					"\n",
					"Decay B0\n",
					"1.000 K*0 e+ e- BTOSLLNP 0 1 "+str(value)+" 0.0;\n",
					"Enddecay\n",
					"\n",
					"Decay anti-K*0\n",
					"1.000 K- pi+ VSS;\n",
					"Enddecay\n",
					"\n",
					"Decay K*0\n",
					"1.000 K+ pi- VSS;\n",
					"Enddecay\n",
					"\n",
					"End"]
	
			f_np = open("np_B2Kstarll_"+flavor+"_"+lepton+"_"+wc_label+".dec", "w+")

			for line in lines:
				f_np.write(line)

			f_np.close()

			f_np_value = open("np_B2Kstarll_"+lepton+"_"+wc_label+".txt", "w+")
			f_np_value.write(str(value))
			f_np_value.close()

			command4 = (
    				"mv " +
	  			"np_B2Kstarll_" + flavor + "_" + lepton + "_" + wc_label + ".dec " +
				"np_B2Kstarll_" + lepton + "_" + wc_label + ".txt " +
    				parent_dir + "/np_" + lepton + "_" + wc_label
)
			subprocess.call(command4, shell=True)
