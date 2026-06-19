import sys
from cProfile import label
import os
from re import sub
#from turtle import color, title   # removed on 17/06 to get rid of it's dependency
import uproot as ur
import numpy as np
import pandas as pd
import subprocess
import glob
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sts
import itertools
from sklearn.preprocessing import MinMaxScaler
import h5py

np.random.seed(42)

def c9_val_getter(subdirectory):
    files_and_folders = os.listdir(subdirectory)

    for filename in files_and_folders:
        if filename.endswith(".txt"):
            f = open(subdirectory+filename, "r") # read saved delta C_9 value
            c9_val = f.read()
            return c9_val.strip()
        else:
            continue

def ctk_binner50(row):
    k = -998
    if -1.0 <= row['ctk'] < -0.96:
        k = int(0)
    elif -0.96 <= row['ctk'] < -0.92:
        k = int(1)
    elif -0.92 <= row['ctk'] < -0.88:
        k = int(2)
    elif -0.88 <= row['ctk'] < -0.84:
        k = int(3)
    elif -0.84 <= row['ctk'] < -0.8:
        k = int(4)
    elif -0.8 <= row['ctk'] < -0.76:
        k = int(5)
    elif -0.76 <= row['ctk'] < -0.72:
        k = int(6)
    elif -0.72 <= row['ctk'] < -0.68:
        k = int(7)
    elif -0.68 <= row['ctk'] < -0.64:
        k = int(8)
    elif -0.64 <= row['ctk'] < -0.6:
        k = int(9)
    elif -0.6 <= row['ctk'] < -0.56:
        k = int(10)
    elif -0.56 <= row['ctk'] < -0.52:
        k = int(11)
    elif -0.52 <= row['ctk'] < -0.48:
        k = int(12)
    elif -0.48 <= row['ctk'] < -0.44:
        k = int(13)
    elif -0.44 <= row['ctk'] < -0.4:
        k = int(14)
    elif -0.4 <= row['ctk'] < -0.36:
        k = int(15)
    elif -0.36 <= row['ctk'] < -0.32:
        k = int(16)
    elif -0.32 <= row['ctk'] < -0.28:
        k = int(17)
    elif -0.28 <= row['ctk'] < -0.24:
        k = int(18)
    elif -0.24 <= row['ctk'] < -0.2:
        k = int(19)
    elif -0.2 <= row['ctk'] < -0.16:
        k = int(20)
    elif -0.16 <= row['ctk'] < -0.12:
        k = int(21)
    elif -0.12 <= row['ctk'] < -0.08:
        k = int(22)
    elif -0.08 <= row['ctk'] < -0.04:
        k = int(23)
    elif -0.04 <= row['ctk'] < 0.0:
        k = int(24)
    elif 0.0 <= row['ctk'] < 0.04:
        k = int(25)
    elif 0.04 <= row['ctk'] < 0.08:
        k = int(26)
    elif 0.08 <= row['ctk'] < 0.12:
        k = int(27)
    elif 0.12 <= row['ctk'] < 0.16:
        k = int(28)
    elif 0.16 <= row['ctk'] < 0.2:
        k = int(29)
    elif 0.2 <= row['ctk'] < 0.24:
        k = int(30)
    elif 0.24 <= row['ctk'] < 0.28:
        k = int(31)
    elif 0.28 <= row['ctk'] < 0.32:
        k = int(32)
    elif 0.32 <= row['ctk'] < 0.36:
        k = int(33)
    elif 0.36 <= row['ctk'] < 0.4:
        k = int(34)
    elif 0.4 <= row['ctk'] < 0.44:
        k = int(35)
    elif 0.44 <= row['ctk'] < 0.48:
        k = int(36)
    elif 0.48 <= row['ctk'] < 0.52:
        k = int(37)
    elif 0.52 <= row['ctk'] < 0.56:
        k = int(38)
    elif 0.56 <= row['ctk'] < 0.6:
        k = int(39)
    elif 0.6 <= row['ctk'] < 0.64:
        k = int(40)
    elif 0.64 <= row['ctk'] < 0.68:
        k = int(41)
    elif 0.68 <= row['ctk'] < 0.72:
        k = int(42)
    elif 0.72 <= row['ctk'] < 0.76:
        k = int(43)
    elif 0.76 <= row['ctk'] < 0.8:
        k = int(44)
    elif 0.8 <= row['ctk'] < 0.84:
        k = int(45)
    elif 0.84 <= row['ctk'] < 0.88:
        k = int(46)
    elif 0.88 <= row['ctk'] < 0.92:
        k = int(47)
    elif 0.92 <= row['ctk'] < 0.96:
        k = int(48)
    elif 0.96 <= row['ctk'] <= 1.0:
        k = int(49)
    return k

