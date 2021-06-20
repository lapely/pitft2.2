import digitalio
import board
import socket
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import time


def get_ip_address():
    ip_address = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


# First define some constants to allow easy resizing of shapes.
BORDER = 20
FONTSIZE = 24

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
backlight = digitalio.DigitalInOut(board.D18)
backlight.switch_to_output()
backlight.value = True
buttonB = digitalio.DigitalInOut(board.D22)
buttonC = digitalio.DigitalInOut(board.D23)
buttonB.switch_to_input()
buttonC.switch_to_input()

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Setup Display 2.2"
disp = ili9341.ILI9341(
    spi,
    rotation=270,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a green filled box as the background
draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
disp.image(image)

# Load a TTF Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE)

# Draw Some Text
ip = "ip: " + get_ip_address()
(font_width, font_height) = font.getsize(ip)
draw.text(
    (width // 4 - font_width // 2, height // 10 - font_height // 2),
    ip,
    font=font,
    fill=(255, 255, 255),
)

# Display image.
disp.image(image)

while True:
    ip = "ip: " + get_ip_address()
    (font_width, font_height) = font.getsize(ip)
    draw.text(
        (width // 4 - font_width // 2, height // 10 - font_height // 2),
        ip,
        font=font,
        fill=(255, 255, 255),
    )
