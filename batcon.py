# Termux battery charger controller.
# The wireless charger is connected  to a Wifi-plug
# starts charging below %70 and stops charging above %80

import os,json,time

os.system("termux-wake-lock")
os.system("termux-wifi-enable true")
while True:
  a=json.loads(os.popen("termux-battery-status").read())
  print a
  p=a['percentage']
  s=a['status']
  if p<70 and s=="DISCHARGING":
    os.system("termux-tts-speak battery percentage "+str(p))
    os.system("termux-tts-speak CHARGING")
    os.system('wget 192.168.1.61/5/on')
    os.remove("on")
  if p>80 and s=="CHARGING":
    os.system("termux-tts-speak battery percentage "+str(p))
    os.system("termux-tts-speak UNPLUGGING")
    os.system('wget 192.168.1.61/5/off')
    os.remove("off")
  time.sleep(300)

