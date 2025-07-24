#include <ESP8266WiFi.h>
#include <DHT.h>

const char* ssid = "BCN";
const char* password = "ruby_dante";
const char* host = "api.thingspeak.com";
String apiKey = "S03NDYNH73O4Q0IL";

// DHT Sensor Setup
#define DHTPIN D4       // Change if needed
#define DHTTYPE DHT22   // DHT11 or DHT22
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  int soil = analogRead(A0); // connect soil sensor to A0

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Failed to read from DHT");
    return;
  }

  WiFiClient client;
  if (client.connect(host, 80)) {
    String url = "/update?api_key=" + apiKey +
                 "&field1=" + String(temp) +
                 "&field2=" + String(hum) +
                 "&field3=" + String(soil);

    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                 "Host: " + host + "\r\n" +
                 "Connection: close\r\n\r\n");

    Serial.println("Data sent: " + url);
    client.stop();
  }

  delay(2000); // Wait 15 seconds
}
