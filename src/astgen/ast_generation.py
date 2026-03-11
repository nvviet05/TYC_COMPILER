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

    # ---- helper: lay token operator tu children cua context ----
    def _get_token_type(self, node):
        if hasattr(node, 'symbol'):
            return node.symbol.type
        return None

    # ---- helper: xay dung kieu du lieu tu explicit_type ----
    def _build_type(self, ctx):
        if ctx.INT():
            return IntType()
        if ctx.FLOAT():
            return FloatType()
        if ctx.STRING():
            return StringType()
        return StructType(ctx.ID().getText())

    # ---- helper: gom cac phan tu tu list_expression (de quy) ----
    def _collect_exprs(self, ctx):
        elems = [self.visit(ctx.expression())]
        if ctx.list_expression():
            elems += self._collect_exprs(ctx.list_expression())
        return elems

    # ---- helper: gom cac statement tu list_statement (de quy) ----
    def _collect_stmts(self, ctx):
        stmts = [self.visit(ctx.statement())]
        tail = ctx.list_statement()
        if tail:
            stmts += self._collect_stmts(tail)
        return stmts

    # ---- helper: xu ly binary expression chung ----
    def _handle_binop(self, ctx, op_check, left_visit, right_visit, fallback_visit):
        tok = op_check()
        if tok:
            l = self.visit(left_visit())
            r = self.visit(right_visit())
            op_str = tok.getText() if hasattr(tok, 'getText') else tok
            return BinaryOp(l, op_str, r)
        return self.visit(fallback_visit())

    # ========================
    #  PROGRAM
    # ========================
    def visitProgram(self, ctx):
        declarations = []
        if not ctx.children:
            return Program(declarations)
        for node in ctx.children:
            if isinstance(node, TyCParser.StructsContext) or isinstance(node, TyCParser.FunctionsContext):
                declarations.append(self.visit(node))
        return Program(declarations)

    # ========================
    #  KHAI BAO STRUCT
    # ========================
    def visitStructs(self, ctx):
        struct_name = ctx.ID().getText()
        member_list = []
        for mem in ctx.struct_member():
            member_list.append(self.visit(mem))
        return StructDecl(struct_name, member_list)

    def visitStruct_member(self, ctx):
        typ = self._build_type(ctx.explicit_type())
        field_name = ctx.ID().getText()
        return MemberDecl(typ, field_name)

    # ========================
    #  KHAI BAO HAM
    # ========================
    def visitFunctions(self, ctx):
        ret = None
        if ctx.return_type():
            ret = self.visit(ctx.return_type())
        func_name = ctx.ID().getText()
        param_ctx = ctx.parameter_list()
        params = self.visit(param_ctx) if param_ctx else []
        func_body = self.visit(ctx.block_statement())
        return FuncDecl(ret, func_name, params, func_body)

    def visitReturn_type(self, ctx):
        if ctx.VOID():
            return VoidType()
        return self._build_type(ctx.explicit_type())

    def visitParameter_list(self, ctx):
        param_nodes = ctx.parameter_decl()
        return [self.visit(p) for p in param_nodes]

    def visitParameter_decl(self, ctx):
        t = self._build_type(ctx.explicit_type())
        n = ctx.ID().getText()
        return Param(t, n)

    def visitExplicit_type(self, ctx):
        return self._build_type(ctx)

    # ========================
    #  KIEU DU LIEU
    # ========================
    def visitLiteral(self, ctx):
        if ctx.INT_LIT():
            val = int(ctx.INT_LIT().getText())
            return IntLiteral(val)
        if ctx.FLOAT_LIT():
            val = float(ctx.FLOAT_LIT().getText())
            return FloatLiteral(val)
        if ctx.STRING_LIT():
            raw = ctx.STRING_LIT().getText()
            return StringLiteral(raw)
        # struct initializer
        return self.visit(ctx.struct_initializer())

    def visitStruct_initializer(self, ctx):
        if ctx.list_expression():
            vals = self._collect_exprs(ctx.list_expression())
        else:
            vals = []
        return StructLiteral(vals)

    # ========================
    #  STATEMENTS
    # ========================
    def visitBlock_statement(self, ctx):
        if ctx.list_statement():
            body = self._collect_stmts(ctx.list_statement())
        else:
            body = []
        return BlockStmt(body)

    def visitList_statement(self, ctx):
        return self._collect_stmts(ctx)

    def visitStatement(self, ctx):
        # kiem tra tung loai statement theo thu tu
        checks = [
            ctx.var_statement, ctx.if_statement, ctx.while_statement,
            ctx.for_statement, ctx.switch_statement, ctx.break_statement,
            ctx.continue_statement, ctx.return_statement, ctx.block_statement
        ]
        for check_fn in checks:
            sub = check_fn()
            if sub:
                return self.visit(sub)

        # truong hop con lai: expression statement
        expr_result = self.visit(ctx.expression())
        if isinstance(expr_result, AssignExpr):
            return AssignStmt(expr_result)
        return ExprStmt(expr_result)

    def visitVar_statement(self, ctx):
        # xac dinh kieu: auto thi None, nguoc lai lay explicit_type
        if ctx.AUTO():
            vtype = None
        else:
            vtype = self._build_type(ctx.explicit_type())
        vname = ctx.ID().getText()
        # kiem tra co gia tri khoi tao khong
        init_ctx = ctx.var_initializer()
        vinit = self.visit(init_ctx) if init_ctx else None
        return VarDecl(vtype, vname, vinit)

    def visitVar_initializer(self, ctx):
        if ctx.struct_initializer():
            return self.visit(ctx.struct_initializer())
        return self.visit(ctx.expression())

    # ---- if / while / for ----
    def visitIf_statement(self, ctx):
        cond = self.visit(ctx.expression())
        then_branch = self.visit(ctx.statement(0))
        else_branch = None
        if ctx.ELSE():
            else_branch = self.visit(ctx.statement(1))
        return IfStmt(cond, then_branch, else_branch)

    def visitWhile_statement(self, ctx):
        cond = self.visit(ctx.expression())
        loop_body = self.visit(ctx.statement())
        return WhileStmt(cond, loop_body)

    def visitFor_statement(self, ctx):
        # moi thanh phan cua for co the vang mat
        init_part = self.visit(ctx.for_init()) if ctx.for_init() else None
        cond_part = self.visit(ctx.expression()) if ctx.expression() else None
        upd_part = self.visit(ctx.for_update()) if ctx.for_update() else None
        loop_body = self.visit(ctx.statement())
        return ForStmt(init_part, cond_part, upd_part, loop_body)

    def visitFor_init(self, ctx):
        if ctx.var_statement():
            return self.visit(ctx.var_statement())
        # truong hop assignment: lvalue = expression
        left = self.visit(ctx.lvalue())
        right = self.visit(ctx.expression())
        return AssignStmt(AssignExpr(left, right))

    def visitFor_update(self, ctx):
        # truong hop assignment
        if ctx.lvalue():
            left = self.visit(ctx.lvalue())
            right = self.visit(ctx.expression())
            return AssignExpr(left, right)

        # truong hop inc/dec voi for_operand
        operand_node = self.visit(ctx.for_operand())

        # tim vi tri cua for_operand trong danh sach children
        pos = -1
        for idx, ch in enumerate(ctx.children):
            if isinstance(ch, TyCParser.For_operandContext):
                pos = idx
                break

        cur = operand_node

        # cac toan tu prefix (truoc operand): ap dung tu trong ra ngoai
        pre_ops = []
        for j in range(pos):
            tt = self._get_token_type(ctx.children[j])
            if tt == TyCParser.INC:
                pre_ops.append("++")
            elif tt == TyCParser.DEC:
                pre_ops.append("--")
        # dao nguoc de toan tu sat operand nhat duoc ap dung truoc
        for op in reversed(pre_ops):
            cur = PrefixOp(op, cur)

        # cac toan tu postfix (sau operand): ap dung trai sang phai
        for j in range(pos + 1, len(ctx.children)):
            tt = self._get_token_type(ctx.children[j])
            if tt == TyCParser.INC:
                cur = PostfixOp("++", cur)
            elif tt == TyCParser.DEC:
                cur = PostfixOp("--", cur)

        return cur

    def visitFor_operand(self, ctx):
        if ctx.call_expr():
            node = self.visit(ctx.call_expr())
        else:
            node = self.visit(ctx.expression_primary())
        # chuoi member access (neu co)
        for tok in ctx.ID():
            node = MemberAccess(node, tok.getText())
        return node

    # ---- switch ----
    def visitSwitch_statement(self, ctx):
        switch_expr = self.visit(ctx.expression())
        all_cases = []
        for sc in ctx.switch_case():
            all_cases.extend(self.visit(sc))
        dflt = None
        if ctx.switch_default():
            dflt = self.visit(ctx.switch_default())
        return SwitchStmt(switch_expr, all_cases, dflt)

    def visitSwitch_case(self, ctx):
        label_list = ctx.switch_label()
        body = self._collect_stmts(
            ctx.list_statement()) if ctx.list_statement() else []
        result = []
        total = len(label_list)
        for idx, lbl in enumerate(label_list):
            expr = self.visit(lbl)
            # chi label cuoi moi co body, cac label truoc la fall-through
            if idx == total - 1:
                result.append(CaseStmt(expr, body))
            else:
                result.append(CaseStmt(expr, []))
        return result

    def visitSwitch_label(self, ctx):
        return self.visit(ctx.expression())

    def visitSwitch_default(self, ctx):
        body = self._collect_stmts(
            ctx.list_statement()) if ctx.list_statement() else []
        return DefaultStmt(body)

    # ---- break / continue / return ----
    def visitBreak_statement(self, ctx):
        return BreakStmt()

    def visitContinue_statement(self, ctx):
        return ContinueStmt()

    def visitReturn_statement(self, ctx):
        val = None
        if ctx.expression():
            val = self.visit(ctx.expression())
        return ReturnStmt(val)

    # ========================
    #  EXPRESSIONS
    # ========================
    def visitExpression(self, ctx):
        # kiem tra xem co phai phep gan khong
        if ctx.lvalue():
            target = self.visit(ctx.lvalue())
            value = self.visit(ctx.expression())
            return AssignExpr(target, value)
        return self.visit(ctx.expression1())

    def visitList_expression(self, ctx):
        return self._collect_exprs(ctx)

    # ---- lvalue: xu ly ben trai phep gan ----
    def visitLvalue(self, ctx):
        # xac dinh base: call_expr, expression trong ngoac, literal, hoac khong co
        base_node = None
        if ctx.call_expr():
            base_node = self.visit(ctx.call_expr())
        elif ctx.expression():
            base_node = self.visit(ctx.expression())
        elif ctx.literal():
            base_node = self.visit(ctx.literal())

        id_tokens = ctx.ID()

        if base_node is None:
            # dang: ID (.ID)*
            # ID dau tien la Identifier, cac ID sau la MemberAccess
            node = Identifier(id_tokens[0].getText())
            i = 1
            while i < len(id_tokens):
                node = MemberAccess(node, id_tokens[i].getText())
                i += 1
            return node
        else:
            # dang: (base) (.ID)+
            node = base_node
            for t in id_tokens:
                node = MemberAccess(node, t.getText())
            return node

    # ---- cac cap do uu tien cua bieu thuc (binary) ----
    def visitExpression1(self, ctx):
        # OR: uu tien thap nhat
        if ctx.OR():
            a = self.visit(ctx.expression1())
            b = self.visit(ctx.expression2())
            return BinaryOp(a, "||", b)
        return self.visit(ctx.expression2())

    def visitExpression2(self, ctx):
        # AND
        if ctx.AND():
            a = self.visit(ctx.expression2())
            b = self.visit(ctx.expression3())
            return BinaryOp(a, "&&", b)
        return self.visit(ctx.expression3())

    def visitExpression3(self, ctx):
        # bang (==) hoac khac (!=)
        op = ctx.EQ() or ctx.NEQ()
        if op:
            a = self.visit(ctx.expression3())
            b = self.visit(ctx.expression4())
            return BinaryOp(a, op.getText(), b)
        return self.visit(ctx.expression4())

    def visitExpression4(self, ctx):
        # so sanh: < <= > >=
        op = ctx.LT() or ctx.LE() or ctx.GT() or ctx.GE()
        if op:
            a = self.visit(ctx.expression4())
            b = self.visit(ctx.expression5())
            return BinaryOp(a, op.getText(), b)
        return self.visit(ctx.expression5())

    def visitExpression5(self, ctx):
        # cong tru
        op = ctx.PLUS() or ctx.MINUS()
        if op:
            a = self.visit(ctx.expression5())
            b = self.visit(ctx.expression6())
            return BinaryOp(a, op.getText(), b)
        return self.visit(ctx.expression6())

    def visitExpression6(self, ctx):
        # nhan chia lay du
        op = ctx.MUL() or ctx.DIV() or ctx.MOD()
        if op:
            a = self.visit(ctx.expression6())
            b = self.visit(ctx.expression7())
            return BinaryOp(a, op.getText(), b)
        return self.visit(ctx.expression7())

    # ---- unary prefix ----
    def visitExpression7(self, ctx):
        if ctx.NOT():
            return PrefixOp("!", self.visit(ctx.expression7()))
        if ctx.PLUS():
            return PrefixOp("+", self.visit(ctx.expression7()))
        if ctx.MINUS():
            return PrefixOp("-", self.visit(ctx.expression7()))
        return self.visit(ctx.prefix_incdec())

    def visitPrefix_incdec(self, ctx):
        if ctx.INC():
            return PrefixOp("++", self.visit(ctx.prefix_incdec()))
        if ctx.DEC():
            return PrefixOp("--", self.visit(ctx.prefix_incdec()))
        return self.visit(ctx.expression9())

    # ---- postfix va member access ----
    def visitExpression9(self, ctx):
        # base la call_expr hoac expression_primary
        if ctx.call_expr():
            node = self.visit(ctx.call_expr())
        else:
            node = self.visit(ctx.expression_primary())

        # noi chuoi member access .field
        for id_t in ctx.ID():
            node = MemberAccess(node, id_t.getText())

        # ap dung cac toan tu postfix ++ --
        for ch in ctx.children:
            tt = self._get_token_type(ch)
            if tt == TyCParser.INC:
                node = PostfixOp("++", node)
            elif tt == TyCParser.DEC:
                node = PostfixOp("--", node)

        return node

    # ---- ham va primary ----
    def visitCall_expr(self, ctx):
        fn_name = ctx.ID().getText()
        if ctx.list_expression():
            arg_list = self._collect_exprs(ctx.list_expression())
        else:
            arg_list = []
        return FuncCall(fn_name, arg_list)

    def visitExpression_primary(self, ctx):
        if ctx.ID():
            return Identifier(ctx.ID().getText())
        if ctx.literal():
            return self.visit(ctx.literal())
        # truong hop trong ngoac don
        return self.visit(ctx.expression())
