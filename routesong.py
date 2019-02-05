# Finds a route through a syllable graph that meets metre constraint.
# Copyright (C) 2019  Steven Baltakatei Sandoval
# See LICENSE for details.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <https://www.gnu.org/licenses/>.

# Import

import csv  # for importing csv files
import networkx as nx   # for graphing and plotting)
import matplotlib.pyplot as plt
import time

## Import random number stuff
import os
clear = lambda: os.system('clear')
import struct
import random

## Debugging
#       import pdb; pdb.set_trace()

# Initialize random number generator
systemRandom = random.SystemRandom()

# Define Static global variables

## Location of metre CSV file.
METRE_CSV_FILE_LOCATION = "DATA/metre/mother_pollyanna.csv"

## Location of graph CSV file.
#GRAPH_CSV_FILE_LOCATION = "DATA/graph/system_connections_pronunciations.csv"
GRAPH_CSV_FILE_LOCATION = "DATA/graph/system_connections_pronunciations_namedregions.csv"
#GRAPH_CSV_FILE_LOCATION = "DATA/graph/system_connections_pronunciations_theforge.csv"
#GRAPH_CSV_FILE_LOCATION = "DATA/graph/system_connections_pronunciations_kimotoro.csv"

## Initial node settings
### Name of first node (must be in graph).
INITIAL_NODE = "Jita"
### Number of syllables of first node (must be in graph)
INITIAL_NODE_SYLLABLES = 2
### Initial score to start with.
FIRST_JUMP_SCORE = float(1.00)

## Route search settings
### Max number of jump attempts (~)
MAX_JUMPS = 1000000
### How much to penalize encountering recently visited nodes.
SHORTLOOP_PENALTY_FACTOR = float(0.30)
### Defines how long in the past is "recent"
SHORTLOOP_LENGTH = 4
### How much to penalize having to backtrack while searching.
BACKTRACK_PENALTY_FACTOR = float(0.90)
### How much to penalize failing a jump forward to a candidate node.
NO_JUMP_PENALTY_FACTOR = float(0.90)
### How much to reward selecting a successful jump forward.
NEW_JUMP_BONUS = float(1.05)
### How much to reward selecting a node with many syllables.
LONGNAME_BONUS_FACTOR = float(1.05)
### Route score below which backtracking is required.
BACKTRACK_THRESHOLD = float(0.10)
### Initial score to assign latest entry in route score list.
NEW_JUMP_SCORE = float(1.00)


