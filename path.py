"""
path.py
Tom Kamstra, Izhar Hamer, Julia Linde
Finds the optimal paths between the chips
"""

from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from code.classes import classes as classs
import copy
from functions import *

import csv

# Create netlist by loading file in class
netlist = classs.Netlist("data/netlist_2.csv").netlist

# Create list for gate coordinates
gate_coordinates = classs.Gate_coordinate("data/pritn_1.csv").gate_coordinates
print(gate_coordinates)

# Create dictionary of gate connections with corresponding shortest distance
distances = {}

for item in netlist:
    gate_start = int(item.gate_1)
    gate_end = int(item.gate_2)
    
    # Create tuple for gates that have to be connected
    connected_gate = (gate_start, gate_end)
    
    coordinate_start = gate_coordinates[gate_start - 1]
    coordinate_end = gate_coordinates[gate_end - 1]

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

# Create dictionary of wires with connected gates
gate_connections = {}
count = 0

# Saves all wires
allwires = []
print("DISTT")
print(distances)


# Connect gates with eachother, starting with smallest distance
for chips in distances:
    gate_start = int(chips[0][0])
    gate_end = int(chips[0][1])
    
    connected_gate = (gate_start, gate_end)

    coordinate_begin = gate_coordinates[gate_start - 1]
    coordinate_end = gate_coordinates[gate_end - 1]
    
    print("COORDINATES")
    print(coordinate_begin)
    print(coordinate_end)

    x_coordinate_start = int(coordinate_begin[0])
    y_coordinate_start = int(coordinate_begin[1])
    z_coordinate_start = int(coordinate_begin[2])

    x_coordinate_end = int(coordinate_end[0])
    y_coordinate_end = int(coordinate_end[1])
    z_coordinate_end = int(coordinate_end[2])

    # Create list for wire coordinates
    wires = []

    # Check whether wire can be made in at least one direction
    x_coordinate_startcheck = x_coordinate_start + 1
    coordinate_1 = [x_coordinate_startcheck, y_coordinate_start, z_coordinate_start]
    x_coordinate_startcheck2 = x_coordinate_start - 1
    coordinate_2 = [x_coordinate_startcheck2, y_coordinate_start, z_coordinate_start]
    y_coordinate_startcheck = y_coordinate_start + 1
    coordinate_3 = [x_coordinate_start, y_coordinate_startcheck, z_coordinate_start]
    y_coordinate_startcheck2 = y_coordinate_start - 1
    coordinate_4 = [x_coordinate_start, y_coordinate_startcheck2, z_coordinate_start]
    z_coordinate_startcheck = z_coordinate_start + 1
    coordinate_5 = [x_coordinate_start, y_coordinate_start, z_coordinate_startcheck]


    coordinate_check = [coordinate_1, coordinate_2, coordinate_3, coordinate_4, coordinate_5]


    all_coordinates = []
    for coo in allwires:
        all_coordinates.append(coo.get_coordinate())


    result = all(elem in all_coordinates for elem in coordinate_check)

    if result:
        for coor in coordinate_check:
            for item_start in allwires:
                if item_start.coordinate == coor and item_start.net[0] != gate_start and item_start.net[1] != gate_start:
                    # Switch order of gates
                    end_gate = item_start.net[0]
                    start_gate = item_start.net[1]
                    distances.append(((start_gate, end_gate), 2))
                    
                    print(gate_connections)
                    # Delete wire from gate connections dictionary
                    try:
                        del gate_connections[item_start.net]
                    except:
                        del gate_connections[(start_gate, end_gate)]

                    print("This is deleted")
                    print(item_start.net)
                    # Delete blocking wire
                    for j, item2_start in enumerate(allwires):
                        if item2_start.net == item_start.net:
                            wire = classs.Wire([0, 0, 0], (0, 0))
                            allwires[j] = wire
                    break
    print("COUNT")
    print(count)
    
    # Create switch variable to switch start moving direction
    if count > len(netlist)+5:
        # Reconnect deleted wires in switched direction
        switch_variable = 1
    else:
        switch_variable = 0
    
    # Overwrite coordinate but save coordinate_begin in different variable        
    coordinate = coordinate_begin
    
    while coordinate != coordinate_end:
        # Determine direction in which wire has to move by step size
        steps = create_steps(x_coordinate_start, x_coordinate_end, y_coordinate_start, y_coordinate_end)
        
        step_x = steps[0]
        step_y = steps[1]

        # Append start coordinate to wire
        wires.append(coordinate)
        print(coordinate)
        wire = classs.Wire(coordinate, connected_gate)
        allwires.append(wire)
        
        if switch_variable == 0:
            # Loop until x-coordinate from start gate equals x-coordinate from end gate
            while x_coordinate_start != x_coordinate_end:
                x_coordinate_start = x_coordinate_start + step_x
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                # Check for other gates or other wires
                if gate_connections:
                    x_z_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, z_coordinate_start, 1)
                    x_coordinate_start = x_z_coor[0]
                    z_coordinate_start = x_z_coor[1]
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        z_y_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, 1, y_coordinate_start, step_y)
                        z_coordinate_start = z_y_coor[0]
                        y_coordinate_start = z_y_coor[1]
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            y_y_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, y_coordinate_start, (-step_y))
                            y_coordinate_start = y_y_coor[1]
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if gate_connections:
                                y_x_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, (-step_y), x_coordinate_start, (-step_x))
                                y_coordinate_start = y_x_coor[0]
                                x_coordinate_start = y_x_coor[1]
                elif coordinate in gate_coordinates and coordinate != coordinate_end:
                    x_coordinate_start = x_coordinate_start - step_x
                    # z kan nu niet meerdere stappen omhoog/omlaag
                    z_coordinate_start = z_coordinate_start + 1
                    #checken of na deze stap geen gate zit
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if coordinate in gate_coordinates and coordinate != coordinate_end:
                        z_coordinate_start = z_coordinate_start - 1
                        y_coordinate_start = y_coordinate_start + step_y
                        #checken of na deze stap geen gate zit
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]  
                        if coordinate in gate_coordinates and coordinate != coordinate_end:
                            y_coordinate_start = y_coordinate_start - step_y - step_y
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if coordinate in gate_coordinates and coordinate != coordinate_end:
                                y_coordinate_start = y_coordinate_start + step_y
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                x_coordinate_start = x_coordinate_start - step_x
                                #checken of na deze stap geen gate zit
        
                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                wires.append(coordinate)
                print(coordinate)
                wire = classs.Wire(coordinate, connected_gate)
                allwires.append(wire)
            
            if y_coordinate_start < y_coordinate_end:
                step_y = 1
            elif y_coordinate_start > y_coordinate_end:
                step_y = -1
                    
            if x_coordinate_start == x_coordinate_end and y_coordinate_start == y_coordinate_end:
                while z_coordinate_start != z_coordinate_end:
                    z_coordinate_start = z_coordinate_start - 1
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    if gate_connections:
                        z_y_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, z_coordinate_start, -1, y_coordinate_start, step_y)
                        z_coordinate_start = z_y_coor[0]
                        y_coordinate_start = z_y_coor[1]
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if gate_connections:
                            y_x_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, x_coordinate_start, step_x)
                            y_coordinate_start = y_x_coor[0]
                            x_coordinate_start = y_x_coor[1]
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if gate_connections:
                                x_x_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, step_x, x_coordinate_start, (-step_x))
                                x_coordinate_start = x_x_coor[1]
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if gate_connections:
                                    x_y_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, x_coordinate_start, (-step_x), y_coordinate_start, (-step_y))
                                    x_coordinate_start = x_y_coor[0]
                                    y_coordinate_start = x_y_coor[1]
                    elif coordinate in gate_coordinates and coordinate != coordinate_end:
                        z_coordinate_start = z_coordinate_start + 1
                        # z kan nu niet meerdere stappen omhoog/omlaag
                        y_coordinate_start = y_coordinate_start + step_y
                        #checken of na deze stap geen gate zit
                        coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                        if coordinate in gate_coordinates and coordinate != coordinate_end:
                            x_coordinate_start = x_coordinate_start + step_x
                            # z kan nu niet meerdere stappen omhoog/omlaag
                            y_coordinate_start = y_coordinate_start - step_y
                            #checken of na deze stap geen gate zit
                            coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                            if coordinate in gate_coordinates and coordinate != coordinate_end:
                                x_coordinate_start = x_coordinate_start - step_x - step_x
                                # z kan nu niet meerdere stappen omhoog/omlaag
                                coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                                if coordinate in gate_coordinates and coordinate != coordinate_end:
                                    y_coordinate_start = y_coordinate_start - step_y
                                    # z kan nu niet meerdere stappen omhoog/omlaag
                                    x_coordinate_start = x_coordinate_start + step_x
                            
                    coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                    wires.append(coordinate)
                    print(coordinate)
                    wire = classs.Wire(coordinate, connected_gate)
                    allwires.append(wire)
                    
                    
        if y_coordinate_start < y_coordinate_end:
            step_y = 1
        elif y_coordinate_start > y_coordinate_end:
            step_y = -1

        while y_coordinate_start != y_coordinate_end:
           y_coordinate_start = y_coordinate_start + step_y
           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           # Check for other gates or other wires
           if gate_connections:
               y_z_coor = change_coor(gate_connections, coordinate, gate_coordinates, wires, coordinate_end, y_coordinate_start, step_y, z_coordinate_start, 1)
               y_coordinate_start = y_z_coor[0]
               z_coordinate_start = y_z_coor[1]
               
               
               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
               if gate_connections:
                   for key in gate_connections:
                       selected_wires = gate_connections[key]
                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                           if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
                               if coordinate != coordinate_end:
                                   x_coordinate_start = x_coordinate_start - step_x - step_x
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   break
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                               if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                           if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                           if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
                               if coordinate != coordinate_end:
                                   x_coordinate_start = x_coordinate_start - step_x - step_x
                                   # z kan nu niet meerdere stappen omhoog/omlaag
                                   break
                       coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                       if gate_connections:
                           for key in gate_connections:
                               selected_wires = gate_connections[key]
                               if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                               if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                           if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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

           # Reset switch variable to be able to move in x-direction
           switch_variable = 0
           
           coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
           wires.append(coordinate)
           print(coordinate)
           wire = classs.Wire(coordinate, connected_gate)
           allwires.append(wire)
           
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
                           if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                               if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                   if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                   if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                               if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                   if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                   if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
                                       if coordinate != coordinate_end:
                                           y_coordinate_start = y_coordinate_start - step_y - step_y
                                           # z kan nu niet meerdere stappen omhoog/omlaag
                                           break
                                           # moet ook uit while loop breken!
                               coordinate = [x_coordinate_start, y_coordinate_start, z_coordinate_start]
                               if gate_connections:
                                   for key in gate_connections:
                                       selected_wires = gate_connections[key]
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                                       if coordinate in selected_wires or coordinate in gate_coordinates or coordinate in wires:
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
                   print(coordinate)
                   wire = classs.Wire(coordinate, connected_gate)
                   allwires.append(wire)
                   
        # Check whether wire isn't running into forever loop
        if len(wires) > 100:
            x_coordinate_check = x_coordinate_end + step_x
            check_coordinate = [x_coordinate_check, y_coordinate_end, z_coordinate_end]
            for item in allwires:
                if item.coordinate == check_coordinate and item.net[0] != gate_end and item.net[1] != gate_end:
                    # Clear wires list
                    wires = []
                    x_coordinate_start = int(coordinate_begin[0])
                    y_coordinate_start = int(coordinate_begin[1])
                    z_coordinate_start = int(coordinate_begin[2])
                    coordinate = coordinate_begin
                    
                    # Switch order of gates
                    end_gate = item.net[0]
                    start_gate = item.net[1]
                    distances.append(((start_gate, end_gate), 2))
                    print("hallo")
                    print(distances)
                    # Delete wire from gate connections dictionary
                    del gate_connections[item.net]
                    
                    # Delete blocking wire
                    for i, item2 in enumerate(allwires):
                        if item2.net == item.net:
                            print("DELETETOM")
                            print(allwires[i])
                            wire = classs.Wire([0, 0, 0], (0, 0))
                            allwires[i] = wire
                    break
                else:
                    copy_gate_connections = copy.deepcopy(gate_connections)
                    for key in copy_gate_connections:
                        if len(copy_gate_connections[key]) > 75:
                            print("deleteee", key)
                            # Clear wires list
                            wires = []
                            x_coordinate_start = int(coordinate_begin[0])
                            y_coordinate_start = int(coordinate_begin[1])
                            z_coordinate_start = int(coordinate_begin[2])
                            coordinate = coordinate_begin
                    
                            # Switch order of gates
                            end_gate = key[0]
                            start_gate = key[1]
                            distances.append(((start_gate, end_gate), 2))
                            
                            del gate_connections[key]
                            
                            for i, item2 in enumerate(allwires):
                                if item2.net == key:
                                    print("DELETETOM")
                                    print(allwires[i])
                                    wire = classs.Wire([0, 0, 0], (0, 0))
                                    allwires[i] = wire
                    break     
            x_coordinate_check = x_coordinate_end - step_x
            check_coordinate = [x_coordinate_check, y_coordinate_end, z_coordinate_end]
            for item in allwires:
                if item.coordinate == check_coordinate and item.net[0] != gate_end and item.net[1] != gate_end:
                    # Clear wires list
                    wires = []
                    x_coordinate_start = int(coordinate_begin[0])
                    y_coordinate_start = int(coordinate_begin[1])
                    z_coordinate_start = int(coordinate_begin[2])
                    coordinate = coordinate_begin
                    
                    # Switch order of gates
                    end_gate = item.net[0]
                    start_gate = item.net[1]
                    distances.append(((start_gate, end_gate), 2))
                    print("hallo")
                    print(distances)
                    # Delete wire from gate connections dictionary
                    del gate_connections[item.net]
                    
                    # Delete blocking wire
                    for i, item2 in enumerate(allwires):
                        if item2.net == item.net:
                            print("DELETETOM")
                            print(allwires[i])
                            wire = classs.Wire([0, 0, 0], (0, 0))
                            allwires[i] = wire
                    break
                else:
                    copy_gate_connections = copy.deepcopy(gate_connections)
                    for key in copy_gate_connections:
                        if len(copy_gate_connections[key]) > 75:
                            print("deleteee", key)
                            # Clear wires list
                            wires = []
                            x_coordinate_start = int(coordinate_begin[0])
                            y_coordinate_start = int(coordinate_begin[1])
                            z_coordinate_start = int(coordinate_begin[2])
                            coordinate = coordinate_begin
                    
                            # Switch order of gates
                            end_gate = key[0]
                            start_gate = key[1]
                            distances.append(((start_gate, end_gate), 2))
                            
                            del gate_connections[key]
                            
                            for i, item2 in enumerate(allwires):
                                if item2.net == key:
                                    print("DELETETOM")
                                    print(allwires[i])
                                    wire = classs.Wire([0, 0, 0], (0, 0))
                                    allwires[i] = wire
                    break
            y_coordinate_check = y_coordinate_end + step_y
            check_coordinate = [x_coordinate_end, y_coordinate_check, z_coordinate_end]
            for item in allwires:
                if item.coordinate == check_coordinate and item.net[0] != gate_end and item.net[1] != gate_end:
                    # Clear wires list
                    wires = []
                    x_coordinate_start = int(coordinate_begin[0])
                    y_coordinate_start = int(coordinate_begin[1])
                    z_coordinate_start = int(coordinate_begin[2])
                    coordinate = coordinate_begin
                    
                    # Switch order of gates
                    end_gate = item.net[0]
                    start_gate = item.net[1]
                    distances.append(((start_gate, end_gate), 2))
                    print("hallo")
                    print(distances)
                    # Delete wire from gate connections dictionary
                    del gate_connections[item.net]

                    # Delete blocking wire
                    for i, item2 in enumerate(allwires):
                        if item2.net == item.net:
                            print("DELETETOM")
                            print(allwires[i])
                            wire = classs.Wire([0, 0, 0], (0, 0))
                            allwires[i] = wire
                    break
                else:
                    copy_gate_connections = copy.deepcopy(gate_connections)
                    for key in copy_gate_connections:
                        if len(copy_gate_connections[key]) > 75:
                            print("deleteee", key)
                            # Clear wires list
                            wires = []
                            x_coordinate_start = int(coordinate_begin[0])
                            y_coordinate_start = int(coordinate_begin[1])
                            z_coordinate_start = int(coordinate_begin[2])
                            coordinate = coordinate_begin
                    
                            # Switch order of gates
                            end_gate = key[0]
                            start_gate = key[1]
                            distances.append(((start_gate, end_gate), 2))
                            
                            del gate_connections[key]
                            
                            
                            for i, item2 in enumerate(allwires):
                                if item2.net == key:
                                    print("DELETETOM")
                                    print(allwires[i])
                                    wire = classs.Wire([0, 0, 0], (0, 0))
                                    allwires[i] = wire
                    break
            y_coordinate_check = y_coordinate_end - step_y
            check_coordinate = [x_coordinate_end, y_coordinate_check, z_coordinate_end]
            for item in allwires:
                if item.coordinate == check_coordinate and item.net[0] != gate_end and item.net[1] != gate_end:
                    # Clear wires list
                    wires = []
                    x_coordinate_start = int(coordinate_begin[0])
                    y_coordinate_start = int(coordinate_begin[1])
                    z_coordinate_start = int(coordinate_begin[2])
                    coordinate = coordinate_begin
                    
                    # Switch order of gates
                    end_gate = item.net[0]
                    start_gate = item.net[1]
                    distances.append(((start_gate, end_gate), 2))
                    print("hallo")
                    print(distances)
                    # Delete wire from gate connections dictionary
                    del gate_connections[item.net]
              
                    # Delete blocking wire
                    for i, item2 in enumerate(allwires):
                        if item2.net == item.net:
                            print("DELETETOM")
                            print(allwires[i])
                            wire = classs.Wire([0, 0, 0], (0, 0))
                            allwires[i] = wire
                    break
                else:
                    copy_gate_connections = copy.deepcopy(gate_connections)
                    for key in copy_gate_connections:
                        if len(copy_gate_connections[key]) > 75:
                            print("deleteee", key)
                            # Clear wires list
                            wires = []
                            x_coordinate_start = int(coordinate_begin[0])
                            y_coordinate_start = int(coordinate_begin[1])
                            z_coordinate_start = int(coordinate_begin[2])
                            coordinate = coordinate_begin
                    
                            # Switch order of gates
                            end_gate = key[0]
                            start_gate = key[1]
                            distances.append(((start_gate, end_gate), 2))
                            
                            del gate_connections[key]
                            
                            for i, item2 in enumerate(allwires):
                                if item2.net == key:
                                    print("DELETETOM")
                                    print(allwires[i])
                                    wire = classs.Wire([0, 0, 0], (0, 0))
                                    allwires[i] = wire
                    break
            z_coordinate_check = z_coordinate_end + 1
            check_coordinate = [x_coordinate_end, y_coordinate_end, z_coordinate_check]
            for item in allwires:
                if item.coordinate == check_coordinate and item.net[0] != gate_end and item.net[1] != gate_end:
                    # Clear wires list
                    wires = []
                    x_coordinate_start = int(coordinate_begin[0])
                    y_coordinate_start = int(coordinate_begin[1])
                    z_coordinate_start = int(coordinate_begin[2])
                    coordinate = coordinate_begin
                    
                    # Switch order of gates
                    end_gate = item.net[0]
                    start_gate = item.net[1]
                    distances.append(((start_gate, end_gate), 2))
         
                    print("hallo")
                    print(distances)
                    # Delete wire from gate connections dictionary
                    del gate_connections[item.net]
              
                    # Delete blocking wire
                    for i, item2 in enumerate(allwires):
                        if item2.net == item.net:
                            print("DELETETOM")
                            print(allwires[i])
                            wire = classs.Wire([0, 0, 0], (0, 0))
                            allwires[i] = wire
                    break
                else:
                    copy_gate_connections = copy.deepcopy(gate_connections)
                    for key in copy_gate_connections:
                        if len(copy_gate_connections[key]) > 75:
                            print("deleteee", key)
                            # Clear wires list
                            wires = []
                            x_coordinate_start = int(coordinate_begin[0])
                            y_coordinate_start = int(coordinate_begin[1])
                            z_coordinate_start = int(coordinate_begin[2])
                            coordinate = coordinate_begin
                    
                            # Switch order of gates
                            end_gate = key[0]
                            start_gate = key[1]
                            distances.append(((start_gate, end_gate), 2))
                            
                            del gate_connections[key]
                            
                            for i, item2 in enumerate(allwires):
                                if item2.net == key:
                                    print("DELETETOM")
                                    print(allwires[i])
                                    wire = classs.Wire([0, 0, 0], (0, 0))
                                    allwires[i] = wire
                    break
                    
            # If no wire can be deleted and current wire can still not reach end gate
            wires = []
            x_coordinate_start = int(coordinate_begin[0])
            y_coordinate_start = int(coordinate_begin[1])
            z_coordinate_start = int(coordinate_begin[2])
            coordinate = coordinate_begin
            # Check y-coordinate first, then x-coordinate
            # Change value of switch variable to start moving in other direction
            switch_variable = 1
        
        # # If wire is deleted: check whether other wires that can probably be shorter can be deleted
   #      if len(wires) == 0:
   #          print("delete2")
   #          for counter in range(len(distances)):
   #              key = distances[counter][0]
   #              print(gate_connections)
   #              try:
   #                  if len(gate_connections[key]) > distances[counter][1]*1.5:
   #                      print("TOR", count)
   #                      wires = []
   #                      x_coordinate_start = int(coordinate_begin[0])
   #                      y_coordinate_start = int(coordinate_begin[1])
   #                      z_coordinate_start = int(coordinate_begin[2])
   #                      coordinate = coordinate_begin
   #
   #                      # Switch order of gates
   #                      end_gate = key[0]
   #                      start_gate = key[1]
   #                      distances.append(((start_gate, end_gate), distances[counter][1]))
   #                      # Delete wire from gate connections dictionary
   #                      del gate_connections[key]
   #
   #                      # Delete blocking wire
   #                      for i, item2 in enumerate(allwires):
   #                          if item2.net == key:
   #                              print("TomJoe", allwires[i])
   #                              wire = classs.Wire([0, 0, 0], (0, 0))
   #                              allwires[i] = wire
   #              except:
   #                  break
               
    count += 1         
    print("WIRESSSS")
    print(wires)
    
    wires_length = len(wires)
    
    # Delete part of wire when wire goes back and forth on one line
    if wires_length > 4:
        indices = []
        for counter in range(wires_length-2):
            coor_1 = wires[counter]
            coor_2 = wires[counter + 1]
            coor_3 = wires[counter + 2]

            # Save indices of wires list
            if coor_1 == coor_3:
                indices.append(counter)
                indices.append(counter + 1)
        
        # Delete wire coordinate with highest index first
        for delete_count in range(wires_length):
            for index in indices:
                if (wires_length - delete_count) == index:
                    wires.pop(index)
    
    net = classs.Net(gate_start, gate_end)
    net.create_wires(wires)
    gate_connections.update({connected_gate: wires})
    # if count > 20:
  #       break

    # if len(gate_connections) == len(netlist):
   #      break
    print("ALL WIRES")
    print(allwires)
    print(net)
    
print(gate_connections)
print(len(gate_connections))
print("JOEJOE")
print("ALL WIRESSS")
print(allwires[0].coordinate)
# print(gate_connections[(17,10)])


length = 0
# Calculate total length of wires
for key in gate_connections:
    wire = gate_connections[key]
    length = length + len(wire)
    
print("TOTAL LENGTH")
# termcolor2

# print c(length).red.on_white.blink.underline.dark


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
            print("LineFromTo", allconnectionlist[i], "To",allconnectionlist[i + 1],  colours[colourcounter])
            draw_line(allconnectionlist[i], allconnectionlist[i+1], colours[colourcounter] )
            plt.pause(0.000001)
        except: 
            break
            
with open('output.csv', mode= 'w') as outputfile:
    output_writer = csv.writer(outputfile, delimiter= ',')

    for keys in gate_connections:
        output_writer.writerow([keys, gate_connections[keys]])

with open('output.csv', mode= 'w') as outputfile:
    output_writer = csv.writer(outputfile, delimiter= ',')

    for keys in gate_connections:
        output_writer.writerow([keys, gate_connections[keys]])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()
