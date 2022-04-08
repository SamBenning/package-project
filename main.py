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

distance_map = csv_parser.get_distance_map()
package_map = csv_parser.get_package_map()
packages_at_hub = []

distance_map.print()

def init_packages_at_hub():
    for i in range(1,41):
        packages_at_hub.append(package_map.get(i))


def create_truck_delivery_matrix(truck):
    delivery_matrix = {}
    for package in truck.packages:
        package_address = package.address
        package_priority = 1
        if package.deadline == "9:00 AM":
            package_priority = 10
        elif package.deadline == "10:30 AM":
            package_priority = 2
        if delivery_matrix.get(package_address):
            packages_at_address = delivery_matrix.get(package_address)[0]
            updated_priority = delivery_matrix.get(package_address)[1]
            packages_at_address.append(package)
            updated_priority *= package_priority
            updated_entry = {package_address:(packages_at_address, updated_priority)}
            delivery_matrix.update(updated_entry)
        else:
            new_entry = {package_address:([package],package_priority)}
            delivery_matrix.update(new_entry)
    return delivery_matrix


def route_2(truck, current_location, delivery_matrix):
    # print(current_location)
    # print("Delivery matrix" + str(delivery_matrix))
    # print("Truck location:" + truck.location)
    neighbors = distance_map.get(current_location)
    print(neighbors)
    best_neighbor = neighbors[0]
    best_neighbor_score = 0
    for neighbor in neighbors:
        neighbor_address = neighbor[0]
        neighbor_distance = neighbor[1]
        if not delivery_matrix.get(neighbor_address):
            continue
        neighbor_priority = delivery_matrix.get(neighbor_address)[1]

        # print("Neighbor: " + str(neighbor))
        # print("Neighbor distance: " + str(neighbor_distance))
        neighbor_score = neighbor_priority/neighbor_distance
        if neighbor_score > best_neighbor_score:
            best_neighbor = neighbor
            best_neighbor_score = neighbor_score
    # print(best_neighbor)
    # print(delivery_matrix)
    packages_at_best_neighbor = delivery_matrix.get(best_neighbor[0])[0]
    truck.next_delivery = packages_at_best_neighbor
    print("BEST NEIGHBOR: " + str(best_neighbor))
    return best_neighbor



def goto(truck, location):
    miles = location[1]
    address = location[0]

    if truck.time >= datetime.datetime(2022, 1, 1, 10, 20) and package_map.get(9).address == "300 State St":
        if package_map.get(9) in truck.packages:
            package_map.get(9).address = "410 S State St"
            truck.make_delivery(truck.time)
        elif package_map.get(9) in truck.next_delivery:
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            package_map.get(9).address = "410 S State St"
            truck.packages.append(package_map.get(9))
            truck.next_delivery.remove(package_map.get(9))
            if not truck.next_delivery:
                return
        elif package_map.get(9) in truck.delivered_packages:
            # truck.make_delivery(truck.time)
            dist_list = distance_map.get(truck.location)
            dist = 0
            for item in dist_list:
                if item[0] == "300 State St":
                    dist = item[1]
            truck.packages.append(package_map.get(9))
            truck.delivered_packages.remove(package_map.get(9))
            print("RETRIEVING PACKAGE 9 DUE TO INCORRECT DELIVERY")
            goto(truck, ("300 State St", dist))
            return
            address = "300 State St"
            miles = dist


    print(location)
    print(truck.packages)
    for package in truck.packages:
        package.print()
    print("Miles:" + str(miles))
    truck.time += datetime.timedelta(hours=(miles/18))
    truck.add_mileage(miles)
    truck.location = address
    print("NOW AT: " + address)
    truck.make_delivery(truck.time)





def go_home(truck):
    dist_list = distance_map.get(truck.location)
    dist_to_hub = -1
    for item in dist_list:
        if item[0] == "4001 South 700 East,":
            dist_to_hub = item[1]
    truck.time += datetime.timedelta(hours=(dist_to_hub/18))
    truck.add_mileage((dist_to_hub))
    truck.location = "4001 South 700 East,"

def run_truck(truck):
    while truck.packages:
        truck_delivery_matrix = create_truck_delivery_matrix(truck)
        # print("TRUCK LOCATION: " + str(truck.location))
        # next_location = route(truck, truck.location)
        next_location = route_2(truck, truck.location, truck_delivery_matrix)
        # print("NEXT LOCATION: " + str(next_location))
        goto(truck, next_location)

    go_home(truck)
    print("TRUCK MILES: " + str(truck.odometer))




truck_1 = Truck(1, "4001 South 700 East,")
truck_1.time = datetime.datetime(2022,1,1,0,0,0,0)
truck_1.time = truck_1.time + datetime.timedelta(hours=8)
truck_2 = Truck(2, "4001 South 700 East,")
truck_2.time = datetime.datetime(2022,1,1,0,0,0,0)
truck_2.time = truck_2.time + datetime.timedelta(hours=9, minutes=5)

def load_truck(truck):
    while len(truck.packages) < 16 and packages_at_hub:
        first_package = packages_at_hub.pop(0)
        truck.add_package(first_package)

def load_trucks(truck_1, truck_2):
    packages_loaded = []
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
            continue
        packages_at_hub.remove(package_map.get(i))

    package_id = 1
    while len(truck_2.packages) < 16:
        if package_map.get(package_id) in packages_at_hub:
            truck_2.add_package(package_map.get(package_id))
            packages_at_hub.remove(package_map.get(package_id))
        package_id += 1
        if package_id > 40:
            break

    # print("Packages on Truck 1: " + str(len(truck_1.packages)))
    # print("Packages on Truck 2: " + str(len(truck_2.packages)))
    return packages_loaded





def print_truck_contents(truck):
    truck.print_packages()


def main():
    init_packages_at_hub()
    while True:
        print('Start of program:')
        print("Select an option: ")
        print("1. Print out the hashmap.")
        print("2. Quit the program")
        print(datetime.datetime(2022, 1, 1, 10, 20))
        x = input()
        if int(x) == 1:
            print(packages_at_hub)
        elif int(x) == 2:
            break
        elif int(x) == 3:
            # package_map.print()
            print(truck_1.time)
            run_truck(truck_1)
            run_truck(truck_2)

            if len(packages_at_hub) > 0:
                load_truck(truck_1)
                run_truck(truck_1)

            for i in range(1,41):
                package_map.get(i).print()
            truck_1.print_package_list()
            print(truck_1.next_delivery)
            print("Total miles: " + str(truck_1.odometer + truck_2.odometer))

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


main()

