from nicegui import ui
import json
import os
import subprocess
from datetime import datetime
import random

CONFIG_PATH = '/home/vinitbparikh/sensor_config.json'

# Default config
default_config = {
    "pharmacy_name": "",
    "ncpdp": "",
    "sensor_count": 1
}

# Load config
def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    else:
        return default_config.copy()

# Save config
def save_config(data):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(data, f)

config = load_config()

# Simulate sensor readings (replace with real data later)
def get_sensor_data():
    data = []
    for i in range(config["sensor_count"]):
        temp = round(random.uniform(35, 45), 1)
        humidity = round(random.uniform(30, 60), 1)
        data.append({
            "id": i + 1,
            "temperature": temp,
            "humidity": humidity,
            "min_temp": temp - random.uniform(1, 2),
            "max_temp": temp + random.uniform(1, 2),
        })
    return data

with ui.header().classes('items-center justify-between'):
    ui.label('📡 HealtheRx Temperature Dashboard').classes('text-xl')
    ui.button('Edit Info', on_click=lambda: edit_dialog.open())
    ui.button('Update Firmware', on_click=lambda: update_firmware())
    ui.button('Reboot', on_click=lambda: reboot_pi())

# Info panel
with ui.row():
    name_label = ui.label(f"Pharmacy Name: {config['pharmacy_name']}")
    ncpdp_label = ui.label(f"NCPDP: {config['ncpdp']}")
    sensor_label = ui.label(f"Sensors: {config['sensor_count']}")

# Sensor data grid
sensor_grid = ui.grid(columns=3).classes('w-full')

def update_sensor_grid():
    sensor_grid.clear()
    data = get_sensor_data()
    for sensor in data:
        with sensor_grid:
            with ui.card().classes('m-2'):
                ui.label(f"Sensor #{sensor['id']}")
                ui.label(f"Temp: {sensor['temperature']}°F")
                ui.label(f"Humidity: {sensor['humidity']}%")
                ui.label(f"Min: {sensor['min_temp']:.1f}°F")
                ui.label(f"Max: {sensor['max_temp']:.1f}°F")

# Edit Info dialog
with ui.dialog() as edit_dialog:
    with ui.card():
        new_name = ui.input("Pharmacy Name", value=config['pharmacy_name'])
        new_ncpdp = ui.input("NCPDP", value=config['ncpdp'])
        new_sensors = ui.number("Total Sensors", value=config['sensor_count'], min=1, max=10)

        def save_and_close():
            config['pharmacy_name'] = new_name.value
            config['ncpdp'] = new_ncpdp.value
            config['sensor_count'] = int(new_sensors.value)
            save_config(config)
            name_label.text = f"Pharmacy Name: {config['pharmacy_name']}"
            ncpdp_label.text = f"NCPDP: {config['ncpdp']}"
            sensor_label.text = f"Sensors: {config['sensor_count']}"
            update_sensor_grid()
            edit_dialog.close()

        ui.button("Save", on_click=save_and_close)

def update_firmware():
    with ui.dialog():
        with ui.card():
            ui.label("🔄 Updating from GitHub...")
            result = subprocess.run(['git', '-C', '/home/vinitbparikh/sensor-dashboard', 'pull'], capture_output=True)
            msg = result.stdout.decode() if result.returncode == 0 else result.stderr.decode()
            ui.label(msg)

def reboot_pi():
    subprocess.run(['sudo', 'reboot'])

# Refresh sensor grid every 10s
update_sensor_grid()
ui.timer(10, update_sensor_grid)

ui.run(native=True, fullscreen=True, reload=False, title="HealtheRx Dashboard")
