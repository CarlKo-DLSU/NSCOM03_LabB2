import random
import time
import threading

class Channel:
    def __init__(self):
        self.is_busy = False
        self.lock = threading.Lock()  # Use a lock to manage access to the channel

    def transmit(self, device_id):
        with self.lock:  # Ensure that only one device can transmit at a time
            if not self.is_busy:
                self.is_busy = True
                print(f"Device {device_id} is transmitting...")
                # Simulate transmission time
                transmission_time = random.uniform(0.5, 1.5)
                time.sleep(transmission_time)

                # Simulate the possibility of a collision
                if random.random() < 0.2:  # 20% chance of collision
                    print(f"Collision detected during transmission by Device {device_id}!")
                    self.is_busy = False  # Reset the channel state
                    return False  # Indicate that a collision occurred
                else:
                    print(f"Device {device_id} has finished transmitting successfully.")
                    self.is_busy = False
                    return True  # Indicate successful transmission
            else:
                print(f"Device {device_id} found the channel busy and will try again.")
                return False  # Indicate that the channel was busy

class Device(threading.Thread):  # Inherit from threading.Thread
    def __init__(self, device_id, channel):
        super().__init__()
        self.device_id = device_id
        self.channel = channel

    def run(self):
        while True:
            if not self.channel.is_busy:
                if self.channel.transmit(self.device_id):
                    break  # Exit if transmission was successful
                else:
                    # If there was a collision, wait for a random backoff time
                    backoff_time = random.uniform(0.5, 1.5)
                    print(f"Device {self.device_id} will back off for {backoff_time:.2f} seconds due to collision.")
                    time.sleep(backoff_time)
            else:
                print(f"Device {self.device_id} is sensing the channel and found it busy.")
                time.sleep(random.uniform(0.5, 1.5))  # Wait before trying again

def main():
    channel = Channel()
    devices = [Device(i, channel) for i in range(1, 5)]  # Create 4 devices for higher collision chance

    # Start all devices
    for device in devices:
        device.start()

    # Wait for all devices to finish
    for device in devices:
        device.join()

if __name__ == "__main__":
    main()