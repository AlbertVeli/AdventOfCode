class Notgameboy:

    # prog = list of (instr, int) tuples
    def __init__(self, prog):
        self.prog = list(prog)
        self.plen = len(self.prog)
        self.reset()

    def reset(self):
        self.finished = False
        self.loop = False
        self.pc = 0
        self.acc = 0
        self.visited = []

    def do_op(self):
        self.visited.append(self.pc)
        instr = self.prog[self.pc][0]
        op = self.prog[self.pc][1]
        if instr == 'acc':
            self.acc += op
            self.pc += 1
        elif instr == 'nop':
            self.pc += 1
        elif instr == 'jmp':
            self.pc += op
        if self.pc in self.visited:
            self.loop = True
        if self.pc >= self.plen:
            self.finished = True
