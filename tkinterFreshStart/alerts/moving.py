class Moving:
    def __init__(self):
        pass

    def step(self, locations):
        alertLocations = []
        if locations:
            for object in locations:
                object['steps'] = list(reversed(object['steps']))

            for object in locations:
                if len(object['steps']) > 1:
                    print("x0:", round(object['steps'][0]['x']), "x1:", round(object['steps'][1]['x']), "y0:", round(object['steps'][0]['y']), "y1:", round(object['steps'][1]['y']))
                    if round(object['steps'][0]['x']) != round(object['steps'][1]['x']) or round(object['steps'][0]['y']) != round(object['steps'][1]['y']):
                        alertLocations.append(object)

        return alertLocations