def ctl_binner50(row):
    k = -997
    if -1.0 <= row['ctl'] < -0.96:
        k = int(0)
    elif -0.96 <= row['ctl'] < -0.92:
        k = int(1)
    elif -0.92 <= row['ctl'] < -0.88:
        k = int(2)
    elif -0.88 <= row['ctl'] < -0.84:
        k = int(3)
    elif -0.84 <= row['ctl'] < -0.8:
        k = int(4)
    elif -0.8 <= row['ctl'] < -0.76:
        k = int(5)
    elif -0.76 <= row['ctl'] < -0.72:
        k = int(6)
    elif -0.72 <= row['ctl'] < -0.68:
        k = int(7)
    elif -0.68 <= row['ctl'] < -0.64:
        k = int(8)
    elif -0.64 <= row['ctl'] < -0.6:
        k = int(9)
    elif -0.6 <= row['ctl'] < -0.56:
        k = int(10)
    elif -0.56 <= row['ctl'] < -0.52:
        k = int(11)
    elif -0.52 <= row['ctl'] < -0.48:
        k = int(12)
    elif -0.48 <= row['ctl'] < -0.44:
        k = int(13)
    elif -0.44 <= row['ctl'] < -0.4:
        k = int(14)
    elif -0.4 <= row['ctl'] < -0.36:
        k = int(15)
    elif -0.36 <= row['ctl'] < -0.32:
        k = int(16)
    elif -0.32 <= row['ctl'] < -0.28:
        k = int(17)
    elif -0.28 <= row['ctl'] < -0.24:
        k = int(18)
    elif -0.24 <= row['ctl'] < -0.2:
        k = int(19)
    elif -0.2 <= row['ctl'] < -0.16:
        k = int(20)
    elif -0.16 <= row['ctl'] < -0.12:
        k = int(21)
    elif -0.12 <= row['ctl'] < -0.08:
        k = int(22)
    elif -0.08 <= row['ctl'] < -0.04:
        k = int(23)
    elif -0.04 <= row['ctl'] < 0.0:
        k = int(24)
    elif 0.0 <= row['ctl'] < 0.04:
        k = int(25)
    elif 0.04 <= row['ctl'] < 0.08:
        k = int(26)
    elif 0.08 <= row['ctl'] < 0.12:
        k = int(27)
    elif 0.12 <= row['ctl'] < 0.16:
        k = int(28)
    elif 0.16 <= row['ctl'] < 0.2:
        k = int(29)
    elif 0.2 <= row['ctl'] < 0.24:
        k = int(30)
    elif 0.24 <= row['ctl'] < 0.28:
        k = int(31)
    elif 0.28 <= row['ctl'] < 0.32:
        k = int(32)
    elif 0.32 <= row['ctl'] < 0.36:
        k = int(33)
    elif 0.36 <= row['ctl'] < 0.4:
        k = int(34)
    elif 0.4 <= row['ctl'] < 0.44:
        k = int(35)
    elif 0.44 <= row['ctl'] < 0.48:
        k = int(36)
    elif 0.48 <= row['ctl'] < 0.52:
        k = int(37)
    elif 0.52 <= row['ctl'] < 0.56:
        k = int(38)
    elif 0.56 <= row['ctl'] < 0.6:
        k = int(39)
    elif 0.6 <= row['ctl'] < 0.64:
        k = int(40)
    elif 0.64 <= row['ctl'] < 0.68:
        k = int(41)
    elif 0.68 <= row['ctl'] < 0.72:
        k = int(42)
    elif 0.72 <= row['ctl'] < 0.76:
        k = int(43)
    elif 0.76 <= row['ctl'] < 0.8:
        k = int(44)
    elif 0.8 <= row['ctl'] < 0.84:
        k = int(45)
    elif 0.84 <= row['ctl'] < 0.88:
        k = int(46)
    elif 0.88 <= row['ctl'] < 0.92:
        k = int(47)
    elif 0.92 <= row['ctl'] < 0.96:
        k = int(48)
    elif 0.96 <= row['ctl'] <= 1.0:
        k = int(49)
    return k

def chi_binner50(row):
    k = -999
    if 0.0 <= row['chi'] < 0.02:
        k = int(0)
    elif 0.02 <= row['chi'] < 0.04:
        k = int(1)
    elif 0.04 <= row['chi'] < 0.06:
        k = int(2)
    elif 0.06 <= row['chi'] < 0.08:
        k = int(3)
    elif 0.08 <= row['chi'] < 0.1:
        k = int(4)
    elif 0.1 <= row['chi'] < 0.12:
        k = int(5)
    elif 0.12 <= row['chi'] < 0.14:
        k = int(6)
    elif 0.14 <= row['chi'] < 0.16:
        k = int(7)
    elif 0.16 <= row['chi'] < 0.18:
        k = int(8)
    elif 0.18 <= row['chi'] < 0.2:
        k = int(9)
    elif 0.2 <= row['chi'] < 0.22:
        k = int(10)
    elif 0.22 <= row['chi'] < 0.24:
        k = int(11)
    elif 0.24 <= row['chi'] < 0.26:
        k = int(12)
    elif 0.26 <= row['chi'] < 0.28:
        k = int(13)
    elif 0.28 <= row['chi'] < 0.3:
        k = int(14)
    elif 0.3 <= row['chi'] < 0.32:
        k = int(15)
    elif 0.32 <= row['chi'] < 0.34:
        k = int(16)
    elif 0.34 <= row['chi'] < 0.36:
        k = int(17)
    elif 0.36 <= row['chi'] < 0.38:
        k = int(18)
    elif 0.38 <= row['chi'] < 0.4:
        k = int(19)
    elif 0.4 <= row['chi'] < 0.42:
        k = int(20)
    elif 0.42 <= row['chi'] < 0.44:
        k = int(21)
    elif 0.44 <= row['chi'] < 0.46:
        k = int(22)
    elif 0.46 <= row['chi'] < 0.48:
        k = int(23)
    elif 0.48 <= row['chi'] < 0.5:
        k = int(24)
    elif 0.5 <= row['chi'] < 0.52:
        k = int(25)
    elif 0.52 <= row['chi'] < 0.54:
        k = int(26)
    elif 0.54 <= row['chi'] < 0.56:
        k = int(27)
    elif 0.56 <= row['chi'] < 0.58:
        k = int(28)
    elif 0.58 <= row['chi'] < 0.6:
        k = int(29)
    elif 0.6 <= row['chi'] < 0.62:
        k = int(30)
    elif 0.62 <= row['chi'] < 0.64:
        k = int(31)
    elif 0.64 <= row['chi'] < 0.66:
        k = int(32)
    elif 0.66 <= row['chi'] < 0.68:
        k = int(33)
    elif 0.68 <= row['chi'] < 0.7:
        k = int(34)
    elif 0.7 <= row['chi'] < 0.72:
        k = int(35)
    elif 0.72 <= row['chi'] < 0.74:
        k = int(36)
    elif 0.74 <= row['chi'] < 0.76:
        k = int(37)
    elif 0.76 <= row['chi'] < 0.78:
        k = int(38)
    elif 0.78 <= row['chi'] < 0.8:
        k = int(39)
    elif 0.8 <= row['chi'] < 0.82:
        k = int(40)
    elif 0.82 <= row['chi'] < 0.84:
        k = int(41)
    elif 0.84 <= row['chi'] < 0.86:
        k = int(42)
    elif 0.86 <= row['chi'] < 0.88:
        k = int(43)
    elif 0.88 <= row['chi'] < 0.9:
        k = int(44)
    elif 0.9 <= row['chi'] < 0.92:
        k = int(45)
    elif 0.92 <= row['chi'] < 0.94:
        k = int(46)
    elif 0.94 <= row['chi'] < 0.96:
        k = int(47)
    elif 0.96 <= row['chi'] < 0.98:
        k = int(48)
    elif 0.98 <= row['chi'] <= 1.0:
        k = int(49)
    return k

