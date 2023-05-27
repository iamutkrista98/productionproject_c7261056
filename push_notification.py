# importing of necessary libraries and functions
import traceback
from pushbullet import Pushbullet
import os
from datetime import datetime
# the pushbullet api key
# function that receives the notification detail as input


def push_notify(notification):
    now = datetime.now()
    try:
        pb = Pushbullet('o.FfjuN4kzAuqQ65nuo58ADeydRUmwqpRK')
        status = pb.push_note(
            'Watchdog Alert!', 'Hello,\nThis is a notification for:\n' + notification)
        # when the notification delivery is a success
        if status:
            with open('notificationlog.txt', 'a') as file:
                file.write('Notification Successfully Delivered\n' +
                           notification + ' at time ' + str(now) + '\n')
        # when the notification delivery fails
        else:
            with open('notificationlog.txt', 'a') as file:
                file.write('Notification Delivery Failed for ' +
                           notification + ' at time ' + str(now) + '\n')
    except Exception as e:
        # handle the exception when notification delivery fails
        with open('notificationlog.txt', 'a') as file:
            file.write('Notification Delivery Failed for ' +
                       notification + ' at time ' + str(now) + '\n')
            # file.write(traceback.format_exc() + '\n')
