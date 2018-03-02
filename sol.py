'''for each ride:
    find car for which distance to ride == earliest time - current time'''

import sys

rows, columns, fleet_size, num_rides, bonus, steps = map(int, input().split())
curr_step = 0

class Car:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rides = [] # all the rides it has done
        self.assigned = None # index in rides array
        self.has_ride = False # has picked up ride


cars = [Car() for i in range(fleet_size)]
rides = []
for i in range(num_rides):
    data = [i]
    data.extend(list(map(int, input().split())))
    data.append(False)
    rides.append(data)

def is_at_ride(car):
    # check if at start
    if car.x == rides[car.assigned][1] and car.y == rides[car.assigned][2]:
        return True
    return False


def is_early(car):
    if curr_step < rides[car.assigned][5]:
        return True
    return False

def move(car, toStart=True):
    if toStart:
        x = 1
        y = 2
    else:
        x = 3
        y = 4
    if car.x < rides[car.assigned][x]:
        car.x += 1
    elif car.x > rides[car.assigned][x]:
        car.x -= 1
    elif car.y > rides[car.assigned][y]:
        car.y -=1
    elif car.y < rides[car.assigned][y]:
        car.y += 1

def at_destination(car):
    return car.x == rides[car.assigned][3] and car.y == rides[car.assigned][4]

def distance_to_finish(car):
    # | a -x | + | b - y |
    return abs(rides[car.assigned][1] - rides[car.assigned][3]) + abs(rides[car.assigned][2] - rides[car.assigned][4])

def distance_of_ride(i):
    return abs(rides[i][1] - rides[i][3]) + abs(rides[i][2] - rides[i][4])

def distance_to_start_i(car, i):
    # | a -x | + | b - y |
    return abs(car.x - rides[i][1]) + abs(car.y - rides[i][2])

def reset(car):
    rides[car.assigned][7] = True
    car.assigned = None
    car.has_ride = False


def assign():
    for car in cars:
        # free car
        if car.assigned == None:
            best = -1
            best_diff = sys.maxsize
            for i in range(len(rides)):
                #Ride not taken yet
                if not rides[i][7]:
                    if distance_of_ride(i) + curr_step > steps:
                        continue
                    time_until_start = rides[i][5] - curr_step
                    diff = abs(distance_to_start_i(car, i) - time_until_start)
                    if diff <= best_diff:
                        best_diff = diff
                        best = i
            rides[best][7] = True
            car.assigned = best


# ride indexes
# 0   - ride number
# 1,2 - row, col for start
# 3,4 - row, col for destination
# 5   - min start time
# 6   - latest finish time
# 7   - is finished/dropped


assign()

while curr_step < steps:
    # moving of the cars
    for car in cars:
        #if assigned
        if car.assigned is not None:
            if car.has_ride:
                # Move car to its destination
                move(car, toStart=False)
                if at_destination(car):
                    car.rides.append(rides[car.assigned][0])
                    reset(car)
            # if not picked up
            else:
                #on time/late and at ride
                if not is_early(car) and is_at_ride(car):
                    # CANT make it on time for the ride, so forget about it.
                    if distance_to_finish(car) > rides[car.assigned][6] - curr_step:
                        reset(car)
                    else:
                        # picked up the ride and move towards destination
                        car.has_ride = True
                        move(car, toStart=False)
                        if at_destination(car): # one move after start
                            car.rides.append(rides[car.assigned][0])
                            reset(car)

                #If not at the ride, move towards the start position
                elif not is_at_ride(car):
                    move(car, toStart=True)

    assign()
    curr_step+=1

for car in cars:
    print(len(car.rides), " ".join(map(str, car.rides)))
