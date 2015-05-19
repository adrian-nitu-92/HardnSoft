#include <SPI.h>         
#include <WiFi.h>
#include <WiFiUdp.h>
#include <PString.h>

#define WIFI
// Check the modified Twitter lib, with WIFI support
#include <Twitter.h>

#include <MFRC522.h>

#include<TimerOne.h>

#define RST_PIN		9		// 
#define SS_PIN		10		//

MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance
//Twitter twitter("740118787-yM38RvSRo1VWLGqJKa32dbzctr9EYmKLrOAn72Fh"); //@AdrianNitu92
Twitter twitter("3289784783-Pu57mOkeKTUzmvRekphPctsK9vfLGYj1BtZQYeO"); //Bucharest1HnS
// Initialize the client library
WiFiClient client;

int port = 9000;  //HERE
int halfSec = 0;
IPAddress server(192,168,1,132); 

int status = WL_IDLE_STATUS;
char ssid[] = "ALLVIEW V1_ViperS";  //  your network SSID (name) //HERE
char pass[] = "freesxale";       // your network password
//char ssid[] = "Robolab2";  //  your network SSID (name)
//char pass[] = "W3<3R0bots";       // your network password
int keyIndex = 0;            // your network key Index number (needed only for WEP)

unsigned int localPort = 2390;      // local port to listen for UDP packets

IPAddress timeServer(129, 6, 15, 28); // time.nist.gov NTP server

const int NTP_PACKET_SIZE = 48; // NTP time stamp is in the first 48 bytes of the message

byte packetBuffer[ NTP_PACKET_SIZE]; //buffer to hold incoming and outgoing packets 

// A UDP instance to let us send and receive packets over UDP
WiFiUDP Udp;
unsigned long epoch;
unsigned long lastMicros = 0;

