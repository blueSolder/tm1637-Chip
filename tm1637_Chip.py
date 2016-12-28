#!/usr/bin/env python2

"""
blueSolder 12/2016
based on https://github.com/johnlr/raspberrypi-tm1637/blob/master/tm1637.py
modified to work with NextThingCo C.H.I.P
needs https://github.com/xtacocorex/CHIP_IO

The MIT License (MIT)

Copyright (c) 2013, 2014 Damien P. George

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import CHIP_IO.GPIO as GPIO

"""
      A
     ---
  F |   | B
     -G-
  E |   | C
     ---
      D
"""

class tm1637_Chip:
    I2C_COMM1 = 0x40
    I2C_COMM2 = 0xC0
    I2C_COMM3 = 0x80
    digit_to_segment = [
        0b0111111, # 0
        0b0000110, # 1
        0b1011011, # 2
        0b1001111, # 3
        0b1100110, # 4
        0b1101101, # 5
        0b1111101, # 6
        0b0000111, # 7
        0b1111111, # 8
        0b1101111, # 9
        0b1110111, # A
        0b1111100, # b
        0b0111001, # C
        0b1011110, # d
        0b1111001, # E
        0b1110001  # F
        ]

    def __init__(self, clk, dio):
        self.clk = clk
        self.dio = dio
        self.brightness = 0x0f
        
        GPIO.cleanup()
        self.SetupGpio(self.clk, GPIO.OUT)
        self.SetupGpio(self.dio, GPIO.OUT)
        GPIO.output(self.clk, GPIO.LOW)
        GPIO.output(self.dio, GPIO.LOW)
        GPIO.direction(self.clk, GPIO.IN)
        GPIO.direction(self.dio, GPIO.IN)

    def SetupGpio(self, pin, mode):
        try:
            GPIO.setup(pin, mode)
        except:
            GPIO.direction(pin, mode)
        
    def bit_delay(self):
        return
   
    def set_segments(self, segments, pos=0):
        # Write COMM1
        self.start()
        self.write_byte(self.I2C_COMM1)
        self.stop()

        # Write COMM2 + first digit address
        self.start()
        self.write_byte(self.I2C_COMM2 + pos)

        for seg in segments:
            self.write_byte(seg)
        self.stop()

        # Write COMM3 + brightness
        self.start()
        self.write_byte(self.I2C_COMM3 + self.brightness)
        self.stop()

    def start(self):
        GPIO.direction(self.dio, GPIO.OUT)
        self.bit_delay()
   
    def stop(self):
        GPIO.direction(self.dio, GPIO.OUT)
        self.bit_delay()
        GPIO.direction(self.clk, GPIO.IN)
        self.bit_delay()
        GPIO.direction(self.dio, GPIO.IN)
        self.bit_delay()
  
    def write_byte(self, b):
      # 8 Data Bits
        for i in range(8):

            # CLK low
            GPIO.direction(self.clk, GPIO.OUT)
            self.bit_delay()

            GPIO.direction(self.dio, GPIO.IN if b & 1 else GPIO.OUT)

            self.bit_delay()

            GPIO.direction(self.clk, GPIO.IN)
            self.bit_delay()
            b >>= 1
        
        GPIO.direction(self.clk, GPIO.OUT)
        self.bit_delay()
        GPIO.direction(self.clk, GPIO.IN)
        self.bit_delay()
        GPIO.direction(self.clk, GPIO.OUT)
        self.bit_delay()

        return


