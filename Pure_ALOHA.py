import random
import time
import threading

# Parameters
Kmax = 15  # Maximum number of attempts
Tp = 1     # Maximum propagation time (in seconds)
Tf = 1     # Average transmission time for a frame (in seconds)
Tb = 1     # Back-off time (in seconds)

# Shared variables to simulate ACK reception
ack_received_device1 = threading.Event()
ack_received_device2 = threading.Event()
success_count = 0
success_lock = threading.Lock()

def device(device_id, ack_event):
    global success_count
    K = 0  # Number of attempts

    while True:
        print(f"Device {device_id}: Attempt {K}")
        
        # Step 3: Send the frame
        print(f"Device {device_id}: Sending frame...")
        
        # Simulate sending time
        time.sleep(Tf)
        
        # Step 4: Wait for time-out time (2 * Tp)
        print(f"Device {device_id}: Waiting for ACK...")
        time.sleep(2 * Tp)
        
        # Step 5: Check if ACK is received
        if ack_event.is_set():
            with success_lock:
                success_count += 1
            print(f"Device {device_id}: ACK received. Success!")
            break
        else:
            print(f"Device {device_id}: No ACK received.")
            K += 1
        
        # Step 6: Check if K > Kmax
        if K > Kmax:
            print(f"Device {device_id}: Maximum attempts reached. Aborting.")
            break
        
        # Step 7: Choose a random number R between 0 and 2^K - 1
        R = random.randint(0, 2**K - 1)
        print(f"Device {device_id}: Random back-off R = {R}")
        
        # Step 8: Wait Tb time (Tb - R * Tp or R * Tf)
        backoff_time = Tb - (R * Tp) if R * Tp < Tb else R * Tf
        print(f"Device {device_id}: Waiting for back-off time: {backoff_time:.2f} seconds")
        time.sleep(backoff_time)

        # Reset the ACK reception status for the next attempt
        ack_event.clear()

def ack_sender():
    global success_count
    while True:
        # Simulate random ACK sending
        time.sleep(random.uniform(2 * Tp, 5 * Tp))  # Random time to send ACK
        if success_count >= 2:  # Stop sending ACKs after both devices succeed
            print("ACK sender: Both devices have succeeded. Stopping ACK sender.")
            break
        # Randomly send ACK to one of the devices
        if random.choice([True, False]):
            ack_received_device1.set()
            print("ACK sent to Device 1!")
        else:
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