#define DEBUG 0

#include <SPI.h>         
#include <WiFi.h>
#include <WiFiUdp.h>
#include <PString.h>

#define WIFI
// Check the modified Twitter lib, with WIFI support
#include <Twitter.h>
  
#include <MFRC522.h>
#include <SD.h>
#include <Wire.h>
#include "NanoSatisfi_MLX90614.h"
NanoSatisfi_MLX90614 mlx;

#include <Adafruit_HTU21DF.h>
Adafruit_HTU21DF htu = Adafruit_HTU21DF();
#include <RC5.h>
RC5 *rc5;
#include "func.h"

MFRC522 mfrc522(SS_PIN, RST_PIN);	// Create MFRC522 instance
Twitter twitter("740118787-yM38RvSRo1VWLGqJKa32dbzctr9EYmKLrOAn72Fh"); //@AdrianNitu92
//Twitter twitter("3289784783-Pu57mOkeKTUzmvRekphPctsK9vfLGYj1BtZQYeO"); //Bucharest1HnS
// Initialize the client library
WiFiClient client[10];
File myFile;

int port = 9000;  //HERE
IPAddress server(192,168,1,132); 

int status = WL_IDLE_STATUS;
char ssid[] = "ALLVIEW V1_ViperS";  //  your network SSID (name) //HERE
char pass[] = "freesxale";       // your network password
//char ssid[] = "Robolab2";  //  youFile myFile;r network SSID (name)
//char pass[] = "W3<3R0bots";       // your network password
int keyIndex = 0;            // your network key Index number (needed only for WEP)

unsigned int localPort = 2390;      // local port to listen for UDP packets

IPAddress timeServer(129, 6, 15, 28); // time.nist.gov NTP server

const int NTP_PACKET_SIZE = 48; // NTP time stamp is in the first 48 bytes of the message

byte packetBuffer[ NTP_PACKET_SIZE]; //buffer to hold incoming and outgoing packets 

// A UDP instance to let us send and receive packets over UDP
WiFiUDP Udp;
unsigned long epoch;
unsigned long lastmillis = 0;
int STOP_FLAG = 0;
int STARTED_FLAG = 0;
int lastVisited = 0;

char * bioDataName[] = {"BodyTemp", "HeartRate", "NumSteps", "Distance", "AirTemp", "Humidity", "Consumption" };
const int bioDataSize = sizeof(bioDataName) / sizeof(char*);
float bioData[bioDataSize];
char * bioDataSI[bioDataSize] = {"C", "BPM", "", "m", "C", "%", "%" };

int treasures[2];
int gauss ;
char treasureBuffer[200];
PString TreasureHelper(treasureBuffer, sizeof(treasureBuffer));

void setup() 
{
  #warning : set all pin directions
  
 /* pinMode(SA, OUTPUT);
  pinMode(SB, OUTPUT);
  pinMode(SC, OUTPUT);
  */  Serial.begin(115200);
  rc5 = new RC5(5);
  while (!Serial);
  SPI.begin();			// Init SPI bus
  mfrc522.PCD_Init();		// Init MFRC522
  ShowReaderDetails();	// Show details of PCD - MFRC522 Card Reader details
  pinMode(4, OUTPUT);
  pinMode(SA, OUTPUT);
  pinMode(SB, OUTPUT);
  pinMode(SC, OUTPUT);
  pinMode(2,OUTPUT);
  digitalWrite(2, LOW);
  pinMode(5, INPUT);
  if (!SD.begin(4)) {
    Serial.println("SD card initialization failed!");
    return;
  }
  SDTest();
  WifiConnect();
  Udp.begin(localPort);
  Serial.println("Get Local Time");
  while(epoch == 0)
    NTPPart(); //make sure we have a ntp package
  lastmillis = millis();
  myFile = SD.open("/Bucharest1.csv",FILE_WRITE);
  if (htu.begin()) {
    //Serial.print("Temp: "); Serial.print(htu.readTemperature());
    bioData[4] = htu.readTemperature();
    //Serial.print("\t\tHum: "); Serial.println(htu.readHumidity());
    bioData[5] = htu.readHumidity();
  } else {
     Serial.println("Couldn't find sensor!");
  }
  toneFinishedSetup();
}

void WifiConnect()
{
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
}

void logString(char* dataString)
{
    if(! myFile) {
      Serial.println("No logging available");
      return;
    }
    #if DEBUG
    Serial.println("Sd card write:");
    Serial.println(dataString);
    #endif
    myFile.print(dataString);
    myFile.flush();
}
void logPString(PString dataString)
{
    if(! myFile) {
      Serial.println("No logging available");
      return;
    }
    #if DEBUG
    Serial.println("Sd card write:");
    Serial.println(dataString);
    #endif
    myFile.print(dataString);
    myFile.flush();
}


