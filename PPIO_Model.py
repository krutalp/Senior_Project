'''
## Problem Description: 

For a given list of passengers with predefined origin airports and final destination airports, a fixed number of planes in operation, 
and a fixed network topology $G(A,R)$, we want to extract the optimal schedule or itinerary for each plane $p$ and each passenger $h$ 
throughout the day. 

This problem is related to the class of Traveling Salesman Problems, where the goal is to find the shortest distance path through cities 
such that the salesman starts and stops at the same city. The key differences in this optimization problem is that we are interested in 
minimizing the total travel time over each passenger $h$, and we have multiple agents traversing the network at scheduled times.

We will solve this optimization problem using a multi-integer linear programming approach. There are many applications of this optimization 
problem including logistics planning, energy management, crew scheduling, and telecommunications network design.

## PPIO Model Formulation:

This script generates an LP model and executes the program using Gurobi.

The model accepts the following parameters:
    -> Time range T
    -> Set of Airports
    -> List of possible routes
    -> Set of Planes with starting airport
    -> List of passengers with starting and final destination airports
'''

# import packages
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import truncnorm 
import folium
import json
import os
from folium import plugins
import gurobipy as gp
import random
import itertools
import math
from gurobipy import GRB
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def plane_capacity(planes, mean, std, min_h, max_h):
    '''
    Goal: Return passenger capacities for each unique plane:
            This depends on the type of aircraft, amount of cargo, etc 
            We use a uniform distribution over the supports [min h, max h]   
    Parameters:
        planes: (list) list of planes in operation over the network  (defined as string indices)
        mean: (float) the mean passenger capacity over all planes
        std: (float) the stdev of passenger capacity over all planes
        min_h: (int) the minimum number of passengers allowed on a plane
        max_h: (int) the maximum number of passengers allowed on a plane
    Returns:
        capacity_p: (dict) a dictionary of keys as planes with associated passenger capacity
    ''' 

    # define capacity of each plane
    # src: https://www.faa.gov/sites/faa.gov/files/regulations_policies/policy_guidance/benefit_cost/econ-value-section-3-capacity.pdf  
    capacity_p = {}
    # define distribution for plane capacity 
    # truncated normal distribution  (support: {85, 215}) with mean 150 and stdev 80
    a, b = (min_h - mean) / std, (max_h - mean) / std
    for i in planes:
        capacity_p[i] = int(truncnorm.rvs(a, b, loc = mean, scale = std, size=1))
    return capacity_p

def airport_capacity(airports, mean, std, min_a, max_a):
    '''
    Goal: Return planes capacities for each unique airport:
            This depends on the type of airport, amount of cargo, etc 
            We use a uniform distribution over the supports [min a, max a]   
    Parameters:
        airports: (list) list of airports in operation over the network  (defined as string indices)
        mean: (float) the mean plane capacity over all airports
        std: (float) the stdev of plane capacity over all airports
        min_a: (int) the minimum number of planes allowed on a plane
        max_a: (int) the maximum number of planes allowed on a plane
    Returns:
        capacity_a: (dict) a dictionary of keys as airports with associated plane capacity
    '''
    # define capacity of each airport
    capacity_a = {}
    # define distribution for airport capacity 
    # truncated normal distribution  (support: {1, 5}) with mean and stdev
    a, b = (min_a - mean) / std, (max_a - mean) / std
    for i in airports:
        capacity_a[i] = int(truncnorm.rvs(a, b, loc = mean, scale = std, size=1))
    return capacity_a

def create_complete_network(airports):
    '''
    Goal: given a set of airports to serve as nodes of the graph, return a complete airline network topology
    Parameters:
        airports (list): list of airports in the network
    Return:
        G_complete (networkx graph): the complete graph of the airline network topology
    '''
    # consider a complete graph (all possible options)
    G_complete = nx.complete_graph(airports) # we select flights (t + route(i,j)) to operate these   (a flight object is later defined)
    coords = {}
    for i in G_complete.nodes:
        origin_lat = float(airports_data.loc[airports_data['local_code'] == i]['latitude_deg'].values)
        origin_long = float(airports_data.loc[airports_data['local_code'] == i]['longitude_deg'].values)
        coords[i] = (origin_lat, origin_long)
    nx.set_node_attributes(G_complete, coords, name = 'pos')
    G_complete = G_complete.to_directed()
    return G_complete

