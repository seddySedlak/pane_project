import time
import network
import urequests
import ujson
import machine
from umqtt.simple import MQTTClient

# Připojení k Wi-Fi
ssid = 'xxx'
password = 'xxx'
webhook_url = 'xxx'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    print("Připojuji se k WiFi...")
    time.sleep(1)

print("WiFi připojeno:", wifi.ifconfig())

# MQTT nastavení
broker = 'broker.emqx.io'
port = 1883
topic = b"eps32_3dprinter_13579"
client_id = b"esp32_" + machine.unique_id()

def connect_mqtt():
    client = MQTTClient(client_id, broker, port)
    client.connect()
    print("Připojeno k MQTT brokeru!")
    return client

def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        msg = b"messages: %d" % msg_count
        try:
            client.publish(topic, msg, retain="true")
            print(f"Odesláno `{msg}` na topic `{topic.decode()}`")
        except Exception as e:
            print("Chyba při odesílání:", e)
        msg_count += 1
        if msg_count > 5:
            break
def discord():
    headers = {'Content-Type': 'application/json'}
    zprava = f'Teplota tiskove hlavy:tady bude vstupni parametr'  # <-- změněno
    data = {'content': zprava}
    try:
        response = urequests.post(webhook_url, headers=headers, data=ujson.dumps(data))
        print("Status kód:", response.status_code)
        print("Odpověď:", response.text)
        response.close()
    except Exception as e:
        print("Chyba při odesílání:", e)

def run():
    client = connect_mqtt()
    publish(client)
    discord()
    client.disconnect()

run()

