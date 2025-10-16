import warnings
warnings.filterwarnings("ignore")

import pandas as pd

# Load collected data
df = pd.read_csv('system_usage.csv')

# Create rolling average features (smooth short spikes)
df['CPU_avg'] = df['CPU'].rolling(window=3).mean()
df['Memory_avg'] = df['Memory'].rolling(window=3).mean()
df['Disk_avg'] = df['Disk'].rolling(window=3).mean()

# Create 'Idle' label: 1 if CPU < 10% and InputInactive, else 0
df['Idle'] = ((df['CPU_avg'] < 10) & (df['InputActive'] == 0)).astype(int)

# Fill NaN from rolling window
df.fillna(method='bfill', inplace=True)

# Save processed features
df.to_csv('processed_features.csv', index=False)
print("Feature engineering done. Saved to processed_features.csv")
