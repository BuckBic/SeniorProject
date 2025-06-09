#from hx711_gpio1 import HX711
import time
from machine import Pin,PWM
                        #Looking at the panel with sensors facing you
TL = Pin(3, Pin.IN) #LDR top left
TR = Pin(4, Pin.IN) #LDR top right
BL = Pin(5, Pin.IN) #LDR Bottom left
BR = Pin(6, Pin.IN) #ldr Bottom right

# Constants for the stepper motor pins
IN1 = Pin(18, Pin.OUT)
IN2 = Pin(19, Pin.OUT)
IN3 = Pin(20, Pin.OUT)
IN4 = Pin(21, Pin.OUT)

trigger = Pin(12, Pin.OUT)
echo = Pin(13, Pin.IN)

IRSensor = Pin(16, Pin.IN, Pin.PULL_UP)
Photosensor = machine.ADC(28)
#data_pin = Pin(14, Pin.IN, Pin.PULL_DOWN)
#clock_pin = Pin(15, Pin.OUT)
#hx711 = HX711(clock_pin, data_pin)
#hx711.tare()

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
    # Set the input pins
    pins = [IN1, IN2, IN3, IN4]

    # Set the direction of the sequence
    if direction == 'forward':
        sequence = SEQUENCE
    elif direction == 'backward':
        sequence = list(reversed(SEQUENCE))

    # Loop through the specified number of steps
    for i in range(steps):

        # Set the input pins based on the current step
        for j in range(len(pins)):
            pins[j].value(sequence[i%4][j])

        # Delay between steps
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
    if distance >60:
        print("Storage Level Low")
    time.sleep(0.1)

# Main loop
while True: # loop section
    ultra()
    print(IRSensor.value())
    print("ADC: ", Photosensor.read_u16())
    # raw_wt = hx711.read()
    # sf = 340/350000
    # weight = raw_wt*sf

    if (IRSensor.value() == 0 and Photosensor.read_u16() <= 800):  # if bowl is empty (IR) and is daytime(photosensor)
        move_stepper('forward', 512)
        time.sleep(2)

    if (weight.value() <= 600 and Photosensor.read_u16() <= 800):  # if weight is in range and is daytime
        for position in range(500000, 2500000, 5000):  # open lid
            lid.duty_ns(position)
            time.sleep(0.01)

    else:
        for position in range(2500000, 500000, -5000):  # close lid
            lid.duty_ns(position)
            time.sleep(0.01)

    if (TL.value() == 1 and TR.value() == 1 and positiony != 2500000):   #if top left and top right LDR sensors reach their preset values
        Yaxis.duty_ns(positiony)                # move y axis servo to saved variable
        positiony = positiony + 5000            # add 5000 nanoseconds to duty cycle and change the variable value
        time.sleep(0.01)                        # wait 10 milliseconds between each step

    if (TL.value() == 1 and BL.value() == 1 and positionx != 500000):   # same sequences as before with different sensors sets
        Xaxis.duty_ns(positionx)
        positionx = positionx - 5000            # negative indicates reverse direction
        time.sleep(0.01)

    if (BL.value() == 1 and BR.value() == 1 and positiony != 500000):
        Yaxis.duty_ns(positiony)
        positiony = positiony - 5000
        time.sleep(0.01)

    if (TR.value() == 1 and BR.value() == 1 and positionx != 2500000):
        Xaxis.duty_ns(positionx)
        positionx = positionx + 5000
        time.sleep(0.01)
