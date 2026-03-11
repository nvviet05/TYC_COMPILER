"""
AST Generation test cases for TyC compiler.
100 test cases covering all AST node types and language features.
"""

import pytest
from tests.utils import ASTGenerator


# ============================================================
# PROGRAM STRUCTURE (5 tests)
# ============================================================

class TestProgramStructure:

    def test_empty_program(self):
        assert str(ASTGenerator("").generate()) == "Program([])"

    def test_single_void_function(self):
        src = "void main() {}"
        expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
        assert str(ASTGenerator(src).generate()) == expected

    def test_two_functions(self):
        src = "void foo() {} void bar() {}"
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(VoidType(), foo" in result
        assert "FuncDecl(VoidType(), bar" in result

    def test_struct_then_function(self):
        src = "struct Point { int x; }; void main() {}"
        result = str(ASTGenerator(src).generate())
        assert result.startswith("Program([StructDecl(Point")
        assert "FuncDecl(VoidType(), main" in result

    def test_multiple_structs_and_functions(self):
        src = """
        struct A { int x; };
        void foo() {}
        struct B { float y; };
        void bar() {}
        """
        result = str(ASTGenerator(src).generate())
        assert "StructDecl(A" in result
        assert "StructDecl(B" in result
        assert "FuncDecl(VoidType(), foo" in result
        assert "FuncDecl(VoidType(), bar" in result


# ============================================================
# STRUCT DECLARATIONS (8 tests)
# ============================================================

class TestStructDecl:

    def test_struct_single_int_member(self):
        src = "struct Point { int x; };"
        result = str(ASTGenerator(src).generate())
        assert "StructDecl(Point, [MemberDecl(IntType(), x)])" in result

    def test_struct_two_members(self):
        src = "struct Point { int x; int y; };"
        result = str(ASTGenerator(src).generate())
        assert "MemberDecl(IntType(), x)" in result
        assert "MemberDecl(IntType(), y)" in result

    def test_struct_float_member(self):
        src = "struct Data { float value; };"
        result = str(ASTGenerator(src).generate())
        assert "MemberDecl(FloatType(), value)" in result

    def test_struct_string_member(self):
        src = "struct Config { string name; };"
        result = str(ASTGenerator(src).generate())
        assert "MemberDecl(StringType(), name)" in result

    def test_struct_mixed_types(self):
        src = "struct Person { string name; int age; float height; };"
        result = str(ASTGenerator(src).generate())
        assert "MemberDecl(StringType(), name)" in result
        assert "MemberDecl(IntType(), age)" in result
        assert "MemberDecl(FloatType(), height)" in result

    def test_struct_with_struct_member(self):
        src = "struct Point { int x; }; struct Line { Point start; Point end; };"
        result = str(ASTGenerator(src).generate())
        assert "MemberDecl(StructType(Point), start)" in result
        assert "MemberDecl(StructType(Point), end)" in result

    def test_empty_struct(self):
        src = "struct Empty {};"
        result = str(ASTGenerator(src).generate())
        assert "StructDecl(Empty, [])" in result

    def test_struct_three_int_members(self):
        src = "struct Vec3 { int x; int y; int z; };"
        result = str(ASTGenerator(src).generate())
        assert "StructDecl(Vec3, [MemberDecl(IntType(), x), MemberDecl(IntType(), y), MemberDecl(IntType(), z)])" in result


# ============================================================
# FUNCTION DECLARATIONS (10 tests)
# ============================================================

class TestFuncDecl:

    def test_void_no_params(self):
        src = "void main() {}"
        expected = "Program([FuncDecl(VoidType(), main, [], BlockStmt([]))])"
        assert str(ASTGenerator(src).generate()) == expected

    def test_int_return_type(self):
        src = "int getVal() { return 0; }"
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(IntType(), getVal, []" in result

    def test_float_return_type(self):
        src = "float getPI() { return 3.14; }"
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(FloatType(), getPI, []" in result

    def test_string_return_type(self):
        src = 'string getName() { return "hi"; }'
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(StringType(), getName, []" in result

    def test_one_param(self):
        src = "int square(int x) { return x; }"
        result = str(ASTGenerator(src).generate())
        assert "Param(IntType(), x)" in result

    def test_two_params(self):
        src = "int add(int a, int b) { return a; }"
        result = str(ASTGenerator(src).generate())
        assert "Param(IntType(), a)" in result
        assert "Param(IntType(), b)" in result

    def test_mixed_param_types(self):
        src = "void func(int a, float b, string c) {}"
        result = str(ASTGenerator(src).generate())
        assert "Param(IntType(), a)" in result
        assert "Param(FloatType(), b)" in result
        assert "Param(StringType(), c)" in result

    def test_struct_param(self):
        src = "struct P { int x; }; void f(P p) {}"
        result = str(ASTGenerator(src).generate())
        assert "Param(StructType(P), p)" in result

    def test_inferred_return_type(self):
        src = "add(int x, int y) { return x; }"
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(auto, add" in result

    def test_struct_return_type(self):
        src = "struct P { int x; }; P make() { return {0}; }"
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(StructType(P), make" in result


# ============================================================
# VARIABLE DECLARATIONS (10 tests)
# ============================================================

class TestVarDecl:

    def test_auto_with_int(self):
        src = "void main() { auto x = 10; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(auto, x = IntLiteral(10))" in result

    def test_auto_with_float(self):
        src = "void main() { auto f = 3.14; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(auto, f = FloatLiteral(3.14))" in result

    def test_auto_with_string(self):
        src = 'void main() { auto s = "hello"; }'
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(auto, s = StringLiteral('hello'))" in result

    def test_auto_no_init(self):
        src = "void main() { auto x; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(auto, x)" in result

    def test_explicit_int(self):
        src = "void main() { int x = 5; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(IntType(), x = IntLiteral(5))" in result

    def test_explicit_float(self):
        src = "void main() { float f = 2.5; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(FloatType(), f = FloatLiteral(2.5))" in result

    def test_explicit_string(self):
        src = 'void main() { string s = "world"; }'
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(StringType(), s = StringLiteral('world'))" in result

    def test_explicit_no_init(self):
        src = "void main() { int x; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(IntType(), x)" in result

    def test_struct_var_no_init(self):
        src = "struct P { int x; }; void main() { P p; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(StructType(P), p)" in result

    def test_struct_var_with_init(self):
        src = "struct P { int x; int y; }; void main() { P p = {1, 2}; }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(StructType(P), p = StructLiteral({IntLiteral(1), IntLiteral(2)}))" in result


# ============================================================
# LITERALS (8 tests)
# ============================================================

class TestLiterals:

    def test_int_literal_zero(self):
        src = "void main() { auto x = 0; }"
        result = str(ASTGenerator(src).generate())
        assert "IntLiteral(0)" in result

    def test_int_literal_large(self):
        src = "void main() { auto x = 99999; }"
        result = str(ASTGenerator(src).generate())
        assert "IntLiteral(99999)" in result

    def test_float_literal_simple(self):
        src = "void main() { auto x = 1.5; }"
        result = str(ASTGenerator(src).generate())
        assert "FloatLiteral(1.5)" in result

    def test_float_literal_scientific(self):
        src = "void main() { auto x = 1e2; }"
        result = str(ASTGenerator(src).generate())
        assert "FloatLiteral(100.0)" in result

    def test_float_literal_dot_only(self):
        src = "void main() { auto x = .5; }"
        result = str(ASTGenerator(src).generate())
        assert "FloatLiteral(0.5)" in result

    def test_string_literal_empty(self):
        src = 'void main() { auto s = ""; }'
        result = str(ASTGenerator(src).generate())
        assert "StringLiteral('')" in result

    def test_string_literal_with_escape(self):
        src = 'void main() { auto s = "a\\nb"; }'
        result = str(ASTGenerator(src).generate())
        assert "StringLiteral(" in result

    def test_struct_literal_empty(self):
        src = "struct E {}; void main() { E e = {}; }"
        result = str(ASTGenerator(src).generate())
        assert "StructLiteral({})" in result


# ============================================================
# ARITHMETIC EXPRESSIONS (8 tests)
# ============================================================

class TestArithmeticExpr:

    def test_addition(self):
        src = "void main() { auto x = 1 + 2; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(IntLiteral(1), +, IntLiteral(2))" in result

    def test_subtraction(self):
        src = "void main() { auto x = 5 - 3; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(IntLiteral(5), -, IntLiteral(3))" in result

    def test_multiplication(self):
        src = "void main() { auto x = 2 * 3; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(IntLiteral(2), *, IntLiteral(3))" in result

    def test_division(self):
        src = "void main() { auto x = 10 / 2; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(IntLiteral(10), /, IntLiteral(2))" in result

    def test_modulo(self):
        src = "void main() { auto x = 7 % 3; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(IntLiteral(7), %, IntLiteral(3))" in result

    def test_precedence_mul_over_add(self):
        src = "void main() { auto x = 1 + 2 * 3; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(IntLiteral(1), +, BinaryOp(IntLiteral(2), *, IntLiteral(3)))" in result

    def test_left_associativity(self):
        src = "void main() { auto x = 1 - 2 - 3; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(BinaryOp(IntLiteral(1), -, IntLiteral(2)), -, IntLiteral(3))" in result

    def test_parenthesized(self):
        src = "void main() { auto x = (1 + 2) * 3; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(BinaryOp(IntLiteral(1), +, IntLiteral(2)), *, IntLiteral(3))" in result


# ============================================================
# RELATIONAL EXPRESSIONS (6 tests)
# ============================================================

class TestRelationalExpr:

    def test_less_than(self):
        src = "void main() { auto x = a < b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), <, Identifier(b))" in result

    def test_greater_than(self):
        src = "void main() { auto x = a > b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), >, Identifier(b))" in result

    def test_less_equal(self):
        src = "void main() { auto x = a <= b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), <=, Identifier(b))" in result

    def test_greater_equal(self):
        src = "void main() { auto x = a >= b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), >=, Identifier(b))" in result

    def test_equal(self):
        src = "void main() { auto x = a == b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), ==, Identifier(b))" in result

    def test_not_equal(self):
        src = "void main() { auto x = a != b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), !=, Identifier(b))" in result


# ============================================================
# LOGICAL EXPRESSIONS (5 tests)
# ============================================================

class TestLogicalExpr:

    def test_and(self):
        src = "void main() { auto x = a && b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), &&, Identifier(b))" in result

    def test_or(self):
        src = "void main() { auto x = a || b; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(a), ||, Identifier(b))" in result

    def test_not(self):
        src = "void main() { auto x = !a; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(!Identifier(a))" in result

    def test_and_or_precedence(self):
        src = "void main() { auto x = a && b || c; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(BinaryOp(Identifier(a), &&, Identifier(b)), ||, Identifier(c))" in result

    def test_double_not(self):
        src = "void main() { auto x = !!a; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(!PrefixOp(!Identifier(a)))" in result


# ============================================================
# UNARY AND PREFIX/POSTFIX (8 tests)
# ============================================================

class TestUnaryExpr:

    def test_unary_minus(self):
        src = "void main() { auto x = -a; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(-Identifier(a))" in result

    def test_unary_plus(self):
        src = "void main() { auto x = +a; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(+Identifier(a))" in result

    def test_prefix_increment(self):
        src = "void main() { ++x; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(++Identifier(x))" in result

    def test_prefix_decrement(self):
        src = "void main() { --x; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(--Identifier(x))" in result

    def test_postfix_increment(self):
        src = "void main() { x++; }"
        result = str(ASTGenerator(src).generate())
        assert "PostfixOp(Identifier(x)++)" in result

    def test_postfix_decrement(self):
        src = "void main() { x--; }"
        result = str(ASTGenerator(src).generate())
        assert "PostfixOp(Identifier(x)--)" in result

    def test_negative_literal(self):
        src = "void main() { auto x = -5; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(-IntLiteral(5))" in result

    def test_chained_prefix(self):
        src = "void main() { ++++x; }"
        result = str(ASTGenerator(src).generate())
        assert "PrefixOp(++PrefixOp(++Identifier(x)))" in result


# ============================================================
# FUNCTION CALLS (5 tests)
# ============================================================

class TestFuncCall:

    def test_no_args(self):
        src = "void main() { foo(); }"
        result = str(ASTGenerator(src).generate())
        assert "FuncCall(foo, [])" in result

    def test_one_arg(self):
        src = "void main() { printInt(10); }"
        result = str(ASTGenerator(src).generate())
        assert "FuncCall(printInt, [IntLiteral(10)])" in result

    def test_two_args(self):
        src = "void main() { add(1, 2); }"
        result = str(ASTGenerator(src).generate())
        assert "FuncCall(add, [IntLiteral(1), IntLiteral(2)])" in result

    def test_expression_args(self):
        src = "void main() { f(a + b); }"
        result = str(ASTGenerator(src).generate())
        assert "FuncCall(f, [BinaryOp(Identifier(a), +, Identifier(b))])" in result

    def test_nested_call(self):
        src = "void main() { f(g(1)); }"
        result = str(ASTGenerator(src).generate())
        assert "FuncCall(f, [FuncCall(g, [IntLiteral(1)])])" in result


# ============================================================
# MEMBER ACCESS (5 tests)
# ============================================================

class TestMemberAccess:

    def test_simple_member_access(self):
        src = "void main() { auto x = p.x; }"
        result = str(ASTGenerator(src).generate())
        assert "MemberAccess(Identifier(p).x)" in result

    def test_chained_member_access(self):
        src = "void main() { auto v = a.b.c; }"
        result = str(ASTGenerator(src).generate())
        assert "MemberAccess(MemberAccess(Identifier(a).b).c)" in result

    def test_member_assign(self):
        src = "void main() { p.x = 10; }"
        result = str(ASTGenerator(src).generate())
        assert "AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(10))" in result

    def test_member_in_expression(self):
        src = "void main() { auto x = p.x + p.y; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(MemberAccess(Identifier(p).x), +, MemberAccess(Identifier(p).y))" in result

    def test_function_call_member_access(self):
        src = "void main() { auto x = getPoint().x; }"
        result = str(ASTGenerator(src).generate())
        assert "MemberAccess(FuncCall(getPoint, []).x)" in result


# ============================================================
# ASSIGNMENT (5 tests)
# ============================================================

class TestAssignment:

    def test_simple_assign(self):
        src = "void main() { x = 10; }"
        result = str(ASTGenerator(src).generate())
        assert "AssignStmt(AssignExpr(Identifier(x) = IntLiteral(10)))" in result

    def test_chained_assign(self):
        src = "void main() { a = b = 5; }"
        result = str(ASTGenerator(src).generate())
        assert "AssignExpr(Identifier(a) = AssignExpr(Identifier(b) = IntLiteral(5)))" in result

    def test_assign_expression(self):
        src = "void main() { x = a + b; }"
        result = str(ASTGenerator(src).generate())
        assert "AssignExpr(Identifier(x) = BinaryOp(Identifier(a), +, Identifier(b)))" in result

    def test_member_assign_chained(self):
        src = "void main() { a.b.c = 1; }"
        result = str(ASTGenerator(src).generate())
        assert "AssignExpr(MemberAccess(MemberAccess(Identifier(a).b).c) = IntLiteral(1))" in result

    def test_assign_func_call(self):
        src = "void main() { x = foo(); }"
        result = str(ASTGenerator(src).generate())
        assert "AssignExpr(Identifier(x) = FuncCall(foo, []))" in result


# ============================================================
# IF STATEMENT (5 tests)
# ============================================================

class TestIfStmt:

    def test_simple_if(self):
        src = "void main() { if (x) { y = 1; } }"
        result = str(ASTGenerator(src).generate())
        assert "IfStmt(if Identifier(x) then BlockStmt(" in result

    def test_if_else(self):
        src = "void main() { if (x) { a = 1; } else { a = 0; } }"
        result = str(ASTGenerator(src).generate())
        assert "IfStmt(" in result
        assert "else BlockStmt(" in result

    def test_if_no_braces(self):
        src = "void main() { if (x) y = 1; }"
        result = str(ASTGenerator(src).generate())
        assert "IfStmt(if Identifier(x) then AssignStmt(" in result

    def test_nested_if(self):
        src = "void main() { if (a) { if (b) { c = 1; } } }"
        result = str(ASTGenerator(src).generate())
        assert result.count("IfStmt(") == 2

    def test_if_comparison(self):
        src = "void main() { if (x > 0) { y = 1; } }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(Identifier(x), >, IntLiteral(0))" in result


# ============================================================
# WHILE STATEMENT (3 tests)
# ============================================================

class TestWhileStmt:

    def test_simple_while(self):
        src = "void main() { while (x) { x = x - 1; } }"
        result = str(ASTGenerator(src).generate())
        assert "WhileStmt(while Identifier(x) do BlockStmt(" in result

    def test_while_with_break(self):
        src = "void main() { while (1) { break; } }"
        result = str(ASTGenerator(src).generate())
        assert "WhileStmt(" in result
        assert "BreakStmt()" in result

    def test_while_with_continue(self):
        src = "void main() { while (1) { continue; } }"
        result = str(ASTGenerator(src).generate())
        assert "ContinueStmt()" in result


# ============================================================
# FOR STATEMENT (7 tests)
# ============================================================

class TestForStmt:

    def test_full_for_auto(self):
        src = "void main() { for (auto i = 0; i < 10; i++) {} }"
        result = str(ASTGenerator(src).generate())
        assert "ForStmt(for VarDecl(auto, i = IntLiteral(0))" in result

    def test_full_for_explicit(self):
        src = "void main() { for (int i = 0; i < 10; ++i) {} }"
        result = str(ASTGenerator(src).generate())
        assert "VarDecl(IntType(), i = IntLiteral(0))" in result

    def test_for_empty(self):
        src = "void main() { for (;;) { break; } }"
        result = str(ASTGenerator(src).generate())
        assert "ForStmt(for None; None; None do" in result

    def test_for_no_init(self):
        src = "void main() { for (; i < 10; i++) {} }"
        result = str(ASTGenerator(src).generate())
        assert "ForStmt(for None;" in result

    def test_for_no_update(self):
        src = "void main() { for (auto i = 0; i < 10;) {} }"
        result = str(ASTGenerator(src).generate())
        assert "None do" in result

    def test_for_assign_init(self):
        src = "void main() { for (i = 0; i < 10; i++) {} }"
        result = str(ASTGenerator(src).generate())
        assert "AssignStmt(AssignExpr(Identifier(i) = IntLiteral(0)))" in result

    def test_for_assign_update(self):
        src = "void main() { for (auto i = 0; i < 10; i = i + 1) {} }"
        result = str(ASTGenerator(src).generate())
        assert "AssignExpr(Identifier(i) = BinaryOp(Identifier(i), +, IntLiteral(1)))" in result


# ============================================================
# SWITCH STATEMENT (5 tests)
# ============================================================

class TestSwitchStmt:

    def test_simple_switch(self):
        src = """void main() { switch (x) { case 1: y = 1; break; } }"""
        result = str(ASTGenerator(src).generate())
        assert "SwitchStmt(switch Identifier(x)" in result
        assert "CaseStmt(case IntLiteral(1):" in result

    def test_switch_with_default(self):
        src = """void main() { switch (x) { case 1: break; default: y = 0; } }"""
        result = str(ASTGenerator(src).generate())
        assert "DefaultStmt(default:" in result

    def test_switch_multiple_cases(self):
        src = """void main() { switch (x) { case 1: break; case 2: break; } }"""
        result = str(ASTGenerator(src).generate())
        assert result.count("CaseStmt(") == 2

    def test_switch_fallthrough(self):
        src = """void main() { switch (x) { case 1: case 2: y = 1; break; } }"""
        result = str(ASTGenerator(src).generate())
        assert "CaseStmt(case IntLiteral(1): [])" in result

    def test_switch_empty(self):
        src = "void main() { switch (x) {} }"
        result = str(ASTGenerator(src).generate())
        assert "SwitchStmt(switch Identifier(x) cases [])" in result


# ============================================================
# RETURN STATEMENT (3 tests)
# ============================================================

class TestReturnStmt:

    def test_return_void(self):
        src = "void main() { return; }"
        result = str(ASTGenerator(src).generate())
        assert "ReturnStmt(return)" in result

    def test_return_int(self):
        src = "int f() { return 42; }"
        result = str(ASTGenerator(src).generate())
        assert "ReturnStmt(return IntLiteral(42))" in result

    def test_return_expr(self):
        src = "int f(int a, int b) { return a + b; }"
        result = str(ASTGenerator(src).generate())
        assert "ReturnStmt(return BinaryOp(Identifier(a), +, Identifier(b)))" in result


# ============================================================
# EXPRESSION STATEMENTS (3 tests)
# ============================================================

class TestExprStmt:

    def test_func_call_stmt(self):
        src = "void main() { printInt(10); }"
        result = str(ASTGenerator(src).generate())
        assert "ExprStmt(FuncCall(printInt, [IntLiteral(10)]))" in result

    def test_postfix_stmt(self):
        src = "void main() { x++; }"
        result = str(ASTGenerator(src).generate())
        assert "ExprStmt(PostfixOp(Identifier(x)++))" in result

    def test_prefix_stmt(self):
        src = "void main() { ++x; }"
        result = str(ASTGenerator(src).generate())
        assert "ExprStmt(PrefixOp(++Identifier(x)))" in result


# ============================================================
# BLOCK STATEMENTS (2 tests)
# ============================================================

class TestBlockStmt:

    def test_empty_block(self):
        src = "void main() { {} }"
        result = str(ASTGenerator(src).generate())
        assert "BlockStmt([])" in result

    def test_nested_block(self):
        src = "void main() { { int x = 1; } }"
        result = str(ASTGenerator(src).generate())
        assert "BlockStmt([VarDecl(IntType(), x = IntLiteral(1))])" in result


# ============================================================
# COMPLEX / INTEGRATION TESTS (7 tests)
# ============================================================

class TestComplex:

    def test_factorial(self):
        src = """
        int factorial(int n) {
            if (n <= 1) { return 1; }
            else { return n * factorial(n - 1); }
        }
        """
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(IntType(), factorial" in result
        assert "IfStmt(" in result
        assert "FuncCall(factorial" in result

    def test_calculator(self):
        src = """
        int add(int x, int y) { return x + y; }
        void main() {
            auto a = 5;
            auto b = 3;
            auto sum = add(a, b);
            printInt(sum);
        }
        """
        result = str(ASTGenerator(src).generate())
        assert "FuncDecl(IntType(), add" in result
        assert "FuncCall(add, [Identifier(a), Identifier(b)])" in result
        assert "FuncCall(printInt, [Identifier(sum)])" in result

    def test_struct_usage(self):
        src = """
        struct Point { int x; int y; };
        void main() {
            Point p = {10, 20};
            p.x = 30;
            printInt(p.x);
        }
        """
        result = str(ASTGenerator(src).generate())
        assert "StructDecl(Point" in result
        assert "StructLiteral({IntLiteral(10), IntLiteral(20)})" in result
        assert "AssignExpr(MemberAccess(Identifier(p).x) = IntLiteral(30))" in result

    def test_for_loop_with_body(self):
        src = """
        void main() {
            for (auto i = 0; i < 10; ++i) {
                if (i % 2 == 0) {
                    printInt(i);
                }
            }
        }
        """
        result = str(ASTGenerator(src).generate())
        assert "ForStmt(" in result
        assert "IfStmt(" in result
        assert "BinaryOp(BinaryOp(Identifier(i), %, IntLiteral(2)), ==, IntLiteral(0))" in result

    def test_complex_expression(self):
        src = "void main() { auto x = a + b * c - d / e; }"
        result = str(ASTGenerator(src).generate())
        # a + (b * c) - (d / e) → left-assoc: (a + (b*c)) - (d/e)
        assert "BinaryOp(" in result
        assert "BinaryOp(Identifier(b), *, Identifier(c))" in result
        assert "BinaryOp(Identifier(d), /, Identifier(e))" in result

    def test_while_loop_complete(self):
        src = """
        void main() {
            auto i = 0;
            while (i < 10) {
                if (i == 5) { continue; }
                printInt(i);
                i = i + 1;
            }
        }
        """
        result = str(ASTGenerator(src).generate())
        assert "WhileStmt(" in result
        assert "ContinueStmt()" in result
        assert "FuncCall(printInt" in result

    def test_mixed_operations(self):
        src = "void main() { auto x = (a > b) && (c <= d) || !e; }"
        result = str(ASTGenerator(src).generate())
        assert "BinaryOp(" in result
        assert "PrefixOp(!Identifier(e))" in result