# Create graph with CSV file info
#with open('DATA/system_connections_pronunciations.csv', 'r') as csvfile:
#with open('DATA/system_connections_pronunciations_namedregions.csv', 'r') as csvfile:
#with open('DATA/system_connections_pronunciations_theforge.csv', 'r') as csvfile:
with open(GRAPH_CSV_FILE_LOCATION, 'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    # Initialize sublists
    solar_system_name = []
    security_rating = []
    region = []
    constellation = []
    coord_x = []
    coord_z = []
    coord_y = []
    gate_1 = []
    gate_2 = []
    gate_3 = []
    gate_4 = []
    gate_5 = []
    gate_6 = []
    gate_7 = []
    gate_8 = []
    pron_1_sc = []
    pron_1 = []
    pron_2_sc = []
    pron_2 = []
    pron_3_sc = []
    pron_3 = []

    # Populate sublists
    for row in readCSV:
        solar_system_name_sub = row[0]
        security_rating_sub = row[1]
        region_sub = row[2]
        constellation_sub = row[3]
        coord_x_sub = row[4]
        coord_z_sub = row[5]
        coord_y_sub = row[6]
        gate_1_sub = row[7]
        gate_2_sub = row[8]
        gate_3_sub = row[9]
        gate_4_sub = row[10]
        gate_5_sub = row[11]
        gate_6_sub = row[12]
        gate_7_sub = row[13]
        gate_8_sub = row[14]
        pron_1_sc_sub = row[15]
        pron_1_sub = row[16]
        pron_2_sc_sub = row[17]
        pron_2_sub = row[18]
        pron_3_sc_sub = row[19]
        pron_3_sub = row[20]
    
        solar_system_name.append(solar_system_name_sub)
        security_rating.append(security_rating_sub)
        region.append(region_sub)
        constellation.append(constellation_sub)
        coord_x.append(coord_x_sub)
        coord_z.append(coord_z_sub)
        coord_y.append(coord_y_sub)
        gate_1.append(gate_1_sub)
        gate_2.append(gate_2_sub)
        gate_3.append(gate_3_sub)
        gate_4.append(gate_4_sub)
        gate_5.append(gate_5_sub)
        gate_6.append(gate_6_sub)
        gate_7.append(gate_7_sub)
        gate_8.append(gate_8_sub)
        pron_1_sc.append(pron_1_sc_sub)
        pron_1.append(pron_1_sub)
        pron_2_sc.append(pron_2_sc_sub)
        pron_2.append(pron_2_sub)
        pron_3_sc.append(pron_3_sc_sub)
        pron_3.append(pron_3_sub)

    solar_system_name.pop(0)
    security_rating.pop(0)
    region.pop(0)
    constellation.pop(0)
    coord_x.pop(0)
    coord_z.pop(0)
    coord_y.pop(0)
    gate_1.pop(0)
    gate_2.pop(0)
    gate_3.pop(0)
    gate_4.pop(0)
    gate_5.pop(0)
    gate_6.pop(0)
    gate_7.pop(0)
    gate_8.pop(0)
    pron_1_sc.pop(0)
    pron_1.pop(0)
    pron_2_sc.pop(0)
    pron_2.pop(0)
    pron_3_sc.pop(0)
    pron_3.pop(0)

    #convert list of string integers into list of strings
    #pron_1_sc = list(map(int, pron_1_sc))
    #pron_2_sc = list(map(int, pron_2_sc))
    #pron_3_sc = list(map(int, pron_3_sc))

    #convert list of string floats into list of floats
    #coord_x = list(map(float, coord_x))
    #coord_z = list(map(float, coord_z))
    #coord_y = list(map(float, coord_y))
    
# Test print data in lists
#    print(solar_system_name)
#    print(security_rating)
#    print(region)
#    print(constellation)
#    print(coord_x)
#    print(coord_z)
#    print(coord_y)
#    print(gate_1)
#    print(gate_2)
#    print(gate_3)
#    print(gate_4)
#    print(gate_5)
#    print(gate_6)
#    print(gate_7)
#    print(gate_8)
#    print(pron_1_sc)
#    print(pron_1)
#    print(pron_2_sc)
#    print(pron_2)
#    print(pron_3_sc)
#    print(pron_3)

# Create graph
G=nx.Graph()


# Add nodes
G.add_nodes_from(solar_system_name)


# Add edges
count = 0
for origin in solar_system_name:
    #print(count)
    if gate_1[count]:
        #print('Found element')
        #print(*[origin,gate_1[count]])
        G.add_edge(*[origin,gate_1[count]])
    #else:
        #print('Empty element')
    if gate_2[count]:
        #print('Found element')
        #print(*[origin,gate_2[count]])
        G.add_edge(*[origin,gate_2[count]])
    #else:
        #print('Empty element')
    if gate_3[count]:
        #print('Found element')
        #print(*[origin,gate_3[count]])
        G.add_edge(*[origin,gate_3[count]])
    #else:
        #print('Empty element')
    if gate_4[count]:
        #print('Found element')
        #print(*[origin,gate_4[count]])        
        G.add_edge(*[origin,gate_4[count]])
    #else:
        #print('Empty element')
    if gate_5[count]:
        #print('Found element')
        #print(*[origin,gate_5[count]])
        G.add_edge(*[origin,gate_5[count]])
    #else:
        #print('Empty element')
    if gate_6[count]:
        #print('Found element')
        #print(*[origin,gate_6[count]])
        G.add_edge(*[origin,gate_6[count]])
    #else:
        #print('Empty element')
    if gate_7[count]:
        #print('Found element')
        #print(*[origin,gate_7[count]])
        G.add_edge(*[origin,gate_7[count]])
    #else:
        #print('Empty element')
    if gate_8[count]:
        #print('Found element')
        #print(*[origin,gate_8[count]])
        G.add_edge(*[origin,gate_8[count]])
    #else:
        #print('Empty element')
    count += 1

# List edges of graph
#print(G.edges())

# Draw (don't activate if plotting all of New Eden)
#nx.draw(G, with_labels = True)
#plt.show()

#print(G.nodes())
#print(G.edges())
#print(list(G.adj['Jita']))


# Import meter list from CSV file.
with open(METRE_CSV_FILE_LOCATION, 'r') as csvfile2:
    readMetreCSV = csv.reader(csvfile2, delimiter=',')
    metre_master = []
    for row in readMetreCSV:
        metre_master_sub = row[0]
        metre_master.append(metre_master_sub)
    metre_master.pop(0)
    metre_master = list(map(int, metre_master))
    metre = metre_master.copy() # Make working duplicate of metre_master
print('Master metre is:',metre_master)


# Initialize route lists:
score = []
score.append(float(FIRST_JUMP_SCORE)) # initialize and set initial score
route = []
route.append(INITIAL_NODE) # initialize and set initial node
route_syllables = [INITIAL_NODE_SYLLABLES] # initialize route syllables list
metre[0] = metre[0] - INITIAL_NODE_SYLLABLES
metre_master_progress_index = 0 # initialize master metre list index
#print(route)


# Primary search loop
for jump in range (0, MAX_JUMPS):

    # Status calcs.
    adjacent_systems = list(G.adj[route[-1]])
    current_system = route[-1]
    current_system_index = solar_system_name.index(current_system)
    current_score = score[-1]
    remaining_metre = metre[0]
    adjacent_system_count = len(adjacent_systems)
    
    # Status report.
    #clear()
    print(":: :: :: ::")
    print("metre_master        :",metre_master)
    print("We are on jump      :",jump)
    print("Route list so far   :",route)
    print("metre list status   :",metre)
    print("score list status   :",["{0:0.15f}".format(i) for i in score])
    print("syllable_list status:",route_syllables)
    print("Current system:     :",current_system)
    print("Current sys index   :",current_system_index)
    print("Current score is    :",current_score)
    print("remaining_metre     :",remaining_metre)
    print("Adjacent systems    :",adjacent_systems)
    print("Adj. system count   :",adjacent_system_count)

    if remaining_metre == 0: # Check if next jump fully consumed remaining_metre
        print('remaining_metre = 0. Loading next metre element.')
        metre.pop(0) # Removes first element in metre list so next element will be loaded next loop.
        print('====METRE ELEMENT POPPED====')
        # Detect metre depletion.
        if not metre:
            print("========METRE DEPLETED========")
            print(":: :: :: :: :: :: :: :: ::")
            print(":: :: :: :: :: :: :: :: ::")
            print(":: :: :: :: :: :: :: :: ::")
            print(":: :: :: :: :: :: :: :: ::")
            print(":: :: :: :: :: :: :: :: ::")
            print(":: :: :: :: :: :: :: :: ::")
            print(":: :: :: :: :: :: :: :: ::")
            print(":: :: :: :: :: :: :: :: ::")
            print("Master metre list         :", metre_master)
            print("Completed syllable list   :",route_syllables)
            print("Completed route list      :", route)
            print("Completed score list      :", ["{0:0.3f}".format(i) for i in score])
            print("Completed route jump count:",len(route))
            print("Final metre list status:", metre)
            print("Junp evaluation loops initiated:",jump)
            print("Final lyrics:")
            print([str(route[i])+' - '+str(route_syllables[i]) for i in range (len(route))])
            print(":: :: :: :: :: :: :: :: ::")
            print("Total systems in route:",len(route))
            print(":: :: :: :: :: :: :: :: ::")
            sys.exit()
        else:
            remaining_metre = metre[0] # Load new first entry into remaining_metre variable.
            print('remaining_metre  :',remaining_metre)
            metre_master_progress_index += 1 # Update current corresponding position in metre_master
            print('metre_master_progress_index updated to:',metre_master_progress_index)
            print('metre list status   :',metre)

    
    # Select random system for next jump.
    nextRandJumpInvalid = True
    while nextRandJumpInvalid:
        #Select random system from adjacent_systems list
        nextRandJumpAdjacentIndex = systemRandom.randint(0,adjacent_system_count - 1)
        print("Next random jump Index:",nextRandJumpAdjacentIndex)
        nextRandJumpName = adjacent_systems[nextRandJumpAdjacentIndex]
        print("Next random jump Name :",nextRandJumpName)
        if nextRandJumpName in solar_system_name:
            nextRandJumpInvalid = False
            print('Next jump is within loaded solar systems list. Exiting while loop.')
        else:
            nextRandJumpInvalid = True
            print('Next jump is not within loaded solar system list. Remaining in while loop to reroll.')
            
    # Identify syllable count for  next jump
    # Calculate index within solar_system_name that contains nextRandJumpName
    nextRandJumpSolarSystemIndex = solar_system_name.index(nextRandJumpName)
    #print('solar_system_name list:',solar_system_name)
    #print('pron_1_sc',pron_1_sc)
    #print('current_system_index:',nextRandJumpSolarSystemIndex)
    #print('int(pron_1_sc[nextRandJumpSolarSystemIndex]):',int(pron_1_sc[nextRandJumpSolarSystemIndex]))
    nextRandJumpSyllableCount = int(pron_1_sc[nextRandJumpSolarSystemIndex])
    print("Next random jump name syllable count:",nextRandJumpSyllableCount)

    # Apply score penalties
    #Penalty if next jump system is already in last SHORTLOOP_LENGTH entries of route
    if nextRandJumpName in route[-int(SHORTLOOP_LENGTH):]:
        score[-1] = score[-1] * SHORTLOOP_PENALTY_FACTOR
    #Penalty if next jump system is already in last 2*SHORTLOOP_LENGTH entries of route
    if nextRandJumpName in route[-int(2 * SHORTLOOP_LENGTH):]:
        score[-1] = score[-1] * SHORTLOOP_PENALTY_FACTOR
    #Penalty for each occurence of a system within the SHORTLOOP_LENGTH
    if nextRandJumpName in route[-int(SHORTLOOP_LENGTH):]:
        nameOccurencesInShortLoop = route.count(nextRandJumpName)
        score[-1] = score[-1] * SHORTLOOP_PENALTY_FACTOR**(nameOccurencesInShortLoop/2)/2

    # Apply score bonuses
    #Apply bonus scaled to how many syllables name has
        score[-1] = score[-1] * LONGNAME_BONUS_FACTOR**(nextRandJumpSyllableCount - 1)
    
    # Subtract syllables from remaining metre
    remaining_metre = remaining_metre - nextRandJumpSyllableCount
    print("Updated remaining metre:",remaining_metre)

    # If next jump syllable count does NOT cause remaining_metre to go
    # negative, then perform jump (update metre, route, score, and
    #  route_syllable lists)
    # If next jump syllable count does cause remaining_metre to go
    #   negative, then do NOT perform jump (do NOT update metre,
    #   route, or route_syllable lists). Apply penalty to latest
    #   element in score list.
    #   Note: This will cause next loops to try different jumps until
    #     the latest score list element falls below a threshhold.
    # If previous jump score is below BACKTRACK_THRESHOLD then backtrack:
    #   1. Increment remaining_metre by amount in latest
    #      route_syllables list element, restoring metre list to
    #      previous state
    #   2. Adding entry to front of metre list if remaining_metre
    #      incremented above original metre element value (comparison
    #      made against metre_master using
    #      metre_master_progress_index as a reference.
    #   3. Remove latest entry in score list.
    #   4. Remove latest entry in score_syllables list.
    #   5. Remove latest entry in route list.
    #   6. Apply penalty to latest element in score list.
    if score[-1] < BACKTRACK_THRESHOLD: # Check if most recent score low enough to trigger backtracking.
        print('========SCORE VIOLATION========')
        print('Score violation occured. Backtracking.')
        metre[0] = metre[0] + route_syllables[-1]
        print('Backtracked new metre[0] value:',metre[0])
        print('metre_master:',metre_master)
        print('metre_master_progress_index:',metre_master_progress_index)
        print('metre_master[metre_master_progress_index]:',metre_master[metre_master_progress_index])
        # Handle case if backtrack rolls back over a meter boundary
        if metre[0] > metre_master[metre_master_progress_index]:
            # Save value to be stored in restored element to be shortly preappended to metre[]
            backtrack_metre_carryover = metre[0] - metre_master[metre_master_progress_index]
            # Restore first element in metre[] back to original value from metre_master
            metre[0] = metre_master[metre_master_progress_index]
            # Preappend carryover value to be new first element in metre[]
            metre.insert(0,backtrack_metre_carryover)
            # Decrement metre_master_progress by one.
            metre_master_progress_index -= 1
        score.pop() # Removing latest score list element.        
        route_syllables.pop() # Remove latest route_syllables list element.
        route.pop() # Removing latest route list element.
        if not score:
            print('score list depleted. not applying penalty')
            print('score list:',score)
            print('route_syllable list:',route_syllables)
            print('route list:',route)
        else:
            score[-1] = score[-1] * BACKTRACK_PENALTY_FACTOR #Applying penalty to previous score element.
            print('BACKTRACK PENALTY applied to score. Score now:',score[-1])
            # Handle case if route list completely emptied
        if not route:
            # Start again but from random system
            # Select random system from solar_system_name
            initialRandSystemIndex = systemRandom.randint(0,len(solar_system_name)-1)
            initialRandSystemName = solar_system_name[initialRandSystemIndex]
            initialRandSystemSyllableCount = int(pron_1_sc[initialRandSystemIndex])        
            # Reinitialize:
            #   1. route list
            #   2. metre list
            #   3. route_syllable list
            #   4. score list
            route = []
            route.append(initialRandSystemName)
            metre = metre_master.copy()
            metre[0] = metre[0] - initialRandSystemSyllableCount
            route_syllables = [initialRandSystemSyllableCount]
            score = []
            score.append(float(FIRST_JUMP_SCORE))
            metre_master_progress_index = 0
            print('====ROUTE LIST DEPLETED, RESTARTING SEARCH FROM RANDOM NODE====')
            #time.sleep(.1)
    else:
        print('remaining_metre of prospective jump:',remaining_metre)
        if remaining_metre >= 0:    # Check if some syllables still remain
            print('Some or no syllables remain. Updating last element of metre list.')
            metre[0] = remaining_metre   # Set updated remaining_metre to first entry of metre list.
            score[-1] = score[-1] * NEW_JUMP_BONUS # Add bonus to node before jump
            score.append(NEW_JUMP_SCORE) # Add new element to end of score list
            route_syllables.append(nextRandJumpSyllableCount) # Add new element to end of route_syllable list
            route.append(nextRandJumpName) # Add new element to route list containing next rand jump.
            print('====JUMP SUCCESS : NEW JUMP BONUS APPLIED====')
        else:   # What to do if remaining_metre < 0
            print('======METRE VIOLATION : NO JUMP PENALTY======')
            print('Metre violation occured. Jump cancelled.')
            print('No changes made to score, route, or route_syllables lists.')
            score[-1] = score[-1] * NO_JUMP_PENALTY_FACTOR # Applying penalty to previous score element.
            print('NO JUMP PENALTY applied to score. Score now:',score[-1])
    print(":: :: :: ::")
    print("")
    print("")

print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print('====JUMPS DEPLETED, SEARCH FAILED====')
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")
print(":: :: :: :: :: :: :: :: ::")

    
    
    
