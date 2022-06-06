from psychopy import visual, core, event, monitors, sound, parallel
from random import shuffle, sample
import os
import pyfiglet
import numpy as np
import pandas as pd
from datetime import datetime as dt
from fx.addOutput import addOutput, initCSV
from oddball import *
from calibration import *
from ratings import *
try: 
    import u3
    from fx.LJTickDAC import LJTickDAC
except:
    print('no labjack detected, likely in debug mode on a laptop')

# Run task
os.system('cls')
print(pyfiglet.figlet_format("EFFPAIN STUDY"))
ID     = input('Please enter the SUBJECT ID NUMBER: ')
AGE    = input("Please enter the subject's AGE: ")
SEX    = input("Please enter the subject's SEX: ")
DEBUG  = eval(input("Is it DEBUG mode (True/False)? "))

print('Good luck!')

# Window setup
WINSIZE     = [1920, 1080] #if not DEBUG else [1920//1.5, 1080//1.5]
WINFULL     = True #if not DEBUG else False
WINGUI      = False if not DEBUG else True
WIN         = visual.Window(size=WINSIZE, fullscr=WINFULL,allowGUI=WINGUI, allowStencil=False,monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',  blendMode='avg', useFBO=True, units='cm')

# Calibrate pain
out, V_, maxV            = runCalibration(WIN, props=(.1,.9), debug=DEBUG)
calibration_data         = pd.DataFrame(out).T.reset_index(level=0)
calibration_data['PID']  = ID
calibration_data.columns = ['V', 'rating', 'PID']
calibration_data.to_csv(f'data/calibration/calibration_{ID}.csv')

print('='*10)
print(f'Max tolerane = {maxV}V')
print(f'Volts to use in experimenters = {V_}')
print('='*10)

# Rate pain values
ratings              = runRating(WIN, V_, DEBUG)
ratings_data         = pd.DataFrame(ratings)
ratings_data['PID']  = ID
ratings_data.columns = ['V', 'rating', 'PID']
ratings_data.to_csv(f'data/calibration/rating_{ID}.csv')

print('='*10)
print('rating data saved.')
print('='*10)

# Run oddball
runTask(WIN, ID, SEX, AGE, V_, DEBUG)

# Exit
core.quit()





