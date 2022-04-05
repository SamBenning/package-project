from package import Package

class Truck:
    def __init__(self, id, location):
        self.id = id
        self.odometer = 0
        self.location = location
        self.time = None
        self.packages = []
        self.next_delivery = []

    def add_package(self, package):
        package.delivery_status = 'IN TRANSIT - ON TRUCK #' + str(self.id)
        self.packages.append((package))

    def remove_package(self, package):
        # print("BEFORE REMOVE: " + str(self.packages))
        self.packages.remove(package)
        # print("AFTER REMOVE: " + str(self.packages))

    def make_delivery(self, timestamp):
        print("AT: " + str(self.location))
        print("DELIV QUEUE: " + str(self.next_delivery))
        print("---START DELIVERY---")
        for i in range(len(self.next_delivery)):
            package = self.next_delivery[0]
            package.delivery_status = 'DELIVERED AT ' + str(timestamp) + 'by TRUCK #' + str(self.id)
            self.next_delivery.remove(package)
            print("Delivered package #" + str(package.id))
            self.packages.remove(package)
        print("---END DELIVERY---")

    def add_mileage(self, miles):
        if miles >= 0:
            self.odometer += miles

    def print_packages(self):
        # print(self.packages)
        for package in self.packages:
            package.print()

    def print_package_list(self):
        package_list = []
        for package in self.packages:
            package_list.append((package.id, package.notes))
        print(package_list)

