CC = gcc

CFLAGS = -W -Wall -Wextra -Os
LDFLAGS =

OBJS = day1.o
EXE = $(OBJS:.o=)

all: $(EXE)

$(EXE): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LDFLAGS)

clean:
	rm -f $(OBJS) $(EXE)
