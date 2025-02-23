from math import sqrt, pow
from datetime import timedelta
class velocity:
    def __init__(self):
        pass

    def step(self, locations):
        frames = 5
        frames -= 1
        alertLocations = []
        if locations:
            for object in locations:
                object['steps'] = list(reversed(object['steps']))
            for object in locations:
                if len(object['steps']) > frames:
                    distance = sqrt(pow(object['steps'][frames]['x'] - object['steps'][0]['x'], 2) + pow(object['steps'][frames]['y'] - object['steps'][0]['y'], 2))
                    velocity = distance / (object['steps'][0]['time'] - object['steps'][frames]['time']).total_seconds()
                    print("The velocity of object id: " + str(object['id']) + " is " + str(velocity))

        return alertLocations

