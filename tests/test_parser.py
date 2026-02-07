"""
Parser test cases for TyC compiler
100 test cases covering program structure, declarations, statements, and expressions
"""

import pytest
from tests.utils import Parser


# ============================================================
# PROGRAM STRUCTURE TESTS (5 tests)
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

    def test_multiple_structs_and_functions(self):
        """Program with multiple structs and functions"""
        source = """
        struct Point { int x; int y; };
        struct Person { string name; int age; };
        void helper() {}
        void main() {}
        """
        assert Parser(source).parse() == "success"


# ============================================================
# STRUCT DECLARATION TESTS (8 tests)
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

    def test_struct_int_members(self):
        source = "struct Data { int a; int b; int c; };"
        assert Parser(source).parse() == "success"

    def test_struct_float_members(self):
        source = "struct Coords { float x; float y; float z; };"
        assert Parser(source).parse() == "success"

    def test_struct_string_member(self):
        source = "struct Config { string name; string value; };"
        assert Parser(source).parse() == "success"

    def test_struct_mixed_types(self):
        source = "struct Record { int id; string name; float score; };"
        assert Parser(source).parse() == "success"


# ============================================================
# FUNCTION DECLARATION TESTS (10 tests)
# ============================================================

class TestFunctionDeclaration:
    """Test function declaration parsing"""

    def test_void_function_no_params(self):
        source = "void main() {}"
        assert Parser(source).parse() == "success"

    def test_function_with_return_type(self):
        source = "int getNumber() { return 0; }"
        assert Parser(source).parse() == "success"

    def test_function_with_one_param(self):
        source = "int square(int x) { return x * x; }"
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

    def test_function_float_param(self):
        source = "float multiply(float a, float b) { return a * b; }"
        assert Parser(source).parse() == "success"

    def test_function_string_param(self):
        source = "void greet(string name) { printString(name); }"
        assert Parser(source).parse() == "success"

    def test_function_many_params(self):
        source = "void func(int a, int b, int c, float d, string e) {}"
        assert Parser(source).parse() == "success"


# ============================================================
# VARIABLE DECLARATION TESTS (10 tests)
# ============================================================

class TestVariableDeclaration:
    """Test variable declaration parsing"""

    def test_auto_with_int_init(self):
        source = "void main() { auto x = 10; }"
        assert Parser(source).parse() == "success"

    def test_auto_with_float_init(self):
        source = "void main() { auto f = 3.14; }"
        assert Parser(source).parse() == "success"

    def test_auto_with_string_init(self):
        source = 'void main() { auto s = "hello"; }'
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

    def test_explicit_no_init(self):
        source = "void main() { int x; float y; string z; }"
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
# IF STATEMENT TESTS (8 tests)
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

    def test_if_else_without_braces(self):
        source = "void main() { if (x > 0) y = 1; else y = 0; }"
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

    def test_if_with_logical_condition(self):
        source = "void main() { if (x > 0 && y > 0) { z = 1; } }"
        assert Parser(source).parse() == "success"

    def test_if_with_complex_condition(self):
        source = "void main() { if ((x > 0 && y > 0) || z == 0) { a = 1; } }"
        assert Parser(source).parse() == "success"


# ============================================================
# WHILE STATEMENT TESTS (5 tests)
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

    def test_while_with_break(self):
        source = "void main() { while (1) { if (x > 10) break; x = x + 1; } }"
        assert Parser(source).parse() == "success"

    def test_while_with_continue(self):
        source = "void main() { while (i < 10) { if (i == 5) continue; i = i + 1; } }"
        assert Parser(source).parse() == "success"


# ============================================================
# FOR STATEMENT TESTS (8 tests)
# ============================================================

class TestForStatement:
    """Test for statement parsing"""

    def test_full_for_auto(self):
        source = "void main() { for (auto i = 0; i < 10; i++) { } }"
        assert Parser(source).parse() == "success"

    def test_full_for_explicit_type(self):
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

    def test_for_prefix_increment(self):
        source = "void main() { for (auto i = 0; i < 10; ++i) { } }"
        assert Parser(source).parse() == "success"

    def test_for_decrement(self):
        source = "void main() { for (auto i = 10; i > 0; --i) { } }"
        assert Parser(source).parse() == "success"


