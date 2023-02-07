from djitellopy import Tello
import time
import matplotlib.pyplot as plt


# Graph Stuff
graph_x = []
graph_y = []

tello = Tello()

connected = False
while not connected:
	try:
		tello.connect()
		print("connected hopefully!")
		connected = True
	except:
		print("not connected :(")
		time.sleep(1)

tello.set_speed(10) # in cm/s

print("Attempting to takeoff")
tello.takeoff()
print("Took off?")
time.sleep(5)

# all in CM
desired_height = 100
acceptable_delta = 10
correction_factor = 20

upper_height = desired_height + acceptable_delta
lower_height = desired_height - acceptable_delta

def drone_ok():
	if tello.get_battery() < 10:
		print("battery is too low! " + str(tello.get_battery()) + "%")
		return False
	elif tello.get_flight_time() > 60*10:
		print("flight time is too long! " + str(tello.get_flight_time()) + "secs")
		return False
	else:
		return True

# The Levelling System
# This function will attempt to keep the drone at a set height, set above
def levelling_system():
	print("levelling system start")
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

def measuring_system(pos):
	print("measuring system start")

	# get the distance from the drone to the ground
	distance = tello.get_distance_tof()
	print("distance: " + str(distance) + "cm at " + str(pos))

	# add the distance to the graph
	graph_x.append(pos)
	graph_y.append(distance*-1)


forward_errors = 0
def move_forward_loop(dist):
	global forward_errors

	if forward_errors > 5:
		print("failed to move forward 5 times, landing")
		tello.land()

	try:
		tello.move_forward(dist)
	except:
		forward_errors = forward_errors + 1
		print("error moving forward! trying again in a few seconds...")
		time.sleep(5)
		move_forward_loop(dist)

# The Mapping System
pos = 0 # Assumed position of the drone, relative to start point (cm)
end = 150 # End position of the drone (cm)
step = 20 # Increment to move the drone in (cm)
mapping = True # Are we mapping or not?

while mapping:
	print("mapping loop start")

	if not drone_ok() or pos >= end:
		print("drone is not ok or we've reached the end of the line, trying to return home and land")
		
		# tello.move_back(pos) # move back to the start
		# time.sleep(pos*0.8) # arbitrary time to get back to the start
		tello.land()

		print(graph_x)
		print(graph_y)

		plt.plot(graph_x, graph_y)
		plt.xlabel('Distance')
		plt.ylabel('Height')
		plt.title('Heights')
		plt.show()

		mapping = False
		break
	else:
		print("drone is ok and we're not at the end of the line, continuing")
		
		move_forward_loop(step)
		pos += step
		
		print("current position: " + str(pos))
		
		levelling_system()
		measuring_system(pos)

		#time.sleep(5) # arbitrary time to wait (secs)