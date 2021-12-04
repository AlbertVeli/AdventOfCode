import numpy as np

class Board:
    def __init__(self, lines):
        self.board = np.array(lines, int)

    def __str__(self):
        return(self.board.__str__())

    def win(self, drawn):
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
        not_marked = []
        # numpy magic
        board1d = self.board.reshape(25)
        mask = np.in1d(board1d, drawn)
        not_marked = board1d[np.where(~mask)[0]]
        return sum(not_marked) * last_num
