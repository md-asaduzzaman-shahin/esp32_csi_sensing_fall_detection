import serial
import time

ser = serial.Serial('COM11', 115200, timeout=1)
print("Connected. Reading... Press Ctrl+C to stop")

try:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(line)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Stopped")
finally:
    ser.close()