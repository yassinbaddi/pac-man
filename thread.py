import threading
import time

def network_request(site, delay):
    print(f"Starting download from {site}...")
    time.sleep(delay)  # Simulating a network delay
    print(f"Finished download from {site}!")

# 1. Create thread instances
thread1 = threading.Thread(target=network_request, args=("Google", 2))
thread2 = threading.Thread(target=network_request, args=("GitHub", 1))

# 2. Start execution
thread1.start()
thread2.start()

# 3. Wait for threads to finish before moving the main script forward
thread1.join()
thread2.join()

print("All downloads complete.")
