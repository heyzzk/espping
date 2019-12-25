# espping
ESPPing is a wifi ping based on esp8266 and python. It allows you to see the WIFI users and their more information around you in a figure via python.

![example figure](https://github.com/heyzzk/espping/blob/master/figure.png)

The code is pretty simple including a esp/esp.ino file based on Arduino and a main.py python file.
Only two steps to set it up:
1.Load the Arduino file into your esp8266 board and you can get the wifi JSON info via serial.
2.Change the serial port your esp8266 used to the main.py and just run it.

Known Issues
1.The figure is always no respoding.
2.The points on the figure seems too big.
3.Going to add user info like 'wife' 'kid'.
