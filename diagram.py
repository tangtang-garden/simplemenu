{
  "version": 1,
  "author": "Uri Shaked",
  "editor": "wokwi",
  "parts": [
    {
      "type": "board-esp32-devkit-c-v4",
      "id": "esp",
      "top": 9.6,
      "left": -100.76,
      "attrs": { "env": "micropython-20231005-v1.21.0" }
    },
    { "type": "board-ssd1306", "id": "oled1", "top": 99.14, "left": 57.83, "attrs": {} },
    {
      "type": "wokwi-pushbutton",
      "id": "btn1",
      "top": 73.4,
      "left": 172.8,
      "attrs": { "color": "green" }
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn2",
      "top": 188.6,
      "left": 172.8,
      "attrs": { "color": "green" }
    },
    {
      "type": "wokwi-pushbutton",
      "id": "btn3",
      "top": 131,
      "left": 172.8,
      "attrs": { "color": "green" }
    }
  ],
  "connections": [
    [ "esp:TX", "$serialMonitor:RX", "", [] ],
    [ "esp:RX", "$serialMonitor:TX", "", [] ],
    [ "oled1:SCL", "esp:22", "green", [ "v0" ] ],
    [ "oled1:SDA", "esp:21", "blue", [ "v-19.2", "h-124.73" ] ],
    [ "oled1:GND", "esp:GND.2", "black", [ "v-67.2", "h-96" ] ],
    [ "oled1:VCC", "esp:3V3", "red", [ "v-28.8", "h0.15", "v-76.8", "h-201.75" ] ],
    [ "btn2:1.l", "esp:15", "green", [ "h-153.6", "v-28.8" ] ],
    [ "btn3:1.l", "esp:16", "green", [ "h-9.6", "v48", "h-134.4", "v-28.8" ] ],
    [ "esp:GND.2", "btn1:2.r", "black", [ "v0", "h230.4" ] ],
    [ "btn3:2.r", "btn1:2.r", "green", [ "h0" ] ],
    [ "btn2:2.r", "btn3:2.r", "green", [ "h0" ] ],
    [ "esp:17", "btn1:1.l", "green", [ "h28.8", "v-67.2", "h134.4" ] ]
  ],
  "dependencies": {}
}