def ctk_binner100(row):
    k = -998
    if -1.0 <= row['ctk'] < -0.98:
        k = int(0)
    elif -0.98 < row['ctk'] < -0.96:
        k = int(1)
    elif -0.96 < row['ctk'] < -0.94:
        k = int(2)
    elif -0.94 < row['ctk'] < -0.92:
        k = int(3)
    elif -0.92 < row['ctk'] < -0.9:
        k = int(4)
    elif -0.9 < row['ctk'] < -0.88:
        k = int(5)
    elif -0.88 < row['ctk'] < -0.86:
        k = int(6)
    elif -0.86 < row['ctk'] < -0.84:
        k = int(7)
    elif -0.84 < row['ctk'] < -0.8200000000000001:
        k = int(8)
    elif -0.8200000000000001 < row['ctk'] < -0.8:
        k = int(9)
    elif -0.8 < row['ctk'] < -0.78:
        k = int(10)
    elif -0.78 < row['ctk'] < -0.76:
        k = int(11)
    elif -0.76 < row['ctk'] < -0.74:
        k = int(12)
    elif -0.74 < row['ctk'] < -0.72:
        k = int(13)
    elif -0.72 < row['ctk'] < -0.7:
        k = int(14)
    elif -0.7 < row['ctk'] < -0.6799999999999999:
        k = int(15)
    elif -0.6799999999999999 < row['ctk'] < -0.6599999999999999:
        k = int(16)
    elif -0.6599999999999999 < row['ctk'] < -0.64:
        k = int(17)
    elif -0.64 < row['ctk'] < -0.62:
        k = int(18)
    elif -0.62 < row['ctk'] < -0.6:
        k = int(19)
    elif -0.6 < row['ctk'] < -0.5800000000000001:
        k = int(20)
    elif -0.5800000000000001 < row['ctk'] < -0.56:
        k = int(21)
    elif -0.56 < row['ctk'] < -0.54:
        k = int(22)
    elif -0.54 < row['ctk'] < -0.52:
        k = int(23)
    elif -0.52 < row['ctk'] < -0.5:
        k = int(24)
    elif -0.5 < row['ctk'] < -0.48:
        k = int(25)
    elif -0.48 < row['ctk'] < -0.45999999999999996:
        k = int(26)
    elif -0.45999999999999996 < row['ctk'] < -0.43999999999999995:
        k = int(27)
    elif -0.43999999999999995 < row['ctk'] < -0.42000000000000004:
        k = int(28)
    elif -0.42000000000000004 < row['ctk'] < -0.4:
        k = int(29)
    elif -0.4 < row['ctk'] < -0.38:
        k = int(30)
    elif -0.38 < row['ctk'] < -0.36:
        k = int(31)
    elif -0.36 < row['ctk'] < -0.33999999999999997:
        k = int(32)
    elif -0.33999999999999997 < row['ctk'] < -0.31999999999999995:
        k = int(33)
    elif -0.31999999999999995 < row['ctk'] < -0.29999999999999993:
        k = int(34)
    elif -0.29999999999999993 < row['ctk'] < -0.28:
        k = int(35)
    elif -0.28 < row['ctk'] < -0.26:
        k = int(36)
    elif -0.26 < row['ctk'] < -0.24:
        k = int(37)
    elif -0.24 < row['ctk'] < -0.21999999999999997:
        k = int(38)
    elif -0.21999999999999997 < row['ctk'] < -0.19999999999999996:
        k = int(39)
    elif -0.19999999999999996 < row['ctk'] < -0.17999999999999994:
        k = int(40)
    elif -0.17999999999999994 < row['ctk'] < -0.16000000000000003:
        k = int(41)
    elif -0.16000000000000003 < row['ctk'] < -0.14:
        k = int(42)
    elif -0.14 < row['ctk'] < -0.12:
        k = int(43)
    elif -0.12 < row['ctk'] < -0.09999999999999998:
        k = int(44)
    elif -0.09999999999999998 < row['ctk'] < -0.07999999999999996:
        k = int(45)
    elif -0.07999999999999996 < row['ctk'] < -0.05999999999999994:
        k = int(46)
    elif -0.05999999999999994 < row['ctk'] < -0.040000000000000036:
        k = int(47)
    elif -0.040000000000000036 < row['ctk'] < -0.020000000000000018:
        k = int(48)
    elif -0.020000000000000018 < row['ctk'] < 0.0:
        k = int(49)
    elif 0.0 < row['ctk'] < 0.020000000000000018:
        k = int(50)
    elif 0.020000000000000018 < row['ctk'] < 0.040000000000000036:
        k = int(51)
    elif 0.040000000000000036 < row['ctk'] < 0.06000000000000005:
        k = int(52)
    elif 0.06000000000000005 < row['ctk'] < 0.08000000000000007:
        k = int(53)
    elif 0.08000000000000007 < row['ctk'] < 0.10000000000000009:
        k = int(54)
    elif 0.10000000000000009 < row['ctk'] < 0.1200000000000001:
        k = int(55)
    elif 0.1200000000000001 < row['ctk'] < 0.14000000000000012:
        k = int(56)
    elif 0.14000000000000012 < row['ctk'] < 0.15999999999999992:
        k = int(57)
    elif 0.15999999999999992 < row['ctk'] < 0.17999999999999994:
        k = int(58)
    elif 0.17999999999999994 < row['ctk'] < 0.19999999999999996:
        k = int(59)
    elif 0.19999999999999996 < row['ctk'] < 0.21999999999999997:
        k = int(60)
    elif 0.21999999999999997 < row['ctk'] < 0.24:
        k = int(61)
    elif 0.24 < row['ctk'] < 0.26:
        k = int(62)
    elif 0.26 < row['ctk'] < 0.28:
        k = int(63)
    elif 0.28 < row['ctk'] < 0.30000000000000004:
        k = int(64)
    elif 0.30000000000000004 < row['ctk'] < 0.32000000000000006:
        k = int(65)
    elif 0.32000000000000006 < row['ctk'] < 0.3400000000000001:
        k = int(66)
    elif 0.3400000000000001 < row['ctk'] < 0.3600000000000001:
        k = int(67)
    elif 0.3600000000000001 < row['ctk'] < 0.3800000000000001:
        k = int(68)
    elif 0.3800000000000001 < row['ctk'] < 0.40000000000000013:
        k = int(69)
    elif 0.40000000000000013 < row['ctk'] < 0.41999999999999993:
        k = int(70)
    elif 0.41999999999999993 < row['ctk'] < 0.43999999999999995:
        k = int(71)
    elif 0.43999999999999995 < row['ctk'] < 0.45999999999999996:
        k = int(72)
    elif 0.45999999999999996 < row['ctk'] < 0.48:
        k = int(73)
    elif 0.48 < row['ctk'] < 0.5:
        k = int(74)
    elif 0.5 < row['ctk'] < 0.52:
        k = int(75)
    elif 0.52 < row['ctk'] < 0.54:
        k = int(76)
    elif 0.54 < row['ctk'] < 0.56:
        k = int(77)
    elif 0.56 < row['ctk'] < 0.5800000000000001:
        k = int(78)
    elif 0.5800000000000001 < row['ctk'] < 0.6000000000000001:
        k = int(79)
    elif 0.6000000000000001 < row['ctk'] < 0.6200000000000001:
        k = int(80)
    elif 0.6200000000000001 < row['ctk'] < 0.6400000000000001:
        k = int(81)
    elif 0.6400000000000001 < row['ctk'] < 0.6600000000000001:
        k = int(82)
    elif 0.6600000000000001 < row['ctk'] < 0.6799999999999999:
        k = int(83)
    elif 0.6799999999999999 < row['ctk'] < 0.7:
        k = int(84)
    elif 0.7 < row['ctk'] < 0.72:
        k = int(85)
    elif 0.72 < row['ctk'] < 0.74:
        k = int(86)
    elif 0.74 < row['ctk'] < 0.76:
        k = int(87)
    elif 0.76 < row['ctk'] < 0.78:
        k = int(88)
    elif 0.78 < row['ctk'] < 0.8:
        k = int(89)
    elif 0.8 < row['ctk'] < 0.8200000000000001:
        k = int(90)
    elif 0.8200000000000001 < row['ctk'] < 0.8400000000000001:
        k = int(91)
    elif 0.8400000000000001 < row['ctk'] < 0.8600000000000001:
        k = int(92)
    elif 0.8600000000000001 < row['ctk'] < 0.8800000000000001:
        k = int(93)
    elif 0.8800000000000001 < row['ctk'] < 0.9000000000000001:
        k = int(94)
    elif 0.9000000000000001 < row['ctk'] < 0.9199999999999999:
        k = int(95)
    elif 0.9199999999999999 < row['ctk'] < 0.94:
        k = int(96)
    elif 0.94 < row['ctk'] < 0.96:
        k = int(97)
    elif 0.96 < row['ctk'] < 0.98:
        k = int(98)
    elif 0.98 < row['ctk'] <= 1.0:
        k = int(99)
    return k

