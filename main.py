import machine
from machine import UART
import network
import urequests

# reading data from printer
def readDataFromUart():
    uart = UART(2, 115200)
    #uart = UART(2, baudrate=115200, tx=17, rx=16)
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
                    print("Zadna odpoved")
            else:
                print("UART ticho")

            # progress
            uart.write("M27")
            # uart.write(b"M27\n")
            time.sleep(0.5)
            if uart.any():
                data_progress = uart.readline()
                print("progress: ",data_progress)
                if data_progress:
                    progress = data_progress.decode().strip()
                else:
                    temp = "error/progress"
                    print("Zadna odpoved")
            else:
                print("UART ticho")

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
                    temp = "error/time"
                    print("Zadna odpoved")
            else:
                print("UART ticho")

            print("Teplota:", temp)
            print("Progress:", progress)
            print("Cas tisku:", print_time)
            sendDataToDiscord(temp, progress, print_time)

        except Exception as e:
            print("Chyba:", e)
        time.sleep(10)

def connectToWifi():
    ssid = 'heha'
    password = 'Mrkev007'

    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(ssid, password)

    while not wifi.isconnected():
        print("Připojuji se k WiFi...")
        time.sleep(1)
    print("WiFi připojeno:", wifi.ifconfig())

def sendDataToDiscord(temp, progress, print_time):
    webhook_url = 'https://discord.com/api/webhooks/1358380001757499613/N2qtyS8NYqWkQY-4anMT1tEEz-AlMeNS2MIR8ZUW14JiofTtWaia7oBbfK3htELnIitP'
    headers = {'Content-Type': 'application/json'}
    zprava = f"ESP32:\nTeplota: `{temp}`\nProgress: `{progress}`\nCas tisku: `{print_time}`"
    data = {'content': zprava}
    try:
        response = urequests.post(webhook_url, headers=headers, data=ujson.dumps(data))
        print("Odeslano na Discord")
        response.close()
    except Exception as e:
        print("Chyba pri odesilani na Discord:", e)


connectToWifi()
readDataFromUart()
