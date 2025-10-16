import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import joblib
import time

# Load model
clf = joblib.load('idle_predictor.pkl')

# Load latest data (simulation)
df = pd.read_csv('processed_features.csv')

for i, row in df.iterrows():
    features = [[row['CPU_avg'], row['Memory_avg'], row['Disk_avg'], row['InputActive']]]
    pred = clf.predict(features)
    
    if pred[0] == 1:
        print(f"{row['Timestamp']}: System predicted idle. Suggest entering low-power mode.")
    else:
        print(f"{row['Timestamp']}: System active.")
    time.sleep(0.5)  # slow down for demo