def ctl_binner100(row):
    k = -997
    if -1.0 <= row['ctl'] < -0.98:
        k = int(0)
    elif -0.98 < row['ctl'] < -0.96:
        k = int(1)
    elif -0.96 < row['ctl'] < -0.94:
        k = int(2)
    elif -0.94 < row['ctl'] < -0.92:
        k = int(3)
    elif -0.92 < row['ctl'] < -0.9:
        k = int(4)
    elif -0.9 < row['ctl'] < -0.88:
        k = int(5)
    elif -0.88 < row['ctl'] < -0.86:
        k = int(6)
    elif -0.86 < row['ctl'] < -0.84:
        k = int(7)
    elif -0.84 < row['ctl'] < -0.8200000000000001:
        k = int(8)
    elif -0.8200000000000001 < row['ctl'] < -0.8:
        k = int(9)
    elif -0.8 < row['ctl'] < -0.78:
        k = int(10)
    elif -0.78 < row['ctl'] < -0.76:
        k = int(11)
    elif -0.76 < row['ctl'] < -0.74:
        k = int(12)
    elif -0.74 < row['ctl'] < -0.72:
        k = int(13)
    elif -0.72 < row['ctl'] < -0.7:
        k = int(14)
    elif -0.7 < row['ctl'] < -0.6799999999999999:
        k = int(15)
    elif -0.6799999999999999 < row['ctl'] < -0.6599999999999999:
        k = int(16)
    elif -0.6599999999999999 < row['ctl'] < -0.64:
        k = int(17)
    elif -0.64 < row['ctl'] < -0.62:
        k = int(18)
    elif -0.62 < row['ctl'] < -0.6:
        k = int(19)
    elif -0.6 < row['ctl'] < -0.5800000000000001:
        k = int(20)
    elif -0.5800000000000001 < row['ctl'] < -0.56:
        k = int(21)
    elif -0.56 < row['ctl'] < -0.54:
        k = int(22)
    elif -0.54 < row['ctl'] < -0.52:
        k = int(23)
    elif -0.52 < row['ctl'] < -0.5:
        k = int(24)
    elif -0.5 < row['ctl'] < -0.48:
        k = int(25)
    elif -0.48 < row['ctl'] < -0.45999999999999996:
        k = int(26)
    elif -0.45999999999999996 < row['ctl'] < -0.43999999999999995:
        k = int(27)
    elif -0.43999999999999995 < row['ctl'] < -0.42000000000000004:
        k = int(28)
    elif -0.42000000000000004 < row['ctl'] < -0.4:
        k = int(29)
    elif -0.4 < row['ctl'] < -0.38:
        k = int(30)
    elif -0.38 < row['ctl'] < -0.36:
        k = int(31)
    elif -0.36 < row['ctl'] < -0.33999999999999997:
        k = int(32)
    elif -0.33999999999999997 < row['ctl'] < -0.31999999999999995:
        k = int(33)
    elif -0.31999999999999995 < row['ctl'] < -0.29999999999999993:
        k = int(34)
    elif -0.29999999999999993 < row['ctl'] < -0.28:
        k = int(35)
    elif -0.28 < row['ctl'] < -0.26:
        k = int(36)
    elif -0.26 < row['ctl'] < -0.24:
        k = int(37)
    elif -0.24 < row['ctl'] < -0.21999999999999997:
        k = int(38)
    elif -0.21999999999999997 < row['ctl'] < -0.19999999999999996:
        k = int(39)
    elif -0.19999999999999996 < row['ctl'] < -0.17999999999999994:
        k = int(40)
    elif -0.17999999999999994 < row['ctl'] < -0.16000000000000003:
        k = int(41)
    elif -0.16000000000000003 < row['ctl'] < -0.14:
        k = int(42)
    elif -0.14 < row['ctl'] < -0.12:
        k = int(43)
    elif -0.12 < row['ctl'] < -0.09999999999999998:
        k = int(44)
    elif -0.09999999999999998 < row['ctl'] < -0.07999999999999996:
        k = int(45)
    elif -0.07999999999999996 < row['ctl'] < -0.05999999999999994:
        k = int(46)
    elif -0.05999999999999994 < row['ctl'] < -0.040000000000000036:
        k = int(47)
    elif -0.040000000000000036 < row['ctl'] < -0.020000000000000018:
        k = int(48)
    elif -0.020000000000000018 < row['ctl'] < 0.0:
        k = int(49)
    elif 0.0 < row['ctl'] < 0.020000000000000018:
        k = int(50)
    elif 0.020000000000000018 < row['ctl'] < 0.040000000000000036:
        k = int(51)
    elif 0.040000000000000036 < row['ctl'] < 0.06000000000000005:
        k = int(52)
    elif 0.06000000000000005 < row['ctl'] < 0.08000000000000007:
        k = int(53)
    elif 0.08000000000000007 < row['ctl'] < 0.10000000000000009:
        k = int(54)
    elif 0.10000000000000009 < row['ctl'] < 0.1200000000000001:
        k = int(55)
    elif 0.1200000000000001 < row['ctl'] < 0.14000000000000012:
        k = int(56)
    elif 0.14000000000000012 < row['ctl'] < 0.15999999999999992:
        k = int(57)
    elif 0.15999999999999992 < row['ctl'] < 0.17999999999999994:
        k = int(58)
    elif 0.17999999999999994 < row['ctl'] < 0.19999999999999996:
        k = int(59)
    elif 0.19999999999999996 < row['ctl'] < 0.21999999999999997:
        k = int(60)
    elif 0.21999999999999997 < row['ctl'] < 0.24:
        k = int(61)
    elif 0.24 < row['ctl'] < 0.26:
        k = int(62)
    elif 0.26 < row['ctl'] < 0.28:
        k = int(63)
    elif 0.28 < row['ctl'] < 0.30000000000000004:
        k = int(64)
    elif 0.30000000000000004 < row['ctl'] < 0.32000000000000006:
        k = int(65)
    elif 0.32000000000000006 < row['ctl'] < 0.3400000000000001:
        k = int(66)
    elif 0.3400000000000001 < row['ctl'] < 0.3600000000000001:
        k = int(67)
    elif 0.3600000000000001 < row['ctl'] < 0.3800000000000001:
        k = int(68)
    elif 0.3800000000000001 < row['ctl'] < 0.40000000000000013:
        k = int(69)
    elif 0.40000000000000013 < row['ctl'] < 0.41999999999999993:
        k = int(70)
    elif 0.41999999999999993 < row['ctl'] < 0.43999999999999995:
        k = int(71)
    elif 0.43999999999999995 < row['ctl'] < 0.45999999999999996:
        k = int(72)
    elif 0.45999999999999996 < row['ctl'] < 0.48:
        k = int(73)
    elif 0.48 < row['ctl'] < 0.5:
        k = int(74)
    elif 0.5 < row['ctl'] < 0.52:
        k = int(75)
    elif 0.52 < row['ctl'] < 0.54:
        k = int(76)
    elif 0.54 < row['ctl'] < 0.56:
        k = int(77)
    elif 0.56 < row['ctl'] < 0.5800000000000001:
        k = int(78)
    elif 0.5800000000000001 < row['ctl'] < 0.6000000000000001:
        k = int(79)
    elif 0.6000000000000001 < row['ctl'] < 0.6200000000000001:
        k = int(80)
    elif 0.6200000000000001 < row['ctl'] < 0.6400000000000001:
        k = int(81)
    elif 0.6400000000000001 < row['ctl'] < 0.6600000000000001:
        k = int(82)
    elif 0.6600000000000001 < row['ctl'] < 0.6799999999999999:
        k = int(83)
    elif 0.6799999999999999 < row['ctl'] < 0.7:
        k = int(84)
    elif 0.7 < row['ctl'] < 0.72:
        k = int(85)
    elif 0.72 < row['ctl'] < 0.74:
        k = int(86)
    elif 0.74 < row['ctl'] < 0.76:
        k = int(87)
    elif 0.76 < row['ctl'] < 0.78:
        k = int(88)
    elif 0.78 < row['ctl'] < 0.8:
        k = int(89)
    elif 0.8 < row['ctl'] < 0.8200000000000001:
        k = int(90)
    elif 0.8200000000000001 < row['ctl'] < 0.8400000000000001:
        k = int(91)
    elif 0.8400000000000001 < row['ctl'] < 0.8600000000000001:
        k = int(92)
    elif 0.8600000000000001 < row['ctl'] < 0.8800000000000001:
        k = int(93)
    elif 0.8800000000000001 < row['ctl'] < 0.9000000000000001:
        k = int(94)
    elif 0.9000000000000001 < row['ctl'] < 0.9199999999999999:
        k = int(95)
    elif 0.9199999999999999 < row['ctl'] < 0.94:
        k = int(96)
    elif 0.94 < row['ctl'] < 0.96:
        k = int(97)
    elif 0.96 < row['ctl'] < 0.98:
        k = int(98)
    elif 0.98 < row['ctl'] <= 1.0:
        k = int(99)
    return k

