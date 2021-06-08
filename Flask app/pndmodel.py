class DataModel():

	def __init__(self, n,nv,cap):


		import numpy as np
		#np.random.seed(0) #can enable seeding so that you can check solutions with different time limits for the same generated problem
		vc=[cap]*nv #capacities

		N=[i for i in range(1,n+1)] #clients
		V=[0]+N #verticles with central point
		self.__V=V
		x=np.random.rand(len(V))*100
		y=np.random.rand(len(V))*100

		p=[(i,j) for i in V for j in V ] #all posible routes  
		d={(i,j): int(np.hypot([x[i]-x[j]],[y[i]-y[j]])[0]) for (i,j) in p}

		distmat=list()

		for i in range(n+1):
			distances=list()
			for j in range(n+1):
				distances.append(d[(i,j)])
			distmat.append(distances)


		indexes=np.arange(1,n+1)
		np.random.shuffle(indexes) #randomize indexes
		pickups=indexes[0:int((n+1)/2)] #cut indexes in half to create random pickup and delivery points
		deliveries=indexes[int((n+1)/2):(n+1)]

		pnd=list()
		for i in range(len(pickups)):
			pnd.append([pickups[i],deliveries[i]])



		demands=np.zeros(len(pickups)*2+1)

		for i in range(len(pickups)):
			demands[pickups[i]]+=np.random.randint(1,cap+1)
			demands[deliveries[i]]+=(demands[pickups[i]]*(-1))


		self.__distance_matrix = distmat
		self.__pickups_deliveries = pnd
		self.__demands = demands
		self.__vehicle_capacities = vc
		self.__num_vehicles = nv
		self.__depot = 0
		self.__x=x
		self.__y=y
		self.__V=V

	def __createmodel__(self):
		data = {}
		data['distance_matrix'] = self.__distance_matrix
		data['pickups_deliveries'] = self.__pickups_deliveries
		data['demands'] = self.__demands
		data['vehicle_capacities'] = self.__vehicle_capacities
		data['num_vehicles'] = self.__num_vehicles
		data['depot'] = self.__depot
		self.__data=data
		return self.__data

	def __drawpnd__(self):
		import matplotlib
		matplotlib.use('Agg')
		from matplotlib import pyplot as plt
		
		x=self.__x
		y=self.__y
		V=self.__V

		plt.figure(figsize=(16, 12))
		plt.scatter(x[1:],y[1:],c='y')
		for i in V:
			#plt.annotate('q{}({})'.format(i, q[i]), (x[i],y[i]))
			plt.annotate('q{}'.format(i), (x[i],y[i]))
		plt.scatter(x[0],y[0],c='r')

		for pnd in self.__pickups_deliveries:
			i=pnd[0]
			j=pnd[1]
			dx=x[j]-x[i]
			dy=y[j]-y[i]
			plt.arrow(x[i],y[i],dx,dy,width=0.01,length_includes_head=True,head_width=1.5, fc='m', ec='c')
			plt.grid(True)
			plt.title('Pickup and delivery points')
			plt.xlabel('horizontal distance [m]')
			plt.ylabel('vertical distance [m]')
			plt.xlim(0,100)
			plt.ylim(0,100)
		plt.savefig('figpnd.png')
	
	@property
	def data(self):
		"""Gets the model."""
		return self.__data

	@property
	def distance_matrix(self):
		"""Gets the distance matrix."""
		return self.__distance_matrix

	@property
	def demands(self):
		"""Gets the locations demands."""
		return self.__demands

	@property
	def pickups_deliveries(self):
		"""Gets the pickups deliveries."""
		return self.__pickups_deliveries

	@property
	def num_vehicles(self):
		"""Gets the number of vehicles."""
		return self.__num_vehicles

	@property
	def vehicle_capacities(self):
		"""Gets the capacity of each vehicles."""
		return self.__vehicle_capacities


	@property
	def depot(self):
		"""Gets the depot node index."""
		return self.__depot
	@property
	def createmodel(self):
		"""Gets the create model function."""
		return self.__createmodel__()

	@property
	def drawpnd(self):
		"""Gets the drawpnd function."""
		return self.__drawpnd__()
	@property
	def x(self):
		"""Gets x indexes."""
		return self.__x

	@property
	def y(self):
		"""Gets y indexes."""
		return self.__y


		

