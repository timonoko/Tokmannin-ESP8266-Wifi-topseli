
print('Testing Testing 3')

try:
  import usocket as socket
except:
  import socket
import network,time

releet=['-',0,0]

TIMEOUT_NORM=5*60
class d:
    timeout=10
    ajastin=1

def web_page():
  if releet[1]==1: onoff="ON"
  else: onoff="OFF"
  menu="""
    <p> """ + onoff + """ <a href="/5/on"> <button class="button">ON</button></a>
     <a href="/5/off"> <button class="button button2">OFF</button></a></p>
    <p> ALWAYS   <a href="/5/alw"> <button class="button">ON</button></a>"""+str(d.timeout/60)+"""</p>
    <p> LED <a href="/4/on"> <button class="button">ON</button></a>
     <a href="/4/off"> <button class="button button2">OFF</button></a> """+str(releet[2])+"""</p>
    """
  html = """
     <html><head> 
     <title>ESP Kahvinkeitin Web Server</title>
     <meta name="viewport" content="width=device-width, initial-scale=1">
     <link rel="icon" href="data:,">
     <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style>
     </head>
      <body>
     <h1>KAHVINKEITIN</h1> 
     """ + menu + """
     </body>
   </html>"""
  return html

from machine import Pin

BUTTON=Pin(14, Pin.IN)  
SininenLedi=Pin(4, Pin.OUT)  
relayON=Pin(5, Pin.OUT)  
relayOFF=Pin(12, Pin.OUT)  
HI=1; LO=0

def rele(x):
    d.ajastin=time.time()
    releet[1]=x
    relayOFF.value(0)
    relayON.value(releet[1])
    print("RELE:"+str(x)+":"+str(d.ajastin))
    time.sleep(1)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
#    print("VITUUA")
    if releet[1]==1:
        if (time.time()-d.ajastin)>d.timeout:
            print("TIMEOUT:"+str(time.time())+":"+str(d.ajastin))
            rele(0)
    s.settimeout(0.2)
    try:
        conn, addr = s.accept()
        request = conn.recv(1024)
        request = str(request)
        s.settimeout(5.0)
        if request.find('/5/on') == 6:
            d.timeout=TIMEOUT_NORM
            rele(1)
        if request.find('/5/off') == 6: rele(0)
        if request.find('/5/alw') == 6:
            d.timeout=2*d.timeout
            rele(1)
        if request.find('/4/on') == 6:
            releet[2]=1
            SininenLedi.value(1)
        if request.find('/4/off') == 6:
            releet[2]=0
            SininenLedi.value(0)
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError:
        if BUTTON.value()==LO:
            d.timeout=TIMEOUT_NORM
            rele((releet[1]+1)%2)
            



