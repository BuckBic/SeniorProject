import time
from machine import Pin, PWM, ADC

class SolarTracker:
    def __init__(self):
        # Initialize LDR sensors
        self.TL = Pin(3, Pin.IN)  # Top Left
        self.TR = Pin(4, Pin.IN)  # Top Right
        self.BL = Pin(5, Pin.IN)  # Bottom Left
        self.BR = Pin(6, Pin.IN)  # Bottom Right
        
        # Initialize axis servos
        self.Xaxis = PWM(Pin(2))
        self.Yaxis = PWM(Pin(17))
        
        # Set PWM frequency
        self.Xaxis.freq(50)
        self.Yaxis.freq(50)
        
        # Initialize positions
        self.positionx = 1500000  # Start at midpoint in nanoseconds
        self.positiony = 1500000
        
        # Initialize stepper motor pins
        self.IN1 = Pin(18, Pin.OUT)
        self.IN2 = Pin(19, Pin.OUT)
        self.IN3 = Pin(20, Pin.OUT)
        self.IN4 = Pin(21, Pin.OUT)
        self.IRSensor = Pin(16, Pin.IN, Pin.PULL_UP)
        self.Photosensor = ADC(28)
        self.lid = PWM(Pin(2))
        self.lid.freq(50)
        
        # Stepper motor sequence
        self.SEQUENCE = [[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]]

    def move_servo(self, axis, direction):
        """Move servo in specified direction"""
        if axis == 'x':
            servo = self.Xaxis
            position = self.positionx
        else:
            servo = self.Yaxis
            position = self.positiony
            
        position += direction * 5000  # 5000ns step size
        servo.duty_ns(position)
        time.sleep(0.01)
        
        # Update position
        if axis == 'x':
            self.positionx = position
        else:
            self.positiony = position

    def move_stepper(self, direction, steps):
        """Move stepper motor in specified direction"""
        pins = [self.IN1, self.IN2, self.IN3, self.IN4]
        sequence = self.SEQUENCE if direction == 'forward' else list(reversed(self.SEQUENCE))
        
        for _ in range(steps):
            for j in range(len(pins)):
                pins[j].value(sequence[_ % 4][j])
            time.sleep(0.002)

    def control_lid(self, open=True):
        """Control lid position"""
        start = 500000 if open else 2500000
        end = 2500000 if open else 500000
        step = 5000 if open else -5000
        
        for position in range(start, end, step):
            self.lid.duty_ns(position)
            time.sleep(0.01)

    def check_sensors(self):
        """Check sensor values and return status"""
        return {
            'ir': self.IRSensor.value(),
            'photo': self.Photosensor.read_u16()
        }

    def run(self):
        """Main control loop"""
        while True:
            # Check LDR sensors for solar tracking
            if self.TL.value() == 1 and self.TR.value() == 1:
                self.move_servo('y', 1)  # Move up
            
            if self.TL.value() == 1 and self.BL.value() == 1:
                self.move_servo('x', -1)  # Move left
            
            if self.BL.value() == 1 and self.BR.value() == 1:
                self.move_servo('y', -1)  # Move down
            
            if self.TR.value() == 1 and self.BR.value() == 1:
                self.move_servo('x', 1)  # Move right

            # Check sensors for lid control
            sensors = self.check_sensors()
            print(f"IR: {sensors['ir']}, Photo: {sensors['photo']}")
            
            if sensors['ir'] == 0 and sensors['photo'] <= 800:
                self.move_stepper('forward', 512)
                time.sleep(2)
            
            # Lid control based on photosensor
            if sensors['photo'] <= 800:
                self.control_lid(open=True)
            else:
                self.control_lid(open=False)

# Create and run the solar tracker
if __name__ == "__main__":
    tracker = SolarTracker()
    tracker.run()
