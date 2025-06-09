import time
from machine import Pin, PWM, ADC

IN1 = Pin(18, Pin.OUT)
IN2 = Pin(19, Pin.OUT)
IN3 = Pin(20, Pin.OUT)
IN4 = Pin(21, Pin.OUT)

IRSensor = Pin(16, Pin.IN, Pin.PULL_UP)
Photosensor = ADC(28)
lid = PWM(Pin(2))
lid.freq(50)

SEQUENCE = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]

def move_stepper(direction, steps):
    pins = [IN1, IN2, IN3, IN4]
    sequence = SEQUENCE if direction == 'forward' else list(reversed(SEQUENCE))
    for i in range(steps):
        for j in range(4):
            pins[j].value(sequence[i % 4][j])
        time.sleep(0.002)

while True:
    print("IR:", IRSensor.value(), "Light:", Photosensor.read_u16())

    if IRSensor.value() == 0 and Photosensor.read_u16() <= 800:
        move_stepper('forward', 512)
        time.sleep(2)

    if Photosensor.read_u16() <= 800:
        for pos in range(500000, 2500000, 5000):
            lid.duty_ns(pos)
            time.sleep(0.01)
    else:
        for pos in range(2500000, 500000, -5000):
            lid.duty_ns(pos)
            time.sleep(0.01)
