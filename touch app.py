import streamlit as st
import pandas as pd
import psutil
import time
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
import joblib
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(page_title="Smart Sleep / Power Management", layout="wide")

st.title("Smart Sleep / Power Management Using Data Science")

# Sidebar options
option = st.sidebar.selectbox(
    "Choose an action:",
    ["Collect Data", "Train Model", "Predict Idle Periods", "Visualize Usage"]
)

# -------------------------------
if option == "Collect Data":
    st.subheader("Data Collection")
    duration = st.slider("Duration (seconds):", min_value=10, max_value=300, value=60, step=10)
    interval = st.slider("Sampling Interval (seconds):", min_value=1, max_value=10, value=5, step=1)
    
    if st.button("Start Data Collection"):
        st.write("Collecting data...")
        data = []
        start_time = time.time()
        while time.time() - start_time < duration:
            timestamp = datetime.now()
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            users = psutil.users()
            input_active = 1 if users else 0

            data.append([timestamp, cpu, memory, disk, input_active])
            st.write(f"{timestamp} | CPU: {cpu}% | Memory: {memory}% | Disk: {disk}% | InputActive: {input_active}")
            time.sleep(interval - 1)

        df = pd.DataFrame(data, columns=['Timestamp', 'CPU', 'Memory', 'Disk', 'InputActive'])
        df.to_csv("system_usage.csv", index=False)
        st.success("Data collection finished. Saved to system_usage.csv")

# -------------------------------
elif option == "Train Model":
    st.subheader("Feature Engineering & Model Training")
    try:
        df = pd.read_csv("system_usage.csv")
    except:
        st.error("system_usage.csv not found. Please collect data first.")
        st.stop()
    
    # Feature engineering
    df['CPU_avg'] = df['CPU'].rolling(window=3).mean()
    df['Memory_avg'] = df['Memory'].rolling(window=3).mean()
    df['Disk_avg'] = df['Disk'].rolling(window=3).mean()
    df['Idle'] = ((df['CPU_avg'] < 10) & (df['InputActive'] == 0)).astype(int)
    df.fillna(method='bfill', inplace=True)
    df.to_csv("processed_features.csv", index=False)
    
    # Train model
    X = df[['CPU_avg', 'Memory_avg', 'Disk_avg', 'InputActive']]
    y = df['Idle']
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X, y)
    joblib.dump(clf, "idle_predictor.pkl")
    st.success("Model trained and saved as idle_predictor.pkl")
    st.write(df.head())

# -------------------------------
elif option == "Predict Idle Periods":
    st.subheader("Idle Period Predictions")
    try:
        df = pd.read_csv("processed_features.csv")
        clf = joblib.load("idle_predictor.pkl")
    except:
        st.error("Required files not found. Please train the model first.")
        st.stop()
    
    predictions = []
    for i, row in df.iterrows():
        features = [[row['CPU_avg'], row['Memory_avg'], row['Disk_avg'], row['InputActive']]]
        pred = clf.predict(features)
        predictions.append(pred[0])
    
    df['PredictedIdle'] = predictions
    st.write(df[['Timestamp', 'CPU', 'Memory', 'Disk', 'InputActive', 'PredictedIdle']].head(20))
    st.success("Predictions done!")

# -------------------------------
elif option == "Visualize Usage":
    st.subheader("System Resource Usage & Idle Periods")
    try:
        df = pd.read_csv("processed_features.csv")
    except:
        st.error("processed_features.csv not found. Please run previous steps first.")
        st.stop()
    
    plt.figure(figsize=(12,6))
    plt.plot(pd.to_datetime(df['Timestamp']), df['CPU_avg'], label='CPU %', color='blue')
    plt.plot(pd.to_datetime(df['Timestamp']), df['Memory_avg'], label='Memory %', color='green')
    plt.plot(pd.to_datetime(df['Timestamp']), df['Disk_avg'], label='Disk %', color='orange')
    
    idle_times = df[df['Idle'] == 1]
    plt.scatter(pd.to_datetime(idle_times['Timestamp']), idle_times['CPU_avg'], color='red', label='Idle Periods', marker='x')
    
    plt.xticks(rotation=45)
    plt.xlabel('Timestamp')
    plt.ylabel('Usage %')
    plt.title('System Resource Usage & Idle Periods')
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)
