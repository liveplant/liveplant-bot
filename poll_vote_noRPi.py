__author__ = 'vlad'
#######################################################################
#   poll_vote_noRPi.py v.0.3
#
#   This code does NOT NEED  a Rasperry PI to run
#   The import RPi.GPIO and all related calls are commented out so developer can
#   try/debug all logic of the poll_vote.py of the same version without need to
#   have the Raspberry PI
#
#######################################################################

import requests
import json
import time
#import RPi.GPIO as GPIO

#TODO - save and retreive the next config param into a some kind of config file or a DB
poll_url = 'http://liveplant.herokuapp.com/current_action'
poll_time = 30
## DO_NOT_FORGET Whenever a new action added to Rasperry Pi and liveplant-server you have to add the entry to the next array!!!
actions = {'water' : {'GPIO' : 4, 'TIME_ON' : 15 }, \
           'light' : {'GPIO' : 3, 'TIME_ON' : 30 }}
sleep_time = poll_time


# Set GPIOs on the Rasperry Pi
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
for action in actions :
    print('action:', action, ' GPIO:', actions[action]['GPIO'])
#    GPIO.setup(actions[action]['GPIO'], GPIO.OUT)

print('======> Start infinite loop to poll the liveplant server (get current_action JSON) from ',poll_url)
# Poll the liveplant server for current action in an infinite loop

# Temporarely limit by 99 polls, for that use count
count = 99
# var to hold the last unixTimeStamp value (-1 is to make it initially exired)
old_timeStamp = -1

while (count > 0):
    count = count - 1

    # Get JSON from the liveplant server
    try:
        r = requests.get(poll_url)
    except requests.exceptions.RequestException as e:

        # Something terribly wrong, cannot reach the server,
        # just log logg the error and continue till next vote, hopefully somebody checking the log
        print("!!!!!! ERROR Cannot reach the server at",poll_url,". Do nothing till next poll")
        current_action = ''
    else:

        # Parce JSON into object
        try:
            j_obj = json.loads(r.text[0:1000])

            # Get values into variables
            current_action = j_obj['action']
            current_timeStamp = j_obj['unixTimestamp']
            current_timeRemaning = j_obj['votingTimeRemaining']

            print('======> Received: ')
            print('current_action      :',current_action)
            print('current_timeStamp   :',current_timeStamp)
            print('current_timeRemaning:',current_timeRemaning)
        except:
            print("!!!!!! ERROR No JSON received")
            current_action = ''


    # No action received means action is "nothing"
    if not current_action or not (current_action in actions):
        # Set values to defaults
        current_action = 'nothing'
        current_timeStamp = old_timeStamp
        current_timeRemaning = poll_time

        print("======> Faked values (cause did not receive 'action'): ")
        print('current_action         :',current_action)
        print('current_timeStamp      :',current_timeStamp)
        print('current_timeRemaning   :',current_timeRemaning)


    # A ZERO in votingTimeRemaining might indicate server is down... to be safe if ZERO
    # change it to default prevent extremaly frequent poll
    if current_timeRemaning == 0 :
        current_timeRemaning = poll_time


    # Check if timestamp changed
    if old_timeStamp != current_timeStamp :
        # We have got a new timestamp, act...
        old_timeStamp = current_timeStamp

        print("Switching",current_action,"ON for",actions[current_action]['TIME_ON'],'seconds')
#        GPIO.output(actions[current_action]['GPIO'],1)
        time.sleep(actions[current_action]['TIME_ON'])
        print("Switching",current_action,"OFF")
#        GPIO.output(actions[current_action]['GPIO'],0)

        # Check if any time left till next voting?
        if current_timeRemaning > actions[current_action]['TIME_ON'] :
            # Sleep one second longer after a new vote published
            print("Sleep till second later then a new vote published (for",current_timeRemaning - actions[current_action]['TIME_ON'] + 1,"seconds)")
            time.sleep(current_timeRemaning - actions[current_action]['TIME_ON'] + 1)
    else :
        # Do nothing just wait till one second after next votng and loop....
        print("NO action needed, Sleep till second later then a new vote published (for",current_timeRemaning + 1,"seconds)")
        time.sleep(current_timeRemaning + 1)


#GPIO.cleanup()

