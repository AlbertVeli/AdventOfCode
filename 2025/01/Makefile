CC = gcc
#DEBUG = -g -O0
DEBUG = -Os
CFLAGS  = -std=c11 -W -Wall -Wextra $(DEBUG)
LDFLAGS =

OBJS = day1.o
EXE  = day1

.PHONY: all clean

all: $(EXE)

$(EXE): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -f $(OBJS) $(EXE)
