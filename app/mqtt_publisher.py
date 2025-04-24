from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt
import asyncio
from app.gateway import on_message
load_dotenv()
MQTT_TOKEN = os.getenv("MQTT_TOKEN")
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = 1883

mqtt_client = mqtt.Client()
def init_mqtt():
    mqtt_client.username_pw_set(MQTT_TOKEN)
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop_start()
    
def on_connect(client, userdata, flags, rc):
    mqtt_client.subscribe("v1/devices/me/attributes")
    mqtt_client.subscribe("v1/devices/me/attributes/response/+")
    mqtt_client.publish('v1/devices/me/attributes/request/1', '{"sharedKeys":"node_map,value_map"}')
    mqtt_client.subscribe("v1/gateway/attributes")    
    mqtt_client.subscribe("v1/gateway/rpc")    

async def mqtt_publisher(mqtt_publish_queue):
    while True:
        payload = await mqtt_publish_queue.get()
        mqtt_client.publish("v1/gateway/telemetry", payload)
        print(payload)
        await asyncio.sleep(1)