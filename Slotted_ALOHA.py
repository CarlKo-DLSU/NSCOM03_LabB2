import random
import time
import threading

# Parameters
Kmax = 15  # Maximum number of attempts
Tp = 1     # Maximum propagation time (in seconds)
Tf = 1     # Average transmission time for a frame (in seconds)
Tb = 1     # Back-off time (in seconds)
slot_duration = 2  # Duration of each time slot (in seconds)

# Shared variables to simulate ACK reception
ack_received_device1 = threading.Event()
ack_received_device2 = threading.Event()
success_count = 0
success_lock = threading.Lock()
device1_success = False
device2_success = False
device1_attempted = False
device2_attempted = False

def wait_for_slot_start():
    # Wait until the start of the next time slot
    time.sleep(slot_duration)

def device(device_id, ack_event):
    global success_count, device1_success, device2_success, device1_attempted, device2_attempted

    K = 0  # Number of attempts

    while True:
        if (device_id == 1 and device1_success) or (device_id == 2 and device2_success):
            print(f"Device {device_id}: Already successful, exiting.")
            break

        # Wait for the start of a slot
        wait_for_slot_start()

        print(f"Device {device_id}: Attempt {K}")
        
        # Step 4: Send the frame
        print(f"Device {device_id}: Sending frame...")
        
        # Simulate sending time with a slight random delay
        time.sleep(Tf + random.uniform(0, 0.5))  # Add randomness to simulate different sending times
        
        # Step 5: Mark that the device has attempted to send
        if device_id == 1:
            device1_attempted = True
        else:
            device2_attempted = True
        
        # Step 6: Wait for time-out time (2 * Tp)
        print(f"Device {device_id}: Waiting for ACK...")
        time.sleep(2 * Tp)
        
        # Step 7: Check if ACK is received (simulate collision)
        if ack_event.is_set():
            with success_lock:
                success_count += 1
                if device_id == 1:
                    device1_success = True
                else:
                    device2_success = True
            print(f"Device {device_id}: ACK received. Success!")
            break  # Exit the loop immediately after receiving an ACK
        else:
            print(f"Device {device_id}: No ACK received or collision occurred.")
            K += 1
        
        # Step 8: Check if K > Kmax
        if K >= Kmax:
            print(f"Device {device_id}: Maximum attempts reached. Aborting.")
            break
        
        # Step 9: Choose a random number R between 0 and 2^K - 1
        R = random.randint(0, 2**K - 1)
        print(f"Device {device_id}: Random back-off R = {R}")
        
        # Step 10: Wait Tb time (Tb - R * Tp or R * Tf)
        backoff_time = Tb - (R * Tp) if R * Tp < Tb else R * Tf
        print(f"Device {device_id}: Waiting for back-off time: {backoff_time:.2f} seconds")
        time.sleep(backoff_time)

        # Reset the ACK reception status for the next attempt
        ack_event.clear()

def ack_sender():
    global success_count, device1_success, device2_success

    while success_count < 2:  # Continue until both devices succeed
        time.sleep(random.uniform(1, 3))  # Random time to wait before sending ACK
        
        # Send ACKs only if the devices have attempted to send
        if device1_attempted and not device1_success and random.random() < 0.5:  # 50% chance to send ACK to Device 1
            if not ack_received_device1.is_set():  # Only send if not already set
                ack_received_device1.set()
                print("ACK sent to Device 1!")
        
        if device2_attempted and not device2_success and random.random() < 0.5:  # 50% chance to send ACK to Device 2
            if not ack_received_device2.is_set():  # Only send if not already set
                ack_received_device2.set()
                print("ACK sent to Device 2!")

# Create threads for devices
device1_thread = threading.Thread(target=device, args=(1, ack_received_device1))
device2_thread = threading.Thread(target=device, args=(2, ack_received_device2))
ack_sender_thread = threading.Thread(target=ack_sender)

# Start the threads
device1_thread.start()
device2_thread.start()
ack_sender_thread.start()

# Wait for device threads to finish
device1_thread.join()
device2_thread.join()
ack_sender_thread.join()

print("All devices have completed communication.")