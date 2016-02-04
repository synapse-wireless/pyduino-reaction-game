"""Pyduino Reaction Time Game
This example is a simple application using the built-in timer, an LCD shield, and a buzzer to measure
the reaction time.

Note: The Pyduino is not designed with battery back-up so the clock must be reset when power is applied.

Note: The game type can be changed from using only visual cues, audio cues, or both. As a fun fact, you
      may notice that your response time to audio cues is lower than visual ones.
      
Ex.
  #Set as audio only cues
  GAME_TYPE = GAME_TYPE_AUDIO
  
Ex.
  #Set as visual only cues
  GAME_TYPE = GAME_TYPE_VISUAL
"""

from synapse.rf200HardTime import *
from pyduinolcd import *

# IO pins
BUZZER = D0

# Global variables
start_test = 0
blanking_time = 0
best_reaction_time = 1000

# Constants
GAME_TYPE_VISUAL = 0x01
GAME_TYPE_AUDIO = 0x02

# Configure the game type - Currently set to use both audio & visual cues
GAME_TYPE = GAME_TYPE_VISUAL | GAME_TYPE_AUDIO


@setHook(HOOK_STARTUP)
def startup():
    """Startup event to initialize the IO, timers, and LCD display"""  
    # Initialize buzzer IO
    writePin(BUZZER, True)
    setPinDir(BUZZER, True)
    
    # Send the commands to initialize the display
    lcd_init()
    
    # Initialize hardware timers
    initHwTmr()
    
    # Write game instrcutions to screen
    clear_screen()
    write_line1('Reaction time')
    write_line2('press any button')


@setHook(HOOK_100MS)
def timer_100ms():
    """Timer event to control the start time of the game"""
    global start_test
    global best_reaction_time
    if start_test > 0:
        start_test -= 1
        if start_test == 0:
            # Determine the game configuration, choose audio, visual, or both
            if GAME_TYPE == GAME_TYPE_AUDIO | GAME_TYPE_VISUAL:
                reaction_time = test_reaction(random()&0x01)
            elif GAME_TYPE == GAME_TYPE_VISUAL:
                reaction_time = test_reaction(True)
            elif GAME_TYPE == GAME_TYPE_AUDIO:
                reaction_time = test_reaction(False)
                
            # Log the best reaction time
            if reaction_time < best_reaction_time:
                best_reaction_time = reaction_time
            
        
@setHook(HOOK_10MS)
def timer_10ms():
    """Timer event to check for false start button presses"""
    global start_test
    global blanking_time
    
    if check_any_button():
        # Make sure the button isn't pressed before we say GO!
        if start_test > 0:
            write_line1('False start!')
            start_test = 0
        else:
            # Make sure we're not still in the 100ms blanking period
            if blanking_time == 0:
                queue_test()
                
    # Give a 100 millisecond blanking time after a game completes. The gamer will probably
    # still be holding down the button for a certain amount of time
    if blanking_time > 0:
        blanking_time -= 1

def queue_test():
    """Start a game after a random wait from 1-4 seconds"""
    global start_test
    clear_screen()
    write_line1('Get Ready!!!')
    start_test = random() % 30 + 10

def test_reaction(sensor):
    """Audio/visual impulse generator and timer loop to measure reaction time"""
    global blanking_time
    if sensor:
        write_line1('Go!!         ')
    else:
        pulsePin(BUZZER, 200, False)
    resetTmr()
    # Wait for button to be pressed, or timeout after 1 second
    while tmrMs() < 1000 and readAdc(A0) > 950:
        pass
    time = tmrMs()
    write_line1('Reaction time   ')
    write_line2(str(time) + ' ms')
    blanking_time = 10
    return time
    
def get_best_time():
    """Return the best reaction time"""
    return best_reaction_time
