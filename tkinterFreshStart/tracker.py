from datetime import datetime, timedelta
from copy import deepcopy
from random import randint
import json
class tracker:
    def __init__(self):
        self.locations = None

    def track(self, yoloResults):
        results = []
        for r in yoloResults:
            for i in range(len(r.boxes.xywh.tolist())):
                try:
                    if r.boxes.id is not None and int(r.boxes.cls[i].item()) == 0: # sometimes when there is a lot of change between frames YOLO doesn't attribute Ids, similar to this bug report: https://github.com/ultralytics/ultralytics/issues/3399
                        results.append({
                                    "xywh": r.boxes.xywh[i].tolist(),
                                    "cls": int(r.boxes.cls[i].item()),
                                    "id": int(r.boxes.id[i].item()),
                                    "conf": float(r.boxes.conf[i].item())
                                })

                except Exception as e:
                    raise(e)
                    print(e)
            res = []
            for r in results:
                if "id" in r:
                    res.append(r['id'])
            print(res)
            if self.locations is None:
                self.locations = []
                for i in results:
                    self.locations.append({
                        'id': i['id'],
                        'yoloIDs': [i['id']],
                        'class': i['cls'],
                        'steps': [{
                            'time': datetime.utcnow(),
                            'x': i['xywh'][0],
                            'y': i['xywh'][1],
                            'w': i['xywh'][2],
                            'h': i['xywh'][3]
                        }]
                    })
            else:
                for o in results:
                # if result id matches a location id - add a step to existing location id
                    match = next((loc for loc in self.locations if loc['id'] == o['id']), None)
                    if match:
                        print('we matched id: ' + str(match['id']))
                        match['steps'].append({
                            'time': datetime.utcnow(),
                            'x': o['xywh'][0],
                            'y': o['xywh'][1],
                            'w': o['xywh'][2],
                            'h': o['xywh'][3]
                        })
                    else:
                        # if the result is near an existing location which doesn't appear in these results - replace the
                        # location id with the result id
                        for loc in self.locations:
                            if (abs(o['xywh'][0] - loc['steps'][-1]['x']) < 200 and
                                    abs(o['xywh'][1] - loc['steps'][-1]['y']) < 200 and
                                    not any(oldresult['id'] == loc['id'] for oldresult in results)):
                                print('we swapped an id: ' + str(loc['id']) + ' with: ' + str(o['id']))
                                loc['id'] = o['id']
                                loc['steps'].append({
                                    'time': datetime.utcnow(),
                                    'x': o['xywh'][0],
                                    'y': o['xywh'][1],
                                    'w': o['xywh'][2],
                                    'h': o['xywh'][3]
                                })
                                break

                    # if we still haven't added the current result id into the locations, add a new location id
                    if not any(loc['id'] == o['id'] for loc in self.locations):
                        print('we added a new id: ' + str(o['id']))
                        self.locations.append({
                            'id': o['id'],
                            'yoloIDs': [o['id']],
                            'class': o['cls'],
                            'steps': [{
                                'time': datetime.utcnow(),
                                'x': o['xywh'][0],
                                'y': o['xywh'][1],
                                'w': o['xywh'][2],
                                'h': o['xywh'][3]
                            }]
                        })

    def getLocations(self):
        if self.locations:
            returnList = deepcopy(self.locations)
            for object in returnList:
                object['steps'] = list(reversed(object['steps']))
            return returnList
        return None

    def convert2dateTime(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()

    def saveLocations2File(self, createLogs):
        rand = randint(0, len(self.locations) - 1)
        if self.locations[rand]['steps'][0]['time'] < datetime.utcnow() - timedelta(seconds = 90):
            if self.locations[rand]['steps'][-1]['time'] < datetime.utcnow() - timedelta(seconds = 60):
                if createLogs:
                    filePath = f"logs/{str(datetime.utcnow().isoformat()).replace(":", "")}Archive{str(self.locations[rand]['id'])}.json"
                    with open(filePath, "w") as json_file:
                        json.dump(self.locations[rand], json_file, default=self.convert2dateTime, indent=5)
                self.locations.pop(rand)
            else:
                stepsToArchive = []
                for i in self.locations[rand]['steps']:
                    if i['time'] < datetime.utcnow() - timedelta(seconds = 60):
                        if createLogs:
                            stepsToArchive.append(i)
                        self.locations[rand]['steps'].remove(i)
                if createLogs:
                    partArchive = {
                            'id': self.locations[rand]['id'],
                            'class': self.locations[rand]['class'],
                            'steps': stepsToArchive
                    }
                    filePath = f"logs/{str(datetime.utcnow().isoformat()).replace(":", "")}PartialArchive{str(partArchive['id'])}.json"
                    with open(filePath, "w") as json_file:
                        json.dump(partArchive, json_file, default=self.convert2dateTime, indent=5)
                # self.locations.pop(rand)

        # if len(self.locations[0]['steps']) >= 1000:
        #     for i in self.locations:
        #         del i['steps'][499:1000]
