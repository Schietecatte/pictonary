"""
Represents a player object on the server side
"""

from .game import Game

class Player(object):
    def __init__(self, ip, name):
        """
        init the player object
        :param ip: str
        :param name: str
        """
        self.game = None
        self.ip = ip
        self.name = name
        self.score = 0
        
    def set_game(self,game):
        """
        set the players game association
        :param game: Game
        :return: None
        """
        self.game = game

    def update_score(self,x):
        self.score += x

    def guess(self, wrd):
        """
        makes a player guess
        :param wrd: str
        :retrun: bool
        """
        return self.game.players_guess(self,wrd)

    def disconnect(self):
        pass

    def get_ip(self):
        """
        get player ip address
        :return: str
        """
        return self.ip

    def get_name(self):
        """
        get player name
        :return: str
        """
        return self.name
    
    def get_score(self):
        """
        get player scores
        :return: int
        """
        return self.score