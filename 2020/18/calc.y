%{

#include <stdio.h>
#include <stdlib.h>

extern int yylex();
extern int yyparse();
extern FILE* yyin;

void yyerror(const char* s);
%}

%union {
	long lval;
}

%token<lval> T_INT
%token T_PLUS T_MULTIPLY T_LEFT T_RIGHT T_NEWLINE
/* Specify precedence with %left
 * Part1: %left T_PLUS T_MULTIPLY
 * Part2 below
 */
%left T_MULTIPLY
%left T_PLUS

%type<lval> expression

%start calculation

%%

calculation:
	   | calculation line
;

line: T_NEWLINE
    | expression T_NEWLINE { printf("result: %ld\n", $1); }
;

expression: T_INT				{ $$ = $1; }
	  | expression T_PLUS expression	{ $$ = $1 + $3; }
	  | expression T_MULTIPLY expression	{ $$ = $1 * $3; }
	  | T_LEFT expression T_RIGHT		{ $$ = $2; }
;

%%

int main() {
	yyin = stdin;

	do {
		yyparse();
	} while(!feof(yyin));

	return 0;
}

void yyerror(const char* s) {
	fprintf(stderr, "Parse error: %s\n", s);
	exit(1);
}
