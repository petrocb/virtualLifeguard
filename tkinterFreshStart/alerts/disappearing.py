from math import sqrt, pow
from datetime import datetime, timedelta
class disappearing:
    def __init__(self):
        pass

    def step(self, locations):
        # frames = 5
        # frames -= 1
        alertLocations = []
        if locations:
            for object in locations:
                    if (datetime.utcnow() - object['steps'][0]['time']).total_seconds() > 10:
                        # distance = sqrt(pow(object['steps'][frames]['x'] - object['steps'][0]['x'], 2) + pow(object['steps'][frames]['y'] - object['steps'][0]['y'], 2))
                        # velocity = distance / (object['steps'][0]['time'] - object['steps'][frames]['time']).total_seconds()
                        print("object id: " + str(object['id']) + " has disappeared")

        return alertLocations

