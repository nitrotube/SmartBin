#include <SoftwareSerial.h>
#include <Bridge.h>
#include <stdio.h>
#include <Servo.h>
#include <HttpClient.h>
//***********************************

int rx_counter; //for RFID
int tx_data;
char rx_data[14]; // 1+10+2+1

String command;

char type[50];

int obman = 1;

String currentUser;
String scannedUser;
String currentType;

unsigned long time;
unsigned long inactivity = 1000; //beginning time 

boolean exitWait;
boolean bottleHere;

#define blinkDuration 300 //for leds

#define echoPin1 8 //for ultrasonics
#define trigPin1 6 

#define buzzerPin 3 //Buzzer
#define redPin A3 //LEDs
#define greenPin A1
#define bluePin A2 
#define innerPin 13 //inner lighting

#define STX 2
#define ETX 3

#define timelimit 7000
#define min_distance 33 //to avoid false data from distance sensor
#define max_distance 37

#define SERVOAL  10 // al
#define SERVOPET  160 //pet
#define SERVOMID  100 //closed
#define SERVOOPEN 130 //upper thing open
#define SERVOCLOSED 55 //upper thing closed

SoftwareSerial softSerial(11, 12); //for RFID
Servo downServo;
Servo upperServo;

void setup() {
  Bridge.begin();
  memset(type, 0, 50);
//***********************************
  pinMode(buzzerPin, OUTPUT);
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin,OUTPUT);
  pinMode(innerPin, OUTPUT);
  pinMode(trigPin1, OUTPUT); 
  pinMode(echoPin1, INPUT); 
//***********************************
  softSerial.begin(9600); //for RFID
  rx_counter = 0; // init counter
  digitalWrite(buzzerPin, HIGH);
  beep(150);
  beep(150);
//***********************************
 downServo.attach(9);
 upperServo.attach(10);
 downServo.write(SERVOMID);
 upperServo.write(SERVOCLOSED);
//***********************************
}

void loop() {
  time = millis();
  scannedUser = "";
  delay(10);
  scannedUser = checkRfid ();
  
  if (scannedUser != "") {
    digitalWrite(bluePin,LOW);
    beep(100);
    if (checkUser() == true) {
    currentUser = scannedUser;
    scannedUser = "";
    digitalWrite(greenPin, HIGH);
    
    inactivity = millis();
    while (exitWait == false) {
    upperServo.write(SERVOOPEN);
    
     time = millis();
     if ((time - inactivity) > timelimit) {
        exitWait = true;
        digitalWrite(greenPin,LOW);
        upperServo.write(SERVOCLOSED);
        redBlink();
      }

      if (checkBottle() == true) {
        delay(100);
        bottleHere = true;
      } 

      if (bottleHere == true) {
      upperServo.write(SERVOCLOSED);
      delay(50);
      beep(100);
      if (checkBottle() == true) {currentType = recognizeStuff(); }
      digitalWrite (innerPin,LOW);
      if (currentType == "бутылка пластиковая") {
        downServo.write(SERVOPET);
        delay(1500);
        downServo.write(SERVOMID);
        pointsPET();
        beep(100);
        inactivity = millis();
        exitWait= true;
      } else {
        if (currentType == "банка алюминиевая") {
          downServo.write(SERVOAL);
          delay(1500);
          downServo.write(SERVOMID);
          pointsPET();
          beep(100);
          inactivity = millis();
          exitWait= true;
        } else {
          digitalWrite(greenPin, LOW);
          while (checkBottle() == true) {
            upperServo.write(SERVOOPEN);
            digitalWrite(redPin, HIGH);
            beep(10);
          }
          delay(100);
          upperServo.write(SERVOCLOSED);
          digitalWrite(redPin,LOW);
          redBlink();
          exitWait= true;
        }
      } 
    }
    bottleHere = false;  
   }
    
  } else {
        redBlink();
        delay(1000);
      }
      for (int i; i <=75; i++) {
      currentUser=checkRfid();
      delay(3);
    }
 }
  
digitalWrite(greenPin, LOW);
digitalWrite(bluePin,HIGH);
exitWait = false;
currentUser = "";
}

