import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import subprocess
import os
from os.path import join
from Services import helpers
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
x = 0

# Load fonts
font = ImageFont.truetype(join(os.getcwd(), 'fonts/OpenSans-Bold.ttf'), 18)
font1 = ImageFont.truetype(join(os.getcwd(), 'fonts/OpenSans-Bold.ttf'), 12)
font2 = ImageFont.load_default()

# Switch for pages
currentPage = 0

def drawPage(data):
    global currentPage

    if currentPage == 0:
        drawHelper(drawIntroPage)
    elif currentPage == 1:
        drawHelper(drawCcLevel, data)
    elif currentPage == 2:
        drawHelper(drawStatsPage)

    if currentPage > 2:
        currentPage = 0

# Screen helpers
def drawHelper(currentDrawer, parameters=False):
    global currentPage
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Call the current drawer
    if parameters != False:
        currentDrawer(parameters)
    else:
        currentDrawer()

    # Display image.
    disp.image(image)
    disp.display()
    currentPage += 1

def textCenter(msg, font):
    w, h = draw.textsize(msg, font)
    return draw.text(((width-w)/2,(height-h)/2), msg, font=font, fill=255)

def textHorizontalCenter(verticalHeight, msg, font):
    w, h = draw.textsize(msg, font)
    return draw.text(((width-w)/2,verticalHeight), msg, font=font, fill=255)

# Actual pages
def drawIntroPage():
    textHorizontalCenter(top, "CC", font)
    textHorizontalCenter(top+20, "PIXELFUSION", font1)

def drawCcLevel(data):
    if data['connection'] == False:
        textHorizontalCenter(top, "%s %%" % helpers.calculatePercentage(data['level']), font)
        textHorizontalCenter(top+20, "WiFi Error", font2)
    else:
        textCenter("%s %%" % helpers.calculatePercentage(data['level']), font)

def drawStatsPage():
    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )
    cmd = "hostname -I | cut -d\' \' -f1"
    IP = subprocess.check_output(cmd, shell = True )
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )

    draw.text((x, top+0), str(MemUsage),  font=font2, fill=255)
    draw.text((x, top+8), str(Disk),  font=font2, fill=255)
    draw.text((x, top+16), "IP: " + str(IP),  font=font2, fill=255)
    draw.text((x, top+25), str(CPU), font=font2, fill=255)
