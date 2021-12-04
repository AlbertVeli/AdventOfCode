import numpy as np

class Board:
    def __init__(self, lines):
        self.board = np.array(lines, int)

    def __str__(self):
        """ This is run for print(board) """
        return(self.board.__str__())

    def win(self, drawn):
        """ Did I win yet? Did I? Please! """
        # rows
        for row in self.board:
            mask = np.in1d(row, drawn)
            nmark = len(np.where(mask)[0])
            if nmark == 5:
                return True

        # cols
        for col in range(5):
            mask = np.in1d(self.board[:,col], drawn)
            nmark = len(np.where(mask)[0])
            if nmark == 5:
                return True

        return False

    def score(self, last_num, drawn):
        """
        My totally logic score which is:
        sum of all numbers *not* drawn
        times last number drawn.
        Some serious numpy magic going on.
        """
        board1d = self.board.reshape(25)
        mask = np.in1d(board1d, drawn)
        not_marked = board1d[np.where(~mask)[0]]
        return sum(not_marked) * last_num
