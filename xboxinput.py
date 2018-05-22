#!/usr/bin/python
import struct
import time
import sys

# type
EV_SYN           = 0x00
EV_KEY           = 0x01
EV_ABS           = 0x03

# code
SYN_REPORT       = 0

# key
BTN_GAMEPAD      = 0x130
BTN_SOUTH        = 0x130
BTN_A            = BTN_SOUTH
BTN_EAST         = 0x131
BTN_B            = BTN_EAST
BTN_C            = 0x132
BTN_NORTH        = 0x133
BTN_X            = BTN_NORTH
BTN_WEST         = 0x134
BTN_Y            = BTN_WEST
BTN_Z            = 0x135
BTN_TL           = 0x136
BTN_TR           = 0x137
BTN_TL2          = 0x138
BTN_TR2          = 0x139
BTN_SELECT       = 0x13a
BTN_START        = 0x13b
BTN_MODE         = 0x13c
BTN_THUMBL       = 0x13d
BTN_THUMBR       = 0x13e

# abs
ABS_X            = 0x00
ABS_Y            = 0x01
ABS_Z            = 0x02
ABS_RX           = 0x03
ABS_RY           = 0x04
ABS_RZ           = 0x05
ABS_THROTTLE     = 0x06
ABS_RUDDER       = 0x07
ABS_WHEEL        = 0x08
ABS_GAS          = 0x09
ABS_BRAKE        = 0x0a
ABS_HAT0X        = 0x10
ABS_HAT0Y        = 0x11
ABS_HAT1X        = 0x12
ABS_HAT1Y        = 0x13
ABS_HAT2X        = 0x14
ABS_HAT2Y        = 0x15
ABS_HAT3X        = 0x16
ABS_HAT3Y        = 0x17

class InputEvent:
    def __init__(self):
        self.fmt = 'llHHi'
        self.sec = 0
        self.usec = 0
        self.type = 0
        self.code = 0
        self.value = 0
    
    def updateFromEvent(self, event):
        (self.sec, self.usec, \
        self.type, self.code, self.value) = struct.unpack(self.fmt, event)
        
    def size(self):
        return struct.calcsize(self.fmt)

class XboxInputValue:
    X1    = 0
    Y1    = 0
    X2    = 0
    Y2    = 0
    A     = 0
    B     = 0
    X     = 0
    Y     = 0
    du    = 0
    dd    = 0
    dl    = 0
    dr    = 0
    back  = 0
    guide = 0
    start = 0
    lt    = 0
    lb    = 0
    rt    = 0
    rb    = 0
        
class XboxInput:
    def __init__(self, dev, handler = None):
        self.fd = open(dev, "rb")
        self.handler = handler
        self.event = InputEvent()
        self.inputVal = XboxInputValue()
    
    def run(self):
        size = self.event.size()
        event = self.fd.read(size)
        while event:
            self.parse(event)
            event = self.fd.read(size)
    
    def close(self):
        if self.fd is None:
            return
        self.fd.close()
        
    def syncInput(self):
        if self.handler is None:
            print "X1:%6d Y1:%6d X2:%6d Y2:%6d du:%d dd:%d dl:%d dr:%d A:%d B:%d X:%d Y:%d lt:%6d rt:%6d lb:%d rb:%d back:%d guide:%d start:%d" % \
              (self.inputVal.X1, self.inputVal.Y1, self.inputVal.X2, self.inputVal.Y2, \
               self.inputVal.du, self.inputVal.dd, self.inputVal.dl, self.inputVal.dr, \
               self.inputVal.A, self.inputVal.B, self.inputVal.X, self.inputVal.Y, \
               self.inputVal.lt, self.inputVal.rt, self.inputVal.lb, self.inputVal.rb, \
               self.inputVal.back, self.inputVal.guide, self.inputVal.start)
        else:
            self.handler(self.inputVal)
    
    def parse(self, event):
        self.event.updateFromEvent(event)
        if EV_SYN == self.event.type:
            self.parseSyn()
        elif EV_KEY == self.event.type:
            self.parseKey()
        elif EV_ABS == self.event.type:
            self.parseAbs()
        else:
            print "type:%d code:%d" % (self.event.type, self.event.code)
    
    def parseSyn(self):
        if SYN_REPORT == self.event.code:
            self.syncInput()
        else:
            print "syn code:%d value:%d" % (self.event.code, self.event.value)
    
    def parseKey(self):
        if BTN_A == self.event.code:
            self.inputVal.A = self.event.value
        elif BTN_B == self.event.code:
            self.inputVal.B = self.event.value
        elif BTN_X == self.event.code:
            self.inputVal.X = self.event.value
        elif BTN_Y == self.event.code:
            self.inputVal.Y = self.event.value
        elif BTN_TL == self.event.code:
            self.inputVal.lb = self.event.value
        elif BTN_TR == self.event.code:
            self.inputVal.rb = self.event.value
        elif BTN_MODE == self.event.code:
            self.inputVal.guide = self.event.value
        elif BTN_SELECT == self.event.code:
            self.inputVal.back = self.event.value
        elif BTN_START == self.event.code:
            self.inputVal.start = self.event.value
        else:
            print "key code:%d value:%d" % (self.event.code, self.event.value)
    
    def parseAbs(self):
        if ABS_X == self.event.code:
            self.inputVal.X1 = self.event.value
        elif ABS_Y == self.event.code:
            self.inputVal.Y1 = self.event.value
        elif ABS_Z == self.event.code:
            self.inputVal.lt = self.event.value
        elif ABS_RX == self.event.code:
            self.inputVal.X2 = self.event.value
        elif ABS_RY == self.event.code:
            self.inputVal.Y2 = self.event.value
        elif ABS_RZ == self.event.code:
            self.inputVal.rt = self.event.value
        elif ABS_HAT0X == self.event.code:
            if self.event.value == -1:
                self.inputVal.dl = 1
            elif self.event.value == 1:
                self.inputVal.dr = 1
            else:
                self.inputVal.dl = 0
                self.inputVal.dr = 0
        elif ABS_HAT0Y == self.event.code:
            if self.event.value == -1:
                self.inputVal.du = 1
            elif self.event.value == 1:
                self.inputVal.dd = 1
            else:
                self.inputVal.du = 0
                self.inputVal.dd = 0
        else:
            print "abs code:%d value:%d" % (self.event.code, self.event.value)
        

def ValHanlder(inputVal):
    print "--X1:%6d Y1:%6d X2:%6d Y2:%6d du:%d dd:%d dl:%d dr:%d A:%d B:%d X:%d Y:%d lt:%6d rt:%6d lb:%d rb:%d back:%d guide:%d start:%d" % \
              (inputVal.X1, inputVal.Y1, inputVal.X2, inputVal.Y2, \
               inputVal.du, inputVal.dd, inputVal.dl, inputVal.dr, \
               inputVal.A, inputVal.B, inputVal.X, inputVal.Y, \
               inputVal.lt, inputVal.rt, inputVal.lb, inputVal.rb, \
               inputVal.back, inputVal.guide, inputVal.start)
               
def main():
    xbox = XboxInput("/dev/input/event0", ValHanlder)
    try:  
        xbox.run()  
    except KeyboardInterrupt:  
        xbox.close()
        print 'Exit...'
    
if __name__ == '__main__':
    main()