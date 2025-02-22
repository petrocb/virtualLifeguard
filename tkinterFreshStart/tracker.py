# from pip._internal import locations
# from datetime import datetime

# class tracker:
#
#     def __init__(self):
#         self.locations = None
#         self.lastLocation = None
#         self.ids = None
#
#     def track(self, results):
#         if not self.locations:
#             self.locations = []
#             self.lastLocation = []
#             for i in results:
#                 self.locations.append({'id': i['id'], 'steps': [{'time': datetime.utcnow(), 'x': i['xywh'][0], 'y': i['xywh'][1], 'w': i['xywh'][2], 'h': i['xywh'][3]}]})
#                 self.lastLocation.append({'id': i['id'], 'steps': [{'time': datetime.utcnow(), 'x': i['xywh'][0], 'y': i['xywh'][1], 'w': i['xywh'][2], 'h': i['xywh'][3]}]})
#             # self.locations = [results]
#             # for i in
#
#         else:
#             for o in results:
#                 for i in self.locations:
#                     if i['id'] == o['id']:
#                         # pass
#                         i['steps'].append({'time': datetime.utcnow(), 'x': o['xywh'][0], 'y': o['xywh'][1], 'w': o['xywh'][2], 'h': o['xywh'][3]})
#                         break
#
#                 self.locations.append({'id': i['id'], 'steps': [
#                     {'time': datetime.utcnow(), 'x': o['xywh'][0], 'y': o['xywh'][1], 'w': o['xywh'][2], 'h': o['xywh'][3]}]})
#             for o in results:
#                 closest = None
#                 closestID = None
#                 for i in self.lastLocation:
#                     dif = abs(o['xywh'][0] - i['steps'][0]['x']) + abs(o['xywh'][1] - i['steps'][0]['y'])
#                     if closest and dif < closest:
#                         closest = dif
#                         closestID = o['id']
#                     else:
#                         closest = dif
#                         closestID = o['id']
#





        # else:
        #     for i in locations:
        #         pass
        #     self.locations.append(results)

from datetime import datetime

class tracker:
    def __init__(self):
        self.locations = None
        self.unfoundLocations = None

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
                    # for m in range(len(r.boxes.xywh)):
                    # for m in self.locations:
                    #     if m['id'] == o['id']:
                    #         m['steps'].append(
                    #             {'time': datetime.utcnow(), 'x': o['xywh'][0], 'y': o['xywh'][1],
                    #              'w': o['xywh'][2],
                    #              'h': o['xywh'][3]})
                    #         break

                    # if any(loc['id'] == o['id'] for loc in self.locations):
                    #     loc['steps'].append(
                    #         {'time': datetime.utcnow(), 'x': o['xywh'][0], 'y': o['xywh'][1],
                    #          'w': o['xywh'][2],
                    #          'h': o['xywh'][3]})

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


                        # for i in m['yoloIDs']:
                        #     if i == o['id']:
                        #         m['steps'].append(
                        #             {'time': datetime.utcnow(), 'x': o['xywh'][0], 'y': o['xywh'][1],
                        #              'w': o['xywh'][2],
                        #              'h': o['xywh'][3]})
                        #         break

                #     "xywh": r.boxes.xywh[i].tolist(),  # Convert tensor to list
                # "cls": int(r.boxes.cls[i].item()),  # Convert single-value tensor to int
                # "id": int(r.boxes.id[i].item()),  # Convert single-value tensor to int
                # "conf": float(r.boxes.conf[i].item())  # Convert single-value tensor to float
                # })
        # pass

