"""
Lexer test cases for TyC compiler
110 test cases covering all lexical elements
Updated to match merged TyC.g4 grammar
"""

from tests.utils import Tokenizer
import pytest
import os
import sys

# Setup path for imports
_build_dir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'build')
sys.path.insert(0, _build_dir)


# ============================================================
# KEYWORD TESTS (16 tests)
# ============================================================

class TestKeywords:
    """Test keyword token recognition"""

    def test_keyword_auto(self):
        """Test 'auto' keyword"""
        assert "AUTO,auto" in Tokenizer("auto").get_tokens_as_string()

    def test_keyword_break(self):
        """Test 'break' keyword"""
        assert "BREAK,break" in Tokenizer("break").get_tokens_as_string()

    def test_keyword_case(self):
        """Test 'case' keyword"""
        assert "CASE,case" in Tokenizer("case").get_tokens_as_string()

    def test_keyword_continue(self):
        """Test 'continue' keyword"""
        assert "CONTINUE,continue" in Tokenizer(
            "continue").get_tokens_as_string()

    def test_keyword_default(self):
        """Test 'default' keyword"""
        assert "DEFAULT,default" in Tokenizer("default").get_tokens_as_string()

    def test_keyword_else(self):
        """Test 'else' keyword"""
        assert "ELSE,else" in Tokenizer("else").get_tokens_as_string()

    def test_keyword_float(self):
        """Test 'float' keyword"""
        assert "FLOAT,float" in Tokenizer("float").get_tokens_as_string()

    def test_keyword_for(self):
        """Test 'for' keyword"""
        assert "FOR,for" in Tokenizer("for").get_tokens_as_string()

    def test_keyword_if(self):
        """Test 'if' keyword"""
        assert "IF,if" in Tokenizer("if").get_tokens_as_string()

    def test_keyword_int(self):
        """Test 'int' keyword"""
        assert "INT,int" in Tokenizer("int").get_tokens_as_string()

    def test_keyword_return(self):
        """Test 'return' keyword"""
        assert "RETURN,return" in Tokenizer("return").get_tokens_as_string()

    def test_keyword_string(self):
        """Test 'string' keyword"""
        assert "STRING,string" in Tokenizer("string").get_tokens_as_string()

    def test_keyword_struct(self):
        """Test 'struct' keyword"""
        assert "STRUCT,struct" in Tokenizer("struct").get_tokens_as_string()

    def test_keyword_switch(self):
        """Test 'switch' keyword"""
        assert "SWITCH,switch" in Tokenizer("switch").get_tokens_as_string()

    def test_keyword_void(self):
        """Test 'void' keyword"""
        assert "VOID,void" in Tokenizer("void").get_tokens_as_string()

    def test_keyword_while(self):
        """Test 'while' keyword"""
        assert "WHILE,while" in Tokenizer("while").get_tokens_as_string()


# ============================================================
# OPERATOR TESTS (18 tests)
# ============================================================

class TestOperators:
    """Test operator token recognition"""

    def test_plus(self):
        """Test '+' operator"""
        assert "PLUS,+" in Tokenizer("+").get_tokens_as_string()

    def test_minus(self):
        """Test '-' operator"""
        assert "MINUS,-" in Tokenizer("-").get_tokens_as_string()

    def test_multiply(self):
        """Test '*' operator"""
        assert "MUL,*" in Tokenizer("*").get_tokens_as_string()

    def test_divide(self):
        """Test '/' operator"""
        assert "DIV,/" in Tokenizer("/").get_tokens_as_string()

    def test_modulo(self):
        """Test '%' operator"""
        assert "MOD,%" in Tokenizer("%").get_tokens_as_string()

    def test_increment(self):
        """Test '++' operator - should be single INC token"""
        result = Tokenizer("++").get_tokens_as_string()
        assert "INC,++" in result
        assert result.count("PLUS,+") == 0  # Not two PLUS tokens

    def test_decrement(self):
        """Test '--' operator - should be single DEC token"""
        result = Tokenizer("--").get_tokens_as_string()
        assert "DEC,--" in result

    def test_equal(self):
        """Test '==' operator"""
        result = Tokenizer("==").get_tokens_as_string()
        assert "EQ,==" in result

    def test_not_equal(self):
        """Test '!=' operator"""
        assert "NEQ,!=" in Tokenizer("!=").get_tokens_as_string()

    def test_less_than(self):
        """Test '<' operator"""
        assert "LT,<" in Tokenizer("<").get_tokens_as_string()

    def test_greater_than(self):
        """Test '>' operator"""
        assert "GT,>" in Tokenizer(">").get_tokens_as_string()

    def test_less_equal(self):
        """Test '<=' operator"""
        result = Tokenizer("<=").get_tokens_as_string()
        assert "LE,<=" in result

    def test_greater_equal(self):
        """Test '>=' operator"""
        result = Tokenizer(">=").get_tokens_as_string()
        assert "GE,>=" in result

    def test_logical_and(self):
        """Test '&&' operator"""
        assert "AND,&&" in Tokenizer("&&").get_tokens_as_string()

    def test_logical_or(self):
        """Test '||' operator"""
        assert "OR,||" in Tokenizer("||").get_tokens_as_string()

    def test_logical_not(self):
        """Test '!' operator"""
        assert "NOT,!" in Tokenizer("!").get_tokens_as_string()

    def test_assign(self):
        """Test '=' operator"""
        assert "ASSIGN,=" in Tokenizer("=").get_tokens_as_string()

    def test_dot(self):
        """Test '.' operator"""
        assert "DOT,." in Tokenizer(".").get_tokens_as_string()


