import time
from machine import Pin

relayON =Pin(5, Pin.OUT)  
relayOFF =Pin(12, Pin.OUT)  
relayON.value(1)

SininenLedi = Pin(4, Pin.OUT)  
for x in range(50):
    SininenLedi.value(1)
    time.sleep(0.2)
    SininenLedi.value(0)
    time.sleep(0.2)

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    while not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('Jorpakko', 'Juhannusyona')
        while not sta_if.isconnected():
            time.sleep(10)
    print('IF network config:', sta_if.ifconfig())

do_connect() 

def do_not_connect():
    import network
    ap_if = network.WLAN(network.AP_IF)
    print('AP network config:', ap_if.ifconfig())
    ap_if.active(False)
    print('AP network config:', ap_if.ifconfig())
    
import gc
gc.collect()

import esp
esp.osdebug(None)

import os
print(os.listdir())

def ls():
    print(os.listdir())

import webrepl
webrepl.start()

do_not_connect()

for x in range(10):
    print('waiting')
    SininenLedi.value(1)
    time.sleep(0.1)
    SininenLedi.value(0)
    time.sleep(1.9)

import vahtikoira






