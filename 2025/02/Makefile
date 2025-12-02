CC = gcc
# For readable assembly
DEBUG = -Os -fno-stack-protector -fno-asynchronous-unwind-tables -fomit-frame-pointer -fcf-protection=none -D_FORTIFY_SOURCE=0
CFLAGS  = -std=c89 -W -Wall -Wextra $(DEBUG)

EXE  = day2
OBJS = day2.o

.PHONY: all clean

all: $(EXE)

$(EXE): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

# Save object file from assembly
# for inspection
day2.o: day2.s
	as -v --64 -o $@ $^

# Generate assembly file from C source
# for analysis and optimization
day2.s: day2.c
	$(CC) $(CFLAGS) -S -o $@ $<

clean:
	rm -f $(OBJS) $(EXE) day2.s
