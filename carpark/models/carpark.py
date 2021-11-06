class CarPark:
    long = 0
    lat = 0
    name = ""
    freeSpace = 0
    distanceInKm = 0
     
    def __init__(self, long, lat, name, freeSpace):
        self.long = long
        self.lat = lat
        self.name = name
        self.freeSpace = freeSpace