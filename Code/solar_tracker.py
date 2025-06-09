import time
from machine import Pin, PWM

TL = Pin(3, Pin.IN)
TR = Pin(4, Pin.IN)
BL = Pin(5, Pin.IN)
BR = Pin(6, Pin.IN)

Xaxis = PWM(Pin(2))
Yaxis = PWM(Pin(17))
Xaxis.freq(50)
Yaxis.freq(50)

positionx = 1500000
positiony = 1500000

while True:
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
