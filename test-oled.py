from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas
from PIL import ImageFont

# Set up I2C interface (port=1 is default on Pi, address 0x3C from your i2cdetect)
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial)

# Load default font
font = ImageFont.load_default()

# Display text
with canvas(device) as draw:
    draw.text((0, 0), "Hello, world!", fill="white", font=font)
    draw.text((0, 20), "SSD1306 Test", fill="white", font=font)
