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
        self.assigned = None # suppose to do this ride number
        self.has_ride = False # has picked up ride

    #def __str__(self):
    #    return "{}".format(self.rides)

cars = [Car() for i in range(fleet_size)]
free_cars = []
rides = []
for i in range(num_rides):
    data = [i]
    data.extend(list(map(int, input().split())))
    data.append(False)
    rides.append(data)
#rides.sort(key=lambda x: x[5])

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
    #print("moving")
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

def distance_between(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def distance_to_start(car, x, y):
    # | a -x | + | b - y |
    return abs(x - car.x) + abs(y - car.y)

def assign():
    for car in cars:
        # free car
        if car.assigned == None:
            best = -1
            best_diff = sys.maxsize
            for i in range(len(rides)):
                #Ride not taken yet
                if not rides[i][7]:
                    '''
                    Could definitely change this, sub-optimal (waiting times)
                    If at the position
                    dist to start == 0,
                    earliest start = 500
                    curr step = 0
                    result = -500
                    car waits for 500 lol
                    '''
                    if (abs(rides[i][1] - rides[i][3]) + abs(rides[i][2] - rides[i][4])) + curr_step > steps:
                        continue
                    total_dist = distance_between(rides[i][1], rides[i][2], rides[i][3], rides[i][4])
                    diff = abs(distance_to_start(car, rides[i][1], rides[i][2]) - (rides[i][5] - curr_step))*total_dist
                    if diff <= best_diff:
                        best_diff = diff
                        best = i
            if best > -1:
                rides[best][7] = True
                car.assigned = best


# ride indexes
# 0   - ride number
# 1,2 - row, col for start
# 3,4 - row, col for destination
# 5   - min start time
# 6   - latest finish time

def reset(car):
    rides[car.assigned][7] = True
    car.assigned = None
    car.has_ride = False

assign()

while not curr_step == steps:

    # moving of the cars
    for car in cars:
        #if assigned
        if not car.assigned == None:
            # if not picked up
            if not car.has_ride:
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
                        else:
                            continue # go on to the next car
                # early and not at ride
                elif is_early(car) and not is_at_ride(car):
                    move(car, toStart=True)
                elif not is_early(car) and not is_at_ride(car):
                    move(car, toStart=True)
            else:
                # have someone
                move(car, toStart=False)
                if at_destination(car):
                    car.rides.append(rides[car.assigned][0])
                    reset(car)
                else:
                    continue # go on to the next car
    assign()
    curr_step+=1

for car in cars:
    print(len(car.rides), " ".join(map(str, car.rides)))
