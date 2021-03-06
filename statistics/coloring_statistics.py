from __future__ import division
import copy
import sys
sys.path.insert(0, 'D:/College/BTP/VPool/')
import optimization.infinite_vehicle_allocator as iva
import distance_statistics as dStats
import vehicle_statistics as vStats
import route_statistics as rStats
import os


def coloring_statistics(coloring, vehicles, distance_from_destination, source_data, destination_data, source_destination_data, rates, requests, text_output):
	"""
	Function to calculate statistics related to the coloring
	obtained, statistics range from vehicle to route
	statistics and statistics about operator profits.

	Args:
		coloring: The obtained color class from graph coloring.

		vehicles: The vehicles allocated to the given color
		class.

		distance_from_destination: Distance of each rider from
		their destination.

		source_data: Distance matrix of sources of riders

		destination_data: Distance matrix of destinations
		of riders

		source_destination_data: Distance matrix of sources
		and destinations of riders

		rates: The list of rates charged to each rider for
		being part of the system.

		requests: A list of objects of the class request
		corresponding to each rider in the system.

		text_output: The output text file used to communicate
		with jsprit java code.

	Returns:
		The statistics obtained of the given
		coloring.
	"""
	total_operator_cost = 0
	total_used_vehicles = 0
	in_source_distances = 0
	users_above_slab = 0
	average_ratio = 0.0
	combined_distance = 0.0
	vehicle_distance = 0.0
	single_user_vehicles = 0

	for color in coloring:
		cost, allotment = iva.allot_vehicles(coloring[color], vehicles)
		total_used_vehicles += len(allotment)
		distance_results = dStats.get_distance_from_allocation(allotment,distance_from_destination)

		for vehicle in allotment:
			cost_incurred = 0

			file_contents = []
			file_contents.append(str(len(vehicle.passengers))+'\n')
			file_contents.append(str(vehicle.cap)+'\n')

			occupants_string = ""
			for user in vehicle.passengers:
				occupants_string = occupants_string + str(user) +','
			occupants_string = occupants_string[:len(occupants_string)-1]

			file_contents.append(occupants_string+'\n')

			file_contents.append('40.730610,-73.935242\n')

			for user in vehicle.passengers:
				if requests[user].source_lat != 0.0:
					file_contents.append(str(requests[user].source_lat)+','+str(requests[user].source_long)+'\n')
				else:
					file_contents.append('40.730610,-73.935242\n')

			for user in vehicle.passengers:
				if requests[user].dest_lat != 0.0:
					file_contents.append(str(requests[user].dest_lat)+','+str(requests[user].dest_long)+'\n')			
				else:
					file_contents.append('40.730610,-73.935242\n')			

			file = open(text_output,"w+")
			file.writelines(file_contents)
			file.close()

			query_string = 'java -jar vehicle_routing.jar ' + text_output
			route = os.popen(query_string).read()
			route_statistics = rStats.in_vehicle_user_stats(vehicle.passengers, route, source_data, destination_data, source_destination_data)
			average_ratio = average_ratio + route_statistics[0]
			combined_distance = combined_distance + route_statistics[1]
			vehicle_distance = vehicle_distance + route_statistics[2]

			if len(vehicle.passengers) == 1:
				rates[vehicle.passengers[0]] = route_statistics[2]*20
				single_user_vehicles += 1
			elif vehicle.cap > 4:
				for passenger in vehicle.passengers:
					rates[passenger] = route_statistics[2]*10

			if vehicle.cap == 4:
				cost_incurred = route_statistics[2]*15
			elif vehicle.cap == 6:
				cost_incurred = route_statistics[2]*25
			else:
				cost_incurred = route_statistics[2]*30

			cost = cost + cost_incurred - vehicle.cost

			in_source_distances += dStats.users_stats_in_coloring(vehicle.passengers, source_data)
			users_above_slab += vStats.user_vs_vehicle_comparison(vehicle.passengers, rates, cost_incurred)

		total_operator_cost += cost

	revenue = sum(rates)-total_operator_cost
		
	average_ratio = average_ratio/total_used_vehicles
	combined_distance = combined_distance/total_used_vehicles
	vehicle_distance = vehicle_distance/total_used_vehicles
	return [revenue, in_source_distances/total_used_vehicles, users_above_slab, total_used_vehicles, average_ratio, combined_distance/vehicle_distance, single_user_vehicles, vehicle_distance]


	if __name__ == '__main__':
		pass