void SDTest()
{
   myFile = SD.open("/");
  
  if (myFile) {
     Serial.println("Sd card Contents");
     printDirectory(myFile, 0);
    Serial.println("SD card listing done!");
  }
  else 
  Serial.println("Can't open /");
}

void printDirectory(File dir, int numTabs) {
   while(true) {
     
     File entry =  dir.openNextFile();
     if (! entry) {
       // no more files
       //Serial.println("**nomorefiles**");
       break;
     }
     for (uint8_t i=0; i<numTabs; i++) {
       Serial.print('\t');
     }
     Serial.print(entry.name());
     if (entry.isDirectory()) {
       Serial.println("/");
       printDirectory(entry, numTabs+1);
     } else {
       // files have sizes, directories do not
       Serial.print("\t\t");
       Serial.println(entry.size(), DEC);
     }
     entry.close();
   }
}

void toneFinishedSetup()
{
  tone(3, 440);
  delay(300);
  noTone(3);
  delay(300);
  tone(3, 440);
  delay(300);
  tone(3, 440);
  delay(300);
  noTone(3);
}
void toneFinishedRFID()
{
  tone(3, 880);
  delay(300);
  noTone(3);
  delay(300);
  tone(3, 880);
  delay(300);
  noTone(3);
}


char lastWaypoint[20];
char waypoint[20];
char stopWaypoint[20];
PString waypointHelper(waypoint, sizeof(waypoint));
int scanTweetTag()
{
  unsigned long adcStart = micros();
  char twitterDataBuf[161];
  PString tpost(twitterDataBuf, 161);
  int k;
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    Serial.print("Am iesit print pula");
    return 0;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    Serial.print("Am iesit print penis");
    return 0;
  }
  STARTED_FLAG = 1;
  // Dump debug info about the card; PICC_HaltA() is automatically called
/*
  #if 0
  byte keyBuffer[18];
  byte byteCount;
  mfrc522.MIFARE_Key key;
  for (byte yy = 0; yy < 6; yy++) {
    key.keyByte[yy] = 0xFF;
  }
  int status = PCD_Authenticate(mfrc522.PICC_CMD_MF_AUTH_KEY_A, 0, &key, &(mfrc522.uid));
  if (status != 1) {
    Serial.print(F("MIFARE_Read() failed: "));
  }
  status = mfrc522.MIFARE_Read(0, keyBuffer, &byteCount);
  mfrc522.PICC_HaltA(); // Halt the PICC before stopping the encrypted session.
  mfrc522.PCD_StopCrypto1();
  if (status != 1) {
    Serial.print(F("MIFARE_Read() failed: "));
  }
  mystring.print("Reached waypoint:");
  waypointHelper.begin();
  for(k =0; k < 16; k++){
    waypointHelper.print(keyBuffer[k], HEX);
  }
  #else*/
  pinMode(2, HIGH);
  mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
  tpost.print("Reached waypoint:");
  waypointHelper.begin();
  for(k = 0; k < 16; k++){
    if(mfrc522.publicBuffer[k] < 16 )
        waypointHelper.print("0");
    waypointHelper.print(mfrc522.publicBuffer[k], HEX);
  }
  if(! strcmp(waypoint, lastWaypoint)){
    Serial.println("Same Tag");
    Serial.println(waypoint);
    Serial.println(lastWaypoint);
    pinMode(2, HIGH);
    return 1;
  }
  #if 0
  if(strcmp(waypoint, stopWaypoint)){
    Serial.println("STOP detected");
    Serial.println(waypoint);
    Serial.println(stopWaypoint);
    STOP_FLAG = 1;
  }
  #endif
  memcpy(lastWaypoint, waypoint, 20);
  tpost.print(waypoint);
  Serial.print("rfid tine doar ");
  Serial.println(micros() - adcStart);
  toneFinishedRFID();
  Serial.print(F("RFID data: 0x"));
  tpost.print(" at ");/*
  Serial.print(F("RFID final bits: 0x"));
  Serial.print(mfrc522.publicBuffer[16], HEX);
  Serial.print(mfrc522.publicBuffer[17], HEX);
  Serial.println();*/
  tpost.print(formatEpoch());
  Serial.println("Twitter bors:");
  Serial.println(tpost);
  if (twitter.post(tpost)) { //HERE
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
  lastVisited++;
  tpost.println();
  logPString(tpost);
  pinMode(2, HIGH);
  
  Serial.print("twitter tine doar ");
  Serial.println(micros() - adcStart);
  
  return 1;
}

