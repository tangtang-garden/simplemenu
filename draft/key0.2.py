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
    nowValue = self.pin.value()
    ''' start signal '''
    if nowValue ^ self.currentState:# and not self.keyDown_start and not self.keyUp_start:
      self.keyDown_start = not nowValue
      self.keyUp_start = nowValue
    # else:
    #   return
    ''' re ticks_ms timer '''
    # if self.debounce ^ nowValue :
    #   self.debounce = nowValue
    #   # self.t0 = time.ticks_ms()
    #   self.keyDown_start = False
    #   self.keyUp_start = False
    ''' determine press '''
    if self.keyDown_start:# and time.ticks_diff(time.ticks_ms(),self.t0) > 45 :
      # print(f"keyDown start determine area ->   ",end = '')
      self.currentState = 0
      self.isDown = True
      print("key isDown")
      self.keyDown_start = False
    if self.keyUp_start :#and time.ticks_diff(time.ticks_ms(),self.t0)>80:
      # print(f"keyUp start determine area ->   ",end = '')
      self.currentState = 1
      self.isDown = False
      self.isPressed = True
      print("key isUp and isPressed")
      self.keyUp_start = False
    time.sleep_ms(1)
