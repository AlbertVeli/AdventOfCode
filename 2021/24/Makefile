CFLAGS = -W -Wall -O3 -march=native

all: 24_1 24_2

24_1: 24_1.o
	$(CC) $(CFLAGS) -o $@ $<

24_2: 24_2.o
	$(CC) $(CFLAGS) -o $@ $<

.PHONY: clean

clean:
	rm -f 24_1 24_2 *.o
