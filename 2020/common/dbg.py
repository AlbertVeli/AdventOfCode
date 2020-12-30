import sys

# Turn debugging on/off with this
#debug = True
debug = False

def DBG(*args):
    if debug and len(args) > 0:
        for arg in args[:-1]:
            sys.stdout.write(str(arg) + ' ')
        # last argument, no space but newline instead
        print(args[-1])
