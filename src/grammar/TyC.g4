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
// Hỗ trợ cả return type tường minh và inferred (bỏ qua return type)
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

statement: assign_statement SEMI
         | var_statement SEMI
         | if_statement
         | while_statement
         | for_statement
         | switch_statement
         | break_statement
         | continue_statement
         | return_statement
         | block_statement
         | expression_statement
         ;

// Variable declaration
var_statement: (AUTO | explicit_type) ID (ASSIGN var_initializer)?;

var_initializer: expression | struct_initializer;

struct_initializer: LBRACE list_expression? RBRACE;

// Assignment statement
assign_statement: lvalue ASSIGN expression;

lvalue: ID (DOT ID)*;

// If statement
if_statement: IF LPAREN expression RPAREN statement (ELSE statement)?;

// While statement
while_statement: WHILE LPAREN expression RPAREN statement;

// For statement
for_statement: FOR LPAREN for_init? SEMI expression? SEMI for_update? RPAREN statement;

for_init: var_statement 
        | assign_statement
        ;

for_update: assign_statement
          | lvalue (INC | DEC)
          | (INC | DEC) lvalue
          ;

// Switch statement - linh hoạt: default có thể ở giữa các case
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
expression_statement: expression1 SEMI;

// -------------------- EXPRESSIONS --------------------
// Precedence từ thấp đến cao (top to bottom)

expression: assign_expression | expression1;

assign_expression: lvalue ASSIGN expression;

list_expression: expression COMMA list_expression | expression;

// Logical OR (lowest precedence after assignment)
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

// Postfix and primary
expression9: postfix_expr
           | member_access
           | call_expr
           | expression_primary
           ;

// Postfix increment/decrement: x++, x--
postfix_expr: (member_access | ID | literal | LPAREN expression RPAREN) (INC | DEC)+;

// Function call
call_expr: ID LPAREN list_expression? RPAREN;

// Member access: obj.member.submember
member_access: ID (DOT ID)+;

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

// -------------------- KEYWORDS (phải đặt TRƯỚC ID) --------------------
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

// -------------------- OPERATORS (dài trước, ngắn sau) --------------------
// Increment/Decrement
INC      : '++';
DEC      : '--';

// Relational (2 chars trước)
EQ       : '==';
NEQ      : '!=';
LE       : '<=';
GE       : '>=';

// Logical (2 chars)
OR       : '||';
AND      : '&&';

// Single char operators
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
// ⚠️ QUAN TRỌNG: FLOAT_LIT phải đặt TRƯỚC INT_LIT
// Vì với input "3.14", nếu INT_LIT trước sẽ match "3" trước

FLOAT_LIT
    : [0-9]+ '.' [0-9]* EXPONENT?
    | '.' [0-9]+ EXPONENT?
    | [0-9]+ EXPONENT
    ;

INT_LIT: [0-9]+;

// String literal - tự động bỏ dấu " ở đầu/cuối
STRING_LIT: '"' STR_CHAR* '"' { self.text = self.text[1:-1] };

// -------------------- IDENTIFIER (phải sau keywords) --------------------
ID: [a-zA-Z_][a-zA-Z0-9_]*;

// -------------------- WHITESPACE & COMMENTS --------------------
WS: [ \t\r\n\f]+ -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;

BLOCK_COMMENT: '/*' .*? '*/' -> skip;

// -------------------- ERROR TOKENS (phải đặt CUỐI CÙNG) --------------------

// Illegal escape trong string - phải trước UNCLOSE_STRING
ILLEGAL_ESCAPE: '"' STR_CHAR* ESC_ILLEGAL {
    self.text = self.text[1:]
};

// Unclosed string - string không có dấu " đóng
UNCLOSE_STRING: '"' STR_CHAR* ('\r\n' | '\n' | EOF) {
    self.text = self.text[1:]
};

// Ký tự không nhận dạng được - catch all
ERROR_CHAR: .;

// -------------------- FRAGMENTS --------------------
fragment EXPONENT: [eE] [+-]? [0-9]+;

// String character: bất kỳ ký tự nào trừ ", \, newline, HOẶC valid escape
fragment STR_CHAR: ~[\r\n\\"] | ESC_SEQ;

// Valid escape sequences: \b \f \r \n \t \" \\
fragment ESC_SEQ: '\\' [bfrnt"\\];

// Invalid escape sequence (bất kỳ thứ gì khác sau backslash)
fragment ESC_ILLEGAL: '\\' ~[bfrnt"\\];
