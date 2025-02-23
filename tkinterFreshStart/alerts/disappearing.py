from math import sqrt, pow
from datetime import datetime, timedelta
from uuid import uuid4
class disappearing:
    def __init__(self):
        pass

    def step(self, locations):
        alertLocations = []
        if locations:
            for object in locations:
                    if (datetime.utcnow() - object['steps'][0]['time']).total_seconds() > 10:
                        print("object id: " + str(object['id']) + " has disappeared")
                        alertLocations.append({'objectID' : object['id'],
                                               'alertID' : uuid4(),
                                               'time': object['steps'][0]['time'],
                                               'x': object['steps'][0]['x'],
                                               'y': object['steps'][0]['y'],
                                               'w': object['steps'][0]['w'],
                                               'h': object['steps'][0]['h'],
                                               'dismissed': False,
                                               'type' : "Person has Disappeared"})
        if alertLocations != []:
            return alertLocations
        return None

