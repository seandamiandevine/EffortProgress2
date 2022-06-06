from psychopy import visual, core, event, monitors, sound, parallel
from random import shuffle, sample
import os
import pyfiglet
import numpy as np
import pandas as pd
from datetime import datetime as dt
from fx.addOutput import addOutput, initCSV
try: 
    import u3
    from fx.LJTickDAC import LJTickDAC
except:
    pass

def runTask(WIN, id, sex, age, voltages, debug=False, _thisDir=os.getcwd()):
    """
    @id:       subject id
    @sex:      subject sex
    @age:      subject age
    @voltages: list of high and low voltages from calibration phase
    @debug:    whether this is debug mode or not
    @_thisDir: location of this script, data folder,  stimuli, and instructions

    returns: None

    For question, contact Sean.
    seandamiandevine@gmail.com
    """
    # Initialize datafile
    FILENAME = _thisDir + os.sep + 'data' + os.sep + 'effprog_pain_' + str(id)+'_'+str(dt.now()).replace(':','_')+'.csv'
    HEADER   = ['id', 'age', 'sex','block', 'start','resistance','pain', 'trial', 'trialinblock', 'pfilled', 'common', 'odd', 'odd_idx', 'rt','acc','time']

    # Specify parallel port for shock machine and initalize labjack
    if not debug:
        DEV  = u3.U3()
        DEV.configIO(FIOAnalog=0x0F)
        TDAC = LJTickDAC(DEV, 4, 500.)
        TDAC.update(0, 0) # off
        PORT, PORTNUM = parallel.ParallelPort(address='0xEFF8'), 16
    
    # Set constants
    TEXTCOL     = [-1, -1, -1]                                                 # font colour
    FONTH       = 1                                                            # font height
    STIMDIR     = 'stim/'                                                      # directory where oddball stimuli are
    UP, DOWN    = f'{STIMDIR}oddball_down.png', f'{STIMDIR}oddball_up.png'     # oddball stimuli
    PROGSTART   = [.8, .5]                                                     # where progress bar starts
    FILLRATE    = 0.1 if not debug else 1                                      # amount one correct responses fills up screen
    PRESISTANCE = [0.005, 0.01]                                                # proportion of avg. practice RT for how fast bar fills per frame
    PAIN        = voltages                                                     # amount of pain (in V.) -- from calibration phase
    NREP        = 2                                                            # number of repetitions for all combinations
    NPRAC       = 20 if not debug else 1                                       # number of practice trials
    NBLOCKS     = len(PRESISTANCE)*len(PAIN)*len(PROGSTART)*NREP               # number of blocks
    DEADLINE    = 10000 #0.75                                                  # response deadline
    KEYS        = ['q','w','e', 'escape']                                      # keys to make choices
    BLOCKTIME   = 1                                                            # time for which block feedback stays up (s.)
    PAINTIME    = 0.33                                                         # time for which shock is administered (s.)
    ERRTIME     = 1.5                                                          # time that error screens stay up (s.)
    ITI         = 2                                                            # block-to-block time (s.)
    SCALE       = (WIN.size[0]/3024)*2                                         # scaling parameter for progress bar fill

    # initialize instructions
    INSTDIR     = f'instructions/instructions/'                             
    INSTS       = os.listdir(INSTDIR)
    INSTPIC     = visual.ImageStim(WIN, image=f"{INSTDIR}Slide1.png")

    # initialize trial components
    PROBE1      = visual.ImageStim(WIN, image=UP, pos=(-7.5,0))
    PROBE2      = visual.ImageStim(WIN, image=UP, pos=(0,0))
    PROBE3      = visual.ImageStim(WIN, image=UP, pos=(7.5,0))
    COUNTDOWN   = visual.TextStim(WIN, text='', height=3*FONTH, pos=(0,0), color='White')
    FEEDBACK    = visual.TextStim(WIN, text='', height=3*FONTH, pos=(0,0), color='White')
    PAINFB      = visual.ImageStim(WIN, image=f'{STIMDIR}bolt.png', pos=(0,0), size=(10,10))
    PROGBAR_OUT = visual.Rect(WIN, pos=(0,5), size=(20,2), lineColor='White', fillColor='White')
    PROGBAR     = visual.Rect(WIN, pos=(0,PROGBAR_OUT.pos[1]), size=(0,PROGBAR_OUT.size[1]), fillColor='Red')
    SHOCKLEVEL  = visual.TextStim(WIN, text='', height=FONTH, pos=(0,PROGBAR_OUT.pos[1]+2*FONTH), color='White')

    # initialize effort/reward pairings
    CONDS       = [(r, pr, p) for r in range(NREP) for r in PRESISTANCE for pr in PROGSTART for p in PAIN]    
    shuffle(CONDS)

    #--------------------------------------Start Task-----------------------------------------
    WIN.mouseVisible=True if debug else False

    initCSV(FILENAME, HEADER)

    # Instructions A
    INSTCOUNTER = 1
    while INSTCOUNTER<8:
       INSTPIC.image = f'{INSTDIR}Slide{INSTCOUNTER}.png'
       INSTPIC.draw()
       WIN.flip()
       key_press  = event.waitKeys(keyList=['left', 'right'])
       if key_press[0]=='left':
           INSTCOUNTER -= 1
           if INSTCOUNTER<1: INSTCOUNTER=1
       else:
           INSTCOUNTER += 1

   # Practice phase
    prac_rts = np.zeros(NPRAC)
    for t in range(NPRAC):
       start_time = dt.now()

       # Define stim
       odd_idx = sample([0,1,2], 1)[0]
       common  = sample([UP, DOWN], 1)[0]
       odd     = DOWN if common==UP else UP
       stim    = [common, common, common]
       stim[odd_idx] = odd
       PROBE1.image, PROBE2.image, PROBE3.image = stim

       # Draw and response
       PROBE1.draw()
       PROBE2.draw()
       PROBE3.draw()
       WIN.flip()
       key_press = event.waitKeys(keyList=KEYS)[0]
       if key_press=='escape':
           core.quit()
       rt  = (dt.now() - start_time).total_seconds()
       acc = 1 if key_press==KEYS[odd_idx] else 0

       # Show feedback
       FEEDBACK.text = 'INCORRECT' if acc==0 else 'CORRECT'
       FEEDBACK.draw()
       WIN.flip()
       core.wait(ERRTIME)

       # Save.
       out  = [id, age, sex,'practice', 'NA','NA','NA', 'NA', t, 'NA', common, odd, odd_idx, rt, acc, dt.now().timestamp()]
       addOutput(FILENAME, out)
       prac_rts[t] = rt

   # Instructions B
    while INSTCOUNTER<23:
       INSTPIC.image = f'{INSTDIR}Slide{INSTCOUNTER}.png'
       INSTPIC.draw()
       WIN.flip()
       key_press  = event.waitKeys(keyList=['left', 'right'])
       if key_press[0]=='left':
           INSTCOUNTER -= 1
           if INSTCOUNTER<1: INSTCOUNTER=1
       else:
           INSTCOUNTER += 1

    # Main phase
    # prac_rts     = prac_rts[prac_rts < 1.1] # remove long outliers
    scale_resist = 1/np.mean(prac_rts)      # longer rts = less fill/s, shorter rts = more fill/s
    to           = 0
    for b in range(NBLOCKS):
        resist, start, pain = CONDS[b]

        resist          = resist*scale_resist
        pfilled         = start
        updated_size    = pfilled*PROGBAR_OUT.size[0] 
        offset          = updated_size/SCALE
        updated_pos     = PROGBAR_OUT.pos[0]+PROGBAR_OUT.size[0]/SCALE - offset
        PROGBAR.pos[0]  = updated_pos
        PROGBAR.size[0] = updated_size
        PROGBAR         = visual.Rect(WIN, pos=PROGBAR.pos, size=PROGBAR.size, fillColor='Red')
        SHOCKLEVEL.text = f'SHOCK LEVEL = {int(pain*100)}V'
        t               = 0
        SHOCK           = False

        # countdown 
        for i in range(3):
            COUNTDOWN.text = str(3-i)
            COUNTDOWN.draw()
            WIN.flip()
            core.wait(1)
        WIN.flip()
        core.wait(ITI)

        # go!
        while pfilled > 0:
            start_time = dt.now()

            # define stim
            odd_idx = sample([0,1,2], 1)[0]
            common  = sample([UP, DOWN], 1)[0]
            odd     = DOWN if common==UP else UP
            stim    = [common, common, common]
            stim[odd_idx] = odd
            PROBE1.image, PROBE2.image, PROBE3.image = stim

            # record responses and draw stim
            key_press = []
            while len(key_press)==0:
                time_passed = (dt.now() - start_time).total_seconds()
                if  time_passed > DEADLINE:
                    # timeout
                    break
                key_press = event.getKeys(keyList = KEYS)

                # increment pain bar 
                PROGBAR.pos[0]  -= time_passed*resist
                PROGBAR.size[0] += time_passed*resist*SCALE
                PROGBAR         = visual.Rect(WIN, pos=PROGBAR.pos, size=PROGBAR.size, fillColor='Red')
                pfilled         = PROGBAR.size[0]/PROGBAR_OUT.size[0]
                if pfilled > 1:
                    SHOCK = True
                    break

                # draw per refresh 
                PROBE1.draw()
                PROBE2.draw()
                PROBE3.draw()
                PROGBAR_OUT.draw()
                PROGBAR.draw()
                SHOCKLEVEL.draw()
                WIN.flip()

            if pfilled > 1:
                break
            elif len(key_press)==0: 
                timeout, rt, acc = True, 'NA', 0
            else:
                if key_press[0]=='escape':
                    core.quit()
                timeout = False
                rt  = (dt.now() - start_time).total_seconds()
                acc = 1 if key_press[0]==KEYS[odd_idx] else 0


            if timeout:
                FEEDBACK.text = 'Too Slow!'
                FEEDBACK.draw()
                WIN.flip()
                core.wait(ERRTIME)
            elif acc==1: 
                # update progress bar if correct response
                PROGBAR.pos[0]  += FILLRATE
                PROGBAR.size[0] -= FILLRATE*SCALE
                PROGBAR         = visual.Rect(WIN, pos=PROGBAR.pos, size=PROGBAR.size, fillColor='Red')
                pfilled         = PROGBAR.size[0]/PROGBAR_OUT.size[0]
                
            t  += 1
            to += 1

            out = [id, age, sex, b, start,resist,pain, to, t, pfilled, common, odd, odd_idx, rt, acc, dt.now().timestamp()]
            addOutput(FILENAME, out)

        PAINFB.image = f'{STIMDIR}bolt.png' if SHOCK else f'{STIMDIR}smile.png'
        PAINFB.draw()
        WIN.flip()
        if SHOCK and not debug:
            TDAC.update(pain, 0) # on
            PORT.setData(PORTNUM)
            core.wait(PAINTIME)
            TDAC.update(0,0)     # off
            PORT.setData(0)
        elif SHOCK and debug:
            print(f'block {b}: {pain}V would be sent')
        elif not SHOCK and not debug:
            TDAC.update(0,0)     # double-check it is off
            PORT.setData(0)
        else:
            print(f'block {b}: no shock would be sent')
            
        core.wait(BLOCKTIME)
        WIN.flip()
        core.wait(ITI) # also acts as a cooldown

    FEEDBACK.text   = 'Thank you! You are now done the experiment. See the experimenter for further details'
    FEEDBACK.height = fontH

    FEEDBACK.draw()
    WIN.flip()
    event.waitKeys(keyList='x')

    return None