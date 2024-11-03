import numpy as np
import matplotlib.pyplot as plt

# Step 1: Define the number of devices and their data
devices = {
    'Device 1': (0, np.array([1, 1, 1, 1])),      # Data: 0, Spreading Code
    'Device 2': (0, np.array([1, -1, 1, -1])),     # Data: 0, Spreading Code
    'Device 3': (None, np.array([0, 0, 0, 0])),    # Silent, Spreading Code
    'Device 4': (1, np.array([1, -1, -1, 1]))       # Data: 1, Spreading Code
}

# Step 2: Initialize effective spreading codes
effective_spreading_codes = {}

# Step 3: Calculate effective spreading codes
for device, (data, spreading_code) in devices.items():
    if data is None:  # Silent device
        effective_spreading_codes[device] = np.array([0, 0, 0, 0])
    elif data == 1:  # Data is 1
        effective_spreading_codes[device] = spreading_code
    else:  # Data is 0
        effective_spreading_codes[device] = -spreading_code

# Step 4: Form the data stream by summing effective spreading codes
data_stream = sum(effective_spreading_codes.values())
print("Data Stream:", data_stream)

# Function to decode data for a specific device
def decode_device(device_name):
    spreading_code = devices[device_name][1]
    if devices[device_name][0] is None:  # Check if the device is silent
        return 'Silent'  # Return 'Silent' for Device 3
    # Step 5: Calculate product result
    product_result = np.where(spreading_code == 1, data_stream, -data_stream)
    
    # Step 6: Sum the values of the product result and divide by the number of devices
    decoded_value = np.sum(product_result) / len(devices)
    return 1 if decoded_value > 0 else 0

# Decode the data for each device
decoded_data = {}
for device in devices.keys():
    decoded_data[device] = decode_device(device)

# Print the decoded data along with the original data
print("Decoded Data:")
for device in devices.keys():
    original_data = devices[device][0] if devices[device][0] is not None else 'Silent'
    decoded_value = decoded_data[device]
    print(f"{device}: Original Data = {original_data}, Decoded Data = {decoded_value}")

# Step 7: Plotting the effective spreading codes and the data stream as bar graphs
num_devices = len(devices)
time_slots = np.arange(len(effective_spreading_codes['Device 1'])) + 0.5  # Shifted by 0.5

# Create a figure for the bar graphs
fig, axs = plt.subplots(num_devices + 1, 1, figsize=(5, 12))

# Width of the bars
bar_width = 1  # Adjusted width for the bars

# Define colors for each device
colors = ['blue', 'yellow', 'green', 'red']

# Plot effective spreading codes for each device
for i, (device, code) in enumerate(effective_spreading_codes.items()):
    axs[i].bar(time_slots, code, width=bar_width, color=colors[i], alpha=0.7)
    axs[i].set_title(f'Digital Signal for {device}')
    axs[i].set_ylabel('Amplitude')
    axs[i].set_ylim(-4, 4)  # Set y-limits for better visibility
    axs[i].axhline(0, color='black', lw=2, ls='-')  # Add a horizontal line at y=0
    axs[i].grid()
    axs[i].set_xticks([0, 1, 2, 3, 4])  # Set x-ticks to integers from 0 to 4
    axs[i].set_xticklabels([0, 1, 2, 3, 4], rotation=0)  # Set x-tick labels to integers
    axs[i].set_yticks(np.arange(-4, 5, 1))  # Set y-ticks to increments of 1

# Plot data stream
axs[num_devices].bar(time_slots, data_stream, width=bar_width, color='black', alpha=0.7)
axs[num_devices].set_title ('Data Stream')
axs[num_devices].set_ylabel('Amplitude')
axs[num_devices].set_ylim(-4, 4)  # Set y-limits for better visibility
axs[num_devices].axhline(0, color='black', lw=2, ls='-')  # Add a horizontal line at y=0
axs[num_devices].grid()
axs[num_devices].set_xticks([0, 1, 2, 3, 4])  # Set x-ticks to integers from 0 to 4
axs[num_devices].set_xticklabels([0, 1, 2, 3, 4], rotation=0)  # Set x-tick labels to integers
axs[num_devices].set_yticks(np.arange(-4, 5, 1))  # Set y-ticks to increments of 1

# Set a common xlabel for the last graph
plt.xlabel('Sequence', fontsize=12)

# Adjust layout
plt.tight_layout()
plt.show()