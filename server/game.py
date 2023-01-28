"""
Handles operations related to game and connections between player, board, chat and round
"""

from board import Board
from round import Round
import random

class Game(object):
    
    def __init__(self,id, players, thread):
        """Init the game! once player threshold is met
        :param id: int
        :param player: Player[]
        """
        self.id = id
        self.players = []
        self.words_used = []
        self.round = None
        self.board = Board()
        self.player_draw_ind = 0
        self.round_count = 0
        self.connected_thread = thread
        self.start_new_round()
        
    def start_new_round(self):
        """
        Starts a new round with a new word
        :return: None
        """
        round_word = self.get_word()
        self.round = Round(round_word, self.players[self.player_draw_ind], self.players, self)
        self.player_draw_ind +=1
        self.round_count += 1 
        
        if self.player_draw_ind >= len(self.players):
            self.end_round()
            self.end_game()
    
    
    def create_board(self):
        self.board = Board()
    
    def players_guess(self,player,guess):
        """
        Makes the player guess the word
        :param player: Player
        :param guess: str
        :return: bool
        """
        return self.round.guess(player,guess)
    
    def player_disconnected(self, player):
        """
        call to clean up objects when player disconnects
        :param player: Player
        :raises: Exception()
        """
        if player in self.players:
            player_ind = self.players.index(player)
            if player_ind >= self.player_draw_ind:
                self.player_draw_ind -=1
            self.players.remove(player)
            self.round.player_left(player)
        else:
            raise Exception("Player not in game")
    
        if len(self.players) <= 2:
            self.end_game()
    
    def skip(self):
        """
        Increments the round skips, if skips are greater than
        threshold, starts new round.
        :return: None
        """
        if self.round:
            new_round = self.round.skip()
            if new_round:
                    self.end_round()
        else:
            raise Exception("No round started yet!")
    
    def end_round(self):
        """
        If the round ends, call this
        :return: None
        """
        self.start_new_round()
        self.board.clear()
    
    def update_board(self, x, y, color):
        """
        calls update method on board
        :param x: int
        :param y: int
        :param color: int
        :return: None
        """
        
        if not self.board:
            raise Exception("No board created")
        self.board.update(x,y,color)
        
    
    def end_game(self):
        """
        ends the game
        """
        for player in self.players:
            self.round.player_left(player)
    
    
    def get_word(self):
        """
        gives a word that has not yet been used
        :return: str
        """
        with open("words.txt","r") as f:
            words = []
            
            for line in f:
                wrd = line.strip()
                if wrd not in self.words_used:
                    words.append(wrd)
            
            r = random.randint(0,len(words)-1)
            self.words_used.append(words[r].strip())
            return words[r].strip()
    
    