unsigned long timeStamp[15];
unsigned long timeout[15];
bool at_treasure = false;

void loop()
{
// BIODATA=    {"BodyTemp", "HeartRate", "NumSteps", "Distance", "AirTemp", "Humidity", "Consumption" };
  //{HR, accel, env temp & hum, body temp, consumotopn, Server, twitter,
  //  RFID, stage2}
  timeStamp[0] = timeStamp[1] = timeStamp[2] = 
  timeStamp[3] = timeStamp[4] = timeStamp[5] = 
  timeStamp[6] = timeStamp[7] = millis(); // timeStamp[8] is an exception
  timeStamp[9] = 1500 + (timeStamp[10] = 1500 + (timeStamp[11] = 
  1500 + (timeStamp[12] = 1500 + (timeStamp[13] = 1500 + (timeStamp[14] = timeStamp[5] + 1500)))));
  timeout[0] = timeout[1] = 25; //FAST
  timeout[2] = timeout[3] = timeout[4] = 5000;
  timeout[5] = timeout[9] = timeout[10] = timeout[11] = timeout[12] = timeout[13] = timeout[14] = 10000;
  timeout[6] = 60000;
  timeout[7] = 1000;
  timeout[8] = 15000;
  pinMode(2, LOW);
  while(1) {
   if(STOP_FLAG)
    while(1);
      if(timeStamp[0] + timeout[0] <  millis()){
         int z = readADC(HR); //XXX
         //check over a prag
         //check local peak
         //get last peak time location
         unsigned long perioada = 750; //ms
         bioData[0] = 60.0 * (1000.0/perioada);
         //do smth XXX
         timeStamp[0] = millis();
         Serial.println("HR");
         continue;
      }
      if(timeStamp[1] + timeout[1] <  millis()){
        while(2){
         int x = readADC(X);
         int y = readADC(Y);
         int z = readADC(Z);
         static int THRESHOLD = 15;
         const int UPRIGHT = 950;
         const int INFATZA = 850;
         //int value = sqrt(x*x + y*y + z * z);
  
         int value = z;
         static unsigned long ms = millis();
         // daca nu e pe langa UPRIGHT SI NICI pe langa INFATZA probabil e un step
         // asteapta pana la resetare pe UPRIGHT
         if( ms + 600 < millis() && 
         (value - THRESHOLD > UPRIGHT || value + THRESHOLD < UPRIGHT)){
           //if(!(value - THRESHOLD > INFATZA || value + THRESHOLD < INFATZA)) cacatul asta NU merge :(
           {
                ms = millis();
                if(STARTED_FLAG){
                  bioData[2] +=1;
                  bioData[3] +=0.41;
                }
                Serial.println("Crecă e un pas aici?");
            }
         }
         Serial.println(value);
         Serial.println("ACC");
         timeStamp[1] = millis();
        }
         continue;
      }
      if(timeStamp[2] + timeout[2] <  millis()){
         bioData[4] = htu.readTemperature();
         bioData[5] = htu.readHumidity(); //XXX do the split read thing? :)
         timeStamp[2] = millis();
         Serial.println("temp hum");         
         continue;
      }
      if(timeStamp[3] + timeout[3] <  millis()){
         int z = readADC(TEMP);
         timeStamp[3] = millis();
         Serial.println("TEMP");         
         continue;
      }
      if(timeStamp[4] + timeout[4] <  millis()){
         float z = readADC(INA);
         z = (z / 1024.0) * 3.3; //get voltage back
         // 20 * value = volts -> volts = I * 0.2
         // I = 100 * (ADC/3.3) A
         bioData[6] = z / 4.0;  
         timeStamp[4] = millis();
         Serial.println("INA"); 
         Serial.println(bioData[6]);        
         continue;
      }
      if(timeStamp[5] + timeout[5] <  millis()){
          if(STARTED_FLAG){
            dataToServer(0);
            Serial.println("Server");
          }
         timeStamp[5] = millis();
         continue;
      }
      if(timeStamp[9] + timeout[9] <  millis()){
          if(STARTED_FLAG){
            dataToServer(1);
            Serial.println("Server");
          }
         timeStamp[9] = millis();
         continue;
      }
      if(timeStamp[10] + timeout[10] <  millis()){
          if(STARTED_FLAG){
            dataToServer(2);
            Serial.println("Server");
          }
         timeStamp[10] = millis();
         continue;
      }
      if(timeStamp[11] + timeout[11] <  millis()){
          if(STARTED_FLAG){
            dataToServer(3);
            Serial.println("Server");
          }
         timeStamp[11] = millis();
         continue;
      }
      if(timeStamp[12] + timeout[12] <  millis()){
          if(STARTED_FLAG){
            dataToServer(4);
            Serial.println("Server");
          }
         timeStamp[12] = millis();
         continue;
      }
      if(timeStamp[13] + timeout[13] <  millis()){
          if(STARTED_FLAG){
            dataToServer(5);
            Serial.println("Server");
          }
         timeStamp[13] = millis();
         continue;
      }
      if(timeStamp[14] + timeout[14] <  millis()){
          if(STARTED_FLAG){
            dataToServer(6);
            Serial.println("Server");
          }
         timeStamp[14] = millis();
         continue;
      }
      if(timeStamp[6] + timeout[6] <  millis()){
          if(STARTED_FLAG){
            tweetData();
            Serial.println("Tweet");
          }
         timeStamp[6] = millis();
         continue;
      }
      if (at_treasure && (timeStamp[8] + timeout[8] > millis())) {
        TreasureData();
        continue;
      } else {
        at_treasure = 0;
      }
      if(timeStamp[7] + timeout[7] <  millis()){
         Serial.println("RFID");
         at_treasure |= scanTweetTag();
         timeStamp[7] = millis();
         timeStamp[8] = millis(); //for timeout[8] seconds we have the sensors ON
         treasures[0] = NOTHING;
         treasures[1] = NOTHING;
         continue;
      }
  }
}

