from math import sqrt, pow
from datetime import datetime, timedelta
class velocity:
    def __init__(self):
        pass

    def step(self, locations):
        frames = 5
        frames -= 1
        alertLocations = []
        if locations:
            # for object in locations:
            #     object['steps'] = list(reversed(object['steps']))
            for object in locations:
                if len(object['steps']) > frames:
                    if (datetime.utcnow() - object['steps'][0]['time']).total_seconds() < 5:
                        distance = sqrt(pow(object['steps'][frames]['x'] - object['steps'][0]['x'], 2) + pow(object['steps'][frames]['y'] - object['steps'][0]['y'], 2))
                        velocity = distance / (object['steps'][0]['time'] - object['steps'][frames]['time']).total_seconds()
                        print("The velocity of object id: " + str(object['id']) + " is " + str(velocity))
                        alertLocations.append({'id': object['id'], 'time': object['steps'][0]['time'],
                                               'x': object['steps'][0]['x'], 'y': object['steps'][0]['y'],
                                               'w': object['steps'][0]['w'], 'h': object['steps'][0]['h'],
                                               'dismissed': False})

        return alertLocations

