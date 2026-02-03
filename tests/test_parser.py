"""
Parser test cases for TyC compiler
File: tests/test_parser.py
"""

import pytest
from tests.utils import Parser


# ============================================================
# PROGRAM STRUCTURE TESTS
# ============================================================

class TestProgramStructure:
    """Test overall program structure"""

    def test_empty_program(self):
        """Empty program is valid"""
        assert Parser("").parse() == "success"

    def test_single_function(self):
        """Program with one function"""
        assert Parser("void main() {}").parse() == "success"

    def test_multiple_functions(self):
        """Program with multiple functions"""
        source = """
        void foo() {}
        int bar() { return 0; }
        void main() {}
        """
        assert Parser(source).parse() == "success"

    def test_struct_and_function(self):
        """Program with struct and function"""
        source = """
        struct Point { int x; int y; };
        void main() {}
        """
        assert Parser(source).parse() == "success"


# ============================================================
# STRUCT DECLARATION TESTS
# ============================================================

class TestStructDeclaration:
    """Test struct declaration parsing"""

    def test_simple_struct(self):
        source = "struct Point { int x; };"
        assert Parser(source).parse() == "success"

    def test_struct_multiple_members(self):
        source = """
        struct Person {
            string name;
            int age;
            float height;
        };
        """
        assert Parser(source).parse() == "success"

    def test_struct_with_struct_member(self):
        """Struct member can be another struct type"""
        source = """
        struct Point { int x; int y; };
        struct Line { Point start; Point end; };
        """
        assert Parser(source).parse() == "success"

    def test_empty_struct(self):
        """Empty struct is valid"""
        source = "struct Empty {};"
        assert Parser(source).parse() == "success"


# ============================================================
# FUNCTION DECLARATION TESTS
# ============================================================

class TestFunctionDeclaration:
    """Test function declaration parsing"""

    def test_void_function_no_params(self):
        source = "void main() {}"
        assert Parser(source).parse() == "success"

    def test_function_with_return_type(self):
        source = "int add() { return 0; }"
        assert Parser(source).parse() == "success"

    def test_function_with_params(self):
        source = "int add(int x, int y) { return x + y; }"
        assert Parser(source).parse() == "success"

    def test_function_inferred_return_type(self):
        """Return type can be omitted (inferred)"""
        source = "add(int x, int y) { return x + y; }"
        assert Parser(source).parse() == "success"

    def test_function_struct_param(self):
        source = """
        struct Point { int x; int y; };
        void print(Point p) {}
        """
        assert Parser(source).parse() == "success"

    def test_function_struct_return(self):
        source = """
        struct Point { int x; int y; };
        Point create() { return {0, 0}; }
        """
        assert Parser(source).parse() == "success"


# ============================================================
# VARIABLE DECLARATION TESTS
# ============================================================

class TestVariableDeclaration:
    """Test variable declaration parsing"""

    def test_auto_with_init(self):
        source = "void main() { auto x = 10; }"
        assert Parser(source).parse() == "success"

    def test_auto_without_init(self):
        source = "void main() { auto x; }"
        assert Parser(source).parse() == "success"

    def test_explicit_int(self):
        source = "void main() { int x = 10; }"
        assert Parser(source).parse() == "success"

    def test_explicit_float(self):
        source = "void main() { float f = 3.14; }"
        assert Parser(source).parse() == "success"

    def test_explicit_string(self):
        source = 'void main() { string s = "hello"; }'
        assert Parser(source).parse() == "success"

    def test_struct_var_no_init(self):
        source = """
        struct Point { int x; int y; };
        void main() { Point p; }
        """
        assert Parser(source).parse() == "success"

    def test_struct_var_with_init(self):
        source = """
        struct Point { int x; int y; };
        void main() { Point p = {10, 20}; }
        """
        assert Parser(source).parse() == "success"


# ============================================================
# IF STATEMENT TESTS
# ============================================================

class TestIfStatement:
    """Test if statement parsing"""

    def test_simple_if(self):
        source = "void main() { if (x > 0) { y = 1; } }"
        assert Parser(source).parse() == "success"

    def test_if_else(self):
        source = "void main() { if (x > 0) { y = 1; } else { y = 0; } }"
        assert Parser(source).parse() == "success"

    def test_if_without_braces(self):
        source = "void main() { if (x > 0) y = 1; }"
        assert Parser(source).parse() == "success"

    def test_nested_if(self):
        source = """
        void main() {
            if (x > 0) {
                if (y > 0) {
                    z = 1;
                }
            }
        }
        """
        assert Parser(source).parse() == "success"

    def test_if_else_if(self):
        source = """
        void main() {
            if (x > 0) {
                y = 1;
            } else if (x < 0) {
                y = -1;
            } else {
                y = 0;
            }
        }
        """
        assert Parser(source).parse() == "success"


# ============================================================
# WHILE STATEMENT TESTS
# ============================================================

class TestWhileStatement:
    """Test while statement parsing"""

    def test_simple_while(self):
        source = "void main() { while (x < 10) { x = x + 1; } }"
        assert Parser(source).parse() == "success"

    def test_while_without_braces(self):
        source = "void main() { while (x < 10) x = x + 1; }"
        assert Parser(source).parse() == "success"

    def test_nested_while(self):
        source = """
        void main() {
            while (i < 10) {
                while (j < 10) {
                    j = j + 1;
                }
                i = i + 1;
            }
        }
        """
        assert Parser(source).parse() == "success"


# ============================================================
# FOR STATEMENT TESTS
# ============================================================