char buf[1000];
PString mystring(buf, sizeof(buf));
void setup() 
{
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  SPI.begin();			// Init SPI bus
  mfrc522.PCD_Init();		// Init MFRC522
  ShowReaderDetails();	// Show details of PCD - MFRC522 Card Reader details
  Serial.println(F("Scan PICC to see UID, type, and data blocks..."));


  // check for the presence of the shield:
  if (WiFi.status() == WL_NO_SHIELD) {
    Serial.println("WiFi shield not present"); 
    // don't continue:
    while(true);
  } 
  String fv = WiFi.firmwareVersion();
  if( fv != "1.1.0" )
    Serial.println("Please upgrade the firmware");
  // attempt to connect to Wifi network:
  while ( status != WL_CONNECTED) { 
    Serial.print("Attempting to connect to SSID: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network. Change this line if using open or WEP network:    
    status = WiFi.begin(ssid, pass); //HERE
    //status = WiFi.begin("wireless.usv.ro");
    // wait 10 seconds for connection:
    delay(10000);
  }
  Serial.println("Connected to wifi");
  printWifiStatus();
  
  Udp.begin(localPort);
  Serial.println("Get Local Time");
  while(epoch == 0)
    NTPPart(); //make sure we have a ntp package
  lastMicros = micros();
}

char lastWaypoint[20];
char waypoint[20];
PString waypointHelper(waypoint, sizeof(waypoint));
void loop()
{
  int k;
  mystring.begin();
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  // Dump debug info about the card; PICC_HaltA() is automatically called
  mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
  mystring.print("Reached waypoint:");
  waypointHelper.begin();
  for(k =0; k < 16; k++){
    waypointHelper.print(mfrc522.publicBuffer[k], HEX);
  }
  if(! strcmp(waypoint, lastWaypoint))
    return;
  memcpy(lastWaypoint, waypoint, 20);
  Serial.print(F("RFID data: 0x"));
  mystring.print(waypointHelper);
  mystring.print(" at ");
  Serial.print(F("RFID final bits: 0x"));
  Serial.print(mfrc522.publicBuffer[16], HEX);
  Serial.print(mfrc522.publicBuffer[17], HEX);
  Serial.println();
  mystring.print(formatEpoch());
  Serial.println("Twitter bors:");
  Serial.println(mystring);
  if (twitter.post(mystring)) { //HERE
    int status = twitter.wait(&Serial);
    Serial.print("Status is");
    Serial.println(status);
    if (status == 200) {
      Serial.println("Twitter ok");
    } else {
      Serial.print("Twitter failed : code ");
      Serial.println(status);
    }
  }
  
 if (client.connect(server, port)) { //HERE
      Serial.println("connected");
      // Make a HTTP request:
      char buffy[60];
      PString req(buffy, 60);
      req.print("GET /putNumSteps?time=");
      req.print(epoch);
      req.print(".");
      if(halfSec)
         req.print("50");
      else
         req.print("00");
      req.print("&value=42"); //XXX
      Serial.print(req);
      client.print(req);
      client.println();
      client.println();
      client.flush();
      client.stop();
    } else {
      Serial.println("Can't connect to Server");
}
}

unsigned long NTPPart()
{
  sendNTPpacket(timeServer); // send an NTP packet to a time server
    // wait to see if a reply is available
  delay(1000);  
  Serial.println( Udp.parsePacket() );
  if ( Udp.parsePacket() ) { 
    Serial.println("packet received"); 
    // We've received a packet, read the data from it
    Udp.read(packetBuffer,NTP_PACKET_SIZE);  // read the packet into the buffer

    //the timestamp starts at byte 40 of the received packet and is four bytes,
    // or two words, long. First, esxtract the two words:

    unsigned long highWord = word(packetBuffer[40], packetBuffer[41]);
    unsigned long lowWord = word(packetBuffer[42], packetBuffer[43]);  
    // combine the four bytes (two words) into a long integer
    // this is NTP time (seconds since Jan 1 1900):
    unsigned long secsSince1900 = highWord << 16 | lowWord;  
    Serial.print("Seconds since Jan 1 1900 = " );
    Serial.println(secsSince1900);               

    // now convert NTP time into everyday time:
    Serial.print("Unix time = ");
    // Unix time starts on Jan 1 1970. In seconds, that's 2208988800:
    const unsigned long seventyYears = 2208988800UL;     
    // subtract seventy years:
    epoch = secsSince1900 - seventyYears;
    epoch += 3*3600; //set Romania time :)
    // print Unix time:
    Serial.print("The UTC time is ");       // UTC is the time at Greenwich Meridian (GMT)
    Serial.println(epoch);                           
    Serial.println(formatEpoch());
    mystring.print(formatEpoch());
  }
  // wait ten seconds before asking for the time again
//  delay(10000); 
  
  return epoch;
}
// send an NTP request to the time server at the given address 
unsigned long sendNTPpacket(IPAddress& address)
{
  //Serial.println("1");
  // set all bytes in the buffer to 0
  memset(packetBuffer, 0, NTP_PACKET_SIZE); 
  // Initialize values needed to form NTP request
  // (see URL above for details on the packets)
  //Serial.println("2");
  packetBuffer[0] = 0b11100011;   // LI, Version, Mode
  packetBuffer[1] = 0;     // Stratum, or type of clock
  packetBuffer[2] = 6;     // Polling Interval
  packetBuffer[3] = 0xEC;  // Peer Clock Precision
  // 8 bytes of zero for Root Delay & Root Dispersion
  packetBuffer[12]  = 49; 
  packetBuffer[13]  = 0x4E;
  packetBuffer[14]  = 49;
  packetBuffer[15]  = 52;
  
  //Serial.println("3");

  // all NTP fields have been given values, now
  // you can send a packet requesting a timestamp: 		   
  Udp.beginPacket(address, 123); //NTP requests are to port 123
  //Serial.println("4");
  Udp.write(packetBuffer,NTP_PACKET_SIZE);
  //Serial.println("5");
  Udp.endPacket(); 
  //Serial.println("6");
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}


void ShowReaderDetails() {
  // Get the MFRC522 software version
  byte v = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  Serial.print(F("MFRC522 Software Version: 0x"));
  Serial.print(v, HEX);
  if (v == 0x91)
    Serial.print(F(" = v1.0"));
  else if (v == 0x92)
    Serial.print(F(" = v2.0"));
  else
    Serial.print(F(" (unknown)"));
  Serial.println("");
  // When 0x00 or 0xFF is returned, communication probably failed
  if ((v == 0x00) || (v == 0xFF)) {
    Serial.println(F("WARNING: Communication failure, is the MFRC522 properly connected?"));
  }
}

char formattedEpoch[25];
PString fe(formattedEpoch, sizeof(formattedEpoch));
char * formatEpoch()
{  
    unsigned long mm = micros();
    epoch += (mm - lastMicros)/1000000;
    lastMicros = mm; 
    fe.begin();
    // print the hour, minute and second:
    fe.print((epoch  % 86400L) / 3600); // print the hour (86400 equals secs per day)
    fe.print(':'); 
    if ( ((epoch % 3600) / 60) < 10 ) {
      // In the first 10 minutes of each hour, we'll want a leading '0'
      fe.print('0');
    }
    fe.print((epoch  % 3600) / 60); // print the minute (3600 equals secs per minute)
    fe.print(':'); 
    if ( (epoch % 60) < 10 ) {
      // In the first 10 seconds of each minute, we'll want a leading '0'
      fe.print('0');      
    }
    fe.print(epoch %60); // print the second
    fe.print(".");
    fe.print((mm % 1000000) / 10000); 
    return formattedEpoch; 
}



