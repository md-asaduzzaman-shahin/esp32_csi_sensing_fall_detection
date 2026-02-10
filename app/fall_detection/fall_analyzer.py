import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast  # Safely evaluates the string "[1, 2]" into a list
import os

def parse_csi_data(csv_file_path):
    """
    Reads the ESP32 CSI CSV file and converts the 'data' column 
    from a string to a numpy array of Amplitudes.
    """
    print(f"Loading: {csv_file_path} ...")
    
    # 1. Read CSV
    try:
        df = pd.read_csv(csv_file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return None, None

    # 2. Filter only CSI_DATA rows
    df = df[df['type'] == 'CSI_DATA']
    
    if df.empty:
        print("No CSI_DATA found in this file.")
        return None, None

    timestamps = pd.to_datetime(df['timestamp'])
    
    # 3. Parse the 'data' column (The hard part)
    # The format is "[r1, i1, r2, i2, ...]"
    # We need to calculate Amplitude = sqrt(r^2 + i^2)
    
    amplitudes_list = []
    
    for index, row in df.iterrows():
        try:
            # Convert string "[-10, 0...]" to list [-10, 0...]
            raw_list = ast.literal_eval(row['data'])
            
            # Separate Real and Imaginary parts
            # raw_list[0::2] takes elements 0, 2, 4... (Real)
            # raw_list[1::2] takes elements 1, 3, 5... (Imaginary)
            real_parts = np.array(raw_list[0::2])
            imag_parts = np.array(raw_list[1::2])
            
            # Calculate Amplitude
            amplitude = np.sqrt(real_parts**2 + imag_parts**2)
            amplitudes_list.append(amplitude)
            
        except Exception as e:
            print(f"Error parsing row {index}: {e}")
            continue

    # Convert to a 2D Matrix (Time x Subcarriers)
    csi_matrix = np.array(amplitudes_list)
    
    return timestamps, csi_matrix

def plot_fall_signature(timestamps, csi_matrix, title="CSI Data Analysis"):
    """
    Plots the Raw Subcarriers and the 'Variance' (Motion Energy).
    """
    plt.figure(figsize=(12, 8))

    # --- Plot 1: All Subcarriers (Heatmap Style) ---
    plt.subplot(2, 1, 1)
    # We plot all 52 lines. If a person falls, ALL lines should splash.
    plt.plot(timestamps, csi_matrix, alpha=0.3) 
    plt.title(f"{title} - Raw Subcarrier Amplitudes")
    plt.ylabel("Amplitude")
    plt.grid(True, linestyle='--', alpha=0.5)

    # --- Plot 2: Motion Energy (Variance) ---
    # This is the "Fall Detector" logic.
    # We calculate the Standard Deviation across all subcarriers for each packet.
    # High Std Dev = Chaos (Movement). Low Std Dev = Silence.
    
    motion_energy = np.std(csi_matrix, axis=1)
    
    plt.subplot(2, 1, 2)
    plt.plot(timestamps, motion_energy, color='red', linewidth=2)
    plt.title("Motion Energy (Standard Deviation)")
    plt.ylabel("Energy Level")
    plt.xlabel("Time")
    plt.grid(True)
    
    # Add a 'Threshold' line to visualize where a trigger might be
    plt.axhline(y=np.mean(motion_energy) + 2*np.std(motion_energy), color='green', linestyle='--', label='Threshold Estimate')
    plt.legend()

    plt.tight_layout()
    plt.show()

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # USER: CHANGE THIS PATH TO ONE OF YOUR FILES
    # Example: "data/move/2026-02-10_11-00-53-306_104_20.csv"
    target_file = "data/move/2026-02-10_11-00-53-306_104_20.csv" 
    
    # Check if file exists to prevent errors
    if not os.path.exists(target_file):
        print(f"File not found: {target_file}")
        print("Please edit the 'target_file' variable in the script to point to your CSV.")
    else:
        times, data = parse_csi_data(target_file)
        if data is not None:
            print(f"Data Loaded: {data.shape[0]} Packets x {data.shape[1]} Subcarriers")
            plot_fall_signature(times, data, title="Walking / Moving Data")