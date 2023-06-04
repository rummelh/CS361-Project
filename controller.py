import mysql.connector
import zmq
import json

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

cnx = mysql.connector.connect(user = 'cs340_rummelh', password = '3496', host = 'classmysql.engr.oregonstate.edu',
database = 'cs340_rummelh')

cursor = cnx.cursor()

query = ("SELECT product_name, inventory_level FROM Products")

cursor.execute(query)

json_dict = {}

for product_name, inventory_level in cursor:
    json_dict[product_name] = inventory_level

json_file = json.dumps(json_dict)

socket.send_json(json_file)

message = socket.recv_json()
print(f"received reply [ {message}]")