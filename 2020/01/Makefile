#CC = gcc-10
CFLAGS = -W -Wall -O2 -fomit-frame-pointer

EXE = 1
OBJS = $(EXE).o

1: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

.PHONY: clean
clean:
	rm -f $(OBJS) $(EXE)
