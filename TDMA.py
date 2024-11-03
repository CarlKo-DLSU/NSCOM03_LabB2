import time
import threading
import matplotlib.pyplot as plt
import numpy as np

# Define the number of devices and their time slots
NUM_DEVICES = 4
DURATION = 2
FREQUENCY = 8
TIME_SLOTS = [DURATION] * NUM_DEVICES  # Transmission times for each device
DEVICE_NAMES = [f"Device {i + 1}" for i in range(NUM_DEVICES)]
COLORS = ['blue', 'orange', 'green', 'red']  # Color for each device

# Function to simulate data transmission for a device
def transmit_data(device_id, time_slot):
    print(f"{DEVICE_NAMES[device_id]} is ready to transmit.")
    time.sleep(time_slot)  # Simulate transmission time
    print(f"{DEVICE_NAMES[device_id]} has finished transmitting.")

# Create threads for each device
threads = []
for device_id in range(NUM_DEVICES):
    time_slot = TIME_SLOTS[device_id]
    thread = threading.Thread(target=transmit_data, args=(device_id, time_slot))
    threads.append(thread)

# Start the transmission in a TDMA manner
for device_id in range(NUM_DEVICES):
    threads[device_id].start()  # Start the thread for the current device
    threads[device_id].join()    # Wait for the current device to finish before starting the next

print("All devices have completed their transmissions.")

# Data for the histogram
heights = [FREQUENCY] * NUM_DEVICES
x_positions = np.arange(1, len(heights) * DURATION, DURATION)  # X positions for the bars

# Create a new figure
plt.figure(figsize=(10, 6))

# Create the bars and store the bar objects for the legend
bars = plt.bar(x_positions, heights, width=DURATION, color=COLORS, edgecolor='black', alpha=0.7)

# Set the title and labels for the axes
plt.title('TDMA')
plt.xlabel('Time (seconds)')
plt.ylabel('Frequency (Hz)')

# Set the x and y limits
plt.xlim(0, 10)  # Adjust the x-axis limit as needed
plt.ylim(0, 10)  # Adjust the y-axis limit as needed

# Set x-ticks from 0 to 10 in multiples of 1
plt.xticks(range(11))  # This will create ticks at 0, 1, 2, ..., 10

# Add grid lines for better visibility
plt.grid(axis='y')

# Create a legend
plt.legend([bars[0], bars[1], bars[2], bars[3]], ['Device 1', 'Device 2', 'Device 3', 'Device 4'], loc='upper right')

# Show the histogram
plt.show()