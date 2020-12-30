%option noyywrap

%{
#include <stdio.h>
#include <stdlib.h>

#define YY_DECL int yylex()

#include "calc.tab.h"

%}

%%

[ \t]	; /* ignore whitespace */
[0-9]+	{ yylval.lval = strtol(yytext, NULL, 10); return T_INT; }
\n	{ return T_NEWLINE; }
"+"	{ return T_PLUS; }
"*"	{ return T_MULTIPLY; }
"("	{ return T_LEFT; }
")"	{ return T_RIGHT; }
%%
