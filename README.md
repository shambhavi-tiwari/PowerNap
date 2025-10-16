# PowerNap

PowerNap is a Python-based system that intelligently predicts idle periods on a laptop and visualizes system usage to optimize power management. The project leverages Operating System monitoring, data collection, and machine learning to provide insights into CPU, Memory, and Disk usage and suggest low-power or sleep modes during idle periods.

This project demonstrates a real-world application of data science in operating systems, helping extend battery life without user intervention.

## Screenshots

**PowerNap Home Page**
![Data Collection](dashboard.jpeg)

**Visuals**
![Resource Usage](dashboard-cont.jpeg)
![Graphs](visuals.jpeg)

---

## Features

Collects real-time system resource usage (CPU, Memory, Disk).

Visualizes resource usage in interactive line charts.

Predicts idle periods using a Random Forest machine learning model.

Provides an interactive Streamlit web app interface.

Saves data and predictions for offline analysis.

---


## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites
1. Python 3.x installed on your system.

2. Pip for installing Python packages.

3. Required Python libraries:
```sh
pip3 install streamlit pandas psutil scikit-learn matplotlib joblib
```

4. Terminal/Command Line access to run the app.


### Installation

1.  **Clone the repository:**
    ```sh
    https://github.com/shambhavi-tiwari/PowerNap.git
    cd PowerNap
    ```

2.  **Install dependencies:**
    ```sh
    python3 -m venv venv
    source venv/bin/activate   # For Mac/Linux
    venv\Scripts\activate      # For Windows
    ```

3.  **Set up environment variables:**
    ```env
    pip install streamlit pandas psutil matplotlib
    ```

4.  **Run:**
    ```sh
    streamlit run app.py
    ```

The application should now be running on a localhost on your laptop/PC. 

---

## Visual Structure

```
PowerNap/
│
├─ app.py                  # Main Streamlit app
├─ data_collection.py      # Script for collecting system usage data
├─ ml_model.py             # (Optional) predictive model scripts
├─ system_usage.csv        # Sample or generated data file
├─ background_new.jpg      # Background image for Streamlit app
├─ requirements.txt        # Python dependencies
└─ README.md               # Project documentation

```
---

## License

This project is open-source and free for personal, educational, or research use.

© Shambhavi Tiwari, Oct 2025
