import serial
import time
import json
import requests
import paho.mqtt.client as mqtt
from datetime import datetime

# Configuration
PORT = "/dev/ttyUSB1"
BAUDRATE = 115200
WAIT_INTERVAL = 3
GCODE_COMMANDS = ["M31", "M105", "M27"]

# ↓ In the WEBHOOK constant you can change the discord webhook url ↓
WEBHOOK = "https://discord.com/api/webhooks/1358380001757499613/N2qtyS8NYqWkQY-4anMT1tEEz-AlMeNS2MIR8ZUW14JiofTtWaia7oBbfK3htELnIitP"
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "eps32_3dprinter_13579"


def connect_serial(port, baudrate):
    """
    Connects to a serial port with the given port and baudrate.

    Args:
        port (str): Serial port name (e.g., '/dev/ttyUSB1')
        baudrate (int): Communication speed in baud

    Returns:
        serial.Serial: Serial connection object

    Raises:
        SystemExit: If the connection fails
    """
    try:
        ser = serial.Serial(port, baudrate)
        print(f"[INFO] Connected to {port} at {baudrate} baud")
        return ser
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")
        exit(1)


def wait_for_printer_ready(ser, interval):
    """
    Waits until the printer stops sending boot messages.

    Args:
        ser (serial.Serial): Serial connection to the printer
        interval (int): Time in seconds to wait after silence
    """
    print("[INFO] Waiting for the printer to finish boot messages...")
    silence_start = None
    while True:
        if ser.in_waiting:
            line = ser.readline().decode(errors="ignore").strip()
            if line:
                print("[BOOT] " + line)
            silence_start = time.time()
        else:
            if silence_start is not None and (time.time() - silence_start > interval):
                print("[INFO] Printer is idle. Starting to send gcode messages.")
                break


def read_response(ser, timeout=1):
    """
    Reads lines from the printer for a limited time period.

    Args:
        ser (serial.Serial): Serial connection
        timeout (int): Timeout in seconds

    Returns:
        str: Concatenated response lines
    """
    start = time.time()
    lines = []
    while time.time() - start < timeout:
        while ser.in_waiting:
            line = ser.readline().decode(errors="ignore").strip()
            if line:
                lines.append(line)
            start = time.time()
        time.sleep(0.1)
    response = " ; ".join(lines) if lines else "(no response)"
    print("[Printer] <-", response)
    return response


def sendGCodeCommands(ser, interval, commands):
    """
    Sends G-code commands to the printer and captures the responses.

    Args:
        ser (serial.Serial): Serial connection
        interval (int): Delay between commands in seconds
        commands (list): List of G-code command strings

    Returns:
        tuple: (response_M31, response_M105, response_M27)
    """
    try:
        response_M31 = ""
        response_M105 = ""
        response_M27 = ""

        for cmd in commands:
            ser.write((cmd + "\n").encode())
            print("[PC] -> Sent: ", cmd)
            response = read_response(ser)
            time.sleep(interval)

            if cmd == "M31":
                response_M31 = response
            elif cmd == "M105":
                response_M105 = response
            elif cmd == "M27":
                response_M27 = response

        print("\n=== Responses ===")
        print("M31 =>", response_M31)
        print("M105 =>", response_M105)
        print("M27 =>", response_M27)

        return response_M31, response_M105, response_M27
    except KeyboardInterrupt:
        print("\n[INFO] Script terminated by user.")
        ser.close()


def parseM105Gcode(response_M105):
    """
    Parses a G-code M105 response to extract nozzle and bed temperatures.

    Args:
        response_M105 (str): Raw M105 response string

    Returns:
        dict: Parsed temperature values
    """
    result = {}
    parts = response_M105.split(" ")
    for part in parts:
        if part.startswith("T:"):
            result["nozzle_current"] = part.split(":")[1]
            result["nozzle_target"] = parts[2]
        elif part.startswith("B:"):
            result["base_current"] = part.split(":")[1]
            result["base_target"] = parts[4]
    return result


def parseM27Gcode(response_M27):
    """
    Parses a G-code M27 response to determine print progress or status.

    Args:
        response_M27 (str): Raw M27 response string

    Returns:
        str: "Done", percentage string, or error indicator
    """
    parts = response_M27.split(" ; ")
    if parts[0] == "Not SD printing":
        print("Done")
        return "Done"
    elif "/" in parts[0]:
        status = parts[0].split("/")
        done = int(status[0])
        total = int(status[1])
        if total > 0:
            percent = round(((done/total) * 100), 2)
            print(f"{percent}%")
            return f"{percent}%"
        else:
            print("error")
            return "error"
    else:
        print("unknown")
        return "unknown"


def parseM31Gcode(response_M31):
    """
    Parses a G-code M31 response to extract elapsed print time.

    Args:
        response_M31 (str): Raw M31 response string

    Returns:
        str: Extracted time string or "unknown"
    """
    parts = response_M31.split(" ; ")
    for part in parts:
        if part.startswith("echo:"):
            temps = part.split(":")
            return temps[1]
        else:
            continue


def sendToDiscord(data, status, progress, webhook):
    """
    Sends parsed printer data to a Discord webhook.

    Args:
        data (dict): Temperature info from M105
        status (str): Print status from M27
        progress (str): Elapsed time from M31
        webhook (str): Discord webhook URL
    """
    nozzle_info = f"{data['nozzle_current']}/{data['nozzle_target']}"
    base_info = f"{data['base_current']}/{data['base_target']}"
    last_update = datetime.now().strftime("%H:%M:%S")

    message = (
        "---INFO FROM 3D PRINTER---\n"
        f"Last update: {last_update}\n"
        f"Status: {status}\n"
        f"Progress: {progress}\n"
        f"Nozzle: {nozzle_info}\n"
        f"Base: {base_info}\n"
    )

    payload = {"content": message}
    response = requests.post(webhook, json=payload)
    if response.status_code in [200, 204]:
        print("Successfully sent to Discord!")
    else:
        print(f"Error during sending: {response.status_code}, {response.text}")


def MQTTPublisher(data, status, progress, broker, port, topic):
    """
    Publishes printer data to an MQTT broker.

    Args:
        data (dict): Temperature info from M105
        status (str): Print status from M27
        progress (str): Elapsed time from M31
        broker (str): MQTT broker URL
        port (int): MQTT port
        topic (str): MQTT topic name
    """
    last_update = datetime.now().strftime("%H:%M:%S")
    payload = {
        "status": status,
        "progress": progress,
        "nozzle": f"{data['nozzle_current']}/{data['nozzle_target']}",
        "base": f"{data['base_current']}/{data['base_target']}",
        "update": last_update
    }

    client = mqtt.Client()
    client.connect(broker, port)
    client.publish(topic, json.dumps(payload), retain=True)
    client.disconnect()
    print("Successfully uploaded to MQTT!")


# Execution 
if __name__ == "__main__":
    ser = connect_serial(PORT, BAUDRATE)
    wait_for_printer_ready(ser, WAIT_INTERVAL)
    response_M31, response_M105, response_M27 = sendGCodeCommands(ser, WAIT_INTERVAL, GCODE_COMMANDS)

    data = parseM105Gcode(response_M105)
    status = parseM27Gcode(response_M27)
    progress = parseM31Gcode(response_M31)

    sendToDiscord(data, status, progress, WEBHOOK)
    MQTTPublisher(data, status, progress, MQTT_BROKER, MQTT_PORT, MQTT_TOPIC)
