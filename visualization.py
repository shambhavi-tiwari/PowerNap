import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt

# Load processed data
df = pd.read_csv('processed_features.csv')

plt.figure(figsize=(12,6))
plt.plot(df['Timestamp'], df['CPU_avg'], label='CPU %', color='blue')
plt.plot(df['Timestamp'], df['Memory_avg'], label='Memory %', color='green')
plt.plot(df['Timestamp'], df['Disk_avg'], label='Disk %', color='orange')

# Highlight idle periods
idle_times = df[df['Idle'] == 1]
plt.scatter(idle_times['Timestamp'], idle_times['CPU_avg'], color='red', label='Idle Periods', marker='x')

plt.xticks(rotation=45)
plt.xlabel('Timestamp')
plt.ylabel('Usage %')
plt.title('System Resource Usage & Idle Periods')
plt.legend()
plt.tight_layout()
plt.show()
