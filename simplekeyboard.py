from machine import Pin
import time

class KeyBoard:
  ...

class Key:
  def __init__(self,pin) -> None:
    self.pin = pin if isinstance(pin,Pin) else Pin(pin,Pin.IN,Pin.PULL_UP)
    self.keyDown_start = False # signal press down start
    self.keyUp_start = False  # signal press up start
    self.currentState = 1 # current Pin.value state
    self.debounce = 1 # reset ticks_ms signal
    self.t0 = 0 # timer start
    self.isPressed = False # pressed flag
    self.isDown = False
    # self.isLongPressed = False
  def update(self):
    currentValue = self.pin.value()
    ''' start signal '''
    if currentValue ^ self.currentState and not self.keyDown_start and not self.keyUp_start:
      if currentValue == 0:
        self.keyDown_start = True
      else:
        self.keyUp_start = True
    ''' re ticks_ms timer '''
    if self.debounce ^ currentValue :
      self.debounce = currentValue
      self.t0 = time.ticks_ms()
    ''' determine press '''
    if self.keyDown_start and time.ticks_diff(time.ticks_ms(),self.t0) > 45 :
      # print(f"keyDown start determine area ->   ",end = '')
      if currentValue == 0:
        self.currentState = 0
        self.keyDown_start = False
        self.isDown = True
        # print("key isDown")
      else:
        self.keyDown_start = False
    if self.keyUp_start and time.ticks_diff(time.ticks_ms(),self.t0)>80:
      # print(f"keyUp start determine area ->   ",end = '')
      if currentValue == 1:
        self.currentState = 1
        self.keyUp_start = False
        self.isPressed = True
        # print("key isUp and isPressed")
    time.sleep_ms(1)
