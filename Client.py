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
        self.Events()

        if "connecting" in self.statusLabel:
            self.statusLabel = "connecting..."


if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    c = Client(host, int(port))
    while 1:
        c.Loop()
        sleep(0.001)
