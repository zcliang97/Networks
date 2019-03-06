TRANSMISSION_RATE = 1000000 # 1 Mbps

class Packet:
    def __init__(self, length):
        self.length = length

    def getTransmissionTime(self):
        return self.length / TRANSMISSION_RATE
