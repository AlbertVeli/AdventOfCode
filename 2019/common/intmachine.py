import array
from dbg import DBG

class Intmachine:

    # iq, oq = deques
    def __init__(self, name, prog, iq, oq):
        self.prog = array.array('q', prog)
        self.plen = len(self.prog)
        self.name = name
        self.reset()
        self.iq = iq
        self.oq = oq

    def reset(self):
        self.finished = False
        # Work with mem, prog is never touched
        self.mem = array.array('q', self.prog)
        # Add 3k 0 initialized memory.
        # Adjust this number if more memory is needed
        self.mem += array.array('q', [0] * 10 * 1024)
        self.pc = 0
        self.base = 0

    # push an int to input queue
    def push(self, val):
        self.iq.appendleft(val)

    # pop an int from output queue
    def pop(self):
        return self.oq.pop()

    # poke val to mem addr
    def poke(self, addr, val):
        self.mem[addr] = val

    # peek mem addr
    def peek(self, addr):
        return self.mem[addr]

    def get_input(self):
        inp = self.iq.pop()
        DBG(' <-- %s input %d' % (self.name, inp))
        return inp

    def put_output(self, output):
        DBG(' --> %s output %d' % (self.name, output))
        self.oq.appendleft(output)

    def get_name(self):
        return self.name

    # Returns True if program finished nicely with opcode 99
    def finished_nice(self):
        return self.finished

    def dump_mem(self):
        print(list(self.mem))

    def get_mem(self, mode, a):
        if mode == 0:
            res = self.mem[a]
            DBG('get_mem: mode 0 ret %d mem[%d]' % (res, a))
        elif mode == 1:
            res = a
            DBG('get_mem: mode 1 ret %d' % (res))
        else:
            # mode 2
            res = self.mem[a + self.base]
            DBG('get_mem: mode 2 ret %d, mem[%d] (%d + %d)' % (res, a + self.base, a, self.base))
        return res

    def get_addr(self, mode, a):
        if mode == 0:
            DBG('get_addr: mode 0 ret %d' % (a))
            return a
        # mode 2, mode 1 is illegal for destination
        DBG('get_addr: mode 2 ret %d (%d + %d)' % (a + self.base, a, self.base))
        return a + self.base

    # Check if next instruction would hang waiting for input
    def would_stall(self):
        op = self.mem[self.pc]
        if op == 3 and len(self.iq) == 0:
            return True
        return False

    def do_op(self):

        if self.finished:
            # Already finished, reset before running again
            return False

        # Put modes for parameter 1-3 to m1-m3
        # 0 = parameter mode, 1 = immediate mode, 2 = relative mode
        op = self.mem[self.pc]
        opm = '{:05d}'.format(op)
        m1 = int(opm[2])
        m2 = int(opm[1])
        m3 = int(opm[0])
        op = int(opm[3:])
        DBG(' * do_op: %s pc %d, op %d, (m%d m%d)' % (self.name, self.pc, op, m1, m2))
        self.pc += 1

        # exit
        if op == 99:
            self.finished = True
            return False

        # add
        elif op == 1:
            a, b, c = self.mem[self.pc : self.pc + 3]
            res = self.get_mem(m1, a)
            res += self.get_mem(m2, b)
            addr = self.get_addr(m3, c)
            self.mem[addr] = res
            self.pc += 3
            DBG('add: mem[%d] <- %d' % (addr, res))

        # mul
        elif op == 2:
            a, b, c = self.mem[self.pc : self.pc + 3]
            res = self.get_mem(m1, a)
            res *= self.get_mem(m2, b)
            addr = self.get_addr(m3, c)
            self.mem[addr] = res
            self.pc += 3
            DBG('mul: mem[%d] <- %d' % (addr, res))

        # input
        elif op == 3:
            if len(self.iq) == 0:
                # Starving, input queue is empty.
                # Restore pc and try again later.
                self.pc -= 1
            else:
                # Input available
                a = self.mem[self.pc]
                addr = self.get_addr(m1, a)
                i = self.get_input()
                self.mem[addr] = i
                self.pc += 1

        # output
        elif op == 4:
            a = self.mem[self.pc]
            self.put_output(self.get_mem(m1, a))
            self.pc += 1

        # jnz
        elif op == 5:
            a, b = self.mem[self.pc : self.pc + 2]
            aa = self.get_mem(m1, a)
            if aa != 0:
                bb = self.get_mem(m2, b)
                self.pc = bb
                DBG('jnz: jump to = %d' % (bb))
            else:
                self.pc += 2
                DBG('jnz: jump not taken')

        # jz
        elif op == 6:
            a, b = self.mem[self.pc : self.pc + 2]
            aa = self.get_mem(m1, a)
            if aa == 0:
                bb = self.get_mem(m2, b)
                self.pc = bb
                DBG('jz: jump to = %d' % (bb))
            else:
                self.pc += 2
                DBG('jz: jump not taken')

        # less than
        elif op == 7:
            a, b, c = self.mem[self.pc : self.pc + 3]
            aa = self.get_mem(m1, a)
            bb = self.get_mem(m2, b)
            addr = self.get_addr(m3, c)
            if aa < bb:
                self.mem[addr] = 1
                DBG('lt: mem[%d] = 1' % (addr))
            else:
                self.mem[addr] = 0
                DBG('lt: mem[%d] = 0' % (addr))
            self.pc += 3

        # equal
        elif op == 8:
            a, b, c = self.mem[self.pc : self.pc + 3]
            aa = self.get_mem(m1, a)
            bb = self.get_mem(m2, b)
            addr = self.get_addr(m3, c)
            if aa == bb:
                self.mem[addr] = 1
                DBG('eq: mem[%d] = 1' % (addr))
            else:
                self.mem[addr] = 0
                DBG('eq: mem[%d] = 0' % (addr))
            self.pc += 3

        # adjust relative base, added in day 9
        elif op == 9:
            a = self.mem[self.pc]
            aa = self.get_mem(m1, a)
            self.base += aa
            self.pc += 1
            DBG('relative base <- %d (changed %d)' % (self.base, aa))

        else:
            # Should really crash here, but let it continue for the fun of it
            print('%s: Error, illegal op %d at pos %d' % (self.name, op, self.pc))
            return False

        # Input finished, but didn't end with opcode 99. Something wrong.
        if self.pc >= self.plen:
            print('%s: Warning, program out of bounds at %d with opcode %d, should finish with opcode 99'
                    % (self.name, self.pc, op))
            return False

        # True means program is still running
        return True
