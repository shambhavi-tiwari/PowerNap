import streamlit as st
import pandas as pd
import psutil
import time
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# ---------------- Streamlit Page Config ----------------
st.set_page_config(page_title="Smart Sleep Project", layout="wide")

# ---------------- Custom CSS for background & fonts ----------------
st.markdown(
    f"""
    <style>
    /* Background image */
    .stApp {{
        background: url("background_new.jpg");
        background-size: cover;
        background-attachment: fixed;
    }}
    /* Title */
    .big-font {{
        font-size:50px !important;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }}
    /* Footer */
    .footer {{
        font-size:16px;
        color:#ffffff;
        text-align:center;
        margin-top:20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- Title ----------------
st.markdown('<p class="big-font">PowerNap</p>', unsafe_allow_html=True)

# ---------------- Subheading ----------------
st.markdown(
    '<p style="font-size:22px; color:#e0e0e0; text-align:center; font-weight:300;">Smart sleep management for laptops</p>', 
    unsafe_allow_html=True
)

st.write("---")

# ---------------- Sidebar ----------------
st.sidebar.title("Options")
option = st.sidebar.selectbox("Select Action:", ["Collect Data", "Visualize Data"])

# ---------------- Sidebar Footer ----------------
st.sidebar.markdown("<p style='font-size:14px;color:gray;'>Created by Shambhavi Tiwari © Oct 2025</p>", unsafe_allow_html=True)

# ---------- Collect Data ----------
if option == "Collect Data":
    st.subheader("Data Collection")
    duration = st.slider("Duration (seconds)", 10, 60, 20)
    interval = st.slider("Interval (seconds)", 1, 10, 5)
    
    if st.button("Start Data Collection"):
        st.info("Collecting data...")
        data = []
        start_time = time.time()
        progress_bar = st.progress(0)
        status_text = st.empty()

        while time.time() - start_time < duration:
            timestamp = datetime.now()
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            users = psutil.users()
            input_active = 1 if users else 0

            data.append([timestamp, cpu, memory, disk, input_active])
            status_text.text(f"{timestamp} | CPU: {cpu}% | Memory: {memory}% | Disk: {disk}% | InputActive: {input_active}")
            
            # Update progress
            progress_bar.progress(min((time.time() - start_time)/duration, 1.0))
            time.sleep(interval - 1)

        df = pd.DataFrame(data, columns=['Timestamp', 'CPU', 'Memory', 'Disk', 'InputActive'])
        df.to_csv("system_usage.csv", index=False)
        st.success("Data collection finished! Saved as system_usage.csv")

        # ---------- Plot graph ----------
        st.subheader("System Usage Graph")
        st.line_chart(df[['CPU', 'Memory', 'Disk']])

# ---------- Visualize Data ----------
elif option == "Visualize Data":
    st.subheader("Visualization")
    try:
        df = pd.read_csv("system_usage.csv")
        st.write(df.head())
        st.line_chart(df[['CPU', 'Memory', 'Disk']])
    except:
        st.error("system_usage.csv not found. Please collect data first.")

# ---------- Footer ----------
st.markdown('<p class="footer">Made by Shambhavi Tiwari</p>', unsafe_allow_html=True)
