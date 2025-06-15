from hx711 import HX711     # <-- added
import time
from machine import Pin, PWM, ADC

# Looking at the panel with sensors facing you
TL = Pin(3, Pin.IN) # LDR top left
TR = Pin(4, Pin.IN) # LDR top right
BL = Pin(5, Pin.IN) # LDR Bottom left
BR = Pin(6, Pin.IN) # LDR Bottom right

# Constants for the stepper motor pins
IN1 = Pin(18, Pin.OUT)
IN2 = Pin(19, Pin.OUT)
IN3 = Pin(20, Pin.OUT)
IN4 = Pin(21, Pin.OUT)

trigger = Pin(12, Pin.OUT)
echo = Pin(13, Pin.IN)

IRSensor = Pin(16, Pin.IN, Pin.PULL_UP)
Photosensor = ADC(28)

# HX711 Load Cell Setup
data_pin = Pin(14, Pin.IN, Pin.PULL_DOWN)   # <-- added
clock_pin = Pin(15, Pin.OUT)               # <-- added
hx711 = HX711(clock_pin, data_pin)         # <-- added
hx711.tare()                               # <-- added

Xaxis = PWM(Pin(2)) # sets x and y axis servo pins as pwm signal
Yaxis = PWM(Pin(17))
lid = PWM(Pin(11))

Xaxis.freq(50) # sets x and y axis and lid pwm output frequency
Yaxis.freq(50)
lid.freq(50)

positionx = 1500000 # start each servo to their midpoint position in nanseconds as duty cycle
positiony = 1500000

# Sequence for moving the stepper motor
SEQUENCE = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]

# Function to move the stepper motor
def move_stepper(direction, steps):
    pins = [IN1, IN2, IN3, IN4]

    if direction == 'forward':
        sequence = SEQUENCE
    elif direction == 'backward':
        sequence = list(reversed(SEQUENCE))

    for i in range(steps):
        for j in range(len(pins)):
            pins[j].value(sequence[i % 4][j])
        time.sleep(0.002)

def ultra():
    trigger.low()
    time.sleep_us(2)
    trigger.high()
    time.sleep_us(5)
    trigger.low()
    while echo.value() == 0:
        signaloff = time.ticks_us()
    while echo.value() == 1:
        signalon = time.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print("The distance from object is ", distance, "cm")
    if distance > 60:
        print("Storage Level Low")
    time.sleep(0.1)

# Main loop
while True:
    ultra()
    print(IRSensor.value())
    print("ADC: ", Photosensor.read_u16())

    # Read weight from load cell
    raw_weight = hx711.read()                           # <-- added
    scale_factor = 340 / 350000                         # <-- adjust as needed
    weight = raw_weight * scale_factor                  # <-- added
    print("Weight: {:.2f}g".format(weight))             # <-- added

    if (IRSensor.value() == 0 and Photosensor.read_u16() <= 800):
        move_stepper('forward', 512)
        time.sleep(2)

    if (weight <= 600 and Photosensor.read_u16() <= 800):  # <-- replaced weight.value()
        for position in range(500000, 2500000, 5000):
            lid.duty_ns(position)
            time.sleep(0.01)
    else:
        for position in range(2500000, 500000, -5000):
            lid.duty_ns(position)
            time.sleep(0.01)

    if (TL.value() == 1 and TR.value() == 1 and positiony != 2500000):
        Yaxis.duty_ns(positiony)
        positiony = positiony + 5000
        time.sleep(0.01)

    if (TL.value() == 1 and BL.value() == 1 and positionx != 500000):
        Xaxis.duty_ns(positionx)
        positionx = positionx - 5000
        time.sleep(0.01)

    if (BL.value() == 1 and BR.value() == 1 and positiony != 500000):
        Yaxis.duty_ns(positiony)
        positiony = positiony - 5000
        time.sleep(0.01)

    if (TR.value() == 1 and BR.value() == 1 and positionx != 2500000):
        Xaxis.duty_ns(positionx)
        positionx = positionx + 5000
        time.sleep(0.01)
