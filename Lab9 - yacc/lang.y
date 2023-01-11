%{
#include <stdio.h>
#include <stdlib.h>
#define YYDEBUG 1

%}

%token IN
%token OUT
%token IDK
%token NUMBER
%token STRING
%token CHARACTER
%token IF
%token END
%token END_IF
%token END_FOR
%token WHILE
%token END_WHILE
%token ELSE
%token FOR 

%token ASSIGNMENT
%token EQ
%token LT
%token LTE
%token GT
%token GTE
%token NE
%token AND
%token OR
%token NOT

%token IDENTIFIER
%token CONSTANT

%left '+' '-' '*' '/'

%token ADD 
%token SUB
%token DIV 
%token MOD 
%token MUL 

%token OPEN_CURLY_BRACKET
%token CLOSED_CURLY_BRACKET 
%token OPEN_ROUND_BRACKET
%token CLOSED_ROUND_BRACKET
%token OPEN_RIGHT_BRACKET
%token CLOSED_RIGHT_BRACKET 

%token COMMA 
%token SEMI_COLON
%token COLON

%start program
%error-verbose

%%

program : IDK COLON statement_list END 
		;
statement_list : statement | statement statement_list 
			   ;
statement : simple_statement | if_stmt | while_stmt | for_stmt
		  ;	  
simple_statement : declaration | io_stmt | assignment_stmt
				 ;
declaration : type IDENTIFIER SEMI_COLON
			;		
type : simple_type
	;
simple_type : NUMBER | STRING | CHARACTER
			;
io_stmt : IN IDENTIFIER SEMI_COLON | OUT IDENTIFIER SEMI_COLON | OUT CONSTANT SEMI_COLON
		;
assignment_stmt : IDENTIFIER ASSIGNMENT expression SEMI_COLON
				;
expression : expression ADD term | expression SUB term | term
		   ;
term : term MUL factor | term DIV factor | term MOD factor | factor
	 ;
factor : OPEN_CURLY_BRACKET expression CLOSED_CURLY_BRACKET | IDENTIFIER | CONSTANT
	   ;
if_stmt : IF condition COLON statement_list END_IF | IF condition COLON statement_list ELSE statement_list END_IF
		;
condition : OPEN_CURLY_BRACKET expression relation expression CLOSED_CURLY_BRACKET | NOT OPEN_CURLY_BRACKET expression CLOSED_CURLY_BRACKET
		  ;
relation : EQ | NE | LT | LTE | GT | GTE | AND | OR | NOT 
		 ;
while_stmt : WHILE condition COLON statement_list END_WHILE
		   ;
for_stmt : FOR IDENTIFIER ASSIGNMENT CONSTANT COMMA IDENTIFIER COMMA CONSTANT COLON statement_list END_FOR
		 ;
%%

yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
  if(argc>1) yyin = fopen(argv[1], "r");
  if((argc>2)&&(!strcmp(argv[2],"-d"))) yydebug = 1;
  if(!yyparse()) fprintf(stderr,"\tO.K.\n");
}

