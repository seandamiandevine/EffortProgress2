import os
import webbrowser as web
import pyfiglet
import pandas as pd 
from glob import glob
from warnings import warn
import shutil

print(pyfiglet.figlet_format("EFFPROG STUDY"))
ID     = input('Please enter the SUBJECT ID NUMBER: ')
AGE    = input("Please enter the subject's AGE: ")
SEX    = input("Please enter the subject's SEX: ")
DEBUG  = input("Is it DEBUG mode (true/false)? ")

_data = 'var tmp = \'[{"ID" : "' + ID + '", "AGE" : "'+AGE+'", "SEX" : "'+SEX+'", "DEBUG" : "'+DEBUG+'"} ]\'';

with open('tmp.js', 'w') as f:
    f.write(_data)

web.open('file://' + os.path.realpath('index.html'))

print('='*20)
input('EXPERIMENTER: Press ENTER when experiment is done.')

# remove tmp 
os.remove('tmp.js')

# get data file
HOME = os.path.expanduser('~')
file = [f for f in glob(f'{HOME}/Downloads/*.csv') if f'oddball_{ID}_' in f]

if len(file) > 1:
    warn('Warning: more than one data file found with same ID. Using one of them, but double check Downloads folder to be safe.')
    file = file[-1]
else: 
    file = file[0]

# print earnings
sub      = pd.read_csv(file)
earnings = sub.totalTokens.max()

print('='*20)
print(f'Pay subject a bonus of ${earnings}')

# move file to data/
print('='*20)
try: 
    shutil.move(file, file.replace(f'{HOME}/Downloads/', 'data/'))
    print('data successfully moved to data/ folder')
except:
    print('could not move data to data/ folder. Check manually.')



