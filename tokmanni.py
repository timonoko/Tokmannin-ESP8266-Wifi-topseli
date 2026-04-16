
print('Testing 3')

try:
  import usocket as socket
except:
  import socket

import network,time,uping,machine
from machine import Pin
from machine import WDT


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
s.setblocking(False)


relayON =Pin(5, Pin.OUT)  
relayOFF =Pin(12, Pin.OUT)  
SininenLedi = Pin(4, Pin.OUT)  
BUTTON=Pin(14, Pin.IN)  
LO=0;HI=1

relayState=0
laskuri=0

WDTON=False
wdt=False

def buttoni():
    global relayState,laskuri,WDTON,wdt
    if BUTTON.value()==LO:
      if relayState==1:
        relayState=0
        relayON.value(0)
      elif not WDTON:
        relayState=1
        relayOFF.value(0)
        relayON.value(1)
      else: machine.reset()
      time.sleep(1)
    elif relayState==0:
        laskuri+=1
        if (laskuri%10)==0: print(laskuri)
        if laskuri%1000==0:
            print('ping-testi')
            p=uping.ping('192.168.1.11',count=1,timeout=100)
            if p[1]==0:
                machine.reset()
        if laskuri==21:
            print('WDT ON')
            wdt=WDT()
            WDTON=True
        if laskuri>10000:
            machine.reset()

def web_page():
    RS=" button2"
    if relayState==1: RS=""
    if WDTON:
        nap="ON/wdt"
    else:
        nap="ON"
    menu="""<p><a href="/5/on"><button class="button%s">%s</button> </a>"""%(RS,nap)
    menu+="""<a href="/5/off"><button class="button button3">OFF</button> </a>"""
    sta_if = network.WLAN(network.STA_IF)
    this_ip=sta_if.ifconfig()[0]
    html = """
     <html><head> 
     <title>Tokmanni</title>
     <meta http-equiv="refresh" content="3;url=http://"""+this_ip+"""/">
     <meta name="viewport" content="width=device-width, initial-scale=1"> 
     <link rel="icon" href="data:,">
     <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #ff0000; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4a798a;}
  .button3{background-color: #3f7749;}</style>
     </head>
      <body>
     <h1>Tokmanni</h1> 
     """ + menu + """ <p>
     """ + this_ip + """ <p>
      </body>
   </html>"""
    return html

WEBREPL=False
while not WEBREPL:
    if WDTON: wdt.feed()
    s.settimeout(0.2)
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        if request.find('/5/on') == 6:
            if WDTON: machine.reset()
            elif relayState==0:
                relayState=1
                relayOFF.value(0)
                relayON.value(1)
        if request.find('/5/off') == 6:
            if relayState==0: machine.reset()
            relayState=0
            relayON.value(0)
        if request.find('/4/on') == 6:
            print('SininenLedi ON')
            SininenLedi.value(1)
        if request.find('/4/off') == 6:
            print('SininenLedi OFF')
            SininenLedi.value(0)
        if request.find('/webrepl') == 6:
            if WDTON: machine.reset()
            WEBREPL=True
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError:
        buttoni()
    except:
        if relayState==0: machine.reset()






