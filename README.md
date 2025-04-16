# 🖨️ ESP32 3D Printer Data Sender

> **A microcontroller-based project for reading data from a 3D printer and sending it via Discord and MQTT using an ESP32.**

---

## 🚀 Project Overview

This project focuses on connecting an **ESP32** to a **3D printer** in order to collect print-related data (such as temperature, print progress, status messages, etc.) and send that information to a **Discord server via Webhook** and to a **web interface via MQTT** in real time or at defined intervals.

---

## 🎯 Features

✅ Read data from a 3D printer (e.g., via serial communication)  
✅ Parse relevant information (status, temperature, etc.)  
✅ Send parsed data to a **Discord channel using Webhook**  
✅ Publish data to a **web application via MQTT**  
✅ ESP32-based, low-cost and wireless  
✅ Configurable intervals for updates  
✅ Portable and adaptable to different printer models  

---

## 🔧 Hardware & Tools Used

| Component     | Description                            |
|---------------|----------------------------------------|
| ESP32         | Microcontroller with Wi-Fi support     |
| 3D Printer    | Source of real-time printing data       |
| USB/Serial    | Communication between printer and ESP32 |
| Discord Webhook | Sending messages to Discord           |
| MQTT Broker (EMQX) | Communication with web interface   |

---

## 🧠 How It Will Probably Work

1. ESP32 connects to the 3D printer via UART (Serial).  
2. It reads the data coming from the printer (e.g., G-code responses).  
3. Relevant values are extracted (temperature, status, etc.).  
4. The ESP32 sends the parsed data to a **Discord channel via Webhook**.  
5. The ESP32 also publishes the data to a **web dashboard via MQTT**.  