import csv
from hash import HashTable
from package import Package

# This function uses the distance-table csv file to generate a distance map using the custom hash table class
# found in hash.py. It works by iterating through each row, column cell. It creates a pairing of both row, column, and
# column row, then it adds that pairing to the distance list of both the respective row address and column address.
# This is necessary to store all distance pairings. If we just add the row, column pairs to the hash table, we only
# get half of the distance pairings, and not the full.
def get_distance_map():
    distance_map = HashTable(64)
    header_addresses = []
    with open("distance-table.csv", 'r', newline='') as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        next(reader, '')
        flag = False
        addresses_added = 0
        for k, row in enumerate(reader):
            if flag:
                street_address = row[0].splitlines()[1].strip()
                if street_address == "3575 W Valley Central Sta bus Loop":
                    street_address = "3575 W Valley Central Station bus Loop"
                for i in range(2, len(row)):
                    if row[i]:
                        current_address = header_addresses[i-2]
                        current_distance = float(row[i])
                        distance_pair_row = (current_address, current_distance)
                        distance_pair_column = (street_address, current_distance)
                        current_row_pairs = distance_map.get(street_address)
                        current_column_pairs = distance_map.get(current_address)
                        if not current_row_pairs:
                            current_row_pairs = []
                        if not current_column_pairs:
                            current_column_pairs = []
                        current_row_pairs.append(distance_pair_row)
                        if distance_pair_column not in current_column_pairs:
                            current_column_pairs.append(distance_pair_column)
                        distance_map.add(street_address, current_row_pairs)
                        distance_map.add(current_address, current_column_pairs)
                if addresses_added < len(header_addresses):
                    addresses_added += 1
                continue
            if row[0] == 'DISTANCE BETWEEN HUBS IN MILES':
                del row[0:2]
                for heading in row:
                    items = heading.splitlines()
                    current_heading = items[1].strip()
                    if current_heading == "3575 W Valley Central Sta bus Loop":
                        current_heading = "3575 W Valley Central Station bus Loop"
                    header_addresses.append(current_heading)
                    distance_map.add(current_heading, [])
                flag = True
    return distance_map

# This is much simpler than the distance table. It creates a hash table out of the package-file csv by iterating
# through each row and creating a new Package object by feeding the appropriate cell data into the package constructor.
def get_package_map():
    package_map = HashTable(64)
    with open("package-file.csv", 'r', newline='') as package_file:
        package_reader = csv.reader(package_file, delimiter=",", quotechar='"')
        next(package_reader, '')
        flag = False
        for row in package_reader:
            if flag:
                package = Package(int(row[0]), row[1], row[2], row[4], row[5], row[6], row[7])
                package_map.add(int(row[0]), package)
            if row[0] == 'Package\nID':
                flag = True
    return package_map
