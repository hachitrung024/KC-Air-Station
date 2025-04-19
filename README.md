# KC-Air-Station

**KC-Air-Station** is a Raspberry Pi-based system that communicates with LoRa EBYTE E22 modules for wireless environmental data transmission. The system supports two operational modes:

- **Node** — Receives data from external sensors (e.g., M5Stack Core2) via USB serial.
- **Gateway** — Listens to LoRa data over GPIO UART and publishes it to MQTT brokers.

---

## 🧰 Hardware Setup

### 📟 Raspberry Pi

- Raspberry Pi Zero / 3 / 4
- Waveshare **LoRa-E22-XX (Pi-LoRa)** module

### ⚙️ LoRa Module Configuration (Waveshare Pi-LoRa)

> Make sure to configure the jumpers on the Pi-LoRa board correctly:

✅ Required:

- Connect jumper **to position B** (for using Pi UART)
  
  _This enables UART via GPIO14 (TXD) and GPIO15 (RXD)_

❌ Remove jumpers from **M0** and **M1** if you are setting those pins via GPIO manually in software

```text
Pi GPIO Pinout
--------------
LoRa <-> Raspberry Pi

M0  -> GPIO17
M1  -> GPIO27
TX  -> GPIO15 (RXD)
RX  -> GPIO14 (TXD)
VCC -> 3.3V
GND -> GND
---

## ⚙️ Raspberry Pi Configuration

### 1. Enable UART Hardware Interface

sudo raspi-config
```


Go to:

```
Interface Options → Serial Port
```

- "Login shell over serial?" → **No**
- "Enable serial hardware port?" → **Yes**

Then reboot:

```bash
sudo reboot
```

### 2. Add User Permissions (optional)

```bash
sudo usermod -a -G dialout $USER
```

Logout or reboot to apply.

---

## 🚀 Software Installation

### 1. Install System Dependencies

```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev python3-rpi.gpio
```

### 2. Plug in the Hardware

- Connect **LoRa E22** module to GPIO (TX/RX/GND/3.3V)
- Connect **M5 Core2** (Node) via USB-C → USB-A

### 3. Set Up the Python Environment

```bash
./setup.sh
```

This script will:
- Create a virtual environment with system site-packages
- Install dependencies from `requirements.txt`

---

## ⚙️ Environment Variables

Create a `.env` file to configure serial and MQTT settings:

```env
SERIAL_PORT=/dev/serial0
BAUD_RATE=9600
MQTT_BROKER=localhost
MQTT_PORT=1883
```

---

## ▶️ Running the System

### Node Mode (reads USB serial from M5 Core2)

```bash
./run.sh
```

### Gateway Mode (receives LoRa and pushes to MQTT)

```bash
./run_gateway.sh
```

---

## 📁 Project Structure

```
KC-Air-Station/
├── app/
│   └── lora_handler.py
├── main.py
├── run.sh
├── run_gateway.sh
├── setup.sh
├── requirements.txt
├── .env
└── README.md
```
---
## 🛠 Configuration

All runtime settings are controlled via `settings/config.ini`). You can adjust serial ports, LoRa parameters, station IDs, and more depending on whether you’re running in **Node** or **Gateway** mode.

### 📡 [lora] LoRa Module Settings

| Key            | Description                              |
|----------------|------------------------------------------|
| `device`       | Path to LoRa UART device (`/dev/serial0`) |
| `model`        | LoRa hardware model (e.g. `400T22S`)     |
| `config_model` | Configuration mode type                  |
| `aux_pin`      | GPIO pin used for AUX                    |
| `m0_pin`       | GPIO pin for mode control (M0)           |
| `m1_pin`       | GPIO pin for mode control (M1)           |
| `baudrate`     | UART baudrate for LoRa                   |
| `add_h/l`      | Local LoRa module address (high/low byte)|
| `chan`         | LoRa channel (must match target)         |
| `net_id`       | LoRa network ID (if applicable)          |
| `crypt_h/l`    | Encryption key (if supported)            |

> 🔁 Each LoRa module must have a **unique address** (`add_h`, `add_l`) and must operate on the same `chan` to communicate.

---

### 🧭 [target]

Nodes need to specify the address of the **Gateway** they send data to.

```ini
[target]
add_h = 0x00
add_l = 0x06
chan  = 23
```

> 💡 Make sure this matches the Gateway’s `add_h`, `add_l`, and `chan` settings.

---

### 💻 [uart]

Used when reading data from a USB serial source such as M5Stack:

```ini
[uart]
port     = /dev/ttyACM0
baudrate = 115200
timeout  = 1
```

---

### 🗺 [station_mapping]

This allows friendly names for known LoRa IDs.

```ini
[station_mapping]
9F10AB = KC Air Station 001
9F103C = KC Air Station 002
```

> When a LoRa message is received from `9F10AB`, it will be labeled as **KC Air Station 001**.

---

### 🌡 [sensor_mapping]

Maps variable codes to human-readable sensor types.

```ini
[sensor_mapping]
V1 = temperature
V2 = humidity
V3 = dewpoint
```

> Example: `V1=25.4` becomes `temperature=25.4`.

---

## 🔄 Configuration Tips

- **Each device (Node or Gateway) must have a unique LoRa address (`add_h`/`add_l`).**
- **All devices communicating must share the same channel.**
- **Nodes must configure the `target` section to point to their Gateway.**
- **Gateways don't need a `target`, but must listen on a known `add_h`/`add_l` so nodes can send to it.**
- Configuration files should be passed or loaded automatically in the code. Ensure your main scripts read the correct `config.ini`.

---

```
## 👤 Maintainer

**Author:** hachi  
**License:** MIT

```

---