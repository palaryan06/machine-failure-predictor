Real-Time Machine Failure Prediction System

C++ | MQTT | Python | Logistic Regression

1. Project Overview

  - This project implements a real-time predictive maintenance system that simulates industrial sensor data using C++ and performs machine failure prediction using a Logistic Regression model in Python.

  - Due to the absence of a real industrial hardware environment, sensor readings are simulated using a shuffled and modified dataset. The system mimics real-time IoT data streaming via MQTT and processes incoming batches for failure prediction.

2. Target Industrial Use Case

    - The dataset aligns with a Smart Industrial HVAC and Environmental Control Unit (Air Handling Unit - AHU) deployed in:

    - Smart factories

    - Semiconductor manufacturing facilities

    - Pharmaceutical clean rooms

    - Large industrial production environments

    - The system monitors environmental and operational parameters and predicts potential failure conditions.

3. System Architecture
    3.1 Sensor Simulation (C++ Publisher)

        Reads 6 lines from a CSV file every 6 seconds

        Writes the 6 lines into a temporary CSV file

        Converts the readings into a stream buffer

        Publishes the data using MQTT

        Uses HiveMQ as the MQTT broker

        This simulates real-time industrial sensor transmission.

    3.2 Data Transmission Layer

        Protocol: MQTT

        Broker: HiveMQ

        Communication: Topic-based publish-subscribe architecture
        
    3.3 Machine Learning Prediction (Python Subscriber)

        Upon receiving 6 sensor readings:

        Converts the incoming data into a Pandas DataFrame

        Adds required column structure

        Applies StandardScaler (fitted during training)

        Performs prediction using a trained Logistic Regression model

        Applies Majority Voting (mode) across 6 predictions

        Final Output:

        0 → Machine operating normally

        1 → Machine failure detected

        If the majority of predictions are 1, a failure condition is triggered.
    
4. Machine Learning Model

    Algorithm: Logistic Regression

    Feature Scaling: StandardScaler

    Voting Mechanism: Majority Voting (Mode)

    Training Data: Shuffled and modified dataset simulating industrial conditions

5. Dataset Structure

    Example sample:

    footfall,tempMode,AQ,USS,CS,VOC,RP,IP,Temperature,fail
    190,1,3,3,5,1,20,4,1,0
    31,7,2,2,6,1,24,6,1,0
    640,7,5,6,4,0,68,6,1,0

    Feature Description (Simulated)

    footfall – Operational load indicator

    tempMode – Operating mode

    AQ – Air quality index

    USS – Ultrasonic sensor reading

    CS – Current sensor value

    VOC – Volatile organic compound level

    RP – Rotational parameter

    IP – Input parameter / pressure

    Temperature – System temperature

    fail – Target variable (0 = No Failure, 1 = Failure)

6. Tech Stack

    C++ (Sensor simulation & MQTT publisher)

    Python (ML model & subscriber)

    Pandas

    Scikit-learn

    MQTT (HiveMQ broker)

    CSV-based simulation

7. Execution Flow

    Train the Logistic Regression model in Python

    Start MQTT broker (HiveMQ)

    Run C++ publisher to simulate sensor readings

    Run Python subscriber

    Observe real-time batch-based failure prediction

8. Future Improvements

    Deploy model using REST API (Flask/FastAPI)

    Integrate real IoT sensor hardware

    Add real-time dashboard visualization

    Implement anomaly detection models


9. Author

    Aryan
    B.Tech Computer Science Engineering