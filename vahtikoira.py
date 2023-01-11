
print('Testing ')

try:
  import usocket as socket
except:
  import socket

import network,time,uping

from machine import Pin


relayON =Pin(5, Pin.OUT)  
relayOFF =Pin(12, Pin.OUT)  
SininenLedi = Pin(4, Pin.OUT)  
BUTTON=Pin(14, Pin.IN)  
LO=0;HI=1

ledi_timer=0
VahtiKoira=True
LaskuriTaysi=60*10
VahtiLaskuri=LaskuriTaysi
relayON.value(1)

def web_page():
    RS=" button2"
    if VahtiKoira: RS=""
    menu="""<p><a href="/6/on"><button class="button%s">ON</button> </a>"""%(RS)
    menu+="""<a href="/6/off"><button class="button button3">OFF</button> </a>"""
    menu+="""<p><a href="/reset"><button class="button button3">RESET</button> </a>"""
    sta_if = network.WLAN(network.STA_IF)
    this_ip=sta_if.ifconfig()[0]
    html = """
     <html><head> 
     <title>Vahtikoira</title>
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
     <h1>Vahtikoira</h1> 
     """ + menu + """ <p>
     """ + str(VahtiLaskuri) + """ <p>
     """ + this_ip + """ <p>
      </body>
   </html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

from machine import WDT
wdt=WDT() # about 6 seconds WatchDoG

while True:
    wdt.feed()
    s.settimeout(0.2)
    try:
        conn, addr = s.accept() 
        request = conn.recv(1024)
        request = str(request)
        s.settimeout(5.0)
        if request.find('/6/on') == 6:
            VahtiKoira=True
            VahtiLaskuri=LaskuriTaysi
            relayON.value(1)
        if request.find('/6/off') == 6:
            VahtiKoira=False
        if request.find('/reset') == 6:
            relayON.value(0)
            time.sleep(5)
            relayON.value(1)
            time.sleep(5)
            import machine
            machine.reset()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError:
        if BUTTON.value()==LO:
            if VahtiKoira:
                VahtiKoira=False
                SininenLedi.value(1)
            else:
                VahtiKoira=True
                VahtiLaskuri=LaskuriTaysi
                SininenLedi.value(0)
            time.sleep(10)
        if not VahtiKoira: SininenLedi.value(1)
        if VahtiKoira:
            VahtiLaskuri-=1
            if VahtiLaskuri<0:
                relayON.value(0)
                time.sleep(5)
                relayON.value(1)
                VahtiLaskuri=LaskuriTaysi
                for x in range(300):
                    SininenLedi.value(1)
                    time.sleep(0.05)
                    SininenLedi.value(0)
                    time.sleep(0.05)
            ledi_timer+=1
            if ledi_timer==5:
                SininenLedi.value(1)
            elif ledi_timer>10:
                SininenLedi.value(0)
                ledi_timer=0
                sta_if = network.WLAN(network.STA_IF)
                if sta_if.isconnected():
                    SininenLedi.value(1)
                    p=uping.ping('192.168.1.11',timeout=100,count=1)
                    SininenLedi.value(0)
                    if p[1]!=0:
                        VahtiLaskuri=LaskuriTaysi
                    else:
                        for x in range(5):
                            SininenLedi.value(1)
                            time.sleep(0.1)
                            SininenLedi.value(0)
                            time.sleep(0.1)
                else:
                    for x in range(10):
                        SininenLedi.value(1)
                        time.sleep(0.1)
                        SininenLedi.value(0)
                        time.sleep(0.1)


