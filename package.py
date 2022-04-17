class Package:
    def __init__(self, id, address, city, zip_code, deadline, weight, notes):
        self.id = id
        self.address = address
        self.city = city
        self.zip_code = zip_code
        self.weight = weight
        self.notes = notes
        self.delivery_status = 'AT HUB'
        self.delivery_time = None
        self.deadline = deadline


    def print(self):
        print("----------Package---------")
        print("ID:\t\t\t" + str(self.id))
        print("Street:\t\t" + self.address)
        print("City: \t\t" + self.city)
        print("Zip: \t\t" + self.zip_code)
        print("Deadline:\t" + str(self.deadline))
        print("Weight:\t\t" + self.weight)
        print("Status:\t\t" + str(self.delivery_status))
        print("Notes:\t\t" + self.notes)