def chi_binner100(row):
    k = -999
    if 0.0 <= row['chi'] < 0.01:
        k = int(0)
    elif 0.01 < row['chi'] < 0.02:
        k = int(1)
    elif 0.02 < row['chi'] < 0.03:
        k = int(2)
    elif 0.03 < row['chi'] < 0.04:
        k = int(3)
    elif 0.04 < row['chi'] < 0.05:
        k = int(4)
    elif 0.05 < row['chi'] < 0.06:
        k = int(5)
    elif 0.06 < row['chi'] < 0.07:
        k = int(6)
    elif 0.07 < row['chi'] < 0.08:
        k = int(7)
    elif 0.08 < row['chi'] < 0.09:
        k = int(8)
    elif 0.09 < row['chi'] < 0.1:
        k = int(9)
    elif 0.1 < row['chi'] < 0.11:
        k = int(10)
    elif 0.11 < row['chi'] < 0.12:
        k = int(11)
    elif 0.12 < row['chi'] < 0.13:
        k = int(12)
    elif 0.13 < row['chi'] < 0.14:
        k = int(13)
    elif 0.14 < row['chi'] < 0.15:
        k = int(14)
    elif 0.15 < row['chi'] < 0.16:
        k = int(15)
    elif 0.16 < row['chi'] < 0.17:
        k = int(16)
    elif 0.17 < row['chi'] < 0.18:
        k = int(17)
    elif 0.18 < row['chi'] < 0.19:
        k = int(18)
    elif 0.19 < row['chi'] < 0.2:
        k = int(19)
    elif 0.2 < row['chi'] < 0.21:
        k = int(20)
    elif 0.21 < row['chi'] < 0.22:
        k = int(21)
    elif 0.22 < row['chi'] < 0.23:
        k = int(22)
    elif 0.23 < row['chi'] < 0.24:
        k = int(23)
    elif 0.24 < row['chi'] < 0.25:
        k = int(24)
    elif 0.25 < row['chi'] < 0.26:
        k = int(25)
    elif 0.26 < row['chi'] < 0.27:
        k = int(26)
    elif 0.27 < row['chi'] < 0.28:
        k = int(27)
    elif 0.28 < row['chi'] < 0.29:
        k = int(28)
    elif 0.29 < row['chi'] < 0.3:
        k = int(29)
    elif 0.3 < row['chi'] < 0.31:
        k = int(30)
    elif 0.31 < row['chi'] < 0.32:
        k = int(31)
    elif 0.32 < row['chi'] < 0.33:
        k = int(32)
    elif 0.33 < row['chi'] < 0.34:
        k = int(33)
    elif 0.34 < row['chi'] < 0.35000000000000003:
        k = int(34)
    elif 0.35000000000000003 < row['chi'] < 0.36:
        k = int(35)
    elif 0.36 < row['chi'] < 0.37:
        k = int(36)
    elif 0.37 < row['chi'] < 0.38:
        k = int(37)
    elif 0.38 < row['chi'] < 0.39:
        k = int(38)
    elif 0.39 < row['chi'] < 0.4:
        k = int(39)
    elif 0.4 < row['chi'] < 0.41000000000000003:
        k = int(40)
    elif 0.41000000000000003 < row['chi'] < 0.42:
        k = int(41)
    elif 0.42 < row['chi'] < 0.43:
        k = int(42)
    elif 0.43 < row['chi'] < 0.44:
        k = int(43)
    elif 0.44 < row['chi'] < 0.45:
        k = int(44)
    elif 0.45 < row['chi'] < 0.46:
        k = int(45)
    elif 0.46 < row['chi'] < 0.47000000000000003:
        k = int(46)
    elif 0.47000000000000003 < row['chi'] < 0.48:
        k = int(47)
    elif 0.48 < row['chi'] < 0.49:
        k = int(48)
    elif 0.49 < row['chi'] < 0.5:
        k = int(49)
    elif 0.5 < row['chi'] < 0.51:
        k = int(50)
    elif 0.51 < row['chi'] < 0.52:
        k = int(51)
    elif 0.52 < row['chi'] < 0.53:
        k = int(52)
    elif 0.53 < row['chi'] < 0.54:
        k = int(53)
    elif 0.54 < row['chi'] < 0.55:
        k = int(54)
    elif 0.55 < row['chi'] < 0.56:
        k = int(55)
    elif 0.56 < row['chi'] < 0.5700000000000001:
        k = int(56)
    elif 0.5700000000000001 < row['chi'] < 0.58:
        k = int(57)
    elif 0.58 < row['chi'] < 0.59:
        k = int(58)
    elif 0.59 < row['chi'] < 0.6:
        k = int(59)
    elif 0.6 < row['chi'] < 0.61:
        k = int(60)
    elif 0.61 < row['chi'] < 0.62:
        k = int(61)
    elif 0.62 < row['chi'] < 0.63:
        k = int(62)
    elif 0.63 < row['chi'] < 0.64:
        k = int(63)
    elif 0.64 < row['chi'] < 0.65:
        k = int(64)
    elif 0.65 < row['chi'] < 0.66:
        k = int(65)
    elif 0.66 < row['chi'] < 0.67:
        k = int(66)
    elif 0.67 < row['chi'] < 0.68:
        k = int(67)
    elif 0.68 < row['chi'] < 0.6900000000000001:
        k = int(68)
    elif 0.6900000000000001 < row['chi'] < 0.7000000000000001:
        k = int(69)
    elif 0.7000000000000001 < row['chi'] < 0.71:
        k = int(70)
    elif 0.71 < row['chi'] < 0.72:
        k = int(71)
    elif 0.72 < row['chi'] < 0.73:
        k = int(72)
    elif 0.73 < row['chi'] < 0.74:
        k = int(73)
    elif 0.74 < row['chi'] < 0.75:
        k = int(74)
    elif 0.75 < row['chi'] < 0.76:
        k = int(75)
    elif 0.76 < row['chi'] < 0.77:
        k = int(76)
    elif 0.77 < row['chi'] < 0.78:
        k = int(77)
    elif 0.78 < row['chi'] < 0.79:
        k = int(78)
    elif 0.79 < row['chi'] < 0.8:
        k = int(79)
    elif 0.8 < row['chi'] < 0.81:
        k = int(80)
    elif 0.81 < row['chi'] < 0.8200000000000001:
        k = int(81)
    elif 0.8200000000000001 < row['chi'] < 0.8300000000000001:
        k = int(82)
    elif 0.8300000000000001 < row['chi'] < 0.84:
        k = int(83)
    elif 0.84 < row['chi'] < 0.85:
        k = int(84)
    elif 0.85 < row['chi'] < 0.86:
        k = int(85)
    elif 0.86 < row['chi'] < 0.87:
        k = int(86)
    elif 0.87 < row['chi'] < 0.88:
        k = int(87)
    elif 0.88 < row['chi'] < 0.89:
        k = int(88)
    elif 0.89 < row['chi'] < 0.9:
        k = int(89)
    elif 0.9 < row['chi'] < 0.91:
        k = int(90)
    elif 0.91 < row['chi'] < 0.92:
        k = int(91)
    elif 0.92 < row['chi'] < 0.93:
        k = int(92)
    elif 0.93 < row['chi'] < 0.9400000000000001:
        k = int(93)
    elif 0.9400000000000001 < row['chi'] < 0.9500000000000001:
        k = int(94)
    elif 0.9500000000000001 < row['chi'] < 0.96:
        k = int(95)
    elif 0.96 < row['chi'] < 0.97:
        k = int(96)
    elif 0.97 < row['chi'] < 0.98:
        k = int(97)
    elif 0.98 < row['chi'] < 0.99:
        k = int(98)
    elif 0.99 < row['chi'] <= 1.0:
        k = int(99)
    return k


