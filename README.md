
---

# ESP32-CSI-Sensing-Fall-Detection

**A Real-Time WiFi Sensing & Fall Detection System using ESP32 Channel State Information (CSI).**

This repository contains the source code and tools to turn two standard ESP32 microcontrollers into a high-resolution "Tripwire" radar for detecting human falls. By analyzing the disturbances in WiFi 802.11n (HT) signals, the system can distinguish between walking, sitting, and falling without the use of cameras or wearable sensors.

---

## 📖 Table of Contents

* [Overview](#overview)
* [Hardware Setup](#hardware-setup)
* [Software Requirements](#software-requirements)
* [Project Structure](#project-structure)
* [Installation & Setup](#installation--setup)
    * [1. Flash the Transmitter (TX)](#1-flash-the-transmitter-tx)
    * [2. Flash the Receiver (RX)](#2-flash-the-receiver-rx)
    * [3. Run the Python Application](#3-run-the-python-application)
* [Usage Guide](#usage-guide)
* [Troubleshooting](#troubleshooting)

---

## 🔭 Overview

<!-- Traditional WiFi sensing often struggles with low resolution. This project solves that by forcing **High-Throughput (HT) 802.11n frames** between a dedicated Transmitter and Receiver. -->

* **Technology:** WiFi Channel State Information (CSI).
* **Method:** Passive Sensing (No wearables required).
* **Key Feature:** Real-time visualization, data logging, and fall detection analysis via Python.
* **Application:** Elderly care, home security, and presence detection.

---

## 🛠 Hardware Setup

To replicate this setup, you need:

1. **2x ESP32 Development Boards** (Generic ESP32-WROOM or similar).
2. **2x Tripods** (Recommended height: **1.4 meters**).
* *Why?* This height aligns the Fresnel zone with the human torso for optimal fall detection sensitivity.


3. **2x Micro-USB Cables** (Data sync capable).
4. **PC/Laptop** (Windows/Linux/Mac) for running the Python tools.

**Physical Layout:**
Place the TX and RX boards **2-4 meters apart**. Ensure the PCB antennas are vertical and facing each other.

---

## 💻 Software Requirements

* **Visual Studio Code**
* **Espressif IDF Extension** for VS Code.
* **ESP-IDF v5.5.2** (Installed via the extension).
* **Python 3.x**
* **Git**

---

## 📂 Project Structure

```text
ESP32-CSI-Sensing-Fall-Detection/
├── transmitter/             # Firmware for the 'Illuminator' (TX)
│   ├── main/
│   │   └── app_main.c       # Forced HT-Frame logic
│   └── ...
├── receiver/                # Firmware for the 'Camera' (RX)
│   ├── main/
│   │   └── app_main.c       # CSI Collection & Serial Output logic
│   └── ...
└── app/                     # Main Python Application
    ├── esp_csi_tool_mod.py  # Real-Time GUI & Visualizer
    ├── requirements.txt     # Python dependencies
    ├── data/                # Recorded CSV datasets (move, sit, fall)
    └── fall_detection/      # Fall Detection Engine (The Brain)
        ├── models/          # Trained Machine Learning models (.pkl)
        ├── src/             # Helper scripts (Math & Parsing)
        ├── analyze_fall.py  # Offline Fall Analysis Script
        ├── train_model.py   # Training Script
        └── live_detect.py   # Real-Time Alert Script
```

---

## 🚀 Installation & Setup

### 1. Flash the Transmitter (TX)

1. Connect the **TX Board** to your PC.  
2. Open VS Code → **File > Open Folder...** → select the `transmitter` folder.  
3. Open Device Manager (Windows) to identify the board's COM port.  
4. In VS Code click the COM port selector (bottom status bar) and choose the matching port.  
5. If prompted for a project target, select `esp32` (or your specific chip, e.g., `esp32s3`). If asked for a directory, select the current folder.  
6. Click the ESP-IDF Build/Flash icon (lightning bolt) or press F1 and run "ESP-IDF: Flash Device".  
7. Select `UART` as the flash method if prompted.  
8. Important: Once flashed, unplug the TX board and power it via a wall charger or battery bank to isolate it from the Receiver.

### 2. Flash the Receiver (RX)

1. Connect the **RX Board** to your PC.
2. Open a **New Window** in VS Code -> Select `receiver`.
3. Flash the firmware using the ESP-IDF extension.
4. **CRITICAL:** After flashing, **CLOSE the Serial Monitor** in VS Code. The Python app cannot connect if VS Code is using the port.

### 3. Run the Python Application

1. Open the **ESP-IDF Terminal** in VS Code (or any terminal).
2. Navigate to the `app` folder:
```powershell
cd app

```


3. Install dependencies:
```powershell
pip install -r requirements.txt

```


4. Run the GUI:
```powershell
python esp_csi_tool_mod.py -p COMxx

```


*(Replace `COMxx` with your Receiver's actual port, e.g., `COM10`)*

---

## 📊 Usage Guide

### 1. Real-Time Monitoring & GUI (`esp_csi_tool_mod.py`)

The primary interface for this project is the **`esp_csi_tool_mod.py`** script. This GUI communicates with the Receiver board to visualize WiFi signal disturbances and manage the internal radar algorithm.

* **Run the tool:**
```powershell
python app/esp_csi_tool_mod.py -p COMxx

```


*(Replace `COMxx` with your Receiver's actual port, e.g., `COM10`)*
* **Baseline Calibration (CRITICAL):**
When the system starts, it performs a self-calibration to understand the "Empty Room" state.
* **Rule:** The room must be **completely silent** (no movement, fans off, windows closed) during the first 10-15 seconds of operation.
* **Why:** If the baseline is noisy, the system's sensitivity thresholds will be set too high, causing it to miss actual movements (like breathing or falling).


* **Understanding the Graph:**
The GUI plots four distinct lines to track human activity:
* **Yellow Line (`wander`):** Represents the raw signal variance. Small fluctuations indicate breathing or minor movements.
* **Blue Line (`wander_threshold`):** The dynamic limit for "Stationary" presence. If the Yellow line crosses this Blue line, the system detects a static person.
* **Purple Line (`jitter` / `someone_presence`):** Represents high-frequency signal changes. Large spikes indicate rapid motion (walking, falling).
* **Green Line (`jitter_threshold`):** The dynamic limit for "Motion." If the Purple line crosses this Green line, the system triggers a "Move" event.



For a deeper dive into the original console commands and GUI parameters, refer to the [XIAO ESP-CSI Repository](https://github.com/limengdu/XIAO_esp-csi/tree/master/examples/esp-radar/console_test).

### 2. Data Collection (Training)

To build the Fall Detection dataset, you must record labeled examples of different activities.

* **Navigate:** Go to the **Collect** tab in the GUI.
* **Select Label:** Choose the activity you are performing (e.g., `move`, `sit down`, `jump` for falls).
* **Set Duration:** ~1000 packets (approx. 10 seconds).
* **Action:** Click **Start**, perform the action in the sensing zone, and wait for it to finish.
* **Output:** CSV files will be saved automatically in `app/data/{label}/`.

### 3. Fall Detection Analysis

Once data is collected, use the offline analysis script to identify the unique "Fall Signature."

* **Run the analysis:**
```powershell
python app/fall_detection/analyze_fall.py

```


* **How it works:**
The script reads your recorded CSVs and extracts statistical features (Entropy, Velocity, MAD) to distinguish between controlled actions and falls.
* **The Signature:** A fall typically appears as a massive, high-velocity spike in the **Purple (`jitter`)** line, followed immediately by a flat-line in the **Yellow (`wander`)** line (indicating the subject is lying still). (See <attachments> above for file contents. You may not need to search or read the file again.)


---

## 🔄 The Flow

```
┌─────────────────────────────────────────────────────────────┐
│ ESP32 Device (app_main.c)                                   │
├─────────────────────────────────────────────────────────────┤
│ 1. Receives WiFi packets → CSI captured                     │
│ 2. esp_radar library processes CSI                          │
│    - Decodes complex numbers                                │
│    - Calculates waveform_wander & waveform_jitter           │
│ 3. Sends RADAR_DATA output via UART/Serial:                 │
│    "RADAR_DADA,seq,timestamp,wander,threshold..."           │
│ 4. Also sends CSI_DATA (raw waveform)                       │
└─────────────────────────────────────────────────────────────┘
                          ↓ Serial Data
┌─────────────────────────────────────────────────────────────┐
│ Python GUI (esp_csi_tool_mod.py)                            │
├─────────────────────────────────────────────────────────────┤
│ 1. RECEIVES & PARSES the data from ESP32                    │
│ 2. csi_data_handle(): Extracts amplitude from raw data      │
│    - Does NOT recalculate wander/jitter                     │
│    - Just visualizes the waveform                           │
│ 3. radar_data_handle(): Displays metrics already calculated │
│    by ESP32                                                 │
│ 4. Shows graphs, tables, statistics                         │
└─────────────────────────────────────────────────────────────┘
```
---

## ⚙️ Technical Implementation & Modifications

This project is built upon the foundational examples provided by the [XIAO ESP-CSI](https://www.google.com/search?q=https://github.com/limengdu/XIAO_esp-csi) and Espressif CSI repositories. However, significant modifications were made to adapt the generic "radar" console test into a dedicated Fall Detection System.

### Firmware Adaptation

The **Receiver** firmware in this repository are derived from the `examples/esp-radar/console_test` project.
The **Transmitter** firmware is adapted from the Espressif example `examples/room_presence_detection/send_TX`, modified to act as a dedicated HT-frame "Illuminator" forcing high-throughput 802.11n traffic to the Receiver for reliable CSI collection.

* **Base Logic:** Utilizes the standard active CSI collection method (ping-pong mechanism).
* **Optimization:** Configured for high-frequency 802.11n (HT) frame exchange to capture rapid vertical acceleration typical of falls.

### GUI Evolution (`esp_csi_tool_mod.py`)

The original `esp_csi_tool.py` provided by Espressif was designed for general-purpose visualization. I developed **`esp_csi_tool_mod.py`** to serve as a specialized data collection and analysis interface for this research.

**Key Modifications:**

1. **Enhanced Data Logging:** Added specific tagging controls (`move`, `sit down`, `jump`, `fall`) to the "Collect" tab, enabling the creation of structured, labeled datasets required for Machine Learning training.
2. **Real-Time Visualization Tweaks:** Adjusted the sensitivity and scaling of the **Purple (`jitter`)** and **Yellow (`wander`)** lines to better represent human torso movements at the 1.4m tripod height.
3. **Stability Fixes:** Improved serial port buffer handling to prevent crashes during long recording sessions (20+ minutes) required for baseline calibration.

---

## ❓ Troubleshooting

**"Failed to open serial port"**

* **Fix:** Close the Serial Monitor in VS Code or Arduino IDE. Only one program can use the COM port at a time.

**"Graph is flat / No Data"**

* **Fix:** Ensure the Transmitter (TX) is powered on. Press the **RST (Reset)** button on the Receiver board while the Python GUI is running.

---

## 📜 License

This project is based on the [XIAO_esp-csi](https://github.com/limengdu/XIAO_esp-csi/tree/master) project.
Modifications and Fall Detection logic by .
