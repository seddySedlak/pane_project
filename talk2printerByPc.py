import serial
import time

PORT = "COM4"
BAUDRATE = 115200
WAIT_INTERVAL = 3  # seconds

# connect to serial port
def connect_serial(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate)
        print(f"[INFO] Connected to {port} at {baudrate} baud")
        return ser
    except Exception as e:
        print(f"[ERROR] Failed to connect: {e}")
        exit(1)


# waiting for all printer boot votes to be written
def wait_for_printer_ready(ser, interval):
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
                print("[INFO] Printer is idle. Starting to send M105.")
                break

# reading what the printer sends
def read_response(ser):
    response = ser.readline().decode(errors="ignore").strip()
    if response:
        print("[Printer] <-", response)
    else:
        print("[Printer] <- (no response)")

# sending M105 gcode message for current temperature
def send_m105_loop(ser, interval):
    try:
        while True:
            ser.write(b"M105\n")
            print("[PC] -> Sent: M105")
            read_response(ser)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n[INFO] Script terminated by user.")
        ser.close()

ser = connect_serial(PORT, BAUDRATE)
wait_for_printer_ready(ser, WAIT_INTERVAL)
send_m105_loop(ser, WAIT_INTERVAL)
