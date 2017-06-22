import sys
from time import sleep

from PodSixNet.Connection import connection, ConnectionListener


class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
        self.players = {}

    def Loop(self):
        self.Pump()
        connection.Pump()

    def Network_initial(self, data):
        #self.players = data['lines']
        print(data['message'])

    def Network_connected(self, data):
        self.statusLabel = "connected"

    def Network_error(self, data):
        print(data)
        import traceback
        traceback.print_exc()
        self.statusLabel = data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        self.statusLabel += " - disconnected"


if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    c = Client(host, int(port))
    while 1:
        c.Loop()
        sleep(0.001)
