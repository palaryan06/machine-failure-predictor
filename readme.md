# Real-Time Machine Failure Prediction System

> **A real-time industrial machine failure prediction system built using C++, MQTT, Python, and Machine Learning.**

## Overview

This project demonstrates an end-to-end predictive maintenance pipeline that simulates industrial IoT sensor data, streams it using MQTT, performs real-time machine failure prediction with a Logistic Regression model, and visualizes the results through a modern Streamlit dashboard.

The objective is to showcase how machine learning can be integrated with software systems to monitor industrial equipment in real time.

---

## Key Features

* Real-time sensor simulation using C++
* MQTT-based publish/subscribe communication
* Machine Learning inference using Logistic Regression
* StandardScaler preprocessing pipeline
* Batch-based prediction using Majority Voting
* Live industrial monitoring dashboard built with Streamlit
* Modular architecture with a shared inference engine
* Relative-path project structure for portability
* One-click project launcher using batch scripts

---

## Architecture

```text
                C++ Sensor Simulator
                         │
                         ▼
                  MQTT (HiveMQ)
                         │
                         ▼
                Python Inference Engine
        (Scaling + Logistic Regression)
                         │
                         ▼
            Shared Inference Module
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   MQTT Subscriber              Streamlit Dashboard
```

---

## Dashboard

The dashboard provides:

* Live MQTT monitoring
* Machine health prediction
* Prediction confidence
* Live sensor visualization
* Prediction history
* Model evaluation metrics
* Confusion Matrix
* ROC Curve
* Feature Importance
* System architecture overview

---

## Machine Learning Pipeline

Model:

* Logistic Regression

Preprocessing:

* StandardScaler

Inference:

* Batch prediction
* Majority Voting (Mode)

Output:

* **0** → Normal Operation
* **1** → Machine Failure

---

## Dataset

Since real industrial hardware was unavailable, this project uses a shuffled and modified dataset to simulate real-time industrial sensor streams.

Features include:

* Footfall
* Temperature Mode
* Air Quality
* Ultrasonic Sensor
* Current Sensor
* VOC
* Rotational Parameter
* Input Parameter
* Temperature

Target:

* **fail**

  * 0 → Normal
  * 1 → Failure

---

## Tech Stack

### Languages

* C++
* Python

### Libraries

* Pandas
* NumPy
* Scikit-learn
* Plotly
* Streamlit
* Paho MQTT

### Communication

* MQTT
* HiveMQ Broker

---

## Project Structure

```text
Machine_failure_detection/

├── mqtt_c++/
├── python/
│   ├── dashboard/
│   ├── inference/
│   ├── mqtt/
│   └── model/
├── requirements.txt
├── setup.bat
├── run_dashboard.bat
├── run_publisher.bat
└── run_project.bat
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd Machine_failure_detection
```

### 2. Install dependencies

Run:

```text
setup.bat
```

This creates a virtual environment and installs all required packages.

---

### 3. Start the project

Run:

```text
run_project.bat
```

This automatically:

* Starts the Streamlit dashboard
* Launches the MQTT publisher
* Opens the dashboard in your browser

---

## Future Improvements

* Support real industrial IoT devices
* Local MQTT broker deployment
* Docker support
* REST API using FastAPI
* Advanced anomaly detection models
* Deep Learning-based failure prediction
* Cloud deployment
* Real-time alert system

---

## Author

**Aryan**

B.Tech Computer Science Engineering

Interested in Machine Learning, Software Engineering, Industrial AI, and Intelligent IoT Systems.
