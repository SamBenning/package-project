import csv
from hash import HashMap
from package import Package


def get_distance_map():
    distance_map = HashMap(64)
    header_addresses = []
    with open("distance-table.csv", 'r', newline='') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, '')
        flag = False
        addresses_added = 0
        for k, row in enumerate(reader):
            if flag:
                street_address = row[0].splitlines()[1].strip()
                # distance_list_row = []
                # print(row[2])
                for i in range(2, len(row)):
                    if row[i]:
                        current_address = header_addresses[i-2]
                        print(row[1])
                        # current_address = row[1][0:(len(row[1]-8))]
                        current_distance = float(row[i])
                        distance_pair_row = (current_address, current_distance)
                        # distance_list_row.append(distance_pair_row)
                        distance_pair_column = (street_address, current_distance)
                        # print("distance_pair row = " + str(distance_pair_row))
                        # print("street address = " + str(street_address))
                        current_row_pairs = distance_map.get(street_address)
                        current_column_pairs = distance_map.get(current_address)
                        if not current_row_pairs:
                            current_row_pairs = []
                        if not current_column_pairs:
                            current_column_pairs = []

                        # print(current_row_pairs)
                        current_row_pairs.append(distance_pair_row)
                        # print(current_row_pairs)
                        if distance_pair_column not in current_column_pairs:
                            current_column_pairs.append(distance_pair_column)

                        distance_map.add(street_address, current_row_pairs)
                        distance_map.add(current_address, current_column_pairs)
                        # print("got this far")

                if addresses_added < len(header_addresses):
                    # distance_map.add(header_addresses[addresses_added], distance_list_row)
                    addresses_added += 1
                continue

            if row[0] == 'DISTANCE BETWEEN HUBS IN MILES':
                del row[0:2]
                for heading in row:
                    items = heading.splitlines()
                    current_heading = items[1].strip()
                    header_addresses.append(current_heading)
                    distance_map.add(current_heading, [])
                flag = True
                distance_map.print()
    return distance_map


def get_package_map():
    package_map = HashMap(64)
    with open("package-file.csv", 'r', newline='') as package_file:
        package_reader = csv.reader(package_file, delimiter=",", quotechar='"')
        next(package_reader, '')
        flag = False
        for row in package_reader:
            if flag:
                package = Package(int(row[0]), row[1], row[2], row[4], row[5], row[6], row[7])
                package_map.add(int(row[0]), package)
                package.print()
            if row[0] == 'Package\nID':
                flag = True
    return package_map
