from machine import Pin, I2C
import ssd1306,time,gc,micropython
from menu import Menu,FullPage,Node,timed_function
micropython.alloc_emergency_exception_buf(100)
# ESP32 Pin assignment 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
keyUp=Pin(17,Pin.IN,Pin.PULL_UP)
keyDone=Pin(16,Pin.IN,Pin.PULL_UP)
keyDown=Pin(15,Pin.IN,Pin.PULL_UP)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
''' menu initial '''
indexPage = None # index page contain sevel tasks
mainpage = FullPage(oled)   #creat Page
mainpage.initPage(Node('Menu'),Node('Toast'),Node('Timer'))
menu = Menu()
menu.initMenu(mainpage)
menu.display()
now = time.ticks_ms()
gc.collect()
while True:
  '''--------------- update ------------------'''

  '''---------------- draw -------------------'''
  oled.fill(0)
  fps = round(1000/time.ticks_diff(time.ticks_ms(),now),2)
  oled.text(str(fps)+' FPS',64,56)
  now = time.ticks_ms()
  menu.display()
  oled.show()
  '''----------------- key -------------------'''
  if keyUp.value()&keyDown.value()&keyDone.value() == 0:
    if keyUp.value()==0:
        while(keyUp.value()==0):pass
        menu.moveUp()
    elif keyDown.value()==0:
        while(keyDown.value()==0):pass
        menu.moveDown()
    elif keyDone.value()==0:
        while(keyDone.value()==0):pass
        menu.click()
  time.sleep_ms(1)