def import_data_and_prepare_for_cnn_images(particle_file, anti_particle_file):
    # Written 09/05/2023

    # convert to Pandas dataframes
    particle_array = particle_file.arrays(library="pd")
    particle_array_reduced = particle_array.copy()

    # scale q2 and chi values
    min_max_scaler = MinMaxScaler()

    particle_array_reduced[["q2", "chi"]] = min_max_scaler.fit_transform(particle_array_reduced[["q2", "chi"]])

    # select only relevant vars
    particle_array_reduced_vars = particle_array_reduced[["q2", "ctk", "ctl", "chi"]]

    df = particle_array_reduced_vars
  
    return df
   
def binAngularData2(df):

    # bin angular data
    df["X"] = df.apply(ctl_binner50, axis=1)
    df["Y"] = df.apply(ctk_binner50, axis=1)
    df["Z"] = df.apply(chi_binner50, axis=1)

    # take average q2; added 11/14/2022
    df_U = df.groupby(['X', 'Y', 'Z'])['q2'].mean().reset_index()

    #return df
    return df_U

def binCTL(df):
    df["X"] = df.apply(ctl_binner, axis=1)
    return df

def binCTK(df):
    df["Y"] = df.apply(ctk_binner, axis=1)
    return df

def binCHI(df):
    df["Z"] = df.apply(chi_binner, axis=1)
    return df

