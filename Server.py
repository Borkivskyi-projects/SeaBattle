from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ServerChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.id = str(self._server.NextId())
        intid = int(self.id)


class GameServer(Server):
    channelClass = ServerChannel

    def __init__(self, *args, **kwargs):
        self.id = 0
        Server.__init__(self, *args, **kwargs)
        self.players = {}
        print('Server started')

    def Connected(self, channel, addr):
        self.AddPlayer(channel)

    def AddPlayer(self, player):
        print("New Player" + str(player.addr))
        self.players[player] = True
        player.Send({
            "action": "initial", 
            "lines": dict([(p.id, {"color": p.color, "lines": p.lines}) for p in self.players])})
        #self.SendPlayers()