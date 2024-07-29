#include <IOXhop_FirebaseESP32.h>
#include <IOXhop_FirebaseStream.h>

#include <DHT22.h>
//define pin data
#define pinDATA 14  // SDA, or almost any other I/O pin
#include <WiFi.h>
#include "time.h"
#define FIREBASE_AUTH "https://dht22-2b353-default-rtdb.firebaseio.com/"
#define FIREBASE_HOST "AIzaSyCNyiQqFqFN5jvo4uOadMUwt2y1Ml7LHgE"


const char* ssid = "Ny Aina Solofo";  // Nom de la box Wi-Fi
const char* password = "00000000";    // MDP de la box Wi-Fi

const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 3600 * 1;
const int daylightOffset_sec = 3600 * 0;

DHT22 dht22(pinDATA);

void setup() {
  Serial.begin(115200);  //1bit=10µs
  Serial.println("\ntest capteur DTH22");
  WiFi.mode(WIFI_STA);  // Optional
  WiFi.begin(ssid, password);
  Serial.println("\nConnecting");

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(100);
  }
  Serial.print("Local ESP32 IP: ");
  Serial.println(WiFi.localIP());
  Firebase.begin(FIREBASE_AUTH, FIREBASE_HOST);

  // On configure le seveur NTP
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void loop() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
  }
  Serial.print(&timeinfo, "%A , %B-%d-%Y , %H:%M:%S , ");

  float t = dht22.getTemperature();
  float h = dht22.getHumidity();
  // set value
  Firebase.setFloat("dht22/Humidity", h);
  if (Firebase.failed()) {
    Serial.println("setting / numbre failed:");
    Serial.println(Firebase.error());
    return;
  }
  Firebase.setFloat("dht22/Temperature", t);
  if (Firebase.failed()) {
    Serial.println("setting / numbre failed:");
    Serial.println(Firebase.error());
    return;
  }

  Serial.print(h, 1);
  Serial.print(" , ");
  Serial.print(t, 1);
  Serial.print(" , ");
  if (t < 21) {
    Serial.print("Froid");
    Serial.print(" , ");
  } else if (t >= 21 && t < 40) {
    Serial.print("Normal");
    Serial.print(" , ");
  } else if (t > 40) {
    Serial.print("chaude");
    Serial.print(" , ");
  }
  if (h < 50) {
    Serial.print("sec");
    Serial.println(" ");
  } else {
    Serial.print("humide");
    Serial.println(" ");
  }
  delay(1000);  //Collecting period should be : >1.7 second
}
