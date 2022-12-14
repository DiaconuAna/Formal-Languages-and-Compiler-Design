
/* A Bison parser, made by GNU Bison 2.4.1.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     IN = 258,
     OUT = 259,
     IDK = 260,
     NUMBER = 261,
     STRING = 262,
     CHARACTER = 263,
     IF = 264,
     END = 265,
     END_IF = 266,
     END_FOR = 267,
     WHILE = 268,
     END_WHILE = 269,
     ELSE = 270,
     FOR = 271,
     ASSIGNMENT = 272,
     EQ = 273,
     LT = 274,
     LTE = 275,
     GT = 276,
     GTE = 277,
     NE = 278,
     AND = 279,
     OR = 280,
     NOT = 281,
     IDENTIFIER = 282,
     CONSTANT = 283,
     ADD = 284,
     SUB = 285,
     DIV = 286,
     MOD = 287,
     MUL = 288,
     OPEN_CURLY_BRACKET = 289,
     CLOSED_CURLY_BRACKET = 290,
     OPEN_ROUND_BRACKET = 291,
     CLOSED_ROUND_BRACKET = 292,
     OPEN_RIGHT_BRACKET = 293,
     CLOSED_RIGHT_BRACKET = 294,
     COMMA = 295,
     SEMI_COLON = 296,
     COLON = 297
   };
#endif



#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


