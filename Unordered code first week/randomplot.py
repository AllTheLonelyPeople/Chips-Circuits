"""
path.py

Tom Kamstra, Izhar Hamer, Julia Linde

Finds the optimal paths between the chips
"""
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import random

import csv

# Open file with netlist
data = open("example_net2.csv")
reader = csv.reader(data)

# Create netlist
netlist = []

for net_1, net_2 in reader:
    net = (net_1, net_2)
    netlist.append(net)

# Open file with gates
gates = open("example_prit2.csv")
reader = csv.reader(gates)

# Create list for gate coordinates
gate_coordinates = []

for number, x, y in reader:
    if x != " x":
        x = int(x)
        y = int(y)
        coordinates = [x, y, 0]
        gate_coordinates.append(coordinates)

# Create dictionary of gate connections with corresponding shortest distance
distances = {}

for chip1, chip2 in netlist:
    if chip1 != "chip_a":
        gate_1 = int(chip1)
        gate_2 = int(chip2)
        
        # Create tuple for gates that have to be connected
        connected_gate = (gate_1, gate_2)
        
        coordinate_start = gate_coordinates[gate_1 - 1]
        coordinate_end = gate_coordinates[gate_2 - 1]
    
        x_coordinate_1 = int(coordinate_start[0])
        y_coordinate_1 = int(coordinate_start[1])

        x_coordinate_2 = int(coordinate_end[0])
        y_coordinate_2 = int(coordinate_end[1])
    
        # Calculate total shortest distance between gates
        total_dist = abs(x_coordinate_1 - x_coordinate_2) + abs(y_coordinate_1 - y_coordinate_2)

        distances.update({connected_gate: total_dist})

# Sort connections from smallest to largest distance in dictionary
distances = list(distances.items())
for max_number in range(len(distances)-1, -1, -1):
    swapped = False
    for count in range(max_number):
        if distances[count][1] > distances[count + 1][1]:
            distances[count], distances[count + 1] = distances[count + 1], distances[count]
            swapped = True
    if not swapped:
        break
        
random.shuffle(distances)

# Create dictionary of wires with connected gates
gate_connections = {}
count = 0