# ============================================================
# SEPARATOR TESTS (6 tests - no brackets in TyC grammar)
# ============================================================

class TestSeparators:
    """Test separator token recognition"""

    def test_lparen(self):
        assert "LPAREN,(" in Tokenizer("(").get_tokens_as_string()

    def test_rparen(self):
        assert "RPAREN,)" in Tokenizer(")").get_tokens_as_string()

    def test_lbrace(self):
        assert "LBRACE,{" in Tokenizer("{").get_tokens_as_string()

    def test_rbrace(self):
        assert "RBRACE,}" in Tokenizer("}").get_tokens_as_string()

    def test_semicolon(self):
        assert "SEMI,;" in Tokenizer(";").get_tokens_as_string()

    def test_comma(self):
        assert "COMMA,," in Tokenizer(",").get_tokens_as_string()


# ============================================================
# INTEGER LITERAL TESTS (10 tests)
# ============================================================

class TestIntegerLiterals:
    """Test integer literal recognition"""

    def test_zero(self):
        assert "INT_LIT,0" in Tokenizer("0").get_tokens_as_string()

    def test_single_digit(self):
        assert "INT_LIT,5" in Tokenizer("5").get_tokens_as_string()

    def test_multi_digit(self):
        assert "INT_LIT,123" in Tokenizer("123").get_tokens_as_string()

    def test_large_number(self):
        assert "INT_LIT,9999999" in Tokenizer("9999999").get_tokens_as_string()

    def test_leading_zeros(self):
        """Leading zeros are valid in TyC"""
        assert "INT_LIT,007" in Tokenizer("007").get_tokens_as_string()

    def test_integer_sequence(self):
        """Multiple integers separated by operators"""
        result = Tokenizer("1 + 2").get_tokens_as_string()
        assert "INT_LIT,1" in result
        assert "INT_LIT,2" in result

    def test_integer_10(self):
        assert "INT_LIT,10" in Tokenizer("10").get_tokens_as_string()

    def test_integer_100(self):
        assert "INT_LIT,100" in Tokenizer("100").get_tokens_as_string()

    def test_integer_255(self):
        assert "INT_LIT,255" in Tokenizer("255").get_tokens_as_string()

    def test_integer_2500(self):
        assert "INT_LIT,2500" in Tokenizer("2500").get_tokens_as_string()


# ============================================================
# FLOAT LITERAL TESTS (15 tests)
# ============================================================

