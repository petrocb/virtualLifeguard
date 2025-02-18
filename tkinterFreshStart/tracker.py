from pip._internal import locations
from datetime import datetime

class tracker:

    def __init__(self):
        self.locations = None
        self.lastLocation = None
        self.ids = None

    def track(self, results):
        if not self.locations:
            self.locations = []
            self.lastLocation = []
            for i in results:
                self.locations.append({'id': i['id'], 'steps': [{'time': datetime.utcnow(), 'x': i['xywh'][0], 'y': i['xywh'][1], 'w': i['xywh'][2], 'h': i['xywh'][3]}]})
                self.lastLocation.append({'id': i['id'], 'steps': [{'time': datetime.utcnow(), 'x': i['xywh'][0], 'y': i['xywh'][1], 'w': i['xywh'][2], 'h': i['xywh'][3]}]})
            # self.locations = [results]
            # for i in

        else:
            for o in results:
                for i in self.locations:
                    if i['id'] == o['id']:
                        # pass
                        i['steps'].append({'time': datetime.utcnow(), 'x': o['xywh'][0], 'y': o['xywh'][1], 'w': o['xywh'][2], 'h': o['xywh'][3]})
                        break

                self.locations.append({'id': i['id'], 'steps': [
                    {'time': datetime.utcnow(), 'x': o['xywh'][0], 'y': o['xywh'][1], 'w': o['xywh'][2], 'h': o['xywh'][3]}]})
            for o in results:
                closest = None
                closestID = None
                for i in self.lastLocation:
                    dif = abs(o['xywh'][0] - i['steps'][0]['x']) + abs(o['xywh'][1] - i['steps'][0]['y'])
                    if closest and dif < closest:
                        closest = dif
                        closestID = o['id']
                    else:
                        closest = dif
                        closestID = o['id']






        # else:
        #     for i in locations:
        #         pass
        #     self.locations.append(results)






