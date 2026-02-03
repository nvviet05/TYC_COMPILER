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
// PARSER RULES (sẽ implement ở section 6.2)
// ============================================================

program: (structDecl | funcDecl)* EOF;

// ... (parser rules sẽ được thêm)

// ============================================================
// LEXER RULES
// ============================================================

// -------------------- KEYWORDS --------------------
// Phải đặt TRƯỚC ID rule
AUTO: 'auto';
BREAK: 'break';
CASE: 'case';
CONTINUE: 'continue';
DEFAULT: 'default';
ELSE: 'else';
FLOAT: 'float';
FOR: 'for';
IF: 'if';
INT: 'int';
RETURN: 'return';
STRING: 'string';
STRUCT: 'struct';
SWITCH: 'switch';
VOID: 'void';
WHILE: 'while';

// -------------------- OPERATORS --------------------
// Operators dài trước, ngắn sau

// Increment/Decrement
PLUS_PLUS: '++';
MINUS_MINUS: '--';

// Relational (2 chars trước)
LE: '<=';
GE: '>=';
EQ: '==';
NEQ: '!=';

// Logical (2 chars)
AND: '&&';
OR: '||';

// Single char operators
PLUS: '+';
MINUS: '-';
MUL: '*';
DIV: '/';
MOD: '%';
LT: '<';
GT: '>';
NOT: '!';
ASSIGN: '=';
DOT: '.';

// -------------------- SEPARATORS --------------------
LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACKET: '[';
RBRACKET: ']';
SEMI: ';';
COMMA: ',';
COLON: ':';

// -------------------- LITERALS --------------------

// Float literal - phải đặt TRƯỚC INT_LIT
// Pattern: digits.digits? exponent? | digits? .digits exponent? | digits exponent
FLOAT_LIT: DIGIT+ '.' DIGIT* EXPONENT?
         | DIGIT* '.' DIGIT+ EXPONENT?
         | DIGIT+ EXPONENT
         ;

// Integer literal
INT_LIT: DIGIT+;

// String literal - valid string
STRING_LIT: '"' STRING_CHAR* '"';

// -------------------- IDENTIFIER --------------------
ID: (LETTER | '_') (LETTER | DIGIT | '_')*;

// -------------------- WHITESPACE & COMMENTS --------------------
WS: [ \t\r\n\f]+ -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;

BLOCK_COMMENT: '/*' .*? '*/' -> skip;

// -------------------- ERROR TOKENS --------------------
// Phải đặt CUỐI CÙNG

// Illegal escape in string
ILLEGAL_ESCAPE: '"' STRING_CHAR* ESC_ILLEGAL
    {
        self.text = self.text[1:]
    };

// Unclosed string
UNCLOSE_STRING: '"' STRING_CHAR*
    {
        self.text = self.text[1:]
    };

// Unrecognized character
ERROR_CHAR: .;

// -------------------- FRAGMENTS --------------------
fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z];
fragment EXPONENT: [eE] [+-]? DIGIT+;

// String character: any char except quote, backslash, newline, OR valid escape
fragment STRING_CHAR: ~["\\\r\n] | ESC_VALID;

// Valid escape sequences
fragment ESC_VALID: '\\' [bfnrt"\\];

// Invalid escape sequence (anything else after backslash)
fragment ESC_ILLEGAL: '\\' ~[bfnrt"\\]
                    | '\\';  // backslash at end

// ============================================================
// PARSER RULES
// ============================================================

// -------------------- PROGRAM --------------------
program: (structDecl | funcDecl)* EOF;

// -------------------- STRUCT DECLARATION --------------------
structDecl: STRUCT ID LBRACE memberDecl* RBRACE SEMI;

memberDecl: typeSpec ID SEMI;

// -------------------- FUNCTION DECLARATION --------------------
funcDecl: typeSpec? ID LPAREN paramList? RPAREN blockStmt;

paramList: param (COMMA param)*;

param: typeSpec ID;

// -------------------- TYPE SPECIFIER --------------------
typeSpec: INT       # IntType
        | FLOAT     # FloatType
        | STRING    # StringType
        | VOID      # VoidType
        | ID        # StructType
        ;

// -------------------- STATEMENTS --------------------
blockStmt: LBRACE stmt* RBRACE;

stmt: varDecl
    | assignStmt
    | ifStmt
    | whileStmt
    | forStmt
    | switchStmt
    | breakStmt
    | continueStmt
    | returnStmt
    | exprStmt
    | blockStmt
    ;

// Variable declaration
varDecl: (AUTO | typeSpec) ID (ASSIGN expr)? SEMI;

// Assignment statement
assignStmt: lhs ASSIGN expr SEMI;

lhs: ID (DOT ID)*;  // Identifier or member access

// If statement
ifStmt: IF LPAREN expr RPAREN stmt (ELSE stmt)?;

// While statement
whileStmt: WHILE LPAREN expr RPAREN stmt;

// For statement
forStmt: FOR LPAREN forInit? SEMI expr? SEMI forUpdate? RPAREN stmt;

forInit: (AUTO | typeSpec) ID ASSIGN expr  // var decl without semi
       | lhs ASSIGN expr                    // assignment without semi
       ;

forUpdate: expr;

// Switch statement
switchStmt: SWITCH LPAREN expr RPAREN LBRACE caseClause* defaultClause? RBRACE;

caseClause: CASE expr COLON stmt*;

defaultClause: DEFAULT COLON stmt*;

// Simple statements
breakStmt: BREAK SEMI;
continueStmt: CONTINUE SEMI;
returnStmt: RETURN expr? SEMI;
exprStmt: expr SEMI;

// -------------------- EXPRESSIONS --------------------
// Precedence từ thấp → cao (top to bottom)

expr: assignExpr;

// Assignment (right associative)
assignExpr: orExpr (ASSIGN assignExpr)?;

// Logical OR
orExpr: andExpr (OR andExpr)*;

// Logical AND
andExpr: eqExpr (AND eqExpr)*;

// Equality
eqExpr: relExpr ((EQ | NEQ) relExpr)*;

// Relational
relExpr: addExpr ((LT | GT | LE | GE) addExpr)*;

// Additive
addExpr: mulExpr ((PLUS | MINUS) mulExpr)*;

// Multiplicative
mulExpr: unaryExpr ((MUL | DIV | MOD) unaryExpr)*;

// Unary (prefix)
unaryExpr: (NOT | MINUS | PLUS | PLUS_PLUS | MINUS_MINUS) unaryExpr
         | postfixExpr
         ;

// Postfix
postfixExpr: primaryExpr postfixOp*;

postfixOp: PLUS_PLUS                    # PostIncrement
         | MINUS_MINUS                  # PostDecrement
         | DOT ID                       # MemberAccess
         | LPAREN argList? RPAREN       # FuncCall
         ;

// Primary
primaryExpr: ID                         # Identifier
           | INT_LIT                    # IntLiteral
           | FLOAT_LIT                  # FloatLiteral
           | STRING_LIT                 # StringLiteral
           | LPAREN expr RPAREN         # ParenExpr
           | structLit                  # StructLiteral
           ;

// Struct literal
structLit: LBRACE (expr (COMMA expr)*)? RBRACE;

// Argument list
argList: expr (COMMA expr)*;