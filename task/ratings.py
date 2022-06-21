from psychopy import visual, core, event, monitors, sound, parallel
import pandas as pd
import numpy as np
from random import shuffle
try: 
	import u3
	from fx.LJTickDAC import LJTickDAC
except: 
	pass

def runRating(WIN, voltages, debug=False):
	"""
	Runs the pain calibration phase: ratings

	@WIN  :  Window on which task is displayed (psychopy.visual.window)
	@props:  Voltages to use (from first calibration phase)
	@debug:  Debug mode (True or False)

	returns: dictionary of voltages and ratings
	"""

	# Set constants 
	NUM_REPS    = 3 if not debug else 1     # number of times each intensity is rated
	COOLDOWN    = 2     					# cooldown time after shock
	PAINTIME    = 0.33  					# time for which signal is sent
	VLIST       = [v for v in voltages for i in range(NUM_REPS)]
	shuffle(VLIST)    

	# Initialize trial components
	INSTDIR     = 'instructions/rating_instructions/'
	INSTPIC     = visual.ImageStim(WIN, image=f"{INSTDIR}Slide1.png")
	SHOCKBOLT   = visual.ImageStim(WIN, image='stim/bolt.png', pos=(0,0), size=(.525,.75))
	TXT         = visual.TextStim(WIN, text='Press ENTER to continue to rate the next shock.', height=.1, pos=(0,0), color='White', wrapWidth=20*0.1)
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
	while INSTCOUNTER<2:
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
	core.wait(COOLDOWN)
	ratings = np.zeros(len(VLIST))
	for t, V in enumerate(VLIST):

		# Confirm next
		TXT.draw()
		WIN.flip()
		key_press = event.waitKeys(keyList=['return', 'escape'])
		if 'escape' in key_press:
			core.quit()

		WIN.flip()
		core.wait(COOLDOWN)

                # Give shock
		SHOCKBOLT.draw()
		WIN.flip()
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
		ratings[t] = pain_rating

	TXT.text = 'Thank you for your ratings. When you are ready, press ENTER to proceed to the main phase of the experiment.'
	TXT.draw()
	WIN.flip()
	event.waitKeys(keyList=['return'])
	WIN.flip()
	core.wait(0.5)
	
	return {'VLIST':VLIST, 'ratings':ratings}

# out = runRating(voltages=(0.01, 0.09), debug=True)
# print(out)




