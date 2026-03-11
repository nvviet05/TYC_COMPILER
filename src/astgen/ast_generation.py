"""
AST Generation module for TyC programming language.
This module contains the ASTGeneration class that converts parse trees
into Abstract Syntax Trees using the visitor pattern.
"""

from __future__ import annotations

import sys
import os

# Add project directories to Python path for import resolution
try:
    _this_dir = os.path.dirname(os.path.abspath(__file__))
    _project_root = os.path.dirname(os.path.dirname(_this_dir))
    for _p in [_project_root, os.path.join(_project_root, 'build'), _this_dir]:
        if _p and _p not in sys.path:
            sys.path.insert(0, _p)
except Exception:
    pass

# Import ANTLR-generated visitor and parser
try:
    from build.TyCVisitor import TyCVisitor
    from build.TyCParser import TyCParser
except Exception:
    try:
        from TyCVisitor import TyCVisitor
        from TyCParser import TyCParser
    except Exception:
        pass

# Import AST node classes
try:
    from src.utils.nodes import *
except Exception:
    try:
        from utils.nodes import *
    except Exception:
        try:
            from nodes import *
        except Exception:
            pass


class ASTGeneration(TyCVisitor):
    """AST Generation visitor for TyC language.
    Converts ANTLR parse trees into AST nodes defined in nodes.py.
    """

    # ================================================================
    # Program and Top-level Declarations
    # ================================================================

    def visitProgram(self, ctx: TyCParser.ProgramContext):
        decls = []
        if ctx.children:
            for child in ctx.children:
                if isinstance(child, TyCParser.StructsContext):
                    decls.append(self.visit(child))
                elif isinstance(child, TyCParser.FunctionsContext):
                    decls.append(self.visit(child))
        return Program(decls)

    def visitStructs(self, ctx: TyCParser.StructsContext):
        name = ctx.ID().getText()
        members = [self.visit(m) for m in ctx.struct_member()]
        return StructDecl(name, members)

    def visitStruct_member(self, ctx: TyCParser.Struct_memberContext):
        member_type = self.visit(ctx.explicit_type())
        name = ctx.ID().getText()
        return MemberDecl(member_type, name)

    def visitFunctions(self, ctx: TyCParser.FunctionsContext):
        return_type = None
        if ctx.return_type():
            return_type = self.visit(ctx.return_type())
        name = ctx.ID().getText()
        params = self.visit(ctx.parameter_list()
                            ) if ctx.parameter_list() else []
        body = self.visit(ctx.block_statement())
        return FuncDecl(return_type, name, params, body)

    def visitReturn_type(self, ctx: TyCParser.Return_typeContext):
        if ctx.VOID():
            return VoidType()
        return self.visit(ctx.explicit_type())

    def visitParameter_list(self, ctx: TyCParser.Parameter_listContext):
        return [self.visit(p) for p in ctx.parameter_decl()]

    def visitParameter_decl(self, ctx: TyCParser.Parameter_declContext):
        param_type = self.visit(ctx.explicit_type())
        name = ctx.ID().getText()
        return Param(param_type, name)

    # ================================================================
    # Type System
    # ================================================================

    def visitExplicit_type(self, ctx: TyCParser.Explicit_typeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:
            return StructType(ctx.ID().getText())

    # ================================================================
    # Statements
    # ================================================================

    def visitBlock_statement(self, ctx: TyCParser.Block_statementContext):
        stmts = self.visit(ctx.list_statement()
                           ) if ctx.list_statement() else []
        return BlockStmt(stmts)

    def visitList_statement(self, ctx: TyCParser.List_statementContext):
        result = [self.visit(ctx.statement())]
        if ctx.list_statement():
            result.extend(self.visit(ctx.list_statement()))
        return result

    def visitStatement(self, ctx: TyCParser.StatementContext):
        if ctx.var_statement():
            return self.visit(ctx.var_statement())
        elif ctx.if_statement():
            return self.visit(ctx.if_statement())
        elif ctx.while_statement():
            return self.visit(ctx.while_statement())
        elif ctx.for_statement():
            return self.visit(ctx.for_statement())
        elif ctx.switch_statement():
            return self.visit(ctx.switch_statement())
        elif ctx.break_statement():
            return self.visit(ctx.break_statement())
        elif ctx.continue_statement():
            return self.visit(ctx.continue_statement())
        elif ctx.return_statement():
            return self.visit(ctx.return_statement())
        elif ctx.block_statement():
            return self.visit(ctx.block_statement())
        else:
            # expression SEMI
            expr = self.visit(ctx.expression())
            if isinstance(expr, AssignExpr):
                return AssignStmt(expr)
            return ExprStmt(expr)

    def visitVar_statement(self, ctx: TyCParser.Var_statementContext):
        var_type = None if ctx.AUTO() else self.visit(ctx.explicit_type())
        name = ctx.ID().getText()
        init_value = self.visit(ctx.var_initializer()
                                ) if ctx.var_initializer() else None
        return VarDecl(var_type, name, init_value)

    def visitVar_initializer(self, ctx: TyCParser.Var_initializerContext):
        if ctx.struct_initializer():
            return self.visit(ctx.struct_initializer())
        return self.visit(ctx.expression())

    def visitStruct_initializer(self, ctx: TyCParser.Struct_initializerContext):
        values = self.visit(ctx.list_expression()
                            ) if ctx.list_expression() else []
        return StructLiteral(values)

    def visitIf_statement(self, ctx: TyCParser.If_statementContext):
        condition = self.visit(ctx.expression())
        then_stmt = self.visit(ctx.statement(0))
        else_stmt = self.visit(ctx.statement(1)) if ctx.ELSE() else None
        return IfStmt(condition, then_stmt, else_stmt)

    def visitWhile_statement(self, ctx: TyCParser.While_statementContext):
        condition = self.visit(ctx.expression())
        body = self.visit(ctx.statement())
        return WhileStmt(condition, body)

    def visitFor_statement(self, ctx: TyCParser.For_statementContext):
        init = self.visit(ctx.for_init()) if ctx.for_init() else None
        condition = self.visit(ctx.expression()) if ctx.expression() else None
        update = self.visit(ctx.for_update()) if ctx.for_update() else None
        body = self.visit(ctx.statement())
        return ForStmt(init, condition, update, body)

    def visitFor_init(self, ctx: TyCParser.For_initContext):
        if ctx.var_statement():
            return self.visit(ctx.var_statement())
        lhs = self.visit(ctx.lvalue())
        rhs = self.visit(ctx.expression())
        return AssignStmt(AssignExpr(lhs, rhs))

    def visitFor_update(self, ctx: TyCParser.For_updateContext):
        if ctx.lvalue():
            lhs = self.visit(ctx.lvalue())
            rhs = self.visit(ctx.expression())
            return AssignExpr(lhs, rhs)

        base = self.visit(ctx.for_operand())
        operand_idx = next(
            i for i, child in enumerate(ctx.children)
            if isinstance(child, TyCParser.For_operandContext)
        )
        result = base

        # Prefix ops (before operand) - innermost (rightmost) first
        prefix_ops = []
        for i in range(operand_idx):
            child = ctx.children[i]
            if hasattr(child, 'symbol'):
                if child.symbol.type == TyCParser.INC:
                    prefix_ops.append("++")
                elif child.symbol.type == TyCParser.DEC:
                    prefix_ops.append("--")
        for op in reversed(prefix_ops):
            result = PrefixOp(op, result)

        # Postfix ops (after operand) - left to right
        for i in range(operand_idx + 1, len(ctx.children)):
            child = ctx.children[i]
            if hasattr(child, 'symbol'):
                if child.symbol.type == TyCParser.INC:
                    result = PostfixOp("++", result)
                elif child.symbol.type == TyCParser.DEC:
                    result = PostfixOp("--", result)

        return result

    def visitFor_operand(self, ctx: TyCParser.For_operandContext):
        if ctx.call_expr():
            base = self.visit(ctx.call_expr())
        else:
            base = self.visit(ctx.expression_primary())
        for id_tok in ctx.ID():
            base = MemberAccess(base, id_tok.getText())
        return base

    def visitSwitch_statement(self, ctx: TyCParser.Switch_statementContext):
        expr = self.visit(ctx.expression())
        cases = []
        for case_ctx in ctx.switch_case():
            cases.extend(self.visit(case_ctx))
        default = self.visit(ctx.switch_default()
                             ) if ctx.switch_default() else None
        return SwitchStmt(expr, cases, default)

    def visitSwitch_case(self, ctx: TyCParser.Switch_caseContext):
        labels = ctx.switch_label()
        stmts = self.visit(ctx.list_statement()
                           ) if ctx.list_statement() else []
        cases = []
        for i, label_ctx in enumerate(labels):
            label_expr = self.visit(label_ctx)
            if i == len(labels) - 1:
                cases.append(CaseStmt(label_expr, stmts))
            else:
                cases.append(CaseStmt(label_expr, []))
        return cases

    def visitSwitch_label(self, ctx: TyCParser.Switch_labelContext):
        return self.visit(ctx.expression())

    def visitSwitch_default(self, ctx: TyCParser.Switch_defaultContext):
        stmts = self.visit(ctx.list_statement()
                           ) if ctx.list_statement() else []
        return DefaultStmt(stmts)

    def visitBreak_statement(self, ctx):
        return BreakStmt()

    def visitContinue_statement(self, ctx):
        return ContinueStmt()

    def visitReturn_statement(self, ctx: TyCParser.Return_statementContext):
        expr = self.visit(ctx.expression()) if ctx.expression() else None
        return ReturnStmt(expr)

    # ================================================================
    # Expressions
    # ================================================================

    def visitExpression(self, ctx: TyCParser.ExpressionContext):
        if ctx.lvalue():
            lhs = self.visit(ctx.lvalue())
            rhs = self.visit(ctx.expression())
            return AssignExpr(lhs, rhs)
        return self.visit(ctx.expression1())

    def visitLvalue(self, ctx: TyCParser.LvalueContext):
        if ctx.call_expr():
            base = self.visit(ctx.call_expr())
        elif ctx.expression():
            base = self.visit(ctx.expression())
        elif ctx.literal():
            base = self.visit(ctx.literal())
        else:
            base = None

        ids = ctx.ID()
        if base is None:
            # Alt 1: ID (DOT ID)* - first ID = identifier, rest = member access
            result = Identifier(ids[0].getText())
            for i in range(1, len(ids)):
                result = MemberAccess(result, ids[i].getText())
            return result
        else:
            # Alt 2: base (DOT ID)+ - all IDs are member names
            result = base
            for id_tok in ids:
                result = MemberAccess(result, id_tok.getText())
            return result

    def visitList_expression(self, ctx: TyCParser.List_expressionContext):
        result = [self.visit(ctx.expression())]
        if ctx.list_expression():
            result.extend(self.visit(ctx.list_expression()))
        return result

    # --- Binary expressions (left-recursive) ---

    def visitExpression1(self, ctx: TyCParser.Expression1Context):
        """Logical OR: expression1 OR expression2 | expression2"""
        if ctx.OR():
            left = self.visit(ctx.expression1())
            right = self.visit(ctx.expression2())
            return BinaryOp(left, "||", right)
        return self.visit(ctx.expression2())

    def visitExpression2(self, ctx: TyCParser.Expression2Context):
        """Logical AND: expression2 AND expression3 | expression3"""
        if ctx.AND():
            left = self.visit(ctx.expression2())
            right = self.visit(ctx.expression3())
            return BinaryOp(left, "&&", right)
        return self.visit(ctx.expression3())

    def visitExpression3(self, ctx: TyCParser.Expression3Context):
        """Equality: expression3 (EQ | NEQ) expression4 | expression4"""
        op_tok = ctx.EQ() or ctx.NEQ()
        if op_tok:
            left = self.visit(ctx.expression3())
            right = self.visit(ctx.expression4())
            return BinaryOp(left, op_tok.getText(), right)
        return self.visit(ctx.expression4())

    def visitExpression4(self, ctx: TyCParser.Expression4Context):
        """Relational: expression4 (LT|LE|GT|GE) expression5 | expression5"""
        op_tok = ctx.LT() or ctx.LE() or ctx.GT() or ctx.GE()
        if op_tok:
            left = self.visit(ctx.expression4())
            right = self.visit(ctx.expression5())
            return BinaryOp(left, op_tok.getText(), right)
        return self.visit(ctx.expression5())

    def visitExpression5(self, ctx: TyCParser.Expression5Context):
        """Additive: expression5 (PLUS | MINUS) expression6 | expression6"""
        op_tok = ctx.PLUS() or ctx.MINUS()
        if op_tok:
            left = self.visit(ctx.expression5())
            right = self.visit(ctx.expression6())
            return BinaryOp(left, op_tok.getText(), right)
        return self.visit(ctx.expression6())

    def visitExpression6(self, ctx: TyCParser.Expression6Context):
        """Multiplicative: expression6 (MUL|DIV|MOD) expression7 | expression7"""
        op_tok = ctx.MUL() or ctx.DIV() or ctx.MOD()
        if op_tok:
            left = self.visit(ctx.expression6())
            right = self.visit(ctx.expression7())
            return BinaryOp(left, op_tok.getText(), right)
        return self.visit(ctx.expression7())

    # --- Unary expressions (right-recursive) ---

    def visitExpression7(self, ctx: TyCParser.Expression7Context):
        """Unary prefix: (NOT|PLUS|MINUS) expression7 | prefix_incdec"""
        if ctx.NOT():
            return PrefixOp("!", self.visit(ctx.expression7()))
        elif ctx.PLUS():
            return PrefixOp("+", self.visit(ctx.expression7()))
        elif ctx.MINUS():
            return PrefixOp("-", self.visit(ctx.expression7()))
        return self.visit(ctx.prefix_incdec())

    def visitPrefix_incdec(self, ctx: TyCParser.Prefix_incdecContext):
        """prefix_incdec: (INC | DEC) prefix_incdec | expression9"""
        if ctx.INC():
            return PrefixOp("++", self.visit(ctx.prefix_incdec()))
        elif ctx.DEC():
            return PrefixOp("--", self.visit(ctx.prefix_incdec()))
        return self.visit(ctx.expression9())

    def visitExpression9(self, ctx: TyCParser.Expression9Context):
        """expression9: (call_expr | expression_primary) (DOT ID)* (INC | DEC)*"""
        base = self.visit(ctx.call_expr()) if ctx.call_expr(
        ) else self.visit(ctx.expression_primary())

        # Member access chain
        for id_tok in ctx.ID():
            base = MemberAccess(base, id_tok.getText())

        # Postfix operators in order
        for child in ctx.children:
            if hasattr(child, 'symbol'):
                if child.symbol.type == TyCParser.INC:
                    base = PostfixOp("++", base)
                elif child.symbol.type == TyCParser.DEC:
                    base = PostfixOp("--", base)

        return base

    # --- Primary expressions ---

    def visitCall_expr(self, ctx: TyCParser.Call_exprContext):
        name = ctx.ID().getText()
        args = self.visit(ctx.list_expression()
                          ) if ctx.list_expression() else []
        return FuncCall(name, args)

    def visitExpression_primary(self, ctx: TyCParser.Expression_primaryContext):
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        elif ctx.literal():
            return self.visit(ctx.literal())
        return self.visit(ctx.expression())

    # --- Literals ---

    def visitLiteral(self, ctx: TyCParser.LiteralContext):
        if ctx.INT_LIT():
            return IntLiteral(int(ctx.INT_LIT().getText()))
        elif ctx.FLOAT_LIT():
            return FloatLiteral(float(ctx.FLOAT_LIT().getText()))
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        return self.visit(ctx.struct_initializer())
