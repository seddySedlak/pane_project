# 🖨️ ESP32 3D Printer Data Sender

> **A microcontroller-based project for reading data from a 3D printer and sending it via Discord and MQTT using an Raspberry Pi 3.**

---

## 🚀 Project Overview

This project focuses on connecting an **Raspberry Pi 3** to a **3D printer** in order to collect print-related data (such as temperature, print progress, status messages, etc.) and send that information to a **Discord server via Webhook** and to a **web interface via MQTT** in real time or at defined intervals.

---

## 🎯 Features

✅ Read data from a 3D printer (e.g., via serial communication)  
✅ Parse relevant information (status, temperature, etc.)  
✅ Send parsed data to a **Discord channel using Webhook**  
✅ Publish data to a **web application via MQTT**  
✅ Raspberry Pi 3-based, low-cost and wireless  
✅ Configurable intervals for updates  
✅ Portable and adaptable to different printer models  

---

## 🔧 Hardware & Tools Used

| Component     | Description                            |
|---------------|----------------------------------------|
| Raspberry Pi 3 | Microcontroller with Wi-Fi support     |
| 3D Printer    | Source of real-time printing data       |
| USB    | Communication between printer and Raspberry Pi 3 |
| Discord Webhook | Sending messages to Discord           |
| MQTT Broker (EMQX) | Communication with web interface   |

---

## 🧠 How It Will Probably Work

1. Raspberry Pi 3 connects to the 3D printer via USB port.  
2. It sends gcode message
2. It reads the data coming from the printer (G-code responses).  
3. Relevant values are extracted (temperature, status, etc.).  
4. The Raspberry Pi 3 sends the parsed data to a **Discord channel via Webhook**.  
5. The Raspberry Pi 3 also publishes the data to a **web dashboard via MQTT**.  

---

## 🌐 Live Data Dashboard

Want to see it in action? You can view the live data coming from the printer on this webpage:  
👉 [https://seddysedlak.github.io/pane_project/](https://seddysedlak.github.io/pane_project/)
