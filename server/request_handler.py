"""
MAIN THREAD
handles all of connections, creating new games and requests from the client(s).
"""

import socket
import threading
import time
from player import Player
from game import Game
from queue import Queue
import json

class Server(object):
    PLAYERS = 8
    
    def __init__(self):
        self.connection_queue = []
        self.gameId = 0

    def player_thread(self,conn, player):
        """
        handles in game communication between clients
        :param conn: connection object
        :param ip: str
        :param name: str
        :return: None
        """
        while True:
            try:
                # Receive request
                data = conn.recv(1024)
                data = json.loads(data)
                
                # Player is not part of game
                keys = [keys for key in data.keys()]
                send_msg = {key:[] for key in keys}
                
                for key in keys:
                    if key == -1: # get game, this returns a list of players
                        if player.game:
                            send_msg[key] = player.game.players
                        else:
                            send_msg[key] = []

                    if player.game:
                        if key == 0: # guess
                            correct = player.game.player_guess(player, data[0][0])
                            send_msg[key] = correct

                        elif key == 1: ## skip
                            skip = player.game.skip()
                            send_msg[key] = skip

                        elif key == 2: # get chat
                            content = player.game.round.chat.get_chat()
                            send_msg[key] = content

                        elif key == 3: # get board
                            brd = player.game.round.board.get_board()
                            send_msg[key] = brd

                        elif key == 4: # get score
                            scores = player.game.get_scores()
                            send_msg[key] = scores

                        elif key == 5: # get round
                            rnd = player.game.rount_count
                            send_msg[key] = rnd

                        elif key == 6: # get round
                            wrd = player.game.round.word
                            send_msg[key] = wrd

                        elif key == 7: #get skips
                            skips = player.game.round.skips
                            send_msg[key] = skips

                        elif key == 8: #update board
                            x,y,color = data[8][0][:3]
                            self.game.update_board(x,y,color)

                        elif key == 9: #get round time
                            t = player.game.round.time
                            send_msg[key] = t
                            
                        else:
                            raise Exception("Not a valid request")
                
                conn.sendall(json.dumps(send_msg))
            except Exception as e:
                print('[EXECPTION]', player.get_name(), 'disconnected')
                conn.close()
                

    def handle_queue(self,player):
        """
        adds player to queue and creates a new game if enough players
        """
        self.connection_queue.append(player)
        
        if len(self.connection_queue) >= 8:
            game = Game(players=self.connection_queue[:], id=self.gameId)
            
            for p in self.connection_queue:
                p.set_game(game)
            
            self.gameId +=1
            self.connection_queue = []
                
            

    def authentication(self,conn, addr):
        try:
            data = conn.recv(1024)
            name = str(data.decode())
            if not name:
                raise Exception("No name received")
        
            conn.sendall("1".encode())
            
            player = Player(addr, name)
            self.handle_queue()
            
            threading.Thread(target=self.player_thread, args=(conn,addr,name))
            
        except Exception as e:
            print('[EXCEPTION]',e)
            conn.close()
    

    def connection_thread(self):
        server = "localhost"
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server,port))
        except socket.error as e:
            str(e)
            
        s.listen(1)
        print('Waiting for a connection, server started')

        while True:
            conn, addr = s.accept()
            print('New connection!')
            
            self.authentication(conn,addr)
            
if __name__=="__main__":
    s = Server()
    threading.Thread(target=s.connection_thread())