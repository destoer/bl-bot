import  requests, time, threading, sys, json, random, re
from threading import Thread

# setup
#go to https://www.python.org/downloads/
#and install the lastest version (python 3.7.1) just follow it as a normal installer

#then open up command prompt (cmd.exe) and type py -m pip install requests


#then right click on the file and click on edit with idle

#then edit the line 
#payload = {'username': 'hunter2', 'password': 'hunter2'}

#with your login details and press f5 to run

#(note rackets will fail if the script is started with the timers not reset on it)


# mask us running as python requests module lol
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'
}

# consider parsing the json
# to get the time requred
# and automatically get the ids

#or post to touch.php
#it returns inmate
#startTime    1544388380
#length    90




def check_jail():
    r = session.post("https://www.bootleggers.us/do/player/touch",headers=header)
    response = r.json() # get jail timer
    try:
        sleeptime = response["inmate"]["length"] # response is json length will return the time we have to wait in jail
    except:
        sleeptime = random.random() # random delay to make it look more legit
        
    print('jail: ' + str(sleeptime))
    return sleeptime

    

def do_crime():
    while True:
        jtime = check_jail()
        time.sleep(jtime)
        payload = {'id' : '5'} # crimes and actions are by id
        r = session.get('https://bootleggers.us/crimes',headers=header)
        r = session.post("https://www.bootleggers.us/do/crimes/commit",data=payload, headers=header) # backend actions under /do/
        print('crimes: ' + r.text)
        try:
            response = r.json() # get the time remaining
            sleeptime = response["timer"]["length"]
            print('time: ' + str(sleeptime))
            time.sleep(sleeptime)
        except:
            time.sleep(80)

def do_auto():
    while True:
        jtime = check_jail()
        time.sleep(jtime)
        payload = {'id' : '2'}
        r = session.get('https://bootleggers.us/auto-theft')
        r = session.post('https://www.bootleggers.us/do/auto-theft/steal-car', data = payload,headers=header)
        print('auto: ' + r.text)

        try:
            response = r.json() # get remaing time
            sleeptime = response["timer"]["length"]
            print('time: ' + str(sleeptime))
            time.sleep(sleeptime)
            
        except: # sleep for the default time
            time.sleep(240)


def do_racket(): # rackets work while in jail?
    while True:
        jtime = check_jail()
        time.sleep(jtime)
        payload = {'id' : '1'}
        r = session.get('https://bootleggers.us/rackets')
        r = session.post('https://www.bootleggers.us/do/rackets/start', data = payload,headers=header)
        print('rackets: ' + r.text)
        try:
            response = r.json() # get remaing time
            sleeptime = response["timer"]["length"]
            print('time: ' + str(sleeptime))
            time.sleep(sleeptime)
        except:
            time.sleep(15*60) # 15 mins for a racket by default
        
        r = session.post('https://www.bootleggers.us/do/rackets/collect',data = payload,headers=header)
        print('rackets col: ' + r.text)        

def do_bootleg():
    while True:
        jtime = check_jail()
        time.sleep(jtime)
        
        #determine max carry capcitity by regexing out the result
        r = session.get('https://bootleggers.us/bootlegging')

        temp = r.text
        regex = re.compile('("capacity":[0-9][0-9])')
        result = regex.findall(temp)

        #print(result)

        regex = re.compile('([0-9]*$)')

        result = regex.findall(result.pop(0))

        capacity = result.pop(0)

        print('Capacity: ' + capacity)

        #determine which state we are in
        r = session.get('https://www.bootleggers.us/do/player/touch')
        response = r.json()
        city = response["dashboard"]["city"]["state"]
        
        #if nj, buy champagne and travel to chicago
        if city == "New Jersey":
                r = session.get('https://www.bootleggers.us/bootlegging')
                payload = {'amount': capacity , 'booze_id' : '6'}
                r = session.post('https://www.bootleggers.us/do/bootlegging/buy', data = payload,headers=header)
                payload = {'id':'5'}
                r = session.post('https://www.bootleggers.us/do/cities/travel', data = payload,headers=header)
                #sell champagne
                payload = {'amount': capacity , 'booze_id' : '6'}
                r = session.post('https://www.bootleggers.us/do/bootlegging/sell', data = payload,headers=header)
        #if penny, buy gin and travel to nj
        if city == "Pennsylvania":
                r = session.get('https://www.bootleggers.us/bootlegging')
                payload = {'amount': capacity , 'booze_id' : '5'}
                r = session.post('https://www.bootleggers.us/do/bootlegging/buy', data = payload,headers=header)
                payload = {'id':'2'}
                r = session.post('https://www.bootleggers.us/do/cities/travel', data = payload,headers=header)
                #sell champagne
                payload = {'amount': capacity , 'booze_id' : '6'}
                r = session.post('https://www.bootleggers.us/do/bootlegging/sell', data = payload,headers=header)
        #if illi, buy whisky and travel to penny.
        if city == "Illinois":
                payload = {'amount': capacity , 'booze_id' : '4'}
                r = session.post('https://www.bootleggers.us/do/bootlegging/buy', data = payload,headers=header)
                payload = {'id':'3'}
                r = session.post('https://www.bootleggers.us/do/cities/travel', data = payload,headers=header)
                #sell whisky
                payload = {'amount': capacity , 'booze_id' : '4'}
                r = session.post('https://www.bootleggers.us/do/bootlegging/sell', data = payload,headers=header)
                
        time.sleep((60*60)+2)

        
session = requests.Session()
payload = {'username': 'hunter2', 'password': 'hunter2'} # send off our login details
r = session.post('https://www.bootleggers.us/do/game/login', data=payload,headers=header)
print('login: ' + r.text)
#payload = {'id': '1'}
#r = session.post('http://bootleggers.us/do/swiss-bank/',data=payload,headers=header)
#print(r.text)

# start threads to perform our actions

Thread(target = do_crime).start()
Thread(target = do_auto).start()
Thread(target = do_racket).start()
Thread(target = do_bootleg).start() #not fully tested 

