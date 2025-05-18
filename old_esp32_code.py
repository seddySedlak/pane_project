"""
This code was part of the initial idea to build the project using ESP32 and MicroPython.

However, this approach was not successful and the project was moved to Raspberry Pi.

For more information, see the file readme_esp32_info.md.
"""

import machine 
from machine import UART
import network
import urequests
import ujson
import time

# reading data from printer
def readDataFromUart():
    uart = UART(2, 115200)
    # uart = UART(2, baudrate=115200, tx=17, rx=16)
    for i in range(5):
    # while True:
        try:
            # temperature
            uart.write("M105")
            # uart.write(b"M105\n")
            time.sleep(0.5)
            if uart.any():
                data_temp = uart.readline()
                print("temp: ", data_temp)
                if data_temp:
                    temp = data_temp.decode().strip()
                else:
                    temp = "error/temp"
                    print("No response")
            else:
                print("UART silent")

            # progress
            uart.write("M27")
            # uart.write(b"M27\n")
            time.sleep(0.5)
            if uart.any():
                data_progress = uart.readline()
                print("progress: ", data_progress)
                if data_progress:
                    progress = data_progress.decode().strip()
                else:
                    progress = "error/progress"
                    print("No response")
            else:
                print("UART silent")

            # print time
            uart.write("M31")
            # uart.write(b"M31\n")
            time.sleep(0.5)
            if uart.any():
                data_time = uart.readline()
                print("time: ", data_time)
                if data_time:
                    print_time = data_time.decode().strip()
                else:
                    print_time = "error/time"
                    print("No response")
            else:
                print("UART silent")

            print("Temperature:", temp)
            print("Progress:", progress)
            print("Print time:", print_time)
            sendDataToDiscord(temp, progress, print_time)

        except Exception as e:
            print("Error:", e)
        time.sleep(10)

def connectToWifi():
    ssid = 'wifi_name'
    password = 'wifi_password'

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    while not wifi.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    print("WiFi connected:", wifi.ifconfig())

def sendDataToDiscord(temp, progress, print_time):
    webhook_url = 'webhook_url'
    headers = {'Content-Type': 'application/json'}
    message = f"ESP32:\nTemperature: `{temp}`\nProgress: `{progress}`\nPrint time: `{print_time}`"
    data = {'content': message}
    try:
        response = urequests.post(webhook_url, headers=headers, data=ujson.dumps(data))
        print("Sent to Discord")
        response.close()
    except Exception as e:
        print("Error sending to Discord:", e)

connectToWifi()
readDataFromUart()