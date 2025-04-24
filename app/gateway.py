import asyncio
import json
import os

# Đọc file JSON
with open("data/node_map.json", "r") as f:
    station_map = json.load(f)

with open("data/value_map.json", "r") as f:
    sensor_map = json.load(f)

print("Mapping:")
print("Station Map:", station_map)
print("Sensor Map:", sensor_map)

async def gateway_task(lora_rx_queue, mqtt_publish_queue):
    while True:
        await asyncio.sleep(0.01)
        data = await lora_rx_queue.get()
        if isinstance(data, bytes):
            data = data.decode("utf-8", errors='ignore')
        try:
            raw_json = json.loads(data)
        except json.JSONDecodeError:
            continue

        if not isinstance(raw_json, dict) or len(raw_json) != 1:
            continue

        station_id = list(raw_json.keys())[0]
        readings = raw_json[station_id]

        if station_id not in station_map or not isinstance(readings, list):
            continue

        mapped_station = station_map[station_id]
        raw_reading = readings[0]

        # sensor key mapping
        mapped_reading = {}
        for k, v in raw_reading.items():
            if k in sensor_map:
                mapped_reading[sensor_map[k]] = v

        if not mapped_reading:
            continue

        final_payload = json.dumps({mapped_station: [mapped_reading]})
        await mqtt_publish_queue.put(final_payload)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8', errors='ignore')
    print(f"MQTT message received | Topic: {topic} | Payload: {payload}")

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        print("Payload is not a valid json")
        return
    if topic == "v1/devices/me/attributes":
        update_data(data)
    elif topic == "v1/devices/me/attributes/response/1":
        update_data(data["shared"])

def update_data(json_data):
    global station_map, sensor_map
    if not isinstance(json_data, dict):
        print("update_data nhận dữ liệu không hợp lệ.")
        return

    if "node_map" in json_data:
        station_map = json_data["node_map"]
        with open("data/node_map.json", "w") as f:
            json.dump(station_map, f, indent=2)
        print("Updated node_map")

    if "value_map" in json_data:
        sensor_map = json_data["value_map"]
        with open("data/value_map.json", "w") as f:
            json.dump(sensor_map, f, indent=2)
        print("Updated value_map")