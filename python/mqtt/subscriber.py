import pandas as pd 
import paho.mqtt.client as mqtt
import joblib
from statistics import mode
import numpy as np

broker = "test.mosquitto.org"
PORT = 1883
TOPIC = "test/aryan/mqtt"
CLIENT_ID = "aryan_python_subscriber_001"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker successfully")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code", rc)

def on_message(client, userdata, msg):
    print("---- MESSAGE RECEIVED ----")
    print("Topic :", msg.topic)
    print("QoS   :", msg.qos)
    print("Retain:", msg.retain)   

    payload_str = msg.payload.decode("utf-8", errors="replace")

    # with open("C:\\Users\\palar\\OneDrive\\Desktop\\Machine_failure_detection\\hourly.csv", "w", encoding="utf-8", newline="") as f:
    #     f.write("footfall,tempMode,AQ,USS,CS,VOC,RP,IP,Temperature\n")
    #     f.write(payload_str)
    if not payload_str:
        print("empty heartbeat")
        return
    print("payload received")
    data=[]

    for i in enumerate(payload_str.splitlines()):
        data.append([float(x) for x in i[1].split(",")])

    
    evaluate(data)
def evaluate(data):        
    
    df=pd.DataFrame(data,columns=['footfall','tempMode','AQ','USS','CS','VOC','RP','IP','Temperature'])
    df_scaled = scaler.transform(df)
    prediction = model.predict(df_scaled)
    probability = model.predict_proba(df_scaled)
    final_prediction=np.mean(prediction,axis=0)
    final_prediction = mode(prediction)
    
    print("Final Prediction:", final_prediction)




client = mqtt.Client(
    client_id=CLIENT_ID,
    clean_session=True  
)
scaler=joblib.load("C:\\Users\\palar\\OneDrive\\Desktop\\Machine_failure_detection\\python\\model\\scaler.pkl")
model=joblib.load("C:\\Users\\palar\\OneDrive\\Desktop\\Machine_failure_detection\\python\\model\\failure_model.pkl")

client.on_connect = on_connect
client.on_message = on_message


client.connect(broker, PORT, 60)
client.loop_forever()
