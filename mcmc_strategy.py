from utils import load_route, calculate_speed_and_power, update_with_limp_speed, load_lookup_tables

updates_per_iteration = 100 # parameter to tune
max_iterations = 100 # parameter to tune
min_acceptable = 70 # parameter to tune
max_acceptable = 90 # parameter to tune

route_speeds = load_route() # TODO: how best to initialize this?
route_time = 0
power_left = 0

best_route_speeds = route_speeds
best_route_time = route_time
best_power_left = power_left

results = list()

ptd, soc, weather_preds = load_lookup_tables()

num_iterations = 0
while num_iterations < max_iterations:
	new_route_speeds = deepcopy(route_speeds) # TODO: should we start with the current best or with the previous route?

	num_updated = 0
	# TODO: should we update all indexes before running the route? How about trying all speeds before running the route?
	# ie think some more about where calculate_speed_and_power is called relative to updates in the states of the Markov chain
	while num_updated < updates_per_iteration:
		modified_index = random(0, len(new_route_speeds)

		for speed in range(min_acceptable, max_acceptable):
			new_route_speeds[modified_index] = speed
			new_power_left, new_route_time = calculate_speed_and_power(new_route_speeds, ptd, soc, weather_preds)

		# can't run out of power -- if we do, must switch speeds to limp speed
		# so we can still complete the race
		if power_left < power_buffer:
			new_route_speeds, new_power_left, new_route_time = update_with_limp_speed(new_route_speeds, ptd, soc, weather_preds)
		
		if new_route_speeds < route_time:
			route_speeds = new_route_speeds
			route_time = new_route_time
			power_left = new_power_left

		# sometimes we keep it even if it isn't better! 	
		if temp > 0:
			if random.uniform(0, 1) < math.exp(-(route_time - new_route_time))/temp):
				route_speeds = new_route_speeds
				route_time = new_route_time
				power_left = new_power_left

		if new_route_speeds < best_route_time:
			best_route_speeds = new_route_speeds
			best_route_time = new_route_time
			best_power_left = new_power_left

		results.append((route_speeds, route_time, power_left))

	num_updated += 1