def sample_routes(set_of_airports, total_edges):
    '''
    Goal: generate a random subset of directed edges / routes from the complete graph
    Parameters:
        set_of_airports (list): a list of airports in the airline network topology
        total_edge (int): number of routes to sample from complete graph
    Return:
        sampled_routes (list): list of viable routes in the network such that a path exists between all airports
    '''
    def is_connected(random_routes):
        permutations_of_routes = list(itertools.permutations(set_of_airports, 2))
        # ensure the random routes generated forms a connected graph!
        G_check = nx.DiGraph()
        # Add edges from the list of tuples
        G_check.add_edges_from(random_routes)

        for pair in permutations_of_routes:
            if not nx.has_path(G_check, pair[0], pair[1]):
                return False
        return True

    permutations_of_routes = list(itertools.permutations(set_of_airports, 2))
    condition = False
    while not condition:
        sampled_routes = random.sample(permutations_of_routes, total_edges)
        condition = is_connected(sampled_routes)
    return sampled_routes

# DATA: airports IATA Code and Geographical Coordinates
airports_data = pd.read_csv('Data/us-airports.csv')
airports_data = airports_data[['latitude_deg','longitude_deg','local_code']]
airports_data = airports_data.iloc[1:]

# DATA: on time preformance by airlines between two airports : extract distance and duration
us_ontime_market = pd.read_csv('Data/T_ONTIME_MARKETING.csv')
us_ontime_market = us_ontime_market.groupby(['ORIGIN', 'DEST'])[['ACTUAL_ELAPSED_TIME', 'DISTANCE']].mean().reset_index()


class Passenger:
    # Define a passenger object to represent all human passengers traversing the airline network
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination
    def get_origin(self):
        return self.origin
    def get_destination(self):
        return self.destination
    def __repr__(self):
        return f"Passenger traveling from {self.origin} to {self.destination}"
    
# define an object called Flight which consists of a 2-tuple of the route 
# serviced (consisting or origin and destination) airport code and the time t of departure.
class Flight:
    def __init__(self, origin, destination, departure_time, duration=None):
        self.origin = origin
        self.destination = destination
        self.departure_time = departure_time
        self.origin_lat = float(airports_data.loc[airports_data['local_code'] == origin]['latitude_deg'].values)
        self.origin_long = float(airports_data.loc[airports_data['local_code'] == origin]['longitude_deg'].values)
        self.dest_lat = float(airports_data.loc[airports_data['local_code'] == destination]['latitude_deg'].values)
        self.dest_long = float(airports_data.loc[airports_data['local_code'] == destination]['longitude_deg'].values)
        #self.duration = duration or self.get_flight_duration()
        
    def get_origin(self):
        return self.origin

    def get_destination(self):
        return self.destination
        
    def get_departure_time(self):
        return self.departure_time

    def get_fight_duration(self):
        filtrd_data = us_ontime_market[(us_ontime_market['ORIGIN'] == self.origin) & (us_ontime_market['DEST'] == self.destination)]
        flight_duration = int(filtrd_data['ACTUAL_ELAPSED_TIME'].values[0])
        return flight_duration

    def get_arrival_time(self):
        return int(np.ceil(self.get_fight_duration()/60)) + self.departure_time

    def get_distance(self):
        # Radius of the Earth in miles
        earth_radius = 3958.8
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [self.origin_lat, self.origin_long, self.dest_lat, self.dest_long])
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c
        distance = us_ontime_market[(us_ontime_market['ORIGIN'] == self.origin) & (us_ontime_market['DEST'] == self.destination)]['DISTANCE']
        return distance 

    def visualize_route(self):
        m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
        folium.Marker(location=[self.origin_lat, self.origin_long], popup=node).add_to(m)
        folium.Marker(location=[self.dest_lat, self.dest_long], popup=node).add_to(m)
        folium.PolyLine([(self.origin_lat, self.origin_long), (self.dest_lat, self.dest_long)], color="blue").add_to(m)
        return m

    def __repr__(self):
        return f"Flight from {self.origin} to {self.destination} departing at t = {self.departure_time}, and arriving at t = {self.get_arrival_time()}"
    

