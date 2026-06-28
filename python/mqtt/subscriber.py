import sys
from pathlib import Path

import paho.mqtt.client as mqtt

# Allow imports from the shared inference package when run from this directory.
PYTHON_ROOT = Path(__file__).resolve().parent.parent
if str(PYTHON_ROOT) not in sys.path:
    sys.path.insert(0, str(PYTHON_ROOT))

from inference.artifacts import load_model, load_scaler
from inference.evaluate import evaluate
from inference.payload import parse_mqtt_payload

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

    if not payload_str:
        print("empty heartbeat")
        return

    print("payload received")
    data = parse_mqtt_payload(payload_str)
    if not data:
        return

    result = evaluate(data, scaler, model)
    print("Final Prediction:", result["final_prediction"])


client = mqtt.Client(
    client_id=CLIENT_ID,
    clean_session=True,
)
scaler = load_scaler()
model = load_model()

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, PORT, 60)
client.loop_forever()