class TestFloatLiterals:
    """Test float literal recognition"""

    def test_simple_float(self):
        assert "FLOAT_LIT,3.14" in Tokenizer("3.14").get_tokens_as_string()

    def test_zero_float(self):
        assert "FLOAT_LIT,0.0" in Tokenizer("0.0").get_tokens_as_string()

    def test_float_no_decimal(self):
        """Float with dot but no decimal part: 3."""
        assert "FLOAT_LIT,3." in Tokenizer("3.").get_tokens_as_string()

    def test_float_no_integer(self):
        """Float with no integer part: .5"""
        assert "FLOAT_LIT,.5" in Tokenizer(".5").get_tokens_as_string()

    def test_scientific_lowercase(self):
        """Scientific notation with lowercase e"""
        assert "FLOAT_LIT,1e10" in Tokenizer("1e10").get_tokens_as_string()

    def test_scientific_uppercase(self):
        """Scientific notation with uppercase E"""
        assert "FLOAT_LIT,1E10" in Tokenizer("1E10").get_tokens_as_string()

    def test_scientific_positive(self):
        """Scientific notation with positive exponent"""
        assert "FLOAT_LIT,1e+10" in Tokenizer("1e+10").get_tokens_as_string()

    def test_scientific_negative(self):
        """Scientific notation with negative exponent"""
        assert "FLOAT_LIT,1e-10" in Tokenizer("1e-10").get_tokens_as_string()

    def test_combined_float_scientific(self):
        """Float with decimal and scientific notation"""
        assert "FLOAT_LIT,3.14e5" in Tokenizer("3.14e5").get_tokens_as_string()

    def test_float_vs_int_dot_int(self):
        """3.14 should be one FLOAT_LIT, not INT DOT INT"""
        result = Tokenizer("3.14").get_tokens_as_string()
        assert result.count("INT_LIT") == 0
        assert "FLOAT_LIT,3.14" in result

    def test_float_123_456(self):
        assert "FLOAT_LIT,123.456" in Tokenizer(
            "123.456").get_tokens_as_string()

    def test_float_point_123(self):
        assert "FLOAT_LIT,.123" in Tokenizer(".123").get_tokens_as_string()

    def test_float_5e_minus_3(self):
        assert "FLOAT_LIT,5e-3" in Tokenizer("5e-3").get_tokens_as_string()

    def test_float_5E_minus_2(self):
        assert "FLOAT_LIT,5.67E-2" in Tokenizer(
            "5.67E-2").get_tokens_as_string()

    def test_float_1_23e4(self):
        assert "FLOAT_LIT,1.23e4" in Tokenizer("1.23e4").get_tokens_as_string()


# ============================================================
# STRING LITERAL TESTS (12 tests)
# Note: Grammar strips quotes, so "hello" becomes hello in token text
# ============================================================

class TestStringLiterals:
    """Test string literal recognition"""

    def test_simple_string(self):
        """String without quotes in token (grammar strips them)"""
        assert "STRING_LIT,hello" in Tokenizer(
            '"hello"').get_tokens_as_string()

    def test_empty_string(self):
        """Empty string token"""
        result = Tokenizer('""').get_tokens_as_string()
        assert "STRING_LIT," in result

    def test_string_with_spaces(self):
        """String with spaces"""
        assert "STRING_LIT,hello world" in Tokenizer(
            '"hello world"').get_tokens_as_string()

    def test_escape_newline(self):
        """String with newline escape"""
        assert "STRING_LIT,hello\\nworld" in Tokenizer(
            '"hello\\nworld"').get_tokens_as_string()

    def test_escape_tab(self):
        """String with tab escape"""
        assert "STRING_LIT,hello\\tworld" in Tokenizer(
            '"hello\\tworld"').get_tokens_as_string()

    def test_escape_quote(self):
        """String with escaped quote"""
        result = Tokenizer('"say \\"hi\\""').get_tokens_as_string()
        assert "STRING_LIT,say \\" in result

    def test_escape_backslash(self):
        """String with escaped backslash"""
        result = Tokenizer('"path\\\\to"').get_tokens_as_string()
        assert "STRING_LIT,path\\\\" in result

    def test_multiple_escapes(self):
        """String with multiple escape sequences"""
        result = Tokenizer('"a\\n\\t\\r"').get_tokens_as_string()
        assert "STRING_LIT,a\\n\\t\\r" in result

    def test_string_with_numbers(self):
        """String containing numbers"""
        assert "STRING_LIT,test123" in Tokenizer(
            '"test123"').get_tokens_as_string()

    def test_string_with_symbols(self):
        """String with various symbols"""
        assert "STRING_LIT,!@#$%" in Tokenizer(
            '"!@#$%"').get_tokens_as_string()

    def test_string_escape_b(self):
        """String with backspace escape"""
        assert "STRING_LIT,a\\b" in Tokenizer('"a\\b"').get_tokens_as_string()

    def test_string_escape_f(self):
        """String with formfeed escape"""
        assert "STRING_LIT,a\\f" in Tokenizer('"a\\f"').get_tokens_as_string()


