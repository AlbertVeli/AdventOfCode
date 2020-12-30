# To build calc, run:
#
#  make
#
# And run make clean to clean up
#
LEX = flex
YACC = bison
YFLAGS = -v -d

all: calc

calc.tab.c calc.tab.h:	calc.y
	$(YACC) $(YFLAGS) $<

lex.yy.c: calc.l calc.tab.h
	$(LEX) $(LFLAGS) $<

calc: lex.yy.c calc.tab.c calc.tab.h
	$(CC) $(CFLAGS) -o $@ lex.yy.c calc.tab.c

.PHONY: clean
clean:
	rm -f calc calc.tab.c lex.yy.c calc.tab.h calc.output
