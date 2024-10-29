#include <WiFi.h>  // Include the ESP32 WiFi library for Wi-Fi connectivity
#include <HTTPClient.h>  // Include the HTTPClient library to handle HTTP requests
#include <WiFiClientSecure.h>  // Include the WiFiClientSecure library for secure connections (HTTPS)

// Network credentials
const char* ssid = "wifi name";  // Replace with your Wi-Fi network name (SSID)
const char* password = "wifi password";  // Replace with your Wi-Fi password

// Server name is the URL with your PC's IP
const char* serverName = "https://192.168.10.108:1880/data";  // URL to send HTTP POST requests to Node-RED

// Root CA certificate for secure connection
const char* root_ca = \
"-----BEGIN CERTIFICATE-----\n"
"-----certificate------------\n"  // Placeholder for your actual CA certificate
"-----END CERTIFICATE-----\n";

void setup() {
  Serial.begin(115200);  // Initialize serial communication at 115200 baud rate

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);  // Start the Wi-Fi connection using the specified SSID and password
  // Wait until the ESP32 is connected to the Wi-Fi network
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);  // Wait for 1 second before retrying
    Serial.println("Connecting to WiFi...");  // Print message to indicate connection attempt
  }
  // Print the IP address assigned to the ESP32 once connected
  Serial.println("Connected! IP address: " + WiFi.localIP().toString());
}

void loop() {
  // Check if the ESP32 is connected to Wi-Fi
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure client;  // Create a secure Wi-Fi client
    client.setCACert(root_ca);  // Set the CA certificate for SSL verification

    HTTPClient http;  // Create an HTTPClient object
    
    // Specify the URL and HTTPS endpoint for the HTTP request
    http.begin(client, serverName);  // Initialize the HTTP client with the secure connection and server URL

    // Specify the content type for the HTTP request
    http.addHeader("Content-Type", "application/json");

    // Create a JSON payload with random temperature values
    float temperature = random(15, 30);  // Generate a random temperature value between 15 and 30
    String payload = "{\"sensor\":\"temperature\",\"value\":" + String(temperature) + "}";  // Construct JSON string

    // Send the HTTP POST request with the payload
    int httpResponseCode = http.POST(payload);

    // Check the response code from the server
    if (httpResponseCode > 0) {
      String response = http.getString();  // Get the response from the server
      Serial.println("Response from server: " + response);  // Print the server's response
    } else {
      Serial.println("Error on sending POST: " + String(httpResponseCode));  // Print error code if request fails
    }

    // End the HTTP connection
    http.end();  // Close the HTTP connection
  }

  // Delay for 10 seconds before sending the next data point
  delay(10000);  // Wait for 10 seconds
}
