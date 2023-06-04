## Server ##

import time
import json
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    request = socket.recv_json()
    print(f"Received request: {request}")

    #  Do some 'work'
    time.sleep(1)

    #  Find values
    json_dict = json.loads(request)
    min_val = 10
    under_min = {}
    for key in json_dict:
        if key == "Min Value":
            min_val = json_dict[key]
        if json_dict[key] < min_val:
            under_min[key] = json_dict[key]

    #   Send back keys under min value
    json_file = json.dumps(under_min)
    socket.send_json(json_file)