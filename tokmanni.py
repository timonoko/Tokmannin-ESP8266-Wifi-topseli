
print('Testing 3')

try:
  import usocket as socket
except:
  import socket
import network,time


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

from machine import Pin

relayON =Pin(5, Pin.OUT)  
relayOFF =Pin(12, Pin.OUT)  
SininenLedi = Pin(4, Pin.OUT)  
BUTTON=Pin(14, Pin.IN)  
LO=0;HI=1

relayState=0

def buttoni():
   global relayState
   if BUTTON.value()==LO:
      if relayState==1:
        relayState=0
        relayON.value(0)
      else:
        relayState=1
        relayON.value(1)
      time.sleep(1)

def web_page():
    RS=" button2"
    if relayState==1: RS=""
    menu="""<p><a href="/5/on"><button class="button%s">ON</button> </a>"""%(RS)
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

while True:
    s.settimeout(0.2)
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        s.settimeout(5.0)
        if request.find('/5/on') == 6:
            relayState=1
            relayON.value(1)
        if request.find('/5/off') == 6:
            relayState=0
            relayON.value(0)
        if request.find('/4/on') == 6:
            SininenLedi.value(1)
        if request.find('/4/off') == 6:
            SininenLedi.value(0)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError:
        buttoni() 



