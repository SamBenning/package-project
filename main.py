# Samuel Benning
# Student ID: 001486055
# C950 - Data Structures and Algorithms II

import datetime
import csv_parser
from truck import Truck

# Here, the data from both the Distance Map and Package File spreadsheets are imported by calling the csv_parser
# package. Data is stored using my custom hash table implementation from the hash.py file.
distance_map = csv_parser.get_distance_map()
package_map = csv_parser.get_package_map()

# This is a list which is used to store packages that are at the hub.
packages_at_hub = []

# Here, I instantiate two Truck objects. Using the constructor, the location of each truck is set to the hub address.
# Additionally, I set the time field to a datetime of 1/1/22 at 00:00 (I chose 1/1 since the project requirements do
# not specify anything about dates). I also add a time delta of 8 hours to truck 1, as it will be starting at 8:00am,
# and a time delta of 9 hours and 5 minutes to truck 2, since it will be starting at 9:05am.
truck_1 = Truck(1, "4001 South 700 East,")
truck_1.time = datetime.datetime(2022, 1, 1, 0, 0, 0, 0)
truck_1.time = truck_1.time + datetime.timedelta(hours=8)
truck_2 = Truck(2, "4001 South 700 East,")
truck_2.time = datetime.datetime(2022, 1, 1, 0, 0, 0, 0)
truck_2.time = truck_2.time + datetime.timedelta(hours=9, minutes=5)


# This function is used to obtain all packages from the hash map and store them in the packages_at_hub list.
def init_packages_at_hub():
    for i in range(1, 41):
        packages_at_hub.append(package_map.get(i))


# This is a wrapper function that takes in a list of trucks and an end_time and passes them into the run_truck function.
# Additionally, if there are still packages in packages_at_hub, it cycles through the truck list again and calls the
# load_truck function. This is to handle the remaining packages after the trucks have delivered everything they were
# initially loaded with.
def start_day(trucks, end_time=None):
    for truck in trucks:
        run_truck(truck, end_time)
    for truck in trucks:
        if packages_at_hub:
            load_truck(truck)
            run_truck(truck, end_time)
        else:
            break


# This function creates a dictionary at maps each package address in a truck's package list to a tuple containing a list
# of packages at that address and the total priority of those packages. This mapping is used to determine the next
# neighbor to visit in the route function.
# Priority is based on the package deadline. End of day packages have a priority of 1, and packages with earlier
# deadlines have higher priority values so that the routing function will be more likely to choose them.
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
            updated_entry = {package_address: (packages_at_address, updated_priority)}
            delivery_matrix.update(updated_entry)
        else:
            new_entry = {package_address: ([package], package_priority)}
            delivery_matrix.update(new_entry)
    return delivery_matrix

# This function determines a truck's next location based on the neighbor in the delivery matrix with the highest
# calculated score. This is a somewhat
# modified version the Nearest Neighbor Algorithm. Rather than picking the neighbor with the shortest distance to the
# truck's current location outright, the algorthm instead divides the neighbor's priority value by its distance. Because
# distance is in the denominator, if two neighbors share the same priority (meaning they have the same deadline), the
# one with the shorter distance will always have a higher score. However, a higher priority neighbor may have a higher
# score even if it's distance is greater.
def route_2(truck, current_location, delivery_matrix):
    neighbors = distance_map.get(current_location)
    best_neighbor = neighbors[0]
    best_neighbor_score = 0
    for neighbor in neighbors:
        neighbor_address = neighbor[0]
        neighbor_distance = neighbor[1]
        if not delivery_matrix.get(neighbor_address):
            continue
        neighbor_priority = delivery_matrix.get(neighbor_address)[1]
        print("Truck " + str(truck.id) + ":" + truck.location)
        print(neighbor_address)
        try:
            neighbor_score = neighbor_priority / neighbor_distance
        except ZeroDivisionError:
            neighbor_score = 0
        if neighbor_score > best_neighbor_score:
            best_neighbor = neighbor
            best_neighbor_score = neighbor_score
    packages_at_best_neighbor = delivery_matrix.get(best_neighbor[0])[0]
    truck.next_delivery = packages_at_best_neighbor
    return best_neighbor

# This function takes a truck and a location, and handles updating all the relevant data for the truck to travel there.
# It also handles checking if 10:20am has passed yet, and then it does a series of checks to determine the status of
# package 9, the one with the wrong address listed. If the package has not been delivered yet, it simply updates the
# address. If it has been delivered, it makes the truck travel back to pick it back up, then sends it to the correct
# address.
#
# The function also takes in an end_time parameter, which is a datetime. If travelling to the specified location would
# put the truck past this end time, the function returns 1, which will tell the run_truck function to terminate.
def goto(truck, location, end_time=None):
    miles = location[1]
    address = location[0]

    if truck.time >= datetime.datetime(2022, 1, 1, 10, 20) and package_map.get(9).address == "300 State St":
        if package_map.get(9) in truck.packages:
            package_map.get(9).address = "410 S State St"
            truck.make_delivery(truck.time)
        elif package_map.get(9) in truck.next_delivery:
            package_map.get(9).address = "410 S State St"
            truck.packages.append(package_map.get(9))
            truck.next_delivery.remove(package_map.get(9))
            if not truck.next_delivery:
                return
        elif package_map.get(9) in truck.delivered_packages:
            dist_list = distance_map.get(truck.location)
            dist = 0
            for item in dist_list:
                if item[0] == "300 State St":
                    dist = item[1]
            truck.packages.append(package_map.get(9))
            truck.delivered_packages.remove(package_map.get(9))
            goto(truck, ("300 State St", dist), end_time)
            return

    new_time = datetime.timedelta(hours=(miles / 18))
    if truck.time + new_time > end_time:
        return 1
    else:
        truck.time += new_time
    truck.add_mileage(miles)
    truck.location = address
    truck.make_delivery(truck.time)
    return 0

