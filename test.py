from djitellopy import Tello
import time

tello = Tello()

tello.connect()

grid = list()

def fetchHeight():
	return str(tello.get_distance_tof())

print("battery pct " + str(tello.get_battery()))

# tello.takeoff()
# i = 0

# x = 0
# y = 0
# x_max = 10
# y_max = 10

# for cx in range(x_max):
# 	for cy in range (y_max):

# 		print(str(cx) + "," + str(cy) + " " + fetchHeight())
# 		time.sleep(2)


while True:
	print(fetchHeight())
	time.sleep(0.5)