# Connect gates with eachother, starting with smallest distance
for chips in distances:
    gate_start = int(chips[0][0])
    gate_end = int(chips[0][1])
    
    connected_gate = (gate_start, gate_end)

    coordinate = gate_coordinates[gate_start - 1]
    coordinate_end = gate_coordinates[gate_end - 1]
    
    print("COORDINATES")
    print(coordinate)
    print(coordinate_end)

    x_coordinate_start = int(coordinate[0])
    y_coordinate_start = int(coordinate[1])
    z_coordinate_start = int(coordinate[2])

    x_coordinate_end = int(coordinate_end[0])
    y_coordinate_end = int(coordinate_end[1])
    z_coordinate_end = int(coordinate_end[2])

    # Create list for wire coordinates
    wires = []

    while coordinate != coordinate_end:
        # Determine direction in which wire has to move
        if x_coordinate_start < x_coordinate_end:
            step_x = 1
        elif x_coordinate_start > x_coordinate_end:
            step_x = -1
    
        if y_coordinate_start < y_coordinate_end:
            step_y = 1
        elif y_coordinate_start > y_coordinate_end:
            step_y = -1

        # Append start coordinate to wire
        wires.append(coordinate)
        
        # Loop until x-coordinate from start gate equals x-coordinate from end gate
        while x_coordinate_start != x_coordinate_end:
            x_coordinate_start = x_coordinate_start + step_x
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            # Check for other gates or other wires
            if gate_connections:
                for key in gate_connections:
                    selected_wires = gate_connections[key]
                    if coordinate in selected_wires or coordinate in gate_coordinates:
                        if coordinate != coordinate_end:
                            x_coordinate_start = x_coordinate_start - step_x
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            z_coordinate_start = z_coordinate_start + 1
                            #checken of na deze stap geen gate zit
                            break
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                if gate_connections:
                    for key in gate_connections:
                        selected_wires = gate_connections[key]
                        if coordinate in selected_wires or coordinate in gate_coordinates:
                            if coordinate != coordinate_end:
                                z_coordinate_start = z_coordinate_start - 1
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                y_coordinate_start = y_coordinate_start + step_y
                                #checken of na deze stap geen gate zit
                                break
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        for key in gate_connections:
                            selected_wires = gate_connections[key]
                            if coordinate in selected_wires or coordinate in gate_coordinates:
                                if coordinate != coordinate_end:
                                    y_coordinate_start = y_coordinate_start - step_y - step_y
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    break
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            for key in gate_connections:
                                selected_wires = gate_connections[key]
                                if coordinate in selected_wires or coordinate in gate_coordinates:
                                    if coordinate != coordinate_end:
                                        y_coordinate_start = y_coordinate_start + step_y
                                        # z kan nu niet meerdere stappen omhoog/omlaag
                                        x_coordinate_start = x_coordinate_start - step_x
                                        #checken of na deze stap geen gate zit
                                        break
                        elif coordinate in gate_coordinates and coordinate != coordinate_end:
                            y_coordinate_start = y_coordinate_start + step_y
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            x_coordinate_start = x_coordinate_start - step_x
                            #checken of na deze stap geen gate zit
                    elif coordinate in gate_coordinates and coordinate != coordinate_end:
                        y_coordinate_start = y_coordinate_start - step_y - step_y
                        # z kan nu niet meerdere stappen omhoog/omlaag
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            for key in gate_connections:
                                selected_wires = gate_connections[key]
                                if coordinate in selected_wires or coordinate in gate_coordinates:
                                    if coordinate != coordinate_end:
                                        y_coordinate_start = y_coordinate_start + step_y
                                        # z kan nu niet meerdere stappen omhoog/omlaag
                                        x_coordinate_start = x_coordinate_start - step_x
                                        #checken of na deze stap geen gate zit
                                        break
                        elif coordinate in gate_coordinates and coordinate != coordinate_end:
                            y_coordinate_start = y_coordinate_start + step_y
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            x_coordinate_start = x_coordinate_start - step_x
                            #checken of na deze stap geen gate zit
                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                    z_coordinate_start = z_coordinate_start - 1
                    # z kan nu niet meerdere stappen omhoog/omlaag
                    y_coordinate_start = y_coordinate_start + step_y
                    #checken of na deze stap geen gate zit
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        for key in gate_connections:
                            selected_wires = gate_connections[key]
                            if coordinate in selected_wires or coordinate in gate_coordinates:
                                if coordinate != coordinate_end:
                                    y_coordinate_start = y_coordinate_start + step_y
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    x_coordinate_start = x_coordinate_start - step_x
                                    #checken of na deze stap geen gate zit
                                    break
                    elif coordinate in gate_coordinates and coordinate != coordinate_end:
                        y_coordinate_start = y_coordinate_start + step_y
                        # z kan nu niet meerdere stappen omhoog/omlaag
                        x_coordinate_start = x_coordinate_start - step_x
                        #checken of na deze stap geen gate zit
            elif coordinate in gate_coordinates and coordinate != coordinate_end:
                x_coordinate_start = x_coordinate_start - step_x
                # z kan nu niet meerdere stappen omhoog/omlaag
                z_coordinate_start = z_coordinate_start + 1
                #checken of na deze stap geen gate zit
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                if gate_connections:
                    for key in gate_connections:
                        selected_wires = gate_connections[key]
                        if coordinate in selected_wires or coordinate in gate_coordinates:
                            if coordinate != coordinate_end:
                                z_coordinate_start = z_coordinate_start - 1
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                y_coordinate_start = y_coordinate_start + step_y
                                #checken of na deze stap geen gate zit
                                break
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        for key in gate_connections:
                            selected_wires = gate_connections[key]
                            if coordinate in selected_wires or coordinate in gate_coordinates:
                                if coordinate != coordinate_end:
                                    y_coordinate_start = y_coordinate_start - step_y - step_y
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    break
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            for key in gate_connections:
                                selected_wires = gate_connections[key]
                                if coordinate in selected_wires or coordinate in gate_coordinates:
                                    if coordinate != coordinate_end:
                                        y_coordinate_start = y_coordinate_start + step_y
                                        # z kan nu niet meerdere stappen omhoog/omlaag
                                        x_coordinate_start = x_coordinate_start - step_x
                                        #checken of na deze stap geen gate zit
                                        break
                        elif coordinate in gate_coordinates and coordinate != coordinate_end:
                            y_coordinate_start = y_coordinate_start + step_y
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            x_coordinate_start = x_coordinate_start - step_x
                            #checken of na deze stap geen gate zit
                    elif coordinate in gate_coordinates and coordinate != coordinate_end:
                        y_coordinate_start = y_coordinate_start - step_y - step_y
                        # z kan nu niet meerdere stappen omhoog/omlaag
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            for key in gate_connections:
                                selected_wires = gate_connections[key]
                                if coordinate in selected_wires or coordinate in gate_coordinates:
                                    if coordinate != coordinate_end:
                                        y_coordinate_start = y_coordinate_start + step_y
                                        # z kan nu niet meerdere stappen omhoog/omlaag
                                        x_coordinate_start = x_coordinate_start - step_x
                                        #checken of na deze stap geen gate zit
                                        break
                        elif coordinate in gate_coordinates and coordinate != coordinate_end:
                            y_coordinate_start = y_coordinate_start + step_y
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            x_coordinate_start = x_coordinate_start - step_x
                            #checken of na deze stap geen gate zit
                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                    z_coordinate_start = z_coordinate_start - 1
                    # z kan nu niet meerdere stappen omhoog/omlaag
                    y_coordinate_start = y_coordinate_start + step_y
                    #checken of na deze stap geen gate zit
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        for key in gate_connections:
                            selected_wires = gate_connections[key]
                            if coordinate in selected_wires or coordinate in gate_coordinates:
                                if coordinate != coordinate_end:
                                    y_coordinate_start = y_coordinate_start + step_y
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    x_coordinate_start = x_coordinate_start - step_x
                                    #checken of na deze stap geen gate zit
                                    break
                    elif coordinate in gate_coordinates and coordinate != coordinate_end:
                        y_coordinate_start = y_coordinate_start + step_y
                        # z kan nu niet meerdere stappen omhoog/omlaag
                        x_coordinate_start = x_coordinate_start - step_x
                        #checken of na deze stap geen gate zit
            
            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
            wires.append(coordinate)
            print(coordinate)
            
            if y_coordinate_start < y_coordinate_end:
                step_y = 1
            elif y_coordinate_start > y_coordinate_end:
                step_y = -1
                    
            if x_coordinate_start == x_coordinate_end and y_coordinate_start == y_coordinate_end:
                while z_coordinate_start != z_coordinate_end:
                    z_coordinate_start = z_coordinate_start - 1
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        for key in gate_connections:
                            selected_wires = gate_connections[key]
                            if coordinate in selected_wires or coordinate in gate_coordinates:
                                if coordinate != coordinate_end:
                                    z_coordinate_start = z_coordinate_start + 1
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start + step_y
                                    #checken of na deze stap geen gate zit
                                    break
                                    # moet ook uit while loop breken!
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            for key in gate_connections:
                                selected_wires = gate_connections[key]
                                if coordinate in selected_wires or coordinate in gate_coordinates:
                                    if coordinate != coordinate_end:
                                        y_coordinate_start = y_coordinate_start - step_y
                                        # z kan nu niet meerdere stappen omhoog/omlaag
                                        x_coordinate_start = x_coordinate_start + step_x
                                        #checken of na deze stap geen gate zit
                                        break
                                        # moet ook uit while loop breken!
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if gate_connections:
                                for key in gate_connections:
                                    selected_wires = gate_connections[key]
                                    if coordinate in selected_wires or coordinate in gate_coordinates:
                                        if coordinate != coordinate_end:
                                            x_coordinate_start = x_coordinate_start - step_x - step_x
                                            # z kan nu niet meerdere stappen omhoog/omlaag
                                            break
                                            # moet ook uit while loop breken!
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                            elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                x_coordinate_start = x_coordinate_start - step_x - step_x
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                        elif coordinate in gate_coordinates and coordinate != coordinate_end:
                            y_coordinate_start = y_coordinate_start - step_y
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            x_coordinate_start = x_coordinate_start + step_x
                            #checken of na deze stap geen gate zit
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if gate_connections:
                                for key in gate_connections:
                                    selected_wires = gate_connections[key]
                                    if coordinate in selected_wires or coordinate in gate_coordinates:
                                        if coordinate != coordinate_end:
                                            x_coordinate_start = x_coordinate_start - step_x - step_x
                                            # z kan nu niet meerdere stappen omhoog/omlaag
                                            break
                                            # moet ook uit while loop breken!
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                            elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                x_coordinate_start = x_coordinate_start - step_x - step_x
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                    elif coordinate in gate_coordinates and coordinate != coordinate_end:
                        z_coordinate_start = z_coordinate_start + 1
                        # z kan nu niet meerdere stappen omhoog/omlaag
                        y_coordinate_start = y_coordinate_start + step_y
                        #checken of na deze stap geen gate zit
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            for key in gate_connections:
                                selected_wires = gate_connections[key]
                                if coordinate in selected_wires or coordinate in gate_coordinates:
                                    if coordinate != coordinate_end:
                                        y_coordinate_start = y_coordinate_start - step_y
                                        # z kan nu niet meerdere stappen omhoog/omlaag
                                        x_coordinate_start = x_coordinate_start + step_x
                                        #checken of na deze stap geen gate zit
                                        break
                                        # moet ook uit while loop breken!
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if gate_connections:
                                for key in gate_connections:
                                    selected_wires = gate_connections[key]
                                    if coordinate in selected_wires or coordinate in gate_coordinates:
                                        if coordinate != coordinate_end:
                                            x_coordinate_start = x_coordinate_start - step_x - step_x
                                            # z kan nu niet meerdere stappen omhoog/omlaag
                                            break
                                            # moet ook uit while loop breken!
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                            elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                x_coordinate_start = x_coordinate_start - step_x - step_x
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                        elif coordinate in gate_coordinates and coordinate != coordinate_end:
                            y_coordinate_start = y_coordinate_start - step_y
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            x_coordinate_start = x_coordinate_start + step_x
                            #checken of na deze stap geen gate zit
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if gate_connections:
                                for key in gate_connections:
                                    selected_wires = gate_connections[key]
                                    if coordinate in selected_wires or coordinate in gate_coordinates:
                                        if coordinate != coordinate_end:
                                            x_coordinate_start = x_coordinate_start - step_x - step_x
                                            # z kan nu niet meerdere stappen omhoog/omlaag
                                            break
                                            # moet ook uit while loop breken!
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                            elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                x_coordinate_start = x_coordinate_start - step_x - step_x
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    for key in gate_connections:
                                        selected_wires = gate_connections[key]
                                        if coordinate in selected_wires or coordinate in gate_coordinates:
                                            if coordinate != coordinate_end:
                                                x_coordinate_start = x_coordinate_start + step_x
                                                # z kan nu niet meerdere stappen omhoog/omlaag
                                                y_coordinate_start = y_coordinate_start - step_y
                                                #checken of na deze stap geen gate zit
                                                break
                                                # moet ook uit while loop breken!
                                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                    x_coordinate_start = x_coordinate_start + step_x
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    y_coordinate_start = y_coordinate_start - step_y
                                    #checken of na deze stap geen gate zit
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    wires.append(coordinate)
                    
        if y_coordinate_start < y_coordinate_end:
            step_y = 1
        elif y_coordinate_start > y_coordinate_end:
            step_y = -1

        while y_coordinate_start != y_coordinate_end:
           y_coordinate_start = y_coordinate_start + step_y
           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           # Check for other gates or other wires
           if gate_connections:
               for key in gate_connections:
                   selected_wires = gate_connections[key]
                   if coordinate in selected_wires or coordinate in gate_coordinates:
                       if coordinate != coordinate_end:
                           y_coordinate_start = y_coordinate_start - step_y
                           # z kan nu niet meerdere stappen omhoog/omlaag
                           z_coordinate_start = z_coordinate_start + 1
                           #checken of na deze stap geen gate zit
                           break
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               if gate_connections:
                   for key in gate_connections:
                       selected_wires = gate_connections[key]
                       if coordinate in selected_wires or coordinate in gate_coordinates:
                           if coordinate != coordinate_end:
                               z_coordinate_start = z_coordinate_start - 1
                               # z kan nu niet meerdere stappen omhoog/omlaag
                               x_coordinate_start = x_coordinate_start + step_x
                               #checken of na deze stap geen gate zit
                               break
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   if gate_connections:
                       for key in gate_connections:
                           selected_wires = gate_connections[key]
                           if coordinate in selected_wires or coordinate in gate_coordinates:
                               if coordinate != coordinate_end:
                                   x_coordinate_start = x_coordinate_start - step_x - step_x
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   break
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates:
                                   if coordinate != coordinate_end:
                                       x_coordinate_start = x_coordinate_start + step_x
                                       # z kan nu niet meerdere stappen omhoog/omlaag
                                       y_coordinate_start = y_coordinate_start - step_y
                                       #checken of na deze stap geen gate zit
                                       break
                       elif coordinate in gate_coordinates and coordinate != coordinate_end:
                           x_coordinate_start = x_coordinate_start + step_x
                           # z kan nu niet meerdere stappen omhoog/omlaag
                           y_coordinate_start = y_coordinate_start - step_y
                           #checken of na deze stap geen gate zit
                   elif coordinate in gate_coordinates and coordinate != coordinate_end:
                       x_coordinate_start = x_coordinate_start - step_x - step_x
                       # z kan nu niet meerdere stappen omhoog/omlaag
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates:
                                   if coordinate != coordinate_end:
                                       x_coordinate_start = x_coordinate_start + step_x
                                       # z kan nu niet meerdere stappen omhoog/omlaag
                                       y_coordinate_start = y_coordinate_start - step_y
                                       #checken of na deze stap geen gate zit
                                       break
                       elif coordinate in gate_coordinates and coordinate != coordinate_end:
                           x_coordinate_start = x_coordinate_start + step_x
                           # z kan nu niet meerdere stappen omhoog/omlaag
                           y_coordinate_start = y_coordinate_start - step_y
                           #checken of na deze stap geen gate zit
               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                   z_coordinate_start = z_coordinate_start - 1
                   # z kan nu niet meerdere stappen omhoog/omlaag
                   x_coordinate_start = x_coordinate_start + step_x
                   #checken of na deze stap geen gate zit
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   if gate_connections:
                       for key in gate_connections:
                           selected_wires = gate_connections[key]
                           if coordinate in selected_wires or coordinate in gate_coordinates:
                               if coordinate != coordinate_end:
                                   x_coordinate_start = x_coordinate_start + step_x
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   y_coordinate_start = y_coordinate_start - step_y
                                   #checken of na deze stap geen gate zit
                                   break
                   elif coordinate in gate_coordinates and coordinate != coordinate_end:
                       x_coordinate_start = x_coordinate_start + step_x
                       # z kan nu niet meerdere stappen omhoog/omlaag
                       y_coordinate_start = y_coordinate_start - step_y
                       #checken of na deze stap geen gate zit
           elif coordinate in gate_coordinates and coordinate != coordinate_end:
               y_coordinate_start = y_coordinate_start - step_y
               # z kan nu niet meerdere stappen omhoog/omlaag
               z_coordinate_start = z_coordinate_start + 1
               #checken of na deze stap geen gate zit
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               if gate_connections:
                   for key in gate_connections:
                       selected_wires = gate_connections[key]
                       if coordinate in selected_wires or coordinate in gate_coordinates:
                           if coordinate != coordinate_end:
                               z_coordinate_start = z_coordinate_start - 1
                               # z kan nu niet meerdere stappen omhoog/omlaag
                               x_coordinate_start = x_coordinate_start + step_x
                               #checken of na deze stap geen gate zit
                               break
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   if gate_connections:
                       for key in gate_connections:
                           selected_wires = gate_connections[key]
                           if coordinate in selected_wires or coordinate in gate_coordinates:
                               if coordinate != coordinate_end:
                                   x_coordinate_start = x_coordinate_start - step_x - step_x
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   break
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates:
                                   if coordinate != coordinate_end:
                                       x_coordinate_start = x_coordinate_start + step_x
                                       # z kan nu niet meerdere stappen omhoog/omlaag
                                       y_coordinate_start = y_coordinate_start - step_y
                                       #checken of na deze stap geen gate zit
                                       break
                       elif coordinate in gate_coordinates and coordinate != coordinate_end:
                           x_coordinate_start = x_coordinate_start + step_x
                           # z kan nu niet meerdere stappen omhoog/omlaag
                           y_coordinate_start = y_coordinate_start - step_y
                           #checken of na deze stap geen gate zit
                   elif coordinate in gate_coordinates and coordinate != coordinate_end:
                       x_coordinate_start = x_coordinate_start - step_x - step_x
                       # z kan nu niet meerdere stappen omhoog/omlaag
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates:
                                   if coordinate != coordinate_end:
                                       x_coordinate_start = x_coordinate_start + step_x
                                       # z kan nu niet meerdere stappen omhoog/omlaag
                                       y_coordinate_start = y_coordinate_start - step_y
                                       #checken of na deze stap geen gate zit
                                       break
                       elif coordinate in gate_coordinates and coordinate != coordinate_end:
                           x_coordinate_start = x_coordinate_start + step_x
                           # z kan nu niet meerdere stappen omhoog/omlaag
                           y_coordinate_start = y_coordinate_start - step_y
                           #checken of na deze stap geen gate zit
               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                   z_coordinate_start = z_coordinate_start - 1
                   # z kan nu niet meerdere stappen omhoog/omlaag
                   x_coordinate_start = x_coordinate_start + step_x
                   #checken of na deze stap geen gate zit
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   if gate_connections:
                       for key in gate_connections:
                           selected_wires = gate_connections[key]
                           if coordinate in selected_wires or coordinate in gate_coordinates:
                               if coordinate != coordinate_end:
                                   x_coordinate_start = x_coordinate_start + step_x
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   y_coordinate_start = y_coordinate_start - step_y
                                   #checken of na deze stap geen gate zit
                                   break
                   elif coordinate in gate_coordinates and coordinate != coordinate_end:
                       x_coordinate_start = x_coordinate_start + step_x
                       # z kan nu niet meerdere stappen omhoog/omlaag
                       y_coordinate_start = y_coordinate_start - step_y
                       #checken of na deze stap geen gate zit

           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           wires.append(coordinate)
           print(coordinate)
           
           if y_coordinate_start < y_coordinate_end:
               step_y = 1
           elif y_coordinate_start > y_coordinate_end:
               step_y = -1
           
           if x_coordinate_start == x_coordinate_end and y_coordinate_start == y_coordinate_end:
               while z_coordinate_start != z_coordinate_end:
                   z_coordinate_start = z_coordinate_start - 1
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   if gate_connections:
                       for key in gate_connections:
                           selected_wires = gate_connections[key]
                           if coordinate in selected_wires or coordinate in gate_coordinates:
                               if coordinate != coordinate_end:
                                   z_coordinate_start = z_coordinate_start + 1
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start + step_x
                                   #checken of na deze stap geen gate zit
                                   break
                                   # moet ook uit while loop breken!
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates:
                                   if coordinate != coordinate_end:
                                       x_coordinate_start = x_coordinate_start - step_x
                                       # z kan nu niet meerdere stappen omhoog/omlaag
                                       y_coordinate_start = y_coordinate_start + step_y
                                       #checken of na deze stap geen gate zit
                                       break
                                       # moet ook uit while loop breken!
                           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                           if gate_connections:
                               for key in gate_connections:
                                   selected_wires = gate_connections[key]
                                   if coordinate in selected_wires or coordinate in gate_coordinates:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                           elif coordinate in gate_coordinates and coordinate != coordinate_end:
                               y_coordinate_start = y_coordinate_start - step_y - step_y
                               # z kan nu niet meerdere stappen omhoog/omlaag
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                       elif coordinate in gate_coordinates and coordinate != coordinate_end:
                           x_coordinate_start = x_coordinate_start - step_x
                           # z kan nu niet meerdere stappen omhoog/omlaag
                           y_coordinate_start = y_coordinate_start + step_y
                           #checken of na deze stap geen gate zit
                           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                           if gate_connections:
                               for key in gate_connections:
                                   selected_wires = gate_connections[key]
                                   if coordinate in selected_wires or coordinate in gate_coordinates:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                           elif coordinate in gate_coordinates and coordinate != coordinate_end:
                               y_coordinate_start = y_coordinate_start - step_y - step_y
                               # z kan nu niet meerdere stappen omhoog/omlaag
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                   elif coordinate in gate_coordinates and coordinate != coordinate_end:
                       z_coordinate_start = z_coordinate_start + 1
                       # z kan nu niet meerdere stappen omhoog/omlaag
                       x_coordinate_start = x_coordinate_start + step_x
                       #checken of na deze stap geen gate zit
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates:
                                   if coordinate != coordinate_end:
                                       x_coordinate_start = x_coordinate_start - step_x
                                       # z kan nu niet meerdere stappen omhoog/omlaag
                                       y_coordinate_start = y_coordinate_start + step_y
                                       #checken of na deze stap geen gate zit
                                       break
                                       # moet ook uit while loop breken!
                           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                           if gate_connections:
                               for key in gate_connections:
                                   selected_wires = gate_connections[key]
                                   if coordinate in selected_wires or coordinate in gate_coordinates:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                           elif coordinate in gate_coordinates and coordinate != coordinate_end:
                               y_coordinate_start = y_coordinate_start - step_y - step_y
                               # z kan nu niet meerdere stappen omhoog/omlaag
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                       elif coordinate in gate_coordinates and coordinate != coordinate_end:
                           x_coordinate_start = x_coordinate_start - step_x
                           # z kan nu niet meerdere stappen omhoog/omlaag
                           y_coordinate_start = y_coordinate_start + step_y
                           #checken of na deze stap geen gate zit
                           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                           if gate_connections:
                               for key in gate_connections:
                                   selected_wires = gate_connections[key]
                                   if coordinate in selected_wires or coordinate in gate_coordinates:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                           elif coordinate in gate_coordinates and coordinate != coordinate_end:
                               y_coordinate_start = y_coordinate_start - step_y - step_y
                               # z kan nu niet meerdere stappen omhoog/omlaag
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates:
                                           if coordinate != coordinate_end:
                                               y_coordinate_start = y_coordinate_start + step_y
                                               # z kan nu niet meerdere stappen omhoog/omlaag
                                               x_coordinate_start = x_coordinate_start - step_x
                                               #checken of na deze stap geen gate zit
                                               break
                                               # moet ook uit while loop breken!
                               elif coordinate in gate_coordinates and coordinate != coordinate_end:
                                   y_coordinate_start = y_coordinate_start + step_y
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   x_coordinate_start = x_coordinate_start - step_x
                                   #checken of na deze stap geen gate zit
                   coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                   wires.append(coordinate)
        # test
        # if len(wires) > 50:
