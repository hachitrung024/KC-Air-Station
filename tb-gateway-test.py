import time
from tb_gateway_mqtt import TBGatewayMqttClient

DEVICE = "KC Air Station 001"
gateway = TBGatewayMqttClient("app.coreiot.io", username="7fue97cx1qc782x6wms9")
gateway.connect()
gateway.gw_connect_device(DEVICE)

gateway.gw_send_telemetry(DEVICE, {"ts": int(round(time.time() * 1000)), "values": {"temperature": 42.2}})
gateway.gw_send_attributes(DEVICE, {"firmwareVersion": "2.3.1"})

gateway.gw_disconnect_device(DEVICE)
gateway.disconnect()