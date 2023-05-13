from pushbullet import Pushbullet 
import os
from datetime import datetime
#the pushbullet api key
pb = Pushbullet('o.FfjuN4kzAuqQ65nuo58ADeydRUmwqpRK')
#function that receives the notification detail as input 
def push_notify(notification):
    now=datetime.now()
    status=pb.push_note('Watchdog Alert!','Hello,\nThis is a notification for: \n'+notification)
    #when the notification delivery is a success then
    if(status):
        with open('notificationlog.txt','a') as file:
            file.write('Notification Successfully Delivered\n '+notification+' at time '+str(now)+'\n')
    #when the notification delivery is a failure then 
    else:
        with open('notificationlog.txt','a') as file:
            file.write('Notification Delivery Failed for '+notification+' at time '+str(now)+'\n')
