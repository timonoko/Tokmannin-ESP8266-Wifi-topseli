// Vahtikoira. Käynnistää tietokoneen uudelleen,
// jossei sieltä tule pingiä 5 minsan väkein


#include <ESP8266WiFi.h>
#include "ESP8266Ping.h"



#include "password.h" /*
char* wifi_name = "****"; // Your Wifi network name here
char* wifi_pass = "****";    // Your Wifi network password here
*/

WiFiServer server(80);

String header;

String relayONState = "off";
String relayOFFState = "off";
String SininenLediState = "off";
String VahtikoiraState = "off";

const int relayON = 5;
const int relayOFF = 12;
const int SininenLedi = 4;
const int Nappi = 14;

unsigned long previousMillis = 0;
const long interval = 5 * 60*1000; // 5  minsa
int PANIC = 0 ; 

const IPAddress remote_ip(192, 168, 1, 11);

void setup() {
  Serial.begin(115200);
  pinMode(relayON, OUTPUT);
  pinMode(relayOFF, OUTPUT);
  pinMode(SininenLedi, OUTPUT);
  pinMode(Nappi, INPUT);
  digitalWrite(relayON, LOW) ;
  digitalWrite(relayOFF, LOW);
  digitalWrite(SininenLedi, LOW);
  Serial.print("Connecting to ");
  Serial.println(wifi_name);
  WiFi.begin(wifi_name, wifi_pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
  WiFi.softAPdisconnect(true);
  // releet päälle
  digitalWrite(SininenLedi, HIGH);
  SininenLediState = "on";
  digitalWrite(relayON, HIGH);
  relayONState = "on";
  VahtikoiraState = "on";
}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    PANIC = PANIC + 1 ;
    // Paniikki jos on-viestejä ei ole tullut 10*5 minuuttiin
    if (Ping.ping(remote_ip) && PANIC < 10)  delay(1000);  
    else{
      PANIC = 0;
      if (VahtikoiraState=="on") {
	digitalWrite(relayON, LOW);
	delay(5000);
	digitalWrite(relayON, HIGH); 
	relayONState = "on"; }}}
  if ( digitalRead(Nappi) == 0) {
    if (  relayONState == "off" ) {
      PANIC = 0;
      Serial.println("GPIO 5 on");
      relayONState = "on";
      digitalWrite(relayON, HIGH); }
    else {
      Serial.println("GPIO 5 off");
      relayONState = "off";
      digitalWrite(relayON, LOW);
     }
    delay(2000); }
  if (client) {                             // If a new client connects,
    Serial.println("New Client.");          // print a message out in the serial port
    String currentLine = "";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
        Serial.write(c);                    // print it out the serial monitor
        header += c;
        if (c == '\n') {                    // if the byte is a newline character
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            if (header.indexOf("GET /5/on") >= 0) {
              Serial.println("GPIO 5 on");
              relayONState = "on";
              digitalWrite(relayON, HIGH);
	      previousMillis = currentMillis;
	      PANIC = 0;
            } else if (header.indexOf("GET /5/off") >= 0) {
              Serial.println("GPIO 5 off");
              relayONState = "off";
              digitalWrite(relayON, LOW);
            } else if (header.indexOf("GET /4/on") >= 0) {
              Serial.println("GPIO 4 on");
              SininenLediState = "on";
              digitalWrite(SininenLedi, HIGH);
	      PANIC = 0;
            } else if (header.indexOf("GET /4/off") >= 0) {
              Serial.println("GPIO 4 off");
              SininenLediState = "off";
              digitalWrite(SininenLedi, LOW);
	    } else if (header.indexOf("GET /6/on") >= 0) {
              Serial.println("Vahtikoira ON");
              VahtikoiraState = "on";
            } else if (header.indexOf("GET /6/off") >= 0) {
              Serial.println("Vahtikoira OFF");
              VahtikoiraState = "off";

            }
            
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<link rel=\"icon\" href=\"data:,\">");
            client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
            client.println(".button { background-color: #195B6A; border: none; color: white; padding: 16px 40px;");
            client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
            client.println(".button2 {background-color: #77878A;}</style></head>");
            client.println("<body><h1>Vahtikoira</h1> ");
	    client.println("<p>");
	    client.println(WiFi.localIP());            
	    client.println(WiFi.softAPIP());
            client.println("<p>RELE</p>");
            if (relayONState=="off") {
              client.println("<p><a href=\"/5/on\"><button class=\"button\">ON</button></a></p>");
            } else {
              client.println("<p><a href=\"/5/off\"><button class=\"button button2\">OFF</button></a></p>");
	      client.println(5*60-(currentMillis - previousMillis)/1000); // Jäljellä olevat sekunnit
            } 

            client.println("<p>VAHTIKOIRA</p>"); // testauksen vuoksi
            if (VahtikoiraState=="off") {
              client.println("<p><a href=\"/6/on\"><button class=\"button\">ON</button></a></p>");
            } else {
              client.println("<p><a href=\"/6/off\"><button class=\"button button2\">OFF</button></a></p>");
            }
	    
            client.println("<p>SININEN LEDI</p>"); // testauksen vuoksi
            if (SininenLediState=="off") {
              client.println("<p><a href=\"/4/on\"><button class=\"button\">ON</button></a></p>");
            } else {
              client.println("<p><a href=\"/4/off\"><button class=\"button button2\">OFF</button></a></p>");
            }
            client.println("</body></html>");
            client.println();
            break;
          } else { // if you got a newline, then clear currentLine
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    header = "";
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
