""" 
Stores the state of the drawnig board.
"""

class Board(object):
    ROWS = COLS = 720

    def __init__(self):
        """
        Init the board by creating empty board (all white pixels)
        """
        self.data = self._create_empty_board()

    def update(self, x,y,color):
        """
        updates a singular pixel of the boar
        :param x: int
        :param y: int
        :param color: (int,int,int)
        :return:
        """
        self.data[y][x] = color

    def clear(self):
        """
        clears the board to all white
        :return: None
        """
        self.data = self._create_empty_board()

    def _create_empty_board(self):
        """
        creates an empty board of white pixels
        :return: None
        """
        return [[(255,255,255) for _ in range(self.COLS)] for _ in range (self.ROWS)]

    def fill(self, x, y):
        """
        fills in a specific shape or area using recursion
        :param x: int
        :param y: int
        :return: None
        """
        pass

    def get_board(self):
        """
        gets the data of the board
        :return: (int,int,int)[]
        """
        return self.data