# ============================================================
# IDENTIFIER TESTS (10 tests)
# ============================================================

class TestIdentifiers:
    """Test identifier recognition"""

    def test_single_letter(self):
        assert "ID,x" in Tokenizer("x").get_tokens_as_string()

    def test_multiple_letters(self):
        assert "ID,hello" in Tokenizer("hello").get_tokens_as_string()

    def test_with_numbers(self):
        assert "ID,var123" in Tokenizer("var123").get_tokens_as_string()

    def test_with_underscore(self):
        assert "ID,my_var" in Tokenizer("my_var").get_tokens_as_string()

    def test_start_underscore(self):
        assert "ID,_temp" in Tokenizer("_temp").get_tokens_as_string()

    def test_all_underscore(self):
        assert "ID,___" in Tokenizer("___").get_tokens_as_string()

    def test_mixed_case(self):
        assert "ID,MyVariable" in Tokenizer(
            "MyVariable").get_tokens_as_string()

    def test_keyword_prefix_is_identifier(self):
        """'integer' should be ID, not INT + 'eger'"""
        result = Tokenizer("integer").get_tokens_as_string()
        assert "ID,integer" in result
        assert "INT,int" not in result

    def test_keyword_suffix_is_identifier(self):
        """'myif' should be ID"""
        assert "ID,myif" in Tokenizer("myif").get_tokens_as_string()

    def test_camelCase_identifier(self):
        assert "ID,myVariableName" in Tokenizer(
            "myVariableName").get_tokens_as_string()


# ============================================================
# COMMENT TESTS (6 tests)
# ============================================================

class TestComments:
    """Test comment handling"""

    def test_line_comment_skipped(self):
        """Line comment should be skipped"""
        result = Tokenizer("int x; // comment").get_tokens_as_string()
        assert "comment" not in result.lower()
        assert "INT,int" in result

    def test_line_comment_until_newline(self):
        """Line comment ends at newline"""
        result = Tokenizer("// comment\nint x;").get_tokens_as_string()
        assert "INT,int" in result

    def test_block_comment_skipped(self):
        """Block comment should be skipped"""
        result = Tokenizer("int /* comment */ x;").get_tokens_as_string()
        assert "comment" not in result.lower()
        assert "INT,int" in result

    def test_block_comment_multiline(self):
        """Block comment can span multiple lines"""
        result = Tokenizer("int /* multi\nline */ x;").get_tokens_as_string()
        assert "INT,int" in result
        assert "ID,x" in result

    def test_nested_comment_markers(self):
        """// in block comment has no meaning"""
        result = Tokenizer("/* // nested */int x;").get_tokens_as_string()
        assert "INT,int" in result

    def test_block_in_line_comment(self):
        """/* in line comment has no meaning"""
        result = Tokenizer("// /* still line\nint x;").get_tokens_as_string()
        assert "INT,int" in result


# ============================================================
# ERROR TESTS - UNRECOGNIZED CHARACTER (5 tests)
# ============================================================

class TestErrorToken:
    """Test unrecognized character handling"""

    def test_at_symbol(self):
        with pytest.raises(Exception, match="Error Token"):
            Tokenizer("@").get_tokens_as_string()

    def test_hash_symbol(self):
        with pytest.raises(Exception, match="Error Token"):
            Tokenizer("#").get_tokens_as_string()

    def test_dollar_symbol(self):
        with pytest.raises(Exception, match="Error Token"):
            Tokenizer("$").get_tokens_as_string()

    def test_backtick(self):
        with pytest.raises(Exception, match="Error Token"):
            Tokenizer("`").get_tokens_as_string()

    def test_error_in_code(self):
        """Error character in middle of valid code"""
        with pytest.raises(Exception, match="Error Token"):
            Tokenizer("int x = @10;").get_tokens_as_string()


# ============================================================
# ERROR TESTS - UNCLOSED STRING (5 tests)
# ============================================================

