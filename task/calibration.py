from psychopy import visual, core, event, monitors, sound, parallel
import pandas as pd
import numpy as np
from datetime import datetime as dt
try: 
	import u3
	from fx.LJTickDAC import LJTickDAC
except: 
	pass

def runCalibration(WIN, props=(0.1, 0.9), debug=False):
	"""
	Runs the pain calibration phase: ramp up

	@WIN  :  Window on which task is displayed (psychopy.visual.window)
	@props:  Proportion of max voltages to return for next part of experiment
	@debug:  Debug mode (True or False)

	returns: tuple of:  
		- dictionary of ratings for each voltages
		- voltages to use in experiment (props[i] * maxV)
		- maximum voltage subject can tolerate
	"""

	# Set constants 
	INTENSITIES = [i/100 for i in list(range(1,200))]    # voltage ramp (0.01V to 2V)
	COOLDOWN    = 2                                      # cooldown time after shock
	PAINTIME    = 0.33                                   # time for which signal is sent

	# Initialize trial components
	INSTDIR     = 'instructions/calibration_instructions/'
	INSTPIC     = visual.ImageStim(WIN, image=f"{INSTDIR}Slide1.png")
	SHOCKBOLT   = visual.ImageStim(WIN, image='stim/bolt.png', pos=(0,0), size=(10,10))
	TXT         = visual.TextStim(WIN, text='If you think you can tolerate the next shock, tell the experimenter to continue.\n\n\nIf you think you cannot tolerate the next shock, tell the experimenter to stop here.', height=1, pos=(0,0), color='White', wrapWidth=30)
	MIN, MAX    = 0, 20
	SLIDER      = visual.RatingScale(WIN, low=MIN, high=MAX, markerStart=(MIN+MAX)/2, 
		tickHeight=0, textColor='white', scale=None, showValue=False, lineColor='white', markerColor='DarkRed', 
		labels=['Not Painful', 'Very Painful'], 
		acceptPreText = '<- or ->', 
		acceptText = 'Press ENTER')
	
        # Specify ports and connect to labjack 
	if not debug:
                DEV  = u3.U3()
                DEV.configIO(FIOAnalog=0x0F)
                TDAC = LJTickDAC(DEV, 4, 500.)
                TDAC.update(0, 0) # off
                PORT, PORTNUM = parallel.ParallelPort(address='0xEFF8'), 16
        

    #--------------------------------------Start Task-----------------------------------------
	# Show instructions
	INSTCOUNTER = 1
	while INSTCOUNTER<4:
		INSTPIC.image = f'{INSTDIR}Slide{INSTCOUNTER}.png'
		INSTPIC.draw()
		WIN.flip()
		key_press  = event.waitKeys(keyList=['left', 'right'])
		if key_press[0]=='left':
		    INSTCOUNTER -= 1
		    if INSTCOUNTER<1: INSTCOUNTER=1
		else:
		    INSTCOUNTER += 1

	WIN.flip()
	output = {}
	for t, V in enumerate(INTENSITIES):
		SHOCKBOLT.draw()
		WIN.flip()
                # Give shock
		if debug:
			print(f'adminstered shock of {V}V')
		else:
                        TDAC.update(V, 0) # on
                        PORT.setData(PORTNUM)
                        core.wait(PAINTIME)
                        TDAC.update(0,0)     # off
                        PORT.setData(0)
		core.wait(COOLDOWN)

		# Rating
		while SLIDER.noResponse:
			SLIDER.draw()
			WIN.flip()
		pain_rating = SLIDER.getRating()

		SLIDER.reset()

		# save
		output[V] = [pain_rating]

		# Confirm next
		TXT.draw()
		WIN.flip()
		key_press = event.waitKeys(keyList=['return', 'x', 'escape'])
		if 'escape' in key_press:
			core.quit()

		if 'x' in key_press:
                        # subject's stopping point
                        break

		WIN.flip()
		core.wait(COOLDOWN)
		
	V_ = [round(p*V,2) for p in props]
	return output, V_, V






