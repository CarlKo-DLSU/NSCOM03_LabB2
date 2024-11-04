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
                time.sleep(random.uniform(0.5, 1.5))  # Simulate transmission time
                print(f"Device {device_id} has finished transmitting.")
                self.is_busy = False
            else:
                print(f"Device {device_id} found the channel busy and will try again.")

class Device(threading.Thread):  # Inherit from threading.Thread
    def __init__(self, device_id, channel):
        super().__init__()
        self.device_id = device_id
        self.channel = channel

    def run(self):
        while True:
            if not self.channel.is_busy:
                self.channel.transmit(self.device_id)
                break
            else:
                print(f"Device {self.device_id} is sensing the channel and found it busy.")
                # Randomized backoff time to increase collision chances
                backoff_time = random.uniform(0.5, 1.5)  # Longer wait time
                print(f"Device {self.device_id} will wait for {backoff_time:.2f} seconds before trying again.")
                time.sleep(backoff_time)

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