import asyncio
import json
import configparser

config = configparser.ConfigParser()
config.optionxform = str
config.read("config/settings.ini")

station_map = dict(config["station_mapping"])
sensor_map = dict(config["sensor_mapping"])

print("Mapping:")
print(station_map)
print(sensor_map)

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
