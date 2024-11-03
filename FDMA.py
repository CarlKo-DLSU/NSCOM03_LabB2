import time
import random
import threading
import numpy as np
import matplotlib.pyplot as plt

# Define the number of devices and their frequency channels
NUM_DEVICES = 4
FREQUENCY_BANDS = [1, 2, 4, 8]  # Example frequency bands in MHz
DEVICE_NAMES = [f"Device {i + 1}" for i in range(NUM_DEVICES)]
COLORS = ['blue', 'orange', 'green', 'red']  # Colors for each device

# Function to simulate data transmission for a device
def transmit_data(device_id, frequency):
    print(f"Device {device_id} is transmitting on frequency {frequency} MHz.")
    # Simulate transmission time
    transmission_time = random.uniform(1, 3)  # Random time between 1 to 3 seconds
    time.sleep(transmission_time)
    print(f"Device {device_id} has finished transmitting.")

# Create threads for each device
threads = []
for device_id in range(NUM_DEVICES):
    frequency = FREQUENCY_BANDS[device_id]
    thread = threading.Thread(target=transmit_data, args=(device_id + 1, frequency))
    threads.append(thread)

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

print("All devices have completed their transmissions.")

# Plotting the sine waves
t = np.linspace(0, 1, 1000)  # Time vector
plt.figure(figsize=(12, 6))

for i, frequency in enumerate(FREQUENCY_BANDS):
    # Generate sine wave for each frequency
    sine_wave = np.sin(2 * np.pi * frequency * 1e6 * t)  # Convert MHz to Hz
    plt.plot(t, sine_wave, label=DEVICE_NAMES[i], color=COLORS[i])  # No vertical offset

# Adding labels and title
plt.title('FDMA Frequency Allocation as Sine Waves')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Add a horizontal line at y=0
plt.grid()
plt.legend()
plt.show()