from machine import Pin
import time

trigger = Pin(2, Pin.OUT)
echo = Pin(3, Pin.IN)

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
    print("Distance:", distance, "cm")

    if distance > 60:
        print("Storage Level Low")

while True:
    ultra()
    time.sleep(0.1)
