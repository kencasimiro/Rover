#!/usr/bin/env python3
from __future__ import print_function
import socket
import sys
import os
import smbus

class PyCar:
    address = 0x2a

    def __init__(self):
        self.bus = smbus.SMBus(1)

    def control(self, steering, throttle):      
        print('Steering: {}\tThrottle: {}'.format(steering, throttle))
        self.bus.write_i2c_block_data(self.address, steering, [throttle])

if __name__ == '__main__':
    car = PyCar()
    car.control(90, 90)

