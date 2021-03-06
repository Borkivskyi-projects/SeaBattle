import sys
from time import sleep

from PodSixNet.Connection import connection, ConnectionListener


class Client(ConnectionListener):
    def __init__(self, host, port, name):
        self.Connect((host, port))
        self.name = name
        #self.players = {}
        connection.Send({"action": "nickname", "message": self.name})

    def Loop(self):
        self.Pump()
        connection.Pump()

    def Input(self):
        connection.Send({"action": "message", "message": '1','name':self.name})
        
    def Network_show_games(self, data):
        print("Choose one of the games:\n")
        print(data['message'])
        choice = input("Your choice: ")
        connection.Send({"action": "game_choice", "message": choice})

    def Network_message(self, data):
        print(data['name'] + ": " + data['message'])

    def Network_connected(self, data):
        self.statusLabel = "connected"

    def Network_error(self, data):
        print(data)
        self.statusLabel = data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        self.statusLabel = "disconnected"


if len(sys.argv) != 2:
    #print("Usage:", sys.argv[0], "host:port")
    #print("e.g.", sys.argv[0], "localhost:31425")
    host, port = '', 8000
else:
    host, port = sys.argv[1].split(":")
    
c = Client(host, int(port), input("Enter your username: "))
while 1:
    c.Loop()
    sleep(0.001)