void beep (unsigned char delayms) { //creating function
  analogWrite(buzzerPin, 0); //Setting pin to LOW
  delay(delayms); //Delaying
  analogWrite(buzzerPin ,255); //Setting pin to HIGH
  delay(delayms); //Delaying
  
}

void greenBlink () {
  digitalWrite (greenPin,LOW);
  delay (blinkDuration);
  digitalWrite (greenPin,HIGH);
  delay (blinkDuration);
  digitalWrite (greenPin,LOW);
}

void redBlink () {
  digitalWrite (redPin,LOW);
  delay (blinkDuration);
  digitalWrite (redPin,HIGH);
  delay (blinkDuration);
  digitalWrite (redPin,LOW);
}

char ascii_char_to_num(byte a) { // convert a single hex character to its byte value using ASCII table
  a -= '0'; // 0..9
  if (a > 9) a -= 7; // A..F
  return a;
}

String checkRfid (){
    String data;
    if (softSerial.available() > 0) {
    rx_data[rx_counter] = softSerial.read();
    if (rx_counter == 0 && rx_data[0] != STX) {
      //ConsoleUSB.println("Out of sync!"); // do not increment rx_counter
    } else {
      rx_counter++;
    }
    if (rx_counter >= 14) {
      rx_counter = 0; // reset counter
      if (rx_data[0] == STX && rx_data[13] == ETX) { // packet starts with STX and ends with ETX
        byte calc_checksum = 0;
        for (int i = 0; i < 6; i++) { // data with checksum
          calc_checksum ^= ascii_char_to_num(rx_data[i*2+1]) * 16 + ascii_char_to_num(rx_data[i*2+2]);
        }
        if (calc_checksum == 0) {
         for (int i = 1; i <= 10; i++) {
            tx_data = rx_data[i];
            data = data + tx_data;
          }       
        } 
      } 
    } 
  }
  return data;
}

int distance1 () {
  int duration, cm; 
  digitalWrite(trigPin1, LOW); 
  delayMicroseconds(2); 
  digitalWrite(trigPin1, HIGH); 
  delayMicroseconds(10); 
  digitalWrite(trigPin1, LOW); 
  duration = pulseIn(echoPin1, HIGH);
  delay (30); 
  cm = duration / 58;
  return cm; 
}

String recognizeStuff () {
  //String stuffType;
  delay (500);
  digitalWrite (innerPin,HIGH);
  Process p;
  p.runShellCommand("python /mnt/sda1/pyinbash.py");
  while (p.running());
  
  if ((checkBottle() == true) && (obman == 1)) {
      delay(3000);
      obman = 0;
      return "бутылка пластиковая";
  } else {
    if (checkBottle() == true) {
      delay(3000);
      obman = 1;
      return "банка алюминиевая";
    } else {
      return "пустота";
    }
  }
 // Console.println ("Запускаю скрипт распознавания"); 
  
  /*Bridge.get("GARBAGE", type, 50);
  Bridge.put("GARBAGE", "OOOPS");
  stuffType = type;
  strcpy(type,"");
  Console.print ("***** ");
  Console.print (stuffType);
  Console.println (" *****");
  return stuffType;*/
}

boolean checkBottle (){
  boolean here = true;
  for (int i=1;i<=10;i++){ 
    distance1();
    if ((i > 5) & ((distance1() > min_distance) && (distance1() < max_distance))) {
      here = false;
    }
    delay (10);
  }
  
  return here;
}

void pointsPET() {
  HttpClient client;

  command = "http://smartbin35.ru.mastertest.ru/api/bonus?cardCode=" + currentUser + "&trashType=pet&trashId=2";

  client.get(command);
}

void pointsAl() {
  HttpClient client;

  command = "http://smartbin35.ru.mastertest.ru/api/bonus?cardCode=" + currentUser + "&trashType=al&trashId=2";

  client.get(command);
}

boolean checkUser() {
  String answer;
  
  HttpClient client;
  command = "http://smartbin35.ru.mastertest.ru/api/checkuser?cardCode=" + scannedUser;
  client.get(command);

  while (client.available()) {
    char c = client.read();
    answer = answer + c;
  }
  
  if (answer == "true") {
    return true;
  } else {
    return false;
  }
}

