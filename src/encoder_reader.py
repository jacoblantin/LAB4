"""!
@file encoder_reader.py
This file contians a class imlementation to interpret and solve for the values read
from the ME 405 motor through the microcontroller.
This file also contains testing code to read the encoder.

@author Jacob Lantin, Devon Lau, Filippo Maresca Denini
@date 27-Feb-2024

"""

import utime
import pyb

class encoder:
    """!
    This class contains the constructor and two methods that read and zero the position
    read from an encoder on the back of the motor provided in ME 405 Lab.
    """
    
    def __init__(self, pin1, pin2, timer):
        """!
        This constructor initliazes the pins, timer, and timer counter (aka position) for
        use in reading the encoder
        @param pin1 - B6 or C6 pin to be used in channel 1 for the timer, aka encoder channel A
        @param pin2 - B7 or C7 pin to be used in channel 2 for the timer, aka encoder channel B
        @param timer - timer 4 or 8 to be used for B or C pins, respectively
        """
        
        # pin1 (B6 or C6)
        self.pin1 = pin1
        
        # pin2 (B7 or C7)
        self.pin2 = pin2
        
        # timer setup (timer 4 for B, timer 8 for C)
        self.timer = timer
           
        # channel setup (ch1 for pin6, ch2 for pin7)   
        self.ch1 = self.timer.channel(1, pyb.Timer.ENC_AB, pin=pin1)
        self.ch2 = self.timer.channel(2, pyb.Timer.ENC_AB, pin=pin2)
        
        # intiialize counter to 0
        self.counter = 0
        
        # initialize position off of timer counter
        self.pos = self.timer.counter()
        
        # initialize previous value (prev) and new value (new)
        self.prev = 0
        self.new = 0

    def read(self):
        """!
        This method first reads the encoder then checks for overflow or underflow.
        The method returns an encoder position value accounting for overflow or
        underflow.
        """
        # get new value of encoder by reading encoder counter
        self.new = self.timer.counter()
        
        
        # auto-reload (AR) is the max value of the encoder, the period of the timer
        AR = self.timer.period()
        
        # compute delta of encoder
        delta = self.new - self.prev
        
        # do the underflow/overflow calculation
        
        # value of overflow
        overflow = (AR + 1) / 2
        
        # overflow
        if delta >= overflow:
            delta -= overflow * 2
            
        # underflow
        elif delta <= -1 * overflow:
            delta += overflow * 2
            
        # neither
        else:
            delta = delta
            
        # add the delta (after it's been corrected) to current position
        self.pos += int(delta)
        
        # set new previous value to new value (prev = new)
        self.prev = self.new
        
        # return position for encoder read
        return self.pos
                    
    
    def zero(self):
        """!
        This method resets the position of the encoder to 0, while also reseting the prev and new
        values to reset the read() calculation.
        """        
        self.pos = 0
        
        self.prev = 0
        
        self.new = 0


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program.
if __name__ == "__main__":
    
    # initialize encoder w/ pin PC6, pin PC7, and timer 8
    # however, can also be used w/ pin PB6, PB7, and timer 4
    pin1 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    pin2 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    timer = pyb.Timer(8, prescaler = 0, period = 65535)
    
    enc = encoder(pin1, pin2, timer)
   
    # start encoder reading
    prev = enc.read()
    
    while True:
        # only print encoder value if value changes
        new = enc.read()
        if new != prev:
            print(f"\nEncoder value: {new}")
        
        # calculate encoder value every 10 ms
        utime.sleep_ms(10)
    