def generateImages(df, nevents, delta_C9):

    np_voxels = []
    np_voxels_labels = []

    # get number of voxel grids
    n_voxel_grids = int(len(df.index)/nevents)
    
    # Generate images for training for different Belle II integrated luminosities
    for x in range(1, n_voxel_grids+1):
        # generate empty image
        voxelgrid_np = np.zeros((50,50,50))
        
        df_np_reduced = df.iloc[(x - 1) * nevents: x * nevents].copy()
        df_np_reduced_binned = binAngularData2(df_np_reduced)

        for X, Y, Z, Q2 in zip(df_np_reduced_binned["X"], df_np_reduced_binned["Y"], df_np_reduced_binned["Z"], df_np_reduced_binned["q2"]):
            if X >= 0 and Y >= 0 and Z >= 0:
                voxelgrid_np[X][Y][Z] += Q2
            else:
                continue
        
        np_voxels.append(voxelgrid_np)
        np_voxels_labels.append(delta_C9)

    # store images in dataframe
    df_images = pd.DataFrame({"image":np_voxels, "delta_C9":np_voxels_labels})
    df_images_shuffled = df_images.sample(frac=1)
    
    np_voxels = []
    np_voxels_labels = []
    number_of_events = []
    del df_images

    return df_images_shuffled

