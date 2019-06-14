/*********
  Rui Santos
  Complete project details at http://randomnerdtutorials.com  
*********/

// Load Wi-Fi library
#include <ESP8266WiFi.h>

// Replace with your network credentials
const char* ssid     = "Jorpakko";
const char* password = "Juhannusyona";

// Set web server port number to 80
WiFiServer server(80);

// Variable to store the HTTP request
String header;

// Auxiliar variables to store the current output state
String relayONState = "off";
String relayOFFState = "off";
String SininenLediState = "off";

// Assign output variables to GPIO pins
const int relayON = 5;
const int relayOFF = 12;
const int SininenLedi = 4;
const int Nappi = 14;

unsigned long previousMillis = 0;
const long interval = 600000; // 10 minuuttia

void setup() {
  Serial.begin(115200);
  // Initialize the output variables as outputs
  pinMode(relayON, OUTPUT);
  pinMode(relayOFF, OUTPUT);
  pinMode(SininenLedi, OUTPUT);
  pinMode(Nappi, INPUT);
  // Set outputs to LOW
  digitalWrite(relayON, LOW);
  digitalWrite(relayOFF, LOW);
  digitalWrite(SininenLedi, LOW);

  // Connect to Wi-Fi network with SSID and password
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  // Print local IP address and start web server
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
  digitalWrite(SininenLedi, HIGH);
}

void loop(){
  WiFiClient client = server.available();   // Listen for incoming clients
  unsigned long currentMillis = millis();
  if (  relayONState == "on" ) {
      if (currentMillis - previousMillis >= interval) {
      Serial.println("GPIO 5 timer off");
      relayONState = "off";
      digitalWrite(relayON, LOW); } }
  if ( digitalRead(Nappi) == 0) {
    previousMillis = currentMillis; 
    if (  relayONState == "off" ) {
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
          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();
            
            // turns the GPIOs on and off
            if (header.indexOf("GET /5/on") >= 0) {
              Serial.println("GPIO 5 on");
              relayONState = "on";
              digitalWrite(relayON, HIGH);
	      previousMillis = currentMillis; 
            } else if (header.indexOf("GET /5/off") >= 0) {
              Serial.println("GPIO 5 off");
              relayONState = "off";
              digitalWrite(relayON, LOW);
            } else if (header.indexOf("GET /4/on") >= 0) {
              Serial.println("GPIO 4 on");
              SininenLediState = "on";
              digitalWrite(SininenLedi, HIGH);
            } else if (header.indexOf("GET /4/off") >= 0) {
              Serial.println("GPIO 4 off");
              SininenLediState = "off";
              digitalWrite(SininenLedi, LOW);
            }
            
            // Display the HTML web page
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            client.println("<link rel=\"icon\" href=\"data:,\">");
            // CSS to style the on/off buttons 
            // Feel free to change the background-color and font-size attributes to fit your preferences
            client.println("<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}");
            client.println(".button { background-color: #195B6A; border: none; color: white; padding: 16px 40px;");
            client.println("text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}");
            client.println(".button2 {background-color: #77878A;}</style></head>");
            
            // Web Page Heading
            client.println("<body><h1>KAHVINKEITIN</h1> ");
            
            // Display current state, and ON/OFF buttons for GPIO 5  
            client.println("<p>RELE</p>");
            // If the relayONState is off, it displays the ON button       
            if (relayONState=="off") {
              client.println("<p><a href=\"/5/on\"><button class=\"button\">ON</button></a></p>");
            } else {
              client.println("<p><a href=\"/5/off\"><button class=\"button button2\">OFF</button></a></p>");
	      client.println(600-(currentMillis - previousMillis)/1000);
            } 
               

            // Display current state, and ON/OFF buttons for GPIO 4  
            client.println("<p>SININEN LEDI </p>");
            // If the SininenLediState is off, it displays the ON button       
            if (SininenLediState=="off") {
              client.println("<p><a href=\"/4/on\"><button class=\"button\">ON</button></a></p>");
            } else {
              client.println("<p><a href=\"/4/off\"><button class=\"button button2\">OFF</button></a></p>");
            }
            client.println("</body></html>");
            
            // The HTTP response ends with another blank line
            client.println();
            // Break out of the while loop
            break;
          } else { // if you got a newline, then clear currentLine
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    // Clear the header variable
    header = "";
    // Close the connection
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