#             break
    count += 1         
    gate_connections.update({connected_gate: wires})
    # if count > 27:
#         break
print(gate_connections)
print("JOEJOE")
# print(gate_connections[(17,10)])

length = 0

for key in gate_connections:
    wire = gate_connections[key]
    length = length + len(wire)
    
print("TOTAL LENGTH")
print(length)


def make_grid(layers, size):
    for i in range(layers): 
        GridX = np.linspace(0, size, (size + 1))
        GridY = np.linspace(0, size, (size + 1))
        X, Y = np.meshgrid(GridX, GridY)
        Z = (np.sin(np.sqrt(X ** 2 + Y ** 2)) * 0) + i
        # Plot grid
        # ax.plot_wireframe(X, Y, Z, lw=0.5,  color='grey')
    #configure axes
    ax.set_zlim3d(0, layers)
    ax.set_xlim3d(0, size)
    ax.set_ylim3d(0, size)

# Enter coordinates as list with: [X, Y, Z]
def draw_line(crdFrom, crdTo, colour):  
    Xline = [crdFrom[0], crdTo[0]]
    Yline = [crdFrom[1], crdTo[1]]
    Zline = [crdFrom[2], crdTo[2]]
    # Draw line
    ax.plot(Xline, Yline, Zline,lw=2,  color=colour, ms=12)

def set_gate(crd):
    PointX = [crd[0]]
    PointY = [crd[1]]
    PointZ = [crd[2]]
    # Plot points
    ax.plot(PointX, PointY, PointZ, ls="None", marker="o", color='red')


fig = plt.figure()
ax = plt.axes(projection="3d")

make_grid(8, 16)
# plt.pause(3)
for gate_coordinate in gate_coordinates: 
    set_gate(gate_coordinate)
    plt.pause(0.03)

allConnections = []
colours = ['b','lightgreen','cyan','m','yellow','k', 'pink']
colourcounter = 0
for keys in gate_connections:
    allConnections = gate_connections[keys]
    allconnectionlist = []
    for listconnection in allConnections: 
        allconnectionlist.append(listconnection)
    if colourcounter < 6:
        colourcounter += 1
    else: 
        colourcounter = 0
    for i in range(len(allconnectionlist)):
        try:
            print("LineFromTo", allconnectionlist[i],  allconnectionlist[i + 1], colours[colourcounter]  )
            draw_line(allconnectionlist[i], allconnectionlist[i+1], colours[colourcounter] )
            plt.pause(0.000001)
        except: 
            break

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()