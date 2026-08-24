#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

import basf2 as b2
import simulation as si
import reconstruction as re
import mdst as mdst
import glob as glob

parser = argparse.ArgumentParser()
parser.add_argument("events", type=int, help="Number of events to generate")
parser.add_argument("dec_file", type=str, help="Decay file to use for event generation")
parser.add_argument("root_file", type=str, help="Output root file name")

args = parser.parse_args()


# background (collision) files
bg = glob.glob('/group/belle2/dataprod/BGOverlay/early_phase3/release-06-00-05/overlay/BGx1/set0/*.root')
# background if running locally
bg_local = glob.glob('/group/belle2/dataprod/BGOverlay/early_phase3/release-06-00-05/overlay/BGx1/set0/*.root')

# set database conditions (in addition to default)
b2.conditions.prepend_globaltag("mc_production_MC15ri_a")

# create path
main = b2.Path()

# default to early phase 3 (exp=1003), run 0
main.add_module("EventInfoSetter", expList=1003, runList=0, evtNumList= args.events)

# generate events from decfile
#main.add_module('EvtGenInput', userDECFile=b2.find_file('B0B0bar_dstarlnu_hp.dec'))
main.add_module('EvtGenInput', userDECFile=b2.find_file(args.dec_file))

# detector simulation
si.add_simulation(path=main, bkgfiles=bg)

# reconstruction
re.add_reconstruction(path=main)

# Finally add mdst output (file name overwritten on the grid)
mdst.add_mdst_output(path=main, filename=args.root_file)

# process events and print call statistics
b2.process(path=main)
print(b2.statistics)
