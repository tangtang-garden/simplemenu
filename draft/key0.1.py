from machine import Pin, I2C
import ssd1306,time

# ESP32 Pin assignment 
i2c = I2C(0, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
key=Pin(17,Pin.IN,Pin.PULL_UP)
oled.text('Hello, Wokwi!', 10, 10)      
oled.show()
keydown_start = False
keyup_start = False
state = key.value()
follow = state
t0 =0
t100 = 0
pressed = False
longpressed = False
while 1:
  k = key.value()
  if k ^ state and not keydown_start and not keyup_start:
    if k == 0:
      keydown_start = True
    else:
      keyup_start = True
  if follow ^ k:
    follow = k
    t0 = time.ticks_ms()

  if keydown_start and time.ticks_diff(time.ticks_ms(),t0)>45:
    # print(f"enter 1,{k=}")
    if k==0:
      state = 0
      keydown_start = False
      print("pressed down")
      
    else:
      keydown_start = False
  if keyup_start and time.ticks_diff(time.ticks_ms(),t0)>80:
    # print(f"enter 2,{k=}")
    if k== 1:
      state = 1
      keyup_start = False
      print("pressed up")
      pressed = True
  time.sleep_ms(1)
