import random
import serial
import adafruit_thermal_printer
import RPi.GPIO as GPIO
import time
from rpi_ws281x import *

#Creates the list of fortunes to be chosen from.
fortunes = [
    'There will be copious amount of drape in your future.',
    'Your next crew meal will be     steak and lobster.',
    'Your next crew meal will be a   soggy hummus wrap.',
    '404 fortune not found.',
    'Thank you Mario, but your       fortune is in another castle.',
    'Ahhh, the light! Put me back in!',
    'DUCK!',
    'Man, it was hot in there!',
    'You will never experience a     shortage of cable trunks again.',
    'Eating a microphone adds great  nutritional value to your diet',
    'You missed a safety cable.',
    'If you swallow a microphone, youmight become a microphone tree.',
    'SOMEONE TOOK YOUR SHARPIE.',
    'Check 1, 2...is this fortune on?',
    'Remember to drink plenty of     water, but probably not before ageneral session',
    'You will use gaff tape in ways  you never imagined possible.',
    'You will insert a USB drive the right way on the first try.',
    'Your future is important to us, please hold for the next available fortune.',
    'A soundcheck a day keeps the feedback away.',
    'Your next crew meal will be half eaten by a rat.'
    
]

GPIO.setmode(GPIO.BOARD) #Use the physical GPIO number
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Change pin if necessary
GPIO.setwarnings(False) #Ignore warnings

def button():   
    while True: # Run forever
        if GPIO.input(18) == GPIO.HIGH:
            time.sleep(1)
            ledon()
            time.sleep(5)
            getfortune()
            time.sleep(5)
            ledoff()
            
# LED strip configuration:
LED_COUNT      = 32     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ,LED_DMA,LED_INVERT,LED_BRIGHTNESS,LED_CHANNEL)
strip.begin()
    
def ledon():

    for x in range(0,LED_COUNT):
        strip.setPixelColor(x, Color(255,0,0))
    
        strip.show()
        
    print ("led on")
    
        
def ledoff():
    
    for x in range(0,LED_COUNT):
        strip.setPixelColor(x, Color(0,0,0))
    
        strip.show()
        
    print ("led off")

def getfortune():

    #Initiates necessary printer functions
    uart = serial.Serial("/dev/serial0", baudrate=9600, timeout=3000)
    ThermalPrinter = adafruit_thermal_printer.get_printer_class(1.11)
    printer = ThermalPrinter(uart)
    printer.warm_up()

    #Edit the text below to adjust the receipt design
    printer.feed(2) #Blank line
    printer.feed(2) #Blank line
    printer.underline = adafruit_thermal_printer.UNDERLINE_THIN #Add a thin underline
    printer.justify = adafruit_thermal_printer.JUSTIFY_CENTER #Center the text
    printer.print(' Your Fortune... ') #First line of text
    printer.feed(2) #Blank line
    printer.underline = None #Removes underline
    printer.justify = adafruit_thermal_printer.JUSTIFY_LEFT #Left alight text
    printer.print(random.choice(fortunes)) #Second line of text will be a random fortune
    printer.feed(2) #Blank line
    printer.feed(2) #Blank line
    printer.feed(2) #Blank line
    printer.feed(2) #Blank line
    
    print("button was pushed!")
    
button()
strip_cleanup()
GPIO.cleanup() #GPIO clean up


