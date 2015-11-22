__author__ = 'vlad'
#######################################################################
#   poll_vote.py v.0.1
#
#   This code designed to run on a Rasperry PI
#   Please see https://github.com/liveplant/liveplant-bot/README.md for
#   installation and wiring instructions
#
#######################################################################

import requests
import json
import time
import RPi.GPIO as GPIO

#TODO - save and retreive the next config param into a some kind of config file or a DB
poll_url = 'http://liveplant.herokuapp.com/current_action'
poll_time = 30
## DO_NOT_FORGET Whenever a new action added to Rasperry Pi and liveplant-server you have to add the entry to the next array!!!
actions = {'water' : {'GPIO' : 4, 'TIME_ON' : 15, 'TIME_STAMP' : 0 }, \
           'light' : {'GPIO' : 3, 'TIME_ON' : 30, 'TIME_STAMP' : 0 }}
sleep_time = poll_time


# Set GPIOs on the Rasperry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for action in actions :
    print('action:', action, ' GPIO:', actions[action]['GPIO'])
    GPIO.setup(actions[action]['GPIO'], GPIO.OUT)

print('======> Start infinite loop to poll the liveplant server (get current_action JSON) from ',poll_url)
# Poll the liveplant server for current action in an infinite loop

# Temporarely limit by 9 polls, for that use count
count = 9
# var to hold the last unixTimeStamp value (-1 is to make it initially exired)
old_timeStamp = -1

while (count > 0):
    count = count - 1

    # Get JSON from the liveplant server
    r = requests.get(poll_url)
    ##print(r.status_code)
    ##print(r.headers)
    ##print(r.text[0:1000])

    # Parce JSON into object
    j_obj = json.loads(r.text[0:1000])

    # Get values into variables
    current_action = j_obj['action']
    current_timeStamp = j_obj['unixTimestamp']
    current_timeRemaning = j_obj['votingTimeRemaining']

    print('======> Received: ')
    print('current_action         :',current_action)
    print('current_timeStamp:',current_timeStamp)
    print('current_timeRemaning:',current_timeRemaning)

    # A ZERO in votingTimeRemaining might indicate server is down... to be safe if ZERO change it to default
    if current_timeRemaning == 0 :
        current_timeRemaning = poll_time

    # Check if timestamp changed
    if old_timeStamp != current_timeStamp :
        # We have got a new timestamp, act...
        old_timeStamp = current_timeStamp

        print("Switching",current_action,"ON for",actions[current_action]['TIME_ON'],'seconds')
        GPIO.output(actions[current_action]['GPIO'],1)
        time.sleep(actions[current_action]['TIME_ON'])
        print("Switching",current_action,"OFF")
        GPIO.output(actions[current_action]['GPIO'],0)

        # Check if any time left till next voting?
        if current_timeRemaning > actions[current_action]['TIME_ON'] :
            # Sleep one second longer after a new vote published
            print("Sleep till second later then a new vote published")
            time.sleep(current_timeRemaning - actions[current_action]['TIME_ON'] + 1)
    else :
        # We have got a new timestamp, act...
        print("NO action needed, Sleep till second later then a new vote published")
        time.sleep(current_timeRemaning + 1)


GPIO.cleanup()

