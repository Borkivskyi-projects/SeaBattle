from PodSixNet.Connection import connection, ConnectionListener

class Client(ConnectionListener):
    def __init__(self, host, port):
        self.Connect((host, port))
