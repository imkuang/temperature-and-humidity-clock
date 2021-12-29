from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from ds1302 import DS1302
from dht11 import DHT11, InvalidChecksum
import utime

# DHT11传感器定义
dht_pin = Pin(17, Pin.OUT, Pin.PULL_DOWN)
dht_sensor = DHT11(dht_pin)

# DS1302 RTC时钟定义
ds_rtc = DS1302(Pin(2), Pin(3), Pin(4))
# 设置RTC时钟的时间
# ds_rtc.date_time([2021, 12, 29, 3, 22, 13, 3])

# SSD1306驱动OLED定义
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=500000)
oled = SSD1306_I2C(128, 32, i2c)

# DHT11传感器采样频率有限制，使用该计数控制每3秒（6次刷新）读取一次传感器数据
# 未到时间时直接使用上一次读取保存的数据
dht_count = 7
dht_temp = 0
dht_humi = 0

# 亮屏启动画面
oled.fill(1)
oled.show()
utime.sleep(1)

while True:
    # 每过3秒从传感器读取并记录一次数据
    if dht_count > 6:
        try:
            dht_temp = dht_sensor.temperature
            dht_humi = dht_sensor.humidity
            dht_count = 0
        except InvalidChecksum:
            print("Checksum from the sensor was invalid, data can not update")
    
    # oled清屏
    oled.fill(0)
    
    # 写入时间数据
    time_now = ds_rtc.date_time()
    oled.text("%04d-%02d-%02d  W%d" % tuple(time_now[:4]), 2, 2, 1)
    oled.text("%02d:%02d:%02d" % tuple(time_now[4:7]), 2, 12, 1)

    # 写入温度和湿度数据
    oled.text("T:%.1f  H:%.1f" % (dht_temp, dht_humi), 2, 22, 1)
    
    # 显示画面，每0.5秒刷新一次
    oled.show()
    utime.sleep(0.5)
    
    # DHT计数更新
    dht_count += 1
