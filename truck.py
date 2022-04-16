import datetime

from package import Package

class Truck:
    def __init__(self, id, location):
        self.id = id
        self.odometer = 0
        self.location = location
        self.time = None
        self.packages = []
        self.next_delivery = []
        self.delivered_packages = []

    def add_package(self, package):
        package.delivery_status = 'IN TRANSIT - ON TRUCK #' + str(self.id)
        self.packages.append((package))

    def remove_package(self, package):
        self.packages.remove(package)

    def make_delivery(self, timestamp):
        for i in range(len(self.next_delivery)):
            package = self.next_delivery[0]
            package.delivery_status = 'DELIVERED AT ' + str(timestamp) + ' by TRUCK #' + str(self.id)
            self.next_delivery.remove(package)
            self.packages.remove(package)
            self.delivered_packages.append(package)

    def add_mileage(self, miles):
        if miles >= 0:
            self.odometer += miles

    def print_packages(self):
        for package in self.packages:
            package.print()

    def print_package_list(self):
        package_list = []
        for package in self.packages:
            package_list.append((package.id, package.notes))
        print(package_list)

