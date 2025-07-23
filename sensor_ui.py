from nicegui import ui
import json
import os
import subprocess
from datetime import datetime
import random  # Replace with real sensor data import

INFO_FILE = '/home/vinitbparikh/sensor-dashboard/pharmacy_info.json'
SENSOR_COUNT = 4  # You can dynamically set this later

# ---------- Helper Functions ----------

def load_info():
    if os.path.exists(INFO_FILE):
        with open(INFO_FILE, 'r') as f:
            return json.load(f)
    return {'pharmacy_name': '', 'ncpdp': '', 'total_sensors': SENSOR_COUNT}

def save_info(data):
    with open(INFO_FILE, 'w') as f:
        json.dump(data, f)

# ---------- Info Input Modal ----------

info = load_info()

def open_edit_modal():
    name.value = info['pharmacy_name']
    ncpdp.value = info['ncpdp']
    total_sensors.value = info['total_sensors']
    dialog.open()

def save_form():
    info['pharmacy_name'] = name.value
    info['ncpdp'] = ncpdp.value
    info['total_sensors'] = int(total_sensors.value)
    save_info(info)
    ui.notify("Info saved!")
    dialog.close()

with ui.dialog() as dialog, ui.card():
    ui.label('Edit Pharmacy Info').classes('text-lg font-bold')
    name = ui.input('Pharmacy Name')
    ncpdp = ui.input('NCPDP Number')
    total_sensors = ui.input('Total Sensors', value='4').props('type=number')
    ui.button('Save', on_click=save_form).classes('mt-2')
    ui.button('Cancel', on_click=dialog.close)

# ---------- Top Section ----------

with ui.column().classes('items-center'):
    ui.label('HealtheRx Temperature Dashboard').classes('text-2xl font-bold mt-4')
    ui.label(f"Pharmacy: {info['pharmacy_name']} | NCPDP: {info['ncpdp']} | Sensors: {info['total_sensors']}").classes('text-md mb-2')
    ui.button('Edit Info', on_click=open_edit_modal)
    ui.button('Reboot Device', on_click=lambda: subprocess.Popen(['sudo', 'reboot'])).classes('mt-2 bg-red-500 text-white')
    ui.button('Update Firmware', on_click=lambda: update_firmware()).classes('mt-2 bg-blue-600 text-white')

# ---------- Sensor Dashboard ----------

sensor_data = []

def simulate_sensor_data(sensor_id):
    t = round(random.uniform(34.0, 38.0), 2)
    h = round(random.uniform(30.0, 60.0), 2)
    return {'id': sensor_id, 'temp': t, 'humidity': h, 'max_temp': t, 'min_temp': t, 'max_humidity': h, 'min_humidity': h}

def update_sensors():
    for s in sensor_data:
        new_temp = round(random.uniform(34.0, 38.0), 2)
        new_hum = round(random.uniform(30.0, 60.0), 2)

        s['max_temp'] = max(s['max_temp'], new_temp)
        s['min_temp'] = min(s['min_temp'], new_temp)
        s['max_humidity'] = max(s['max_humidity'], new_hum)
        s['min_humidity'] = min(s['min_humidity'], new_hum)

        s['temp'] = new_temp
        s['humidity'] = new_hum

def render_dashboard():
    ui.label('Current Sensor Readings').classes('text-lg mt-6 font-bold')
    with ui.grid(columns=2).classes('gap-4'):
        for s in sensor_data:
            with ui.card():
                ui.label(f"Sensor #{s['id']}").classes('font-bold')
                ui.label(f"🌡️ Temp: {s['temp']} °F (Min: {s['min_temp']} / Max: {s['max_temp']})")
                ui.label(f"💧 Humidity: {s['humidity']}% (Min: {s['min_humidity']} / Max: {s['max_humidity']})")

# ---------- Firmware Update ----------

def update_firmware():
    ui.notify("Checking for updates...")
    result = subprocess.run(['git', '-C', '/home/vinitbparikh/sensor-dashboard', 'pull'], capture_output=True, text=True)
    if "Already up to date" in result.stdout:
        ui.notify("Already up to date.")
    else:
        ui.notify("Update pulled. Rebooting now...")
        subprocess.Popen(['sudo', 'reboot'])

# ---------- Init ----------

sensor_data = [simulate_sensor_data(i + 1) for i in range(info['total_sensors'])]
render_dashboard()
ui.timer(30, lambda: (update_sensors(), ui.run_javascript('location.reload()')))

ui.run()
