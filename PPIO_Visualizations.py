'''
## PPIO Solution Visualizations

The script accepts the following parameters:
    -> X_vars: the values of the resulting X binary variables
    -> W_vars: the values of the resutling W binary variables
    -> Z_vars: the values of the resulting Z binary variables
    -> Y_vars: the values of the resulting Y binary variables
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


def extract_distribution_travel_times(passengers_list):
    travel_times = []

    for i in passengers_list.keys():
        z_1_vars = []
        # Iterate through the dictionary
        for key, gurobi_var in Z_vars.items():
            # Check if the value of the Gurobi variable is equal to 1
            if gurobi_var.X >= 0.5:
                z_1_vars.append(key)
        # extract all passenger h data
        passenger_vars_z = [var for var in z_1_vars if var[1] == i]

        first_word = passenger_vars_z[0][2]
        last_index = len(passenger_vars_z) - 1 - next(idx for idx, (_, _, word) in 
                                                      enumerate(reversed(passenger_vars_z)) if word == first_word)
        
        last_word = passenger_vars_z[-1][2]
        first_instance_index = next(idx for idx, (_, _, string) in 
                                    enumerate(passenger_vars_z) if string == last_word)
        
        time = passenger_vars_z[first_instance_index][0] - passenger_vars_z[last_index][0]
        travel_times.append(time)

    plt.hist(travel_times)
    plt.xlabel('Travel Times (t)')
    plt.ylabel('Frequeny')
    plt.title('Distribution of Passenger Travel Times')
    plt.show()

    return travel_times
        

# extract the iterinary for a passenger during T times

def extract_plane_initinary(p):
    # List to store variables with value 1
    w_1_vars = []

    # Iterate through the dictionary
    for key, gurobi_var in W_vars.items():
        # Check if the value of the Gurobi variable is equal to 1
        if gurobi_var.X >= 0.5:
            w_1_vars.append(key)

    # List to store variables with value 1
    y_1_vars = []

    # Iterate through the dictionary
    for key, gurobi_var in Y_vars.items():
        # Check if the value of the Gurobi variable is equal to 1
        if gurobi_var.X >= 0.5:
            y_1_vars.append(key)
    # extract all passenger p data
    passenger_vars_w = [var for var in w_1_vars if var[1] == p]
    passenger_vars_y = [var for var in y_1_vars if var[0] == p]

    events = {}
    # Process the first list
    for i in range(len(passenger_vars_w) - 1):
        start_time = passenger_vars_w[i][0]
        end_time = passenger_vars_w[i][0] + 1
        airport = passenger_vars_w[i][2]
        events[f'{airport}_{i}'] = {'start': start_time, 'end': end_time, 'label': airport}

    # Process the second list
    for passenger, flight_info in passenger_vars_y:
        start_airport, end_airport, start_time22, end_time22 = flight_info
        flight_label = f'{start_airport} -> {end_airport}'
        events[f'{flight_label}'] = {'start': start_time22, 'end': end_time22 + 1, 'label': f'{start_airport} -> {end_airport}'}


    # Create a dictionary to store the merged events
    merged_events = {}

    # Iterate through the events data
    for event_id, event_info in events.items():
        label = event_info['label']
        
        # Check if the label is already in the merged events dictionary
        if label in merged_events:
            # If yes, update the end time of the existing event
            merged_events[label]['end'] = event_info['end']
        else:
            # If not, add a new entry to the merged events dictionary
            merged_events[label] = {'start': event_info['start'], 'end': event_info['end'], 'label': label}

    # Print the merged events
    for label, event_info in merged_events.items():
        print(f"Event: {label}, Start: {event_info['start']}, End: {event_info['end']}")
    events = merged_events

    fig_1 = plt.figure(figsize = (15,2), facecolor='w',edgecolor='k')

    # Plot each interval on the timeline
    for event, data in merged_events.items():
        start = data['start']
        end = data['end']
        plt.plot([start, end], [0, 0], label=event, linewidth=8)

    # Add labels above the intervals with arrows
    for event, data in merged_events.items():
        start = data['start']
        end = data['end']
        label_x = (start + end) / 2  # Center the label
        label_y = 0.005  # Height above the timeline
        plt.annotate(event, xy=(label_x, label_y), xytext=(label_x, label_y + 0.02),
                    arrowprops=dict(facecolor='black', arrowstyle='wedge,tail_width=0.7', lw=1),
                    ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white'))

    # Customize the plot
    plt.yticks([])  # Hide y-axis ticks
    plt.xlabel('Time')
    plt.title(f'''Itinerary  for plane {p}''')
    plt.show()    

def create_map_flow(airports_list, routes_list, list_of_passengers, t):
    # create a complete map
    network_map = folium.Map(location=[39.8283, -98.5795], zoom_start=5)
    # Iterate through the nodes and add markers for each airport
    for node in airports_list:
        lat = float(airports_data.loc[airports_data['local_code'] == node]['latitude_deg'].values)
        lon = float(airports_data.loc[airports_data['local_code'] == node]['longitude_deg'].values)
        airport_icon = plugins.BeautifyIcon(icon='plane', border_color='red', text_color='red', icon_shape='marker')
        folium.Marker(location=[lat, lon], popup=node, icon=airport_icon).add_to(network_map)
    # Iterate through the edges and draw lines connecting airports
    for u, v in routes_list:
        lat1 = float(airports_data.loc[airports_data['local_code'] == u]['latitude_deg'].values)
        lon1 = float(airports_data.loc[airports_data['local_code'] == u]['longitude_deg'].values)
        lat2 = float(airports_data.loc[airports_data['local_code'] == v]['latitude_deg'].values)
        lon2 = float(airports_data.loc[airports_data['local_code'] == v]['longitude_deg'].values)
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color="blue", smooth_factor = 0.22, dash_array='10').add_to(network_map)

    # iterate through each passenger and extract position with some error at time t
    pass_icon = plugins.BeautifyIcon(icon='circle', border_color='black', text_color='red')

    for h in list_of_passengers.keys():
        data_h = extract_passenger_initinary(h)
        for key, value in data_h.items():
            if value['start'] <= t < value['end']:
                location = key
                break
            else: 
                location = None  # Return None if no associated key is found
        
        if len(location) == 3:
            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)
            # get location + geospatial error
            lat_h = float(airports_data.loc[airports_data['local_code'] == location]['latitude_deg'].values) + lat_offset
            long_h = float(airports_data.loc[airports_data['local_code'] == location]['longitude_deg'].values) + lon_offset
            folium.Marker(location=[lat_h, long_h ], popup=h).add_to(network_map)      

        else:
            a, b = location.split(' -> ')
            lat_a = float(airports_data.loc[airports_data['local_code'] == a]['latitude_deg'].values)
            long_a = float(airports_data.loc[airports_data['local_code'] == a]['longitude_deg'].values) 
            lat_b = float(airports_data.loc[airports_data['local_code'] == b]['latitude_deg'].values)
            long_b = float(airports_data.loc[airports_data['local_code'] == b]['longitude_deg'].values) 

            # Calculate the distance between points A and B
            distance = geodesic((lat_a, long_a), (lat_b, long_b)).meters

            # Define the percentage along the line where you want to place the marker (e.g., 50% for the midpoint)
            percentage_along_line = random.uniform(0.3, 0.7)

            # Interpolate coordinates along the line
            interpolated_lat = lat_a + percentage_along_line * (lat_b - lat_a)
            interpolated_lon = long_a + percentage_along_line * (long_b - long_a)

            folium.Marker([interpolated_lat, interpolated_lon], popup=h).add_to(network_map)

    return network_map


# extract the iterinary for a passenger during T times

def extract_passenger_initinary(h):
    # List to store variables with value 1
    z_1_vars = []

    # Iterate through the dictionary
    for key, gurobi_var in Z_vars.items():
        # Check if the value of the Gurobi variable is equal to 1
        if gurobi_var.X >= 0.5:
            z_1_vars.append(key)

    # List to store variables with value 1
    x_1_vars = []

    # Iterate through the dictionary
    for key, gurobi_var in X_vars.items():
        # Check if the value of the Gurobi variable is equal to 1
        if gurobi_var.X >= 0.5:
            x_1_vars.append(key)

    # extract all passenger h data
    passenger_vars_x = [var for var in x_1_vars if var[1] == h]
    passenger_vars_z = [var for var in z_1_vars if var[1] == h]

    events = {}
    # Process the first list
    for i in range(len(passenger_vars_z) - 1):
        start_time = passenger_vars_z[i][0]
        end_time = passenger_vars_z[i][0] + 1
        airport = passenger_vars_z[i][2]
        events[f'{airport}_{i}'] = {'start': start_time, 'end': end_time, 'label': airport}
    # Process the second list
    for flight_info, passenger in passenger_vars_x:
        start_airport, end_airport, start_time22, end_time22 = flight_info
        flight_label = f'{start_airport} -> {end_airport}'
        events[f'{flight_label}'] = {'start': start_time22, 'end': end_time22 + 1, 'label': f'{start_airport} -> {end_airport}'}
    # Create a dictionary to store the merged events
    merged_events = {}

    # Iterate through the events data
    for event_id, event_info in events.items():
        label = event_info['label']
        
        # Check if the label is already in the merged events dictionary
        if label in merged_events:
            # If yes, update the end time of the existing event
            merged_events[label]['end'] = event_info['end']
        else:
            # If not, add a new entry to the merged events dictionary
            merged_events[label] = {'start': event_info['start'], 'end': event_info['end'], 'label': label}

    return merged_events

def visualize_passenger_initinary(h):
    fig_1 = plt.figure(figsize = (15,2), facecolor='w',edgecolor='k')

    h_events = extract_passenger_initinary(h)

    # Plot each interval on the timeline
    for event, data in h_events.items():
        start = data['start']
        end = data['end']
        plt.plot([start, end], [0, 0], label=event, linewidth=8)

    # Add labels above the intervals with arrows
    for event, data in h_events.items():
        start = data['start']
        end = data['end']
        label_x = (start + end) / 2  # Center the label
        label_y = 0.005  # Height above the timeline
        plt.annotate(event, xy=(label_x, label_y), xytext=(label_x, label_y + 0.02),
                    arrowprops=dict(facecolor='black', arrowstyle='wedge,tail_width=0.7', lw=1),
                    ha='center', va='bottom', bbox=dict(boxstyle='round,pad=0.3', edgecolor='black', facecolor='white'))

    # assign the plane p to the center-most airport  (for label purposes)

    # Customize the plot
    plt.yticks([])  # Hide y-axis ticks
    plt.xlabel('Time')
    plt.title(f'''Itinerary  for Passenger {h}''')
    plt.show()    