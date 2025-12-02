CC = gcc
# For readable assembly
DEBUG = -Os -fno-stack-protector -fno-asynchronous-unwind-tables -fomit-frame-pointer -fcf-protection=none -D_FORTIFY_SOURCE=0
CFLAGS  = -std=c89 -W -Wall -Wextra $(DEBUG)
# This works on amd64 Ubuntu 24.04 at least
CRTPATH = /usr/lib/x86_64-linux-gnu
LD_SO = /lib64/ld-linux-x86-64.so.2
CRT1   := $(CRTPATH)/crt1.o
CRTI   := $(CRTPATH)/crti.o
CRTN   := $(CRTPATH)/crtn.o

EXE  = day2
OBJS = day2.o

.PHONY: all clean

all: $(EXE)

$(EXE): $(OBJS)
	$(LD) -o $@ $(CRT1) $(CRTI) $(OBJS) -lc $(CRTN) --dynamic-linker $(LD_SO)

# Save object file from assembly for inspection
day2.o: day2.s
	as -v --64 -o $@ $^

# Generate assembly file from C source for analysis and optimization
day2.s: day2.c
	$(CC) $(CFLAGS) -S -o $@ $<

clean:
	rm -f $(OBJS) $(EXE) day2.s
