import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import queue
import sys

# CONFIG
PORT = "COM11"
BAUD = 115200
TIMEOUT = 1

MAX_POINTS = 500

# Data queues and lists
data_queue = queue.Queue()
times = []
room_status = []
move_status = []
wander_values = []
jitter_values = []

# Plot setup
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

line_room, = ax1.plot([], [], 'b-', label='Room presence (1=yes)')
line_move, = ax1.plot([], [], 'r-', label='Motion (1=yes)')
ax1.set_ylim(-0.5, 1.5)
ax1.set_ylabel('Status (0/1)')
ax1.legend(loc='upper left')
ax1.grid(True)

line_wander, = ax2.plot([], [], 'g-', label='Wander')
line_jitter, = ax2.plot([], [], 'm-', label='Jitter')
ax2.set_ylabel('Value')
ax2.legend(loc='upper left')
ax2.grid(True)
ax2.set_xlabel('Time (s)')

fig.suptitle("Live Radar Detection - Room & Motion")
plt.tight_layout(rect=[0, 0, 1, 0.96])

# Serial reader thread
def serial_reader():
    ser = None
    try:
        ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
        print(f"Connected to {PORT} at {BAUD} baud. Reading...")
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                data_queue.put(line)
    except Exception as e:
        print(f"Serial error: {e}")
    finally:
        if ser:
            ser.close()

# Start serial thread
thread = threading.Thread(target=serial_reader, daemon=True)
thread.start()

def parse_radar_line(line):
    if not line.startswith("RADAR_DADA"):
        return None
    
    # print("DEBUG received:", line)  # uncomment for debug
    
    try:
        parts = line.split(',')
        if len(parts) < 11:
            return None
        
        seq = int(parts[1])
        timestamp = int(parts[2])
        wander = float(parts[3])
        jitter = float(parts[7])
        move_status = int(float(parts[9]))  # cast to int
        
        # Heuristic for room status (you can adjust threshold)
        room = 1 if wander > 0.005 or jitter > 0.01 else 0
        
        return {
            'seq': seq,
            'timestamp': timestamp,
            'wander': wander,
            'jitter': jitter,
            'room': room,
            'move': move_status
        }
    except Exception as e:
        print("Parse error:", e, "on line:", line)
        return None

def update(frame):
    global times, room_status, move_status, wander_values, jitter_values
    
    added = 0
    while not data_queue.empty():
        line = data_queue.get()
        parsed = parse_radar_line(line)
        if parsed:
            t = time.time()
            times.append(t)
            room_status.append(parsed['room'])
            move_status.append(parsed['move'])
            wander_values.append(parsed['wander'])
            jitter_values.append(parsed['jitter'])
            added += 1
            
            if len(times) > MAX_POINTS:
                times = times[-MAX_POINTS:]
                room_status = room_status[-MAX_POINTS:]
                move_status = move_status[-MAX_POINTS:]
                wander_values = wander_values[-MAX_POINTS:]
                jitter_values = jitter_values[-MAX_POINTS:]
    
    if added > 0:
        print(f"DEBUG: added {added} points this frame, total: {len(times)}")
    
    ax1.clear()
    ax1.plot(times, room_status, 'b-', label='Room presence')
    ax1.plot(times, move_status, 'r-', label='Motion')
    ax1.set_ylim(-0.5, 1.5)
    ax1.legend()
    ax1.grid(True)
    
    ax2.clear()
    ax2.plot(times, wander_values, 'g-', label='Wander')
    ax2.plot(times, jitter_values, 'm-', label='Jitter')
    ax2.legend()
    ax2.grid(True)
    ax2.set_xlabel('Time (s)')
    
    fig.suptitle(f"Live Radar Detection - {len(times)} points")
    plt.tight_layout(rect=[0, 0, 1, 0.96])

# Animation
ani = FuncAnimation(fig, update, interval=200, cache_frame_data=False)

plt.show()

# Cleanup on close
print("Plot closed. Exiting...")