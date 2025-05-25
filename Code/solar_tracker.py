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
    if TL.value() and TR.value():
        Yaxis.duty_ns(positiony)
        positiony += 5000
        time.sleep(0.01)

    if TL.value() and BL.value():
        Xaxis.duty_ns(positionx)
        positionx -= 5000
        time.sleep(0.01)

    if BL.value() and BR.value():
        Yaxis.duty_ns(positiony)
        positiony -= 5000
        time.sleep(0.01)

    if TR.value() and BR.value():
        Xaxis.duty_ns(positionx)
        positionx += 5000
        time.sleep(0.01)