def run_PPIO_model(routes, T, passengers, set_of_airports, planes_p):

    permutations_of_routes = list(itertools.permutations(set_of_airports, 2))

    # define plane and airport capacities respectivily given current aviation data
    capacity_p = plane_capacity(planes_p, 100, 3, 1, 800)
    capacity_a = airport_capacity(set_of_airports, 50, 2, 5, 100)

    # define flights objects for each possible route and Time t
    flights = {}
    counter = 1
    for org, dest in routes:
        for t in T:
            name = f'''f_{counter}'''
            flight_obj = Flight(origin=org, destination=dest, departure_time=t)
            flights[name] = (flight_obj.get_origin(), flight_obj.get_destination(), flight_obj.get_departure_time(), flight_obj.get_arrival_time())
            counter += 1
            
    # these sets of decision variables and indexed variables define the LP model initialization
        # Create a Gurobi model
    m = gp.Model("Flight_Optimization")

    # Create a dictionary to hold the decision variables X[f, h] for each combination of flight and passenger
    X_inds = []
    for f in flights:
        for h in passengers.keys():
            index = (flights[f], h)
            X_inds.append(index)
    X_vars = m.addVars(X_inds, vtype=GRB.BINARY, name='X')

    # create a dictionary to hold the decision variable Y[p,f] for each combination of plane and flight
    Y_inds = []
    for p in planes_p.keys():
        for f in flights:
            index = (p, flights[f])
            Y_inds.append(index)
    Y_vars = m.addVars(Y_inds, vtype=GRB.BINARY, name='Y')

    # create a dictionary to hold the decision variable W[t,p,a] for each combination of time, airport, plane
    W_inds = []
    for t in T:
        for p in planes_p.keys():
            for a in set_of_airports:
                W_inds.append((t,p,a))
    W_vars = m.addVars(W_inds, vtype=GRB.BINARY, name='W')
        
    # create a dictionary to hold the decision variable Z[t,h,a] for each combination of time, passenger, airport
    Z_inds = []
    for t in T:
        for h in passengers.keys():
            for a in set_of_airports:
                Z_inds.append((t,h,a))
    Z_vars = m.addVars(Z_inds, vtype=GRB.BINARY, name='Z')

    m.update()

        # Add the objective function to the model

    # Define the objective expression
    objective_expr = gp.quicksum(Z_vars[(t, h, passengers[h].get_origin())] + 
                                Z_vars[(t, h, passengers[h].get_destination())] 
                                for t in T for h in passengers.keys())

    # Set the objective function to maximize the above expression
    m.setObjective(objective_expr, GRB.MAXIMIZE)
    m.update()
    print('Model Updated with Core Objective Function')


    # Add General boundary conditions to the gurobi model m
    # first add boundary for location of each plane p

    # Define the starting boundary conditions at t=0 for passengers
    for h in passengers.keys():
        m.addConstr(Z_vars[(0, h, passengers[h].get_origin() )] == 1, name=f'StartingBoundaryPassenger_{h}')

    # Define the starting boundary conditions at t=0 for planes (random assignment)
    for p in planes_p.keys():
        m.addConstr(W_vars[(0, p, planes_p[p] )] == 1, name=f'StartingBoundaryPlane_{p}')

    # Define the ending boundary conditions at t=|T|-1 for passengers
    for h in passengers.keys():
        m.addConstr(Z_vars[(len(T) - 1, h, passengers[h].get_destination() )] == 1, name=f'EndingBoundaryPassenger_{h}')

    # Define the ending boundary conditions at t=|T|-1 for planes
    for p in planes_p:
        m.addConstr(W_vars[(len(T) - 1, p,  planes_p[p] )] == 1, name=f'EndingBoundaryPlane_{p}')

    # Define Airport Capacity constraint (Constraint 9)
    for t in T:
        for a in set_of_airports:
            m.addConstr(gp.quicksum(W_vars[t, p, a] for p in planes_p) <= capacity_a[a],
                        name=f'AirportCapacity_{t}_{a}')
            
    # Define Plane Capacity constraint (Constraint 8)
    for f in flights:
        m.addConstr(gp.quicksum(X_vars[flights[f], h] for h in passengers.keys()) <=
                    gp.quicksum(capacity_p[p] * Y_vars[p, flights[f]] for p in planes_p),
                    name=f'PlaneCapacity_{f}')
        

    def conflicting_flights(f1,f2):
        # return true if f1 and f2 form a conflicting flight 
        start_f1 = flights[f1][2]
        end_f1 = flights[f1][3]
        start_f2 = flights[f2][2]
        end_f2 = flights[f2][3]
        return start_f1 <= start_f2 <= end_f1 or start_f2 <= start_f1 <= end_f2
        
    # Define Conflicting Flights for planes (Constraint 8)
    for p in planes_p:
        for f1 in flights:
            for f2 in flights:
                if f1 != f2 and conflicting_flights(f1, f2):
                    m.addConstr(Y_vars[p, flights[f1]] + Y_vars[p, flights[f2]] <= 1, name=f'PlaneConflict_{p}_{f1}_{f2}')

    # Define Conflicting Flights for passengers (Constraint 9)
    for h in passengers.keys():
        for f1 in flights:
            for f2 in flights:
                if f1 != f2 and conflicting_flights(f1, f2):
                    m.addConstr(X_vars[flights[f1], h] + X_vars[flights[f2], h] <= 1, name=f'PassengerConflict_{h}_{f1}_{f2}')

    # Define Conservation Laws for passengers (Constraint 10)
    for h in passengers.keys():
        for t in T:
            m.addConstr(gp.quicksum(Z_vars[(t, h, a)] for a in set_of_airports) +
                        gp.quicksum(X_vars[flights[f], h] for f in flights if flights[f][2] <= t <=  flights[f][3]  ) == 1,
                        name=f'PassengerConservation_{h}_{t}')

    # Define Conservation Laws for planes (Constraint 11)
    for p in planes_p:
        for t in T:
            m.addConstr(gp.quicksum(W_vars[(t, p, a)] for a in set_of_airports) +
                        gp.quicksum(Y_vars[p, flights[f]] for f in flights if flights[f][2] <= t <= flights[f][3]) == 1,
                        name=f'PlaneConservation_{p}_{t}')

    # Define Continuity of Origin Airport for planes (Constraint 12)
    for p in planes_p:
        for f in flights:
            if flights[f][2] > 0:  # Exclude t=0
                m.addConstr(W_vars[flights[f][2] - 1, p, flights[f][0]] >= Y_vars[p, flights[f]], name=f'PlaneOriginContinuity_{p}_{f}')
    # Define Continuity of Origin Airport for passengers (Constraint 13)
    for h in passengers.keys():
        for f in flights:
            if flights[f][2] > 0:  # Exclude t=0
                m.addConstr(Z_vars[flights[f][2] - 1, h, flights[f][0]] >= X_vars[flights[f], h], name=f'PassengerOriginContinuity_{h}_{f}')

    # Define Continuity of Destination Airport for planes (Constraint 14)
    for p in planes_p:
        for t in T:
            for a in set_of_airports:
                if t > 0:  # Exclude t=0
                    m.addConstr(W_vars[t - 1, p, a] +
                                gp.quicksum(Y_vars[p, flights[f]] 
                                            for f in flights 
                                                if flights[f][1] == a and flights[f][3] == t - 1) >= W_vars[t, p, a],
                                name=f'PlaneDestinationContinuity_{p}_{t}_{a}')

    # Define Continuity of Destination Airport for passengers (Constraint 15)
    for h in passengers.keys():
        for t in T:
            for a in set_of_airports:
                if t > 0:  # Exclude t=0
                    m.addConstr(Z_vars[t - 1, h, a] +
                                gp.quicksum(X_vars[flights[f], h] 
                                            for f in flights 
                                                if  flights[f][1] == a and flights[f][3] == t - 1) >= Z_vars[t, h, a],
                                name=f'PassengerDestinationContinuity_{h}_{t}_{a}')
                    
    m.update()
    print('Model updated with all constraints')
    # run the model
    m.optimize()               

    return m, X_vars, W_vars, Z_vars, Y_vars