def writeToNPY(df, label, sample):
    for index, row in df.iterrows():
        array = row
        if sample < 47: # Change these if you need to, according to your own MC generation campaigns
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/test/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        elif sample >= 47 and sample <= 188:
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/train/train/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        elif sample >=189 and sample < 225:
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/train/val/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        else:
            raise Exception("Error!  Sample out of generated range!")

def writeToNPY_interpolated(df, label, sample):
    for index, row in df.iterrows():
        array = row
        if sample < 45:
            np.save('path_to/interpolated_test/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        else:
            raise Exception("Error!  Sample out of generated range!")

def writeToNPY_extrapolated(df, label, sample):
    for index, row in df.iterrows():
        array = row
        if sample < 45:
            np.save('path_to/npy_files/extrapolated_test/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        else:
            raise Exception("Error!  Sample out of generated range!")

def writeToNPY_positive(df, label, sample):
    for index, row in df.iterrows():
        array = row
        if sample < 36:
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/test/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        elif sample >= 36 and sample <= 152:
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/train/train/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        elif sample >= 153 and sample < 180:
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/train/val/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'.npy', array)
        else:
            raise Exception("Error!  Sample out of generated range!")

def writeToNPY_upper_half(df, label, sample):
    for index, row in df.iterrows():
        array = row
        if sample < 18:
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/train/val/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'_upper_half.npy', array)
        elif sample >= 18 and sample < 90:
            np.save('/home/sanjeev/myAnalysis/btokstarll_resnet/npy_files/train/train/images_delta_C9_'+label+'_sample'+str(sample)+'_'+str(index)+'_upper_half.npy', array)
        else:
            raise Exception("Error!  Sample out of generated range!")