class TestForStatement:
    """Test for statement parsing"""

    def test_full_for(self):
        source = "void main() { for (auto i = 0; i < 10; i++) { } }"
        assert Parser(source).parse() == "success"

    def test_for_explicit_type(self):
        source = "void main() { for (int i = 0; i < 10; ++i) { } }"
        assert Parser(source).parse() == "success"

    def test_for_no_init(self):
        source = "void main() { for (; i < 10; i++) { } }"
        assert Parser(source).parse() == "success"

    def test_for_no_condition(self):
        """Infinite loop with break"""
        source = "void main() { for (auto i = 0; ; i++) { break; } }"
        assert Parser(source).parse() == "success"

    def test_for_no_update(self):
        source = "void main() { for (auto i = 0; i < 10; ) { i = i + 1; } }"
        assert Parser(source).parse() == "success"

    def test_for_empty(self):
        """Empty for loop - infinite loop"""
        source = "void main() { for (;;) { break; } }"
        assert Parser(source).parse() == "success"


# ============================================================
# SWITCH STATEMENT TESTS
# ============================================================

class TestSwitchStatement:
    """Test switch statement parsing"""

    def test_simple_switch(self):
        source = """
        void main() {
            switch (x) {
                case 1:
                    y = 1;
                    break;
            }
        }
        """
        assert Parser(source).parse() == "success"

    def test_switch_with_default(self):
        source = """
        void main() {
            switch (x) {
                case 1:
                    y = 1;
                    break;
                default:
                    y = 0;
            }
        }
        """
        assert Parser(source).parse() == "success"

    def test_switch_multiple_cases(self):
        source = """
        void main() {
            switch (x) {
                case 1:
                case 2:
                    y = 1;
                    break;
                case 3:
                    y = 3;
                    break;
                default:
                    y = 0;
            }
        }
        """
        assert Parser(source).parse() == "success"

    def test_switch_fallthrough(self):
        """Cases without break fall through"""
        source = """
        void main() {
            switch (x) {
                case 1:
                    y = 1;
                case 2:
                    z = 2;
                    break;
            }
        }
        """
        assert Parser(source).parse() == "success"


# ============================================================
# EXPRESSION TESTS
# ============================================================

class TestExpressions:
    """Test expression parsing"""

    def test_arithmetic_add(self):
        source = "void main() { auto x = 1 + 2; }"
        assert Parser(source).parse() == "success"

    def test_arithmetic_precedence(self):
        source = "void main() { auto x = 1 + 2 * 3; }"
        assert Parser(source).parse() == "success"

    def test_arithmetic_parentheses(self):
        source = "void main() { auto x = (1 + 2) * 3; }"
        assert Parser(source).parse() == "success"

    def test_relational(self):
        source = "void main() { auto x = a < b; }"
        assert Parser(source).parse() == "success"

    def test_logical_and(self):
        source = "void main() { auto x = a && b; }"
        assert Parser(source).parse() == "success"

    def test_logical_or(self):
        source = "void main() { auto x = a || b; }"
        assert Parser(source).parse() == "success"

    def test_logical_not(self):
        source = "void main() { auto x = !a; }"
        assert Parser(source).parse() == "success"

    def test_unary_minus(self):
        source = "void main() { auto x = -a; }"
        assert Parser(source).parse() == "success"

    def test_prefix_increment(self):
        source = "void main() { ++x; }"
        assert Parser(source).parse() == "success"

    def test_postfix_increment(self):
        source = "void main() { x++; }"
        assert Parser(source).parse() == "success"

    def test_member_access(self):
        source = """
        struct Point { int x; int y; };
        void main() { Point p; auto x = p.x; }
        """
        assert Parser(source).parse() == "success"

    def test_function_call_no_args(self):
        source = """
        int foo() { return 0; }
        void main() { auto x = foo(); }
        """
        assert Parser(source).parse() == "success"

    def test_function_call_with_args(self):
        source = """
        int add(int x, int y) { return x + y; }
        void main() { auto x = add(1, 2); }
        """
        assert Parser(source).parse() == "success"

    def test_complex_expression(self):
        source = "void main() { auto x = a + b * c - d / e % f; }"
        assert Parser(source).parse() == "success"

    def test_assignment_right_associative(self):
        source = "void main() { a = b = c = 10; }"
        assert Parser(source).parse() == "success"


# ============================================================
# SYNTAX ERROR TESTS
# ============================================================

class TestSyntaxErrors:
    """Test syntax error detection"""

    def test_missing_semicolon(self):
        source = "void main() { int x = 10 }"
        result = Parser(source).parse()
        assert result != "success"

    def test_missing_closing_brace(self):
        source = "void main() { int x = 10;"
        result = Parser(source).parse()
        assert result != "success"

    def test_missing_opening_brace(self):
        source = "void main() int x = 10; }"
        result = Parser(source).parse()
        assert result != "success"

    def test_missing_parenthesis_if(self):
        source = "void main() { if x > 0 { } }"
        result = Parser(source).parse()
        assert result != "success"

    def test_missing_condition_while(self):
        source = "void main() { while { } }"
        result = Parser(source).parse()
        assert result != "success"

    def test_invalid_expression(self):
        source = "void main() { auto x = 1 + ; }"
        result = Parser(source).parse()
        assert result != "success"

    def test_double_operator(self):
        source = "void main() { auto x = 1 ++ 2; }"
        result = Parser(source).parse()
        assert result != "success"

    def test_missing_struct_name(self):
        source = "struct { int x; };"
        result = Parser(source).parse()
        assert result != "success"

    def test_missing_function_body(self):
        source = "void main();"
        result = Parser(source).parse()
        assert result != "success"
