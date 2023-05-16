# importing of necessary libraries and functions
import os
from datetime import datetime
# function that receives the event detail as input


def event_trigger(eventinfo):
    now = datetime.now()

    with open('eventlog.txt', 'a') as file:
        file.write(eventinfo+' at time '+str(now)+'\n')
