import csv
from hash import HashMap
from package import Package
from truck import Truck
import csv_parser
import datetime

print(datetime.datetime.today())
def validate_hashmap_keys(keys, hash_map=HashMap):
    for key in keys:
        if hash_map.get(key) is None:
            return False
    return True


def route(truck, current_location):
    neighbors = distance_map.get(current_location)
    # current_address = neighbors[0]
    neighbor_has_delivery = False
    while neighbors:
        closest_neighbor = None
        for neighbor in neighbors:
            if closest_neighbor:
                if neighbor[1] < closest_neighbor[1] and neighbor[1] != 0.0:
                    closest_neighbor = neighbor
                elif closest_neighbor[1] == 0.0:
                    closest_neighbor = neighbor
            else:
                closest_neighbor = neighbor
        for truck_package in truck.packages:
            # print('---Currently at: ' + current_location + '----')
            # print("checking package with address: " + truck_package.address + " against: " + closest_neighbor[0])
            print(". . . checking package " + str(truck_package.id) + " against " + str(closest_neighbor[0]))
            if truck_package.address[0:10] == closest_neighbor[0][0:10]:
                print("MATCHING PACKAGE: " + str(truck_package.id) + " with " + str(closest_neighbor[0]))
                neighbor_has_delivery = True
                # truck.remove_package(truck_package)
                truck.next_delivery.append(truck_package)
                # print("TRUCK NEXT DELIVERY = " + str(truck.next_delivery))
        if neighbor_has_delivery:
            return closest_neighbor
        else:
            neighbor_has_delivery = False
            neighbors.remove(closest_neighbor)
    return 'fuck'


def goto(truck, location):
    miles = location[1]
    address = location[0]
    truck.time += datetime.timedelta(hours=(miles/18))
    truck.add_mileage(miles)
    truck.location = address
    print("NOW AT: " + address)
    truck.make_delivery(truck.time)


def run_truck(truck):
    while truck.packages:
        # print("TRUCK LOCATION: " + str(truck.location))
        next_location = route(truck, truck.location)
        # print("NEXT LOCATION: " + str(next_location))
        goto(truck, next_location)

    print("TRUCK MILES: " + str(truck.odometer))




truck_1 = Truck(1, "4001 South 700 East,")
truck_1.time = datetime.datetime(2022,1,1,0,0,0,0)
truck_1.time = truck_1.time + datetime.timedelta(hours=8)
truck_2 = Truck(2, "4001 South 700 East,")
truck_2.time = datetime.datetime(2022,1,1,0,0,0,0)
truck_2.time = truck_2.time + datetime.timedelta(hours=9, minutes=5)

def load_truck(truck):
    for p in range(1,41):
        truck.add_package(package_map.get(p))

def load_trucks(truck_1, truck_2):
    for i in range(1,41):
        current_package = package_map.get(i)
        if current_package.notes == "Can only be on truck 2":
            truck_2.add_package(current_package)
        elif current_package.notes[0:3] == "Del":
            truck_2.add_package(current_package)
        elif current_package.notes[0:3] == "Wro":
            truck_2.add_package(current_package)
        elif current_package.notes[0:3] == "Mus":
            truck_1.add_package(current_package)
        elif current_package.id == 15 or current_package.id == 19 or current_package.id == 13:
            truck_1.add_package(current_package)
        elif current_package.deadline != "EOD":
            truck_1.add_package(current_package)
        else:
            truck_2.add_package(current_package)





def print_truck_contents(truck):
    truck.print_packages()


distance_map = csv_parser.get_distance_map()
package_map = csv_parser.get_package_map()

while True:
    print('Start of program:')
    print("Select an option: ")
    print("1. Print out the hashmap.")
    print("2. Quit the program")
    x = input()
    if int(x) == 1:
        my_time = datetime.time(8,15)
        print(my_time)
    elif int(x) == 2:
        break
    elif int(x) == 3:
        # package_map.print()
        print(truck_1.time)
        run_truck(truck_1)
        run_truck(truck_2)
        for i in range(1,41):
            package_map.get(i).print()
        truck_1.print_package_list()
        print(truck_1.next_delivery)

    elif int(x) == 4:
        load_trucks(truck_1, truck_2)
        truck_1.print_package_list()
        truck_2.print_package_list()
        for i in range(1,41):
            package_map.get(i).print()
    elif int(x) == 5:
        next = route(truck_1, '4300 S 1300 E')
        print(next)
    elif int(x) == 6:
        print(package_map.get(12).address)




