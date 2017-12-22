import numpy as np 

def load_route():
	routefile = open('wsc_2017.csv', 'r').readlines()
	route = np.zeros((len(routefile), 8))
	i = 0
	for line in routefile:
		data = line.split(',')
		j = 1
		route[i][0] = 75 # default starting speed --> need to come up with a more intelligent way to do this
		for elem in data:
			route[i][j] = float(elem)
			j += 1
		i += 1
	return route


# TODO
def load_lookup_tables():
	power_to_drive = ''
	soc = ''
	weather = ''
	return power_to_drive, soc, weather


def to_mps(kph):
	return kph * 1000 * 60 * 60

# TODO
def array_model(time_of_day, lat, lng, elev, weather_preds):
	pass


CURR_SPEED = 0
LONGITUDE = 1
LATITUDE = 2
DISTANCE = 3
ELEVATION = 4
OTHER_STOP = 5
CONTROLSTOP = 6
SPEED_LIMIT = 7

race_start = # TODO
quiescent = # TODO
pack_start = # TODO

def calculate_speed_and_power(route, ptd, soc, weather_preds):
	power_results = np.zeros((route.shape[0], 3)) # spent_power, made_power, cumulative_driving_time, cumulative_net_power
	prev_time_of_day = race_start

	for i in range(0, route.shape[0]):
		segment = route[i]
		if i != 0:
			segment_distance = segment[DISTANCE] - route[i-1]
		else:
			segment_distance = segment[DISTANCE]

		if segment[CURR_SPEED] < segment[SPEED_LIMIT]:
			speed = segment[SPEED_LIMIT]
		else:
			speed = segment[CURR_SPEED]

		if segment[CONTROLSTOP] == 1:
			spent_power = quiescent
			time_passed = to_mps(32) # control stops are modeled as 32 minutes long
		elif segment[OTHER_STOP] == 1:
			driving_time = to_mps(speed) * segment_distance - STOP_TIME
			spent_power = driving_time * ptd[speed] + quiescent * STOP_TIME
			time_passed = driving_time + STOP_TIME
		else:
			driving_time = to_mps(speed) * segment_distance
			spent_power = driving_time * speed
			time_passed = driving_time

		time_of_day = prev_time_of_day + driving_time
		array_power = array_model(time_of_day, segment[LATITUDE], segment[LONGITUDE], segment[ELEVATION], weather_preds)

		# tally up cumulative results and save them
		power_results[i][0] = spent_power
		power_results[i][1] = array_power
		if i != 0:
			power_results[i][2] = power_results[i-1][2] + time_passed
		else:
			power_results[i][2] = time_passed
		if i != 0:
			power_results[i][3] = power_results[i-1][3] + array_power - spent_power
		else:
			power_results[i][3] = pack_start + array_power - spent_power

		prev_time_of_day = time_of_day

		return lookup_soc(soc, power_results[-1][3]), power_results[-1][2] # SOC and time passed at the end of the route


# TODO
def update_with_limp_speed(route, ptd, soc, weather_preds):
	pass 