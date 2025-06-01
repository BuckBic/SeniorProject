# machine.py – Mocked for Codespaces testing

class Pin:
    IN = 0
    OUT = 1
    PULL_UP = 2

    def __init__(self, pin, mode, pull=None):
        self.pin = pin
        self.mode = mode
        self.state = 0

    def value(self, val=None):
        if val is None:
            return self.state  # simulate read
        else:
            self.state = val
            print(f"[MOCK] Pin {self.pin} set to {val}")

    def low(self):
        self.state = 0
        print(f"[MOCK] Pin {self.pin} LOW")

    def high(self):
        self.state = 1
        print(f"[MOCK] Pin {self.pin} HIGH")


class PWM:
    def __init__(self, pin):
        self.pin = pin
        self.freq_val = None
        print(f"[MOCK] PWM initialized on pin {pin}")

    def freq(self, hz):
        self.freq_val = hz
        print(f"[MOCK] PWM pin {self.pin} frequency set to {hz}Hz")

    def duty_u16(self, val):
        print(f"[MOCK] PWM pin {self.pin} duty set to {val}/65535")

    def duty_ns(self, val):
        print(f"[MOCK] PWM pin {self.pin} duty set to {val}ns")


class ADC:
    def __init__(self, pin):
        self.pin = pin

    def read_u16(self):
        return 700  # Simulate light level or analog input
