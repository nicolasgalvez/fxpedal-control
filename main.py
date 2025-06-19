import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

import RPi.GPIO as GPIO

# === OLED SETUP ===
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Optional: load a custom font or use default
try:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except IOError:
    font = None  # default PIL font

# === BUTTON / ENCODER SETUP ===
ROTARY_BUTTON_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(ROTARY_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# === FAKE PRESET DATA (REPLACE THIS LATER) ===
presets = ["Clean", "Crunch", "Heavy", "Solo"]
preset_index = 0

def get_current_preset():
    return presets[preset_index]

def next_preset():
    global preset_index
    preset_index = (preset_index + 1) % len(presets)

def show_preset(preset):
    with canvas(device) as draw:
        draw.text((0, 0), "Current Preset:", fill="white", font=font)
        draw.text((0, 20), preset, fill="white", font=font)

# === MAIN LOOP ===
last_button_state = GPIO.input(ROTARY_BUTTON_PIN)

try:
    show_preset(get_current_preset())
    while True:
        button_state = GPIO.input(ROTARY_BUTTON_PIN)
        if last_button_state == GPIO.HIGH and button_state == GPIO.LOW:
            next_preset()
            show_preset(get_current_preset())
            time.sleep(0.2)  # debounce delay
        last_button_state = button_state
        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