class Optimization():

	def __init__(self,model,tlimit,x,y):
		
		from ortools.constraint_solver import routing_enums_pb2
		from ortools.constraint_solver import pywrapcp
		
		# Instantiate the data problem.
		data = model
		self.__x=x
		self.__y=y
		self.__tlimit=tlimit
		# Create the routing index manager.
		manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
											   data['num_vehicles'], data['depot'])

		# Create Routing Model.
		routing = pywrapcp.RoutingModel(manager)

		def get_routes(solution, routing, manager):
			"""Get vehicle routes from a solution and store them in an array."""
			# Get vehicle routes and store them in a two dimensional array whose
			# i,j entry is the jth location visited by vehicle i along its route.
			routes = []
			for route_nbr in range(routing.vehicles()):
				index = routing.Start(route_nbr)
				route = [manager.IndexToNode(index)]
				while not routing.IsEnd(index):
					index = solution.Value(routing.NextVar(index))
					route.append(manager.IndexToNode(index))
				routes.append(route)
			return routes

		# Define cost of each arc.
		def distance_callback(from_index, to_index):
			"""Returns the manhattan distance between the two nodes."""
			# Convert from routing variable Index to distance matrix NodeIndex.
			from_node = manager.IndexToNode(from_index)
			to_node = manager.IndexToNode(to_index)
			return data['distance_matrix'][from_node][to_node]

		transit_callback_index = routing.RegisterTransitCallback(distance_callback)
		routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

		def demand_callback(from_index):
			"""Returns the demand of the node."""
			# Convert from routing variable Index to demands NodeIndex.
			from_node = manager.IndexToNode(from_index)
			return data['demands'][from_node]

		demand_callback_index = routing.RegisterUnaryTransitCallback(
			demand_callback)
		routing.AddDimensionWithVehicleCapacity(
			demand_callback_index,
			0,  # null capacity slack
			data['vehicle_capacities'],  # vehicle maximum capacities
			True,  # start cumul to zero
			'Capacity')

		# Add Distance constraint.
		dimension_name = 'Distance'
		routing.AddDimension(
			transit_callback_index,
			0,  # no slack
			3000,  # vehicle maximum travel distance
			True,  # start cumul to zero
			dimension_name)
		distance_dimension = routing.GetDimensionOrDie(dimension_name)
		distance_dimension.SetGlobalSpanCostCoefficient(100)

		# Define Transportation Requests.
		for request in data['pickups_deliveries']:
			pickup_index = manager.NodeToIndex(request[0])
			delivery_index = manager.NodeToIndex(request[1])
			routing.AddPickupAndDelivery(pickup_index, delivery_index)
			routing.solver().Add(
				routing.VehicleVar(pickup_index) == routing.VehicleVar(
					delivery_index))
			routing.solver().Add(
				distance_dimension.CumulVar(pickup_index) <=
				distance_dimension.CumulVar(delivery_index))

		# Setting first solution heuristic.
		search_parameters = pywrapcp.DefaultRoutingSearchParameters()
		search_parameters.first_solution_strategy = (
			routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION)

		search_parameters.local_search_metaheuristic = (
			routing_enums_pb2.LocalSearchMetaheuristic.AUTOMATIC)
		search_parameters.time_limit.FromSeconds(self.__tlimit)
		

		# Solve the problem.
		self.__solution = routing.SolveWithParameters(search_parameters)
		self.__routes = get_routes(self.__solution, routing, manager)
		self.__data=data
		self.__manager=manager
		self.__routing=routing

	@property
	def data(self):
		return self.__data

	@property
	def manager(self):
		return self.__manager

	@property
	def routing(self):
		return self.__routing

	@property
	def solution(self):
		return self.__solution

	def __textsol__(self):
		from ortools.constraint_solver import routing_enums_pb2
		from ortools.constraint_solver import pywrapcp

		 #Create string with solution
		
		solution_string='Objective: '+str(self.__solution.ObjectiveValue())+'<br>'
		total_distance = 0
		total_load = 0
		for vehicle_id in range(self.__data['num_vehicles']):
			index = self.__routing.Start(vehicle_id)
			plan_output = 'Route for vehicle {}:<br>'.format(vehicle_id)
			route_distance = 0
			route_load = 0
			while not self.__routing.IsEnd(index):
				node_index = self.__manager.IndexToNode(index)
				route_load += self.__data['demands'][node_index]
				plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
				previous_index = index
				index = self.__solution.Value(self.__routing.NextVar(index))
				route_distance += self.__routing.GetArcCostForVehicle(
					previous_index, index, vehicle_id)
			plan_output += ' {0} Load({1})<br>'.format(self.__manager.IndexToNode(index),
													 route_load)
			plan_output += 'Distance of the route: {}m<br>'.format(route_distance)
			plan_output += 'Load of the route: {}<br><br>'.format(route_load)
			solution_string+=plan_output
			total_distance += route_distance
			total_load += route_load
		solution_string+=('Total distance of all routes: '+str(total_distance)+' m<br>')
		solution_string+=('Total load of all routes: '+str(total_load)+'<br>')
		self.__solution_string=solution_string
		return self.__solution_string

	@property
	def textsol(self):
		return self.__textsol__()

	def __drawsol__(self):
		import matplotlib
		matplotlib.use('Agg')
		from matplotlib import pyplot as plt
		import numpy as np

		 #Create drawn file with solution
		
		def random_color():
			return tuple(np.random.random() for _ in range(3))

		plt.figure(figsize=(16, 12))
		plt.title('Visualisation of optimized routes')
		plt.grid(True)
		plt.xlabel('horizontal distance [m]')
		plt.ylabel('vertical distance [m]')
		plt.xlim(0,100)
		plt.ylim(0,100)
		plt.scatter(self.__x[1:],self.__y[1:],c='y')
		for i in range(0,len(self.__x)):
			#plt.annotate('q{}({})'.format(i, q[i]), (x[i],y[i]))
			plt.annotate('q{}'.format(i), (self.__x[i],self.__y[i]))
			plt.scatter(self.__x[0],self.__y[0],c='r')

		k=0
		for route in self.__routes:
			c = random_color()
			for ride in range(len(route)-1):
				i=route[ride]
				j=route[ride+1]
				plt.plot([self.__x[i],self.__x[j]],[self.__y[i],self.__y[j]], c=c)
			plt.plot(1000,1000, c=c,label=('Vehicle '+str(k)))
			k+=1
				
		plt.legend()

		plt.savefig('figsol.png')

	@property
	def drawsol(self):
		return self.__drawsol__()
