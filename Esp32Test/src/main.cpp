#include <Arduino.h>
#include <ESP32Servo.h> 
#include <WiFi.h>
#include <IOXhop_FirebaseESP32.h>
#include <ArduinoJson.h>
#include <OneWire.h>
#include <DallasTemperature.h>

//#define DS18B20 15
//OneWire oneWire(DS18B20);
//DallasTemperature Sensor(&oneWire);
//float leitura;

#define FIREBASE_HOST ""
#define FIREBASE_AUTH ""

#define PIN_SERVO 13
Servo myServo;

//int trigPin = 26;
//int echo = 27;

const char* WIFI_SSID = "MultilaserPRO_ZTE_2.4G_SX3SSe";
const char* WIFI_PASS = "Zxt7Zh9x";

void setup()
{
  Serial.begin(115200);

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }

  Serial.println();

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  
  myServo.attach(PIN_SERVO);
  myServo.write(180);

  //Sensor.begin();
  
  //pinMode(trigPin, OUTPUT);
  //pinMode(echoPin, INPUT);
}

void loop()
{
  if(Firebase.getBool("/status/coffe"))
  {
    myServo.write(0);
    delay(1000);
    myServo.write(180);
    //delay(5000);
  }
  
  /*Sensor.requestTemperatures();

  leitura = Sensor.getTempCByIndex(0);

  if(WiFi.status() == WL_CONNECTED)
  {
    Serial.println(leitura);
    Firebase.pushFloat("/temperature", leitura);
  } else {
    Serial.println("Conexão perdida");
  }*/

  /*int distancia;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  unsigned long tempoSom = pulseIn(echoPin, HIGH);
  distancia = tempoSom / 58;
  Serial.print("Distancia: ");
  Serial.print(distancia);
  Serial.println(" cm");
  */
  
  delay(5000);
}