# ============================================================
# SWITCH STATEMENT TESTS (8 tests)
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
                    y = 1;
                    break;
                case 2:
                    y = 2;
                    break;
                case 3:
                    y = 3;
                    break;
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
                case 2:
                    y = 1;
                    break;
            }
        }
        """
        assert Parser(source).parse() == "success"

    def test_switch_empty_cases(self):
        source = """
        void main() {
            switch (x) {
                case 1:
                case 2:
                case 3:
                    y = 1;
                    break;
                default:
            }
        }
        """
        assert Parser(source).parse() == "success"

    def test_switch_only_default(self):
        source = """
        void main() {
            switch (x) {
                default:
                    y = 0;
            }
        }
        """
        assert Parser(source).parse() == "success"

    def test_switch_empty(self):
        source = "void main() { switch (x) { } }"
        assert Parser(source).parse() == "success"

    def test_switch_nested_statement(self):
        source = """
        void main() {
            switch (x) {
                case 1:
                    if (y > 0) {
                        z = 1;
                    }
                    break;
            }
        }
        """
        assert Parser(source).parse() == "success"


# ============================================================
# BREAK/CONTINUE/RETURN TESTS (6 tests)
# ============================================================

class TestControlStatements:
    """Test break, continue, return statements"""

    def test_break_in_while(self):
        source = "void main() { while (1) { break; } }"
        assert Parser(source).parse() == "success"

    def test_break_in_for(self):
        source = "void main() { for (;;) { break; } }"
        assert Parser(source).parse() == "success"

    def test_continue_in_while(self):
        source = "void main() { while (1) { continue; } }"
        assert Parser(source).parse() == "success"

    def test_continue_in_for(self):
        source = "void main() { for (auto i = 0; i < 10; i++) { continue; } }"
        assert Parser(source).parse() == "success"

    def test_return_void(self):
        source = "void main() { return; }"
        assert Parser(source).parse() == "success"

    def test_return_expression(self):
        source = "int get() { return 42; }"
        assert Parser(source).parse() == "success"


# ============================================================
# ARITHMETIC EXPRESSION TESTS (8 tests)
# ============================================================

class TestArithmeticExpressions:
    """Test arithmetic expression parsing"""

    def test_addition(self):
        source = "void main() { auto x = 1 + 2; }"
        assert Parser(source).parse() == "success"

    def test_subtraction(self):
        source = "void main() { auto x = 5 - 3; }"
        assert Parser(source).parse() == "success"

    def test_multiplication(self):
        source = "void main() { auto x = 2 * 3; }"
        assert Parser(source).parse() == "success"

    def test_division(self):
        source = "void main() { auto x = 10 / 2; }"
        assert Parser(source).parse() == "success"

    def test_modulo(self):
        source = "void main() { auto x = 10 % 3; }"
        assert Parser(source).parse() == "success"

    def test_precedence_mul_over_add(self):
        source = "void main() { auto x = 1 + 2 * 3; }"
        assert Parser(source).parse() == "success"

    def test_parentheses(self):
        source = "void main() { auto x = (1 + 2) * 3; }"
        assert Parser(source).parse() == "success"

    def test_complex_arithmetic(self):
        source = "void main() { auto x = a + b * c - d / e % f; }"
        assert Parser(source).parse() == "success"


# ============================================================
# RELATIONAL EXPRESSION TESTS (5 tests)
# ============================================================

class TestRelationalExpressions:
    """Test relational expression parsing"""

    def test_less_than(self):
        source = "void main() { auto x = a < b; }"
        assert Parser(source).parse() == "success"

    def test_greater_than(self):
        source = "void main() { auto x = a > b; }"
        assert Parser(source).parse() == "success"

    def test_less_equal(self):
        source = "void main() { auto x = a <= b; }"
        assert Parser(source).parse() == "success"

    def test_greater_equal(self):
        source = "void main() { auto x = a >= b; }"
        assert Parser(source).parse() == "success"

    def test_equality(self):
        source = "void main() { auto x = a == b; auto y = a != b; }"
        assert Parser(source).parse() == "success"


# ============================================================
# LOGICAL EXPRESSION TESTS (5 tests)
# ============================================================

class TestLogicalExpressions:
    """Test logical expression parsing"""

    def test_logical_and(self):
        source = "void main() { auto x = a && b; }"
        assert Parser(source).parse() == "success"

    def test_logical_or(self):
        source = "void main() { auto x = a || b; }"
        assert Parser(source).parse() == "success"

    def test_logical_not(self):
        source = "void main() { auto x = !a; }"
        assert Parser(source).parse() == "success"

    def test_combined_logical(self):
        source = "void main() { auto x = a && b || c; }"
        assert Parser(source).parse() == "success"

    def test_logical_with_parentheses(self):
        source = "void main() { auto x = (a && b) || (c && d); }"
        assert Parser(source).parse() == "success"


# ============================================================
# UNARY EXPRESSION TESTS (5 tests)
# ============================================================

class TestUnaryExpressions:
    """Test unary expression parsing"""

    def test_unary_minus(self):
        source = "void main() { auto x = -a; }"
        assert Parser(source).parse() == "success"

    def test_unary_plus(self):
        source = "void main() { auto x = +a; }"
        assert Parser(source).parse() == "success"

    def test_prefix_increment(self):
        source = "void main() { ++x; }"
        assert Parser(source).parse() == "success"

    def test_prefix_decrement(self):
        source = "void main() { --x; }"
        assert Parser(source).parse() == "success"

    def test_chained_unary(self):
        source = "void main() { auto x = --a; auto y = !!b; }"
        assert Parser(source).parse() == "success"


# ============================================================
# POSTFIX EXPRESSION TESTS (7 tests)
# ============================================================

class TestPostfixExpressions:
    """Test postfix expression parsing"""

    def test_postfix_increment(self):
        source = "void main() { x++; }"
        assert Parser(source).parse() == "success"

    def test_postfix_decrement(self):
        source = "void main() { x--; }"
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

    def test_chained_member_access(self):
        source = """
        struct Inner { int value; };
        struct Outer { Inner inner; };
        void main() { Outer o; auto v = o.inner.value; }
        """
        assert Parser(source).parse() == "success"

    def test_function_call_with_expression_args(self):
        source = """
        int add(int x, int y) { return x + y; }
        void main() { auto x = add(1 + 2, 3 * 4); }
        """
        assert Parser(source).parse() == "success"


# ============================================================
# ASSIGNMENT EXPRESSION TESTS (4 tests)
# ============================================================

class TestAssignmentExpressions:
    """Test assignment expression parsing"""

    def test_simple_assignment(self):
        source = "void main() { x = 10; }"
        assert Parser(source).parse() == "success"

    def test_assignment_right_associative(self):
        source = "void main() { a = b = c = 10; }"
        assert Parser(source).parse() == "success"

    def test_assignment_member(self):
        source = """
        struct Point { int x; int y; };
        void main() { Point p; p.x = 10; }
        """
        assert Parser(source).parse() == "success"

    def test_assignment_with_expression(self):
        source = "void main() { x = y + z * 2; }"
        assert Parser(source).parse() == "success"


# ============================================================
# SYNTAX ERROR TESTS (10 tests)
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

    def test_invalid_expression_missing_operand(self):
        source = "void main() { auto x = 1 + ; }"
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

    def test_double_keyword(self):
        source = "void main() { int int x; }"
        result = Parser(source).parse()
        assert result != "success"

    def test_missing_closing_parenthesis(self):
        source = "void main() { if (x > 0 { } }"
        result = Parser(source).parse()
        assert result != "success"
