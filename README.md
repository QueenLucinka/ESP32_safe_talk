## ESP32 Safe Data Storage and Visualization

## Project Overview

This project serves as a prototype for securely collecting temperature data from an ESP32 microcontroller and visually representing that data for clients. The data is transmitted to a Node-RED server, where it is processed and stored. A Dash web application is used to display the temperature readings in real time.

## Features

- **Secure Communication**: Data is transmitted over HTTPS using self-signed certificates to ensure secure connections between the ESP32 and Node-RED.
- **Real-Time Visualization**: The temperature data is visualized using a Dash web application, providing a user-friendly interface to monitor sensor readings.
- **Data Storage**: Temperature readings are stored in a text file, allowing for easy retrieval and processing.
  
## HTTPS Protocol
The project utilizes HTTPS (Hypertext Transfer Protocol Secure) to ensure the secure transmission of data between the ESP32 microcontroller and the Node-RED server.

## Key Aspects of HTTPS in This Project:
**Data Encryption**: HTTPS encrypts the data exchanged between the client (ESP32) and the server (Node-RED), preventing eavesdropping and man-in-the-middle attacks.
**Certificate Authentication**: Self-signed certificates are used in this prototype to establish the identity of the server. The ESP32 is configured to trust the root certificate, allowing it to connect securely to the Node-RED server.
**Secure Socket Layer (SSL)**: The underlying technology that enables HTTPS is SSL/TLS (Transport Layer Security), which ensures secure communication over the Internet.

## Components Used
- **ESP32 Microcontroller**: The main device that collects temperature data.
- **Node-RED**: A flow-based development tool for visual programming used to handle incoming data and send it to the storage file.
- **Dash**: A Python framework for building web applications that provides real-time graphing capabilities.
- **OpenSSL**: Used for generating self-signed certificates to secure communications.

## Getting Started

### Requirements
- **Hardware**: ESP32 development board
- **Software**: 
  - Arduino IDE or PlatformIO for ESP32 programming
  - Node-RED installed on your PC
  - Python 3.x with Dash library for the web application

### Installation Steps
1. **Setup Node-RED**:
   - Install Node-RED and run it by executing `node-red` in your PowerShell or terminal.
   - Access Node-RED via `https://<your_IP>:1880`.

2. **Create Node-RED Flow**:
   - Add an **HTTP In** node configured for POST requests.
   - Add an **HTTP Response** node.
   - Include a **Function** node to process the incoming data (see function example below).
   - Finally, add a **Write File** node to store the data in a text file.

   ```javascript
   // Function Node Example
   let temperature = msg.payload.value;  // Extract the temperature value
   let timestamp = new Date().toLocaleTimeString();  // Get current time

   // Format data as "HH:MM:SS,value"
   msg.payload = `${timestamp},${temperature}\n`;  // Append newline

   return msg;
   ```

3. **Setup Dash Web Application**:
   - Run the Dash application by executing `python app.py` in your terminal.
   - Access the Dash app via `http://127.0.0.1:8050`.

## How to Use
- The ESP32 will continuously send temperature readings to the Node-RED server.
- The Node-RED flow processes this data and writes it to a specified text file.
- The Dash application reads from this text file and updates the graph every minute to display the latest temperature data.

## Security Note
- For production use, consider implementing a proper certificate authority for SSL certificates rather than self-signed certificates.
- Always keep private keys secure and follow best practices for data handling and user privacy.

## Conclusion
This prototype demonstrates a secure and efficient way to collect, store, and visualize temperature data from an ESP32. It provides a foundation for further enhancements, such as integrating databases for data storage or expanding the graphical user interface.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


