import sys
from time import sleep

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ServerChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        print("Deleting Player" + str(self.addr))
        del self._server.players[self]
        self._server.SendPlayers()

    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "name": data['name']})


class GameServer(Server):
    channelClass = ServerChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = {}
        print('Server started')
        self.games = []
        self.game_id = 0

    def Connected(self, channel, addr):
        print("New Player" + str(channel.addr))
        self.players[channel] = True
        #channel.Send({"action": "initial", 'message':'Pryvit Anton'})
        self.SendPlayers()

    def SendPlayers(self):
        self.SendToAll({'action':'message','name':'server','message':','.join([str(p) for p in range(len(self.players))])})

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)

# get command line argument of server, port
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("e.g.", sys.argv[0], "localhost:31425")
else:
    host, port = sys.argv[1].split(":")
    s = GameServer(localaddr=(host, int(port)))
    s.Launch()