void TreasureData()
{
   noTone(3);
   tone(3, 440);
   float celsius = 0;
   //XXXcelsius = mlx.getTemp();
   if(celsius > 35 || celsius < 18 )
   {
     TreasureHelper.begin();
     TreasureHelper.print("GET /putTreasure?");
     TreasureHelper.print("time=");
     TreasureHelper.print(epoch);
     TreasureHelper.print("&checkpoint=");
     TreasureHelper.print(lastVisited);
     TreasureHelper.print("&value=");
     TreasureHelper.print(celsius);
     TreasureHelper.print("*C&name=");
     TreasureHelper.print("TEMPERATURE");
     if(treasures[0] == NOTHING) {
       treasures[0] = TEMPERATURE;
     } else if(treasures[1] == NOTHING && treasures[0] != TEMPERATURE) {
       treasures[1] = TEMPERATURE;
     }
     singleDataToServer(&TreasureHelper, 9);
   }
   noTone(3);
   {
     //MIC // teoretic ca la heartrate, dar mama lui de heartrate
     # if 0  
      MIC bors;
     #else
       int static lastGauss = readADC(HALL);
       tone(3, 660);
       Serial.print("Gaussiana");
       Serial.print(gauss);
       Serial.print(" ");
       Serial.println(lastGauss);
       gauss = readADC(HALL);
       if(gauss - 50 > lastGauss || gauss +50 < lastGauss){
         TreasureHelper.begin();
         TreasureHelper.print("GET /putTreasure?");
         TreasureHelper.print("time=");
         TreasureHelper.print(epoch);
         TreasureHelper.print("&checkpoint=");
         TreasureHelper.print(lastVisited);
         TreasureHelper.print("&value=");
         TreasureHelper.print(gauss);
         TreasureHelper.print("G&name=");
         TreasureHelper.print("GAUSS");
         if(treasures[0] == NOTHING) {
           treasures[0] = GAUSS;
         } else if(treasures[1] == NOTHING && treasures[0] != GAUSS) {
           treasures[1] = GAUSS;
         }
         singleDataToServer(&TreasureHelper, 9);
      }
      static long unsigned timesl = millis();
      if(timesl + 1000 < millis()){
        lastGauss = gauss;
        timesl = millis();
      }
     #endif
   }
   {
     int red = readADC(R);
     int gre = readADC(G);
     int blu = readADC(B);         
     Serial.println("Leduri:");
     Serial.println(red);
     Serial.println(gre);
     Serial.println(blu);
   }
   {
     static unsigned long hzStart = 0;
     unsigned long duration;
     const int THRESHOLD = 5;
     if(readADC(SONIC) > THRESHOLD && !hzStart){ //x idk about this one, sa
       hzStart = millis();
     } else {
       duration = millis() - hzStart;
       hzStart = 0;
       //XXX send data ?
     }
   }
   
  byte toggle=0;
  byte address=0;
  byte command=0;
  noTone(3);
  tone(3, 660);
  unsigned long initialTime = micros();
  while(1){
    if(initialTime + 8*14000 < micros()) {
      break;
    }
    if (rc5->read(&toggle, &address, &command))
    {
       TreasureHelper.begin();
       TreasureHelper.print("GET /putTreasure?");
       TreasureHelper.print("time=");
       TreasureHelper.print(epoch);
       TreasureHelper.print("&checkpoint=");
       TreasureHelper.print(lastVisited);
       TreasureHelper.print("&value=0x");
       TreasureHelper.print(toggle, HEX);
       TreasureHelper.print("0x");
       TreasureHelper.print(address, HEX);
       TreasureHelper.print("0x");
       TreasureHelper.print(command, HEX);
       TreasureHelper.print("&name=");
       TreasureHelper.print("IR");
       singleDataToServer(&TreasureHelper, 9);
       if(treasures[0] == NOTHING) {
         treasures[0] = IR;
       } else if(treasures[1] == NOTHING && treasures[0] != IR) {
         treasures[1] = IR;
       }
       break;
    }
  }
  noTone(3);
  Serial.print("Treasures are");
  Serial.print(treasures[0]);
  Serial.print(treasures[1]);
}
void tweetData()
{
  char twitterDataBuf[161];
  PString tpost(twitterDataBuf, 161);
  tpost.print("Bucharest1 Data:");
  for(int k = 0; k < bioDataSize; k++)
  {
    tpost.print(bioDataName[k]);
    tpost.print(" ");    
    tpost.print(bioData[k]);
    tpost.print(bioDataSI[k]);
    tpost.print(",");
  }
  
  tpost.print("at");
  tpost.print(formatEpoch());
  Serial.println("Twitter message is");
  Serial.println(tpost);
  if (twitter.post(tpost)) { //HERE
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
  tpost.println();
  logPString(tpost);
}

void singleDataToServer(PString * req, int id)
{
        client[id].stop();
  unsigned long adcStart = micros();
   if (client[id].connect("randomtest.ngrok.io", 80)) { 
      req->println(" HTTP/1.1");
      req->println("Host: randomtest.ngrok.io");
      req->println("User-Agent: ArduinoWiFi/1.1");
      req->println("Connection: close");
      req->print("\n\n");
      client[id].print(*req);
      Serial.println(*req);
      #if DEBUG
      while(client.available()){
	char c = client.read();
            Serial.print(c);
      }
      //delay(300);
      #endif
    } else {
      Serial.println("Can't connect to Server");
   }
   
  Serial.print("ioana tine doar ");
  Serial.println(micros() - adcStart);
  logPString(*req);
}
char buffy[150];
PString req(buffy, 150);
void dataToServer(int k)
{
  // Make a HTTP request:
    req.begin();
    req.print("GET /put");
    req.print(bioDataName[k]);
    req.print("?statie=");
    req.print(lastVisited);
    req.print("&time=");
    updateEpoch();
    req.print(epoch);
    req.print("007");
    req.print("&value=");
    req.print(bioData[k]);
    singleDataToServer(&req,k);
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
    // print Unix time:
    Serial.print("The UTC time is ");       // UTC is the time at Greenwich Meridian (GMT)
    Serial.println(epoch);                           
    Serial.println(formatEpoch());
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

int readADC(int input)
{
  int ret = -1;
   if(input == HR ||
   input == HALL ||
   input == MIC ||
   input == R ||
   input == G ||
   input == B ||
   input == SONIC ||
   input == INA ||
   input == TEMP){
     setADCMux(input);
//HERE
     ret = analogRead(A0);
   } else {
     if(input == X)
       ret = analogRead(A1);
     if(input == Y)
       ret = analogRead(A2);
     if(input == Z)
       ret = analogRead(A3);
   }
   return ret;
}

int estimateGauss(int adc)
{
   int ret;
   //Serial.println(adc);
//   ret = (adc - 1024/3) * 1  - 1000;
   ret = ((adc*3.3)/512.0 - 5.0 ) * 333.3;
   //Serial.println(ret);
   return adc;
   //return ret;
 }

void setADCMux(int input)
{
  digitalWrite(SA, (((uint8_t)input) & 1) != 0 ? HIGH : LOW);
  digitalWrite(SB, (((uint8_t)input) & 2) != 0 ? HIGH : LOW);
  digitalWrite(SC, (((uint8_t)input) & 4) != 0 ? HIGH : LOW);
  digitalWrite(BODYS, (((uint8_t)input) & 8) != 0 ? HIGH : LOW);
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
unsigned long updateEpoch()
{
    unsigned long mm = millis();
    while(mm > lastmillis + 1000 )
    {
      lastmillis +=1000;
      epoch++;
    }
    return epoch;
}
char * formatEpoch()
{
    fe.begin();
    updateEpoch();
    epoch +=3 * 3600;
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
    epoch -=3 * 3600;
    return formattedEpoch; 
}



