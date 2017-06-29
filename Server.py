# При виходженні з однієї з ігор одного з гравців,
# інший гравець автоматично або закидається в останню існуючу гру,
# або в новостворенну, залежно від заповненості.
# Попередня гра при цьому не видаляється


# Як варіант:
# При видаленні гри проходитися циклом по всіх іграх,
# і переприсвоювати game_index на поточний індекс в списку
# На обмін даними не має вплинути, бо всі цифри відповідно зміняться
# був індекс 4 і позиція 4 - паралельно зсунуться на 3

# при видаленны сортувати ігри за к-стю гравців по спаданню


import sys
from time import sleep

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel


class ServerChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        self.in_game = False

    def Close(self):
        """
        TODO
        Reorganize games after closed client
        """
        print("Deleting Player" + str(self.addr))
        
        for game in self._server.games:
            if self in game.players:
                game.players.remove(self)
        
        '''
        this_game_index = game.game_index
        game.players.remove(self)
        last_player = game.players[0]
        self._server.games.remove(game)
        self._server.games.insert(this_game_index, Game())
        self._server.games[this_game_index].append(last_player)
        self._server.SendPlayers(this_game_index)
        '''

    def Network_nickname(self, data):
        self.nickname = data["message"]
        self._server.SendPlayers(self._server.game_index)

    def Network_message(self, data):
        self._server.SendToAll({"action": "message", "message": data['message'], "name": data['name']})
    
    def Network_game_choice(self, data):
        self._server.Add_player(self, int(data['message']))


class GameServer(Server):
    channelClass = ServerChannel
    AMOUNT_OF_GAMES = 5

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        print('Server started')
        self.game_index = 0
        
        self.games = [Game(i) for i in range(self.AMOUNT_OF_GAMES)]
        

    def Connected(self, channel, addr):
        print("New Player" + str(channel.addr))
        #self.players[channel] = True
        #channel.Send({"action": "initial", 'message':'Pryvit Anton'})
        
        '''
        if len(self.games[-1].players) == 2:
            self.game_index += 1
            self.games.append(Game(self.game_index))

        self.games[-1].players.append(channel)
        '''
        channel.Send({'action':'show_games', 'message':self.games_in_str()})
        
        #self.SendPlayers(self.game_index)
    
    def games_in_str(self):
        line = ''
        
        def return_game_player(game_index, player):
            try:
                return self.games[game_index].players[player].nickname
            except:
                return 'None'
                
        for i in range(self.AMOUNT_OF_GAMES):
            line += return_game_player(i, 0) + ' :Game '+str(i)+': ' + return_game_player(i, 1)+'\n'
        
        return line[:-1]

    def Add_player(self, player, game_index):
        print("Trying to add "+player.nickname+' to Game '+str(game_index)+' - ',end='')
        try_game = self.games[game_index]
        result = 'Added!'
        if not player.in_game and len(try_game.players) < 2:
            try_game.players.append(player)
            player.in_game = True
        else:
            result ="Rejected!"
        print(result)
        player.Send({'action':'show_games', 'message':'\n'+result+'\n'+self.games_in_str()})
        
    def SendToGame(self, game_index, data):
        [p.Send(data) for p in self.games[game_index].players]

    def SendPlayers(self, game_index):
        self.SendToGame(game_index, {'action':'message','name':'server','message':'players: ' + ','.join([p.nickname for p in self.games[game_index].players])})

    def SendToAll(self, data):
        [p.Send(data) for p in self.players]

    def Launch(self):
        while True:
            self.Pump()
            sleep(0.0001)


class Game():
    def __init__(self, index):
        self.game_index = index
        self.players = []
        


# get command line argument of server, port
if len(sys.argv) != 2:
    #print("Usage:", sys.argv[0], "host:port")
    #print("e.g.", sys.argv[0], "localhost:31425")
    host, port = '0.0.0.0', 8000
else:
    host, port = sys.argv[1].split(":")
s = GameServer(localaddr=(host, int(port)))
s.Launch()
