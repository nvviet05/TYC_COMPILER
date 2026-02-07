grammar TyC;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    if tk == self.UNCLOSE_STRING:       
        result = super().emit();
        raise UncloseString(result.text);
    elif tk == self.ILLEGAL_ESCAPE:
        result = super().emit();
        raise IllegalEscape(result.text);
    elif tk == self.ERROR_CHAR:
        result = super().emit();
        raise ErrorToken(result.text); 
    else:
        return super().emit();
}

options {
    language=Python3;
}

// ============================================================
// PARSER RULES
// ============================================================

// -------------------- PROGRAM --------------------
program: (structs | functions)* EOF;

// -------------------- STRUCT DECLARATION --------------------
structs: STRUCT ID LBRACE struct_member* RBRACE SEMI;

struct_member: explicit_type ID SEMI;

// -------------------- FUNCTION DECLARATION --------------------
functions: (return_type ID | ID) LPAREN parameter_list? RPAREN block_statement;

return_type: explicit_type | VOID;

parameter_list: parameter_decl (COMMA parameter_decl)*;

parameter_decl: explicit_type ID;

// -------------------- TYPE SPECIFIER --------------------
explicit_type: INT | FLOAT | STRING | ID;

type: INT | FLOAT | STRING | ID | AUTO;

// -------------------- STATEMENTS --------------------
block_statement: LBRACE list_statement? RBRACE;

list_statement: statement list_statement | statement;

statement: var_statement SEMI
         | if_statement
         | while_statement
         | for_statement
         | switch_statement
         | break_statement
         | continue_statement
         | return_statement
         | block_statement
         | expression SEMI
         ;

// Variable declaration
var_statement: (AUTO | explicit_type) ID (ASSIGN var_initializer)?;

var_initializer: expression | struct_initializer;

struct_initializer: LBRACE list_expression? RBRACE;

// If statement
if_statement: IF LPAREN expression RPAREN statement (ELSE statement)?;

// While statement
while_statement: WHILE LPAREN expression RPAREN statement;

// For statement
for_statement: FOR LPAREN for_init? SEMI expression? SEMI for_update? RPAREN statement;

for_init: var_statement
        | lvalue ASSIGN expression
        ;

for_update: lvalue ASSIGN expression
          | (INC | DEC)+ for_operand (INC | DEC)*
          | for_operand (INC | DEC)+
          ;

// Broader operand for for-update inc/dec: any primary/call with optional member access
for_operand: (call_expr | expression_primary) (DOT ID)*;

// Switch statement
switch_statement: SWITCH LPAREN expression RPAREN 
                  LBRACE 
                      switch_case* 
                      switch_default? 
                      switch_case* 
                  RBRACE;

switch_case: switch_label+ list_statement?;

switch_default: DEFAULT COLON list_statement?;

switch_label: CASE expression COLON;

// Simple statements
break_statement: BREAK SEMI;
continue_statement: CONTINUE SEMI;
return_statement: RETURN expression? SEMI;

// -------------------- EXPRESSIONS --------------------
// Precedence from low to high (top to bottom)

// Assignment (right-associative, lowest precedence)
// LHS restricted to lvalue: bare ID with optional member access, or expressions that end with .ID
expression: lvalue ASSIGN expression | expression1;

lvalue: ID (DOT ID)*
      | (call_expr | LPAREN expression RPAREN | literal) (DOT ID)+
      ;

list_expression: expression COMMA list_expression | expression;

// Logical OR
expression1: expression1 OR expression2 | expression2;

// Logical AND
expression2: expression2 AND expression3 | expression3;

// Equality
expression3: expression3 (EQ | NEQ) expression4 | expression4;

// Relational
expression4: expression4 (LT | LE | GT | GE) expression5 | expression5;

// Additive
expression5: expression5 (PLUS | MINUS) expression6 | expression6;

// Multiplicative
expression6: expression6 (MUL | DIV | MOD) expression7 | expression7;

// Unary (prefix): ! - +
expression7: (NOT | PLUS | MINUS) expression7
           | prefix_incdec
           ;

// Prefix increment/decrement: ++x, --x
prefix_incdec: (INC | DEC) prefix_incdec 
             | expression9
             ;

// Postfix, member access, and primary
// Member access chain first, then optional postfix inc/dec at the end only
expression9: (call_expr | expression_primary) (DOT ID)* (INC | DEC)*;

// Function call
call_expr: ID LPAREN list_expression? RPAREN;

// Primary expressions
expression_primary: ID 
                  | literal 
                  | LPAREN expression RPAREN
                  ;

// Literals
literal: INT_LIT | FLOAT_LIT | STRING_LIT | struct_initializer;

// ============================================================
// LEXER RULES
// ============================================================

// -------------------- KEYWORDS --------------------
AUTO     : 'auto';
BREAK    : 'break';
CASE     : 'case';
CONTINUE : 'continue';
DEFAULT  : 'default';
ELSE     : 'else';
FLOAT    : 'float';
FOR      : 'for';
IF       : 'if';
INT      : 'int';
RETURN   : 'return';
STRING   : 'string';
STRUCT   : 'struct';
SWITCH   : 'switch';
VOID     : 'void';
WHILE    : 'while';

// -------------------- OPERATORS --------------------
INC      : '++';
DEC      : '--';

EQ       : '==';
NEQ      : '!=';
LE       : '<=';
GE       : '>=';

OR       : '||';
AND      : '&&';

PLUS     : '+';
MINUS    : '-';
MUL      : '*';
DIV      : '/';
MOD      : '%';
LT       : '<';
GT       : '>';
NOT      : '!';
ASSIGN   : '=';
DOT      : '.';

// -------------------- SEPARATORS --------------------
LBRACE   : '{';
RBRACE   : '}';
LPAREN   : '(';
RPAREN   : ')';
SEMI     : ';';
COMMA    : ',';
COLON    : ':';

// -------------------- LITERALS --------------------
FLOAT_LIT
    : [0-9]+ '.' [0-9]* EXPONENT?
    | '.' [0-9]+ EXPONENT?
    | [0-9]+ EXPONENT
    ;

INT_LIT: [0-9]+;

STRING_LIT: '"' STR_CHAR* '"' { self.text = self.text[1:-1] };

// -------------------- IDENTIFIER --------------------
ID: [a-zA-Z_][a-zA-Z0-9_]*;

// -------------------- WHITESPACE & COMMENTS --------------------
WS: [ \t\r\n\f]+ -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;

BLOCK_COMMENT: '/*' .*? '*/' -> skip;

// -------------------- ERROR TOKENS --------------------

// Illegal escape in string - must be before UNCLOSE_STRING
ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL {
    self.text = self.text[1:]
};

// Unclosed string - string without closing quote
// The optional '\\' handles a trailing backslash before newline/EOF
UNCLOSE_STRING: '"' STR_CHAR* '\\'? ('\r\n' | '\n' | EOF) {
    self.text = self.text[1:]
};

// Unrecognized character - catch all
ERROR_CHAR: .;

// -------------------- FRAGMENTS --------------------
fragment EXPONENT: [eE] [+-]? [0-9]+;

fragment STR_CHAR: ~[\r\n\\"] | ESC_SEQ;

fragment ESC_SEQ: '\\' [bfrnt"\\];

// Invalid escape: backslash followed by anything except valid escapes AND except newlines
// (backslash before newline is an unclosed string, not an illegal escape)
fragment ESC_ILLEGAL: '\\' ~[bfrnt"\\\r\n];
