import warnings
warnings.filterwarnings("ignore")

import psutil
import pandas as pd
import time
from datetime import datetime

# Parameters
duration = 60  # 1 minute for testing
interval = 5   # data every 5 seconds

# Create empty list to store data
data = []

print("Starting data collection...")

start_time = time.time()
while time.time() - start_time < duration:
    timestamp = datetime.now()
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # User input: Check if system has active users
    users = psutil.users()
    input_active = 1 if users else 0

    # Append data to list
    data.append([timestamp, cpu, memory, disk, input_active])

    # Print live progress
    print(f"{timestamp} | CPU: {cpu}% | Memory: {memory}% | Disk: {disk}% | InputActive: {input_active}")

    time.sleep(interval - 1)  # account for 1 second used by cpu_percent

# Convert to DataFrame
df = pd.DataFrame(data, columns=['Timestamp', 'CPU', 'Memory', 'Disk', 'InputActive'])

# Save to CSV
df.to_csv('system_usage.csv', index=False)
print("Data collection finished. Saved to system_usage.csv")
