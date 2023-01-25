from djitellopy import Tello
import time

tello = Tello()
tello.connect()
print("battery pct " + str(tello.get_battery()))

tello.takeoff()
# tello.move_up(100)

desired_height = 175
acceptable_delta = 20
correction_factor = 20

upper_height = desired_height + acceptable_delta
lower_height = desired_height - acceptable_delta

def heightMeasureRoutine():
	height_ok = False

	while not height_ok:
		current_height = tello.get_height()
		print("currently flying at " + str(current_height) + "cm")

		if current_height < upper_height and current_height > lower_height:
			height_ok = True
			print("this is acceptable (+-" + str(acceptable_delta) + " of " + str(desired_height) + "cm)")
			return print(str(tello.get_distance_tof()))

		if current_height > desired_height:
			print("too high! moving down")
			try:
				tello.move_down(correction_factor)
			except:
				print("brokey when going up!")

		elif current_height < desired_height:
			print("too low! moving up")
			try:
				tello.move_up(correction_factor)
			except:
				print("brokey when going down!")
		
		time.sleep(1)


x = 0
y = 0
x_max = 5
y_max = 5
step = 20
forwards = True
mapping = True

while mapping:

	print("current x: " + str(x) + "\nmax x: " + str(x_max) + "\n\ncurrent y: " + str(y) + "\nmax y: " + str(y_max))
	heightMeasureRoutine()

	if forwards:
		tello.move_forward(step)
		x+=1
	else:
		tello.move_back(step)
		x-=1

	if x == x_max:
		forwards = False
		y+=1
		tello.move_right(step)

		if y == y_max:
			mapping = False
			tello.land()

	time.sleep(5)
	


		




