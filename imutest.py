#!/usr/bin/env python

import time
from icm20948 import ICM20948
import math

print("""read-all.py
Reads all ranges of movement: accelerometer, gyroscope and
compass heading.
Press Ctrl+C to exit!
""")

imu = ICM20948()
ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
last_ax = ax
last_ay = ay

while True:
    x, y, z = imu.read_magnetometer_data()
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()

#     print("""
# Accel: {:05.2f} {:05.2f} {:05.2f}
# Gyro:  {:05.2f} {:05.2f} {:05.2f}
# Mag:   {:05.2f} {:05.2f} {:05.2f}""".format(
#         ax, ay, az, gx, gy, gz, x, y, z
#         ))

    pitch = 180*math.atan(ax/math.sqrt(ay*ay+az*az))/math.pi
    roll = 180*math.atan(ay/math.sqrt(ax*ax+az*az))/math.pi
    yaw = 180*math.atan(az/math.sqrt(ax*ax+ay*ay))/math.pi

    # print(pitch) # up down
    print(pitch) 

    time.sleep(0.25)