# This function simply returns a truck to the hub and updates the truck accordingly.
def go_home(truck):
    dist_list = distance_map.get(truck.location)
    dist_to_hub = -1
    for item in dist_list:
        if item[0] == "4001 South 700 East,":
            dist_to_hub = item[1]
    truck.time += datetime.timedelta(hours=(dist_to_hub / 18))
    truck.add_mileage(dist_to_hub)
    truck.location = "4001 South 700 East,"

# This function runs a single truck until it has no more packages left to deliver, then returns it to the hub.
# If the goto function returns 1, indicating that the end_time would have been exceeded travelling to the next location,
# the function terminates.
def run_truck(truck, end_time=None):
    if end_time:
        hour = int(end_time[0:2])
        minute = int(end_time[3:5])
        end_time = datetime.datetime(2022, 1, 1, hour, minute, 0)
    else:
        end_time = datetime.datetime(2022, 1, 1, 23, 59, 59)
    while truck.packages:
        truck_delivery_matrix = create_truck_delivery_matrix(truck)
        next_location = route_2(truck, truck.location, truck_delivery_matrix)
        goto_status = goto(truck, next_location, end_time)
        if goto_status == 1:
            return 0
    go_home(truck)

# This function removes packages from the packages_at_hub list and loads the into the specified truck until capacity is
# reached, or no more packages are left at the hub.
def load_truck(truck):
    while len(truck.packages) < 16 and packages_at_hub:
        first_package = packages_at_hub.pop(0)
        truck.add_package(first_package)

# This function handles the initial loading of the trucks. I am essentially hand-loading the trucks here. Packages
# meeting certain criteria go on specified trucks, and then the remainder of the trucks' capacity is filled with the
# next available package in packages_at_hub.
def load_trucks(truck_1, truck_2):
    packages_loaded = []
    for i in range(1, 41):
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
    return packages_loaded


# def print_truck_contents(truck):
#     truck.print_packages()

# Validates the time input by the user.
def validate_time_input(time_string):
    if len(time_string) < 5:
        return False
    if time_string[2] != ':':
        return False
    try:
        hour = int(time_string[0:2])
        minute = int(time_string[3:5])
        if hour < 8 or hour >= 24:
            return False
        if minute < 0 or minute >= 60:
            return False
    except ValueError:
        return False
    return True

# Formats and prints the status report to display to the console.
def print_status_report(trucks, report_time=None):
    if not report_time:
        report_time = 'END OF DAY'

    print("***********************************************************")
    print("\t\t\t\tSTATUS REPORT")
    print("***********************************************************")
    print("\n\nReport Time: " + str(report_time) + "\n\n")
    mileage_total = 0
    for truck in trucks:
        print("Truck " + str(truck.id) + " Miles: " + str(truck.odometer))
        mileage_total += truck.odometer
    print("Total Miles: " + str(mileage_total))
    for i in range(1, 41):
        package_map.get(i).print()
    print("\n\n***********************************************************\n\n")
    print("Press Enter to continue")
    input()

# Prints a formatted menu for the CLI.
def print_main_menu():
    print("--------------------------------------\n")
    print("\t\tWGUPS ROUTING PROGRAM")
    print("\t\tCreated by: Samuel Benning")
    print("\n--------------------------------------")
    print("\n\nType the number of the menu item, then press enter:\n")
    print("1. Set specific time and generate status report")
    print("2. Jump to End of Day (delivers all packages) and generate status.")
    print("3. Lookup package by ID")
    print("4. Quit the program")

# Resets the state of the program so that it can be run again.
def reset_state():
    packages_at_hub.clear()
    for i in range(1, 41):
        package = package_map.get(i)
        package.delivery_status = 'AT HUB'
        packages_at_hub.append(package)
    truck_1.odometer = 0
    truck_1.location = "4001 South 700 East,"
    truck_1.packages.clear()
    truck_1.next_delivery.clear()
    truck_1.time = datetime.datetime(2022, 1, 1, 0, 0, 0, 0)
    truck_1.time = truck_1.time + datetime.timedelta(hours=8)
    truck_2.odometer = 0
    truck_2.location = "4001 South 700 East,"
    truck_2.packages.clear()
    truck_2.next_delivery.clear()
    truck_2.time = datetime.datetime(2022, 1, 1, 0, 0, 0, 0)
    truck_2.time = truck_2.time + datetime.timedelta(hours=9, minutes=5)

# Provides the command line interface for the user.
def main():
    init_packages_at_hub()
    while True:
        print_main_menu()
        x = input()
        try:
            if int(x) == 1:
                print("Enter a time to generate status report. Please use 24-hour format HH:MM")
                input_time = input()
                if validate_time_input(input_time):
                    load_trucks(truck_1, truck_2)
                    start_day([truck_1, truck_2], input_time)
                    print_status_report([truck_1, truck_2], input_time)
                    reset_state()
                else:
                    print("INVALID TIME")
            elif int(x) == 2:
                load_trucks(truck_1, truck_2)
                start_day(([truck_1, truck_2]))
                print_status_report([truck_1, truck_2])
                reset_state()
        except ValueError:
            continue


main()
