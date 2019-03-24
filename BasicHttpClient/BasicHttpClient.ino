/**
   BasicHTTPClient.ino

    Created on: 24.05.2015

*/

#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>

ESP8266WiFiMulti WiFiMulti;
uint8_t Rightpin = D0;
uint8_t Leftpin = A0;
float LastID = 0;

void setup() {

  Serial.begin(115200);
  // Serial.setDebugOutput(true);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }
  analogWriteRange(255);
  Serial.println("____range set to 255____");
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("Yash J. Doshi", "pterodactyl");

}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, "http://192.168.43.184:5000/arduino/movement/yashdoshi")) {  // HTTP


      Serial.print("[HTTP] GET...\n");
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
          getValue(payload, ',');
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }

  delay(10000);
}

void getValue(String data, char separator) {

  int found = 0;
  int sep_index[3];
  int data_length = data.length();

  for (int i = 0; i < data_length ; i++) {
    if ((data.charAt(i) == separator) &&
        (found < sizeof(sep_index))) {

      sep_index[found] = i;
      found++;

    }
  }

  String rightVal = data.substring(0, sep_index[0]);
  String leftVal = data.substring(sep_index[0], sep_index[1]);
  String IDVal = data.substring(sep_index[1], data_length);
  float r_pwm = rightVal.toFloat();
  float l_pwm = leftVal.toFloat();
  float id = IDVal.toFloat();
  if ((LastID == (id - 1)) || LastID == 0) {
    Move(r_pwm, l_pwm);
    LastID = id;
  } else {
    Serial.println("Last ID didnt match");
    Serial.println("ID : " + IDVal + "\nLast ID :" + String(LastID));
  }
}
void Move(float r_pwm, float l_pwm) {
  String text = "PWM :" + String(r_pwm) + "," + String(l_pwm);
  Serial.println(text);

  analogWrite(Rightpin, r_pwm);
  analogWrite(Leftpin, l_pwm);
}

