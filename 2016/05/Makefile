CC = gcc
CFLAGS = -W -Wall -g -O0
LDFLAGS = -lssl -lcrypto

eXe = day5
SRCS = day5.c

all: $(eXe)

$(eXe): $(SRCS)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

clean:
	rm -rf $(eXe) $(eXe).dSYM
