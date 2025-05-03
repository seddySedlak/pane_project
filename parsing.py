import json
import requests
import random
import paho.mqtt.client as mqtt
from datetime import datetime
# from umqttsimple import MQTTClient
# from paho.mqtt import client as mqtt

string = "ok T:110.4 /210.0 B:54.7 /120.0 T0:22.8 /0.0 @:0 B@:0 P:0.0 A:31.1"
WEBHOOK = "https://discord.com/api/webhooks/1358380001757499613/N2qtyS8NYqWkQY-4anMT1tEEz-AlMeNS2MIR8ZUW14JiofTtWaia7oBbfK3htELnIitP"
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "eps32_3dprinter_13579"
last_update = datetime.now().strftime("%H:%M:%S")

def parseM105Gcode(string):
    result = {}
    parts = string.split(" ")
    for part in parts:
        if part.startswith("T:"):
            temps = part.split(":")
            result["nozzle_current"] = temps[1]
            result["nozzle_target"] = parts[2]
        elif part.startswith("B:"):
            temps = part.split(":")
            result["base_current"] = temps[1]
            result["base_target"] = parts[4]
    return result

def getRandomStatus():
    statuses = ["printing", "done", "no activity"]
    return random.choice(statuses)

def sendToDiscord(webhook):
    data = parseM105Gcode(string)
    status = getRandomStatus()
    nozzle_info = f"{data['nozzle_current']}{data['nozzle_target']}"
    base_info = f"{data['base_current']}{data['base_target']}"

    message = (
        "---INFO FROM 3D PRINTER---\n"
        f"Last update: {last_update}\n"
        f"Status: {status}\n"
        f"Nozzle: {nozzle_info}\n"
        f"Base: {base_info}\n"
    )
    payload = {
        "content": message
    }

    response = requests.post(webhook, json=payload)
    if response.status_code in [200, 204]:
        print("Successfully sent to Discord!")
    else:
        print(f"Error during sending: {response.status_code}, {response.text}")

def MQTTPublisher(broker, port, topic):
    client = mqtt.Client()
    client.connect(broker, port)
    data = parseM105Gcode(string)
    status = getRandomStatus()

    payload = {
        "status": status,
        "nozzle": f"{data['nozzle_current']}{data['nozzle_target']}",
        "base": f"{data['base_current']}{data['base_target']}",
        "update": last_update
    }

    client.publish(topic, json.dumps(payload), retain=True)
    client.disconnect()
    print("Successfully uploaded to MQTT!")

sendToDiscord(WEBHOOK)
MQTTPublisher(MQTT_BROKER, MQTT_PORT, MQTT_TOPIC)
# parseM105Gcode(string)