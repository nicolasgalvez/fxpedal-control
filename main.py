import time
import json
import subprocess
from pathlib import Path
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont
import RPi.GPIO as GPIO

# === CONFIG ===
GX_PRESET_FILE = Path.home() / ".config/guitarix/banks/Nick.gx"
ROTARY_BUTTON_PIN = 4
MIDI_CHANNEL = 1  # MIDI channels are 1-based

# === OLED SETUP ===
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except IOError:
    font = None

# === BUTTON SETUP ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(ROTARY_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# === LOAD PRESETS ===
def load_presets():
    try:
        with open(GX_PRESET_FILE) as f:
            data = json.load(f)
            return [entry for entry in data if isinstance(entry, str) and not entry.startswith("gx_head_file_version")]
    except Exception as e:
        print(f"Error loading presets: {e}")
        return ["Error"]

presets = load_presets()
preset_index = 0

def show_preset(name):
    with canvas(device) as draw:
        draw.text((0, 0), "Current Preset:", fill="white", font=font)
        draw.text((0, 20), name, fill="white", font=font)

def send_midi_program_change(index):
    try:
        subprocess.run([
            "sendmidi", "dev", "Midi Through Port-0", "ch", str(MIDI_CHANNEL), "pc", str(index)
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to send MIDI: {e}")

def next_preset():
    global preset_index
    preset_index = (preset_index + 1) % len(presets)
    show_preset(presets[preset_index])
    send_midi_program_change(preset_index)

# === MAIN LOOP ===
last_state = GPIO.input(ROTARY_BUTTON_PIN)
show_preset(presets[preset_index])
send_midi_program_change(preset_index)

try:
    while True:
        current_state = GPIO.input(ROTARY_BUTTON_PIN)
        if last_state == GPIO.HIGH and current_state == GPIO.LOW:
            next_preset()
            time.sleep(0.2)  # debounce
        last_state = current_state
        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()

