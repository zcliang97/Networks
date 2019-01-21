class PacketEvent:

    def __init__(self, _type, arrivalTime, length):
        self.type = _type
        self.arrivalTime = arrivalTime
        self.length = length
        self.departureTime = 0.0

    def calculateDeparture(self)
        self.