class TestUncloseString:
    """Test unclosed string handling"""

    def test_no_closing_quote(self):
        with pytest.raises(Exception, match="Unclosed String"):
            Tokenizer('"hello').get_tokens_as_string()

    def test_string_with_newline(self):
        """String cannot contain actual newline"""
        with pytest.raises(Exception, match="Unclosed String"):
            Tokenizer('"hello\n').get_tokens_as_string()

    def test_empty_unclosed(self):
        with pytest.raises(Exception, match="Unclosed String"):
            Tokenizer('"').get_tokens_as_string()

    def test_unclosed_with_escape(self):
        with pytest.raises(Exception, match="Unclosed String"):
            Tokenizer('"hello\\n').get_tokens_as_string()

    def test_unclosed_in_code(self):
        with pytest.raises(Exception, match="Unclosed String"):
            Tokenizer('string s = "hello;').get_tokens_as_string()


# ============================================================
# ERROR TESTS - ILLEGAL ESCAPE (5 tests)
# ============================================================

class TestIllegalEscape:
    """Test illegal escape sequence handling"""

    def test_invalid_escape_x(self):
        with pytest.raises(Exception, match="Illegal Escape"):
            Tokenizer('"hello\\x"').get_tokens_as_string()

    def test_invalid_escape_a(self):
        with pytest.raises(Exception, match="Illegal Escape"):
            Tokenizer('"hello\\a"').get_tokens_as_string()

    def test_invalid_escape_digit(self):
        with pytest.raises(Exception, match="Illegal Escape"):
            Tokenizer('"hello\\1"').get_tokens_as_string()

    def test_invalid_escape_space(self):
        with pytest.raises(Exception, match="Illegal Escape"):
            Tokenizer('"hello\\ "').get_tokens_as_string()

    def test_illegal_after_valid_escape(self):
        """Illegal escape after valid escapes"""
        with pytest.raises(Exception, match="Illegal Escape"):
            Tokenizer('"\\n\\t\\x"').get_tokens_as_string()


# ============================================================
# COMPLEX SEQUENCE TESTS (8 tests)
# ============================================================

class TestComplexSequences:
    """Test complex token sequences"""

    def test_variable_declaration(self):
        """Test variable declaration tokens"""
        result = Tokenizer("int x = 10;").get_tokens_as_string()
        assert "INT,int" in result
        assert "ID,x" in result
        assert "ASSIGN,=" in result
        assert "INT_LIT,10" in result
        assert "SEMI,;" in result

    def test_function_call(self):
        """Test function call tokens"""
        result = Tokenizer("foo(a, b)").get_tokens_as_string()
        assert "ID,foo" in result
        assert "LPAREN,(" in result
        assert "ID,a" in result
        assert "COMMA,," in result
        assert "ID,b" in result
        assert "RPAREN,)" in result

    def test_arithmetic_expression(self):
        """Test arithmetic expression tokens"""
        result = Tokenizer("a + b * c - d / e").get_tokens_as_string()
        assert "ID,a" in result
        assert "PLUS,+" in result
        assert "MUL,*" in result
        assert "MINUS,-" in result
        assert "DIV,/" in result

    def test_comparison_expression(self):
        """Test comparison expression tokens"""
        result = Tokenizer("a < b && c >= d").get_tokens_as_string()
        assert "LT,<" in result
        assert "AND,&&" in result
        assert "GE,>=" in result

    def test_for_loop(self):
        """Test for loop tokens"""
        result = Tokenizer(
            "for (int i = 0; i < 10; i++)").get_tokens_as_string()
        assert "FOR,for" in result
        assert "INT,int" in result
        assert "ID,i" in result
        assert "LT,<" in result
        assert "INC,++" in result

    def test_struct_declaration(self):
        """Test struct declaration tokens"""
        result = Tokenizer("struct Point { int x; };").get_tokens_as_string()
        assert "STRUCT,struct" in result
        assert "ID,Point" in result
        assert "LBRACE,{" in result
        assert "RBRACE,}" in result

    def test_if_else(self):
        """Test if-else tokens"""
        result = Tokenizer("if (x > 0) { } else { }").get_tokens_as_string()
        assert "IF,if" in result
        assert "ELSE,else" in result
        assert "GT,>" in result

    def test_member_access(self):
        """Test member access tokens"""
        result = Tokenizer("p.x = 10;").get_tokens_as_string()
        assert "ID,p" in result
        assert "DOT,." in result
        assert "ID,x" in result
