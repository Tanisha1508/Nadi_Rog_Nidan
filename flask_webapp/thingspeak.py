import urllib.request
import requests
import threading
import json

import random


# Define a function that will post on server every 15 Seconds

# def thingspeak_post():
#     threading.Timer(15,thingspeak_post).start()
#     val=random.randint(1,30)
#     URl='https://api.thingspeak.com/update?api_key='
#     KEY='WRITE KEY XXXXXXXXXXX  '
#     HEADER='&field1={}&field2={}'.format(val,val)
#     NEW_URL=URl+KEY+HEADER
#     print(NEW_URL)
#     data=urllib.request.urlopen(NEW_URL)
#     print(data)

def read_data_thingspeak():
    URL='https://api.thingspeak.com/channels/1605021/feed.json?api_key='
    KEY='FBXCI87KRBC6MM0C'
    NEW_URL=URL+KEY
    print(NEW_URL)

    get_data=requests.get(NEW_URL).json()
    #print(get_data)
    channel_id=get_data['channel']['id']

    feild_1=get_data['feeds']
    #print(feild_1)

    vata=[]
    pitta=[]
    kapha=[]
    for x in feild_1:
        #print(x['field1'])
        vata.append(x['field1'])
        pitta.append(x['field2'])
        kapha.append(x['field3'])
    print(vata)
    print(pitta)
    print(kapha)
    return vata,pitta,kapha    