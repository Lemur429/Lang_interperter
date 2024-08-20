
import Error
from Token import *

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()
        
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    def set_context(self, context=None):
        self.context = context
        return self
    def added_to(self, other):
        if isinstance(other, Number):
             return Number(self.value + other.value).set_context(self.context), None
    def subbed_by(self, other):
        if isinstance(other, Number):
             return Number(self.value - other.value).set_context(self.context), None
    def multed_by(self, other):
        if isinstance(other, Number):
             return Number(self.value * other.value).set_context(self.context), None
    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Error.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
    def modul_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, Error.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Number(self.value % other.value).set_context(self.context), None
    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def get_comparison_l(self, other):
        if isinstance(other, Number):
            return Number(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_g(self, other):
        if isinstance(other, Number):
            return Number(int(self.value > other.value)).set_context(self.context), None

    def get_comparison_le(self, other):
        if isinstance(other, Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def get_comparison_ge(self, other):
        if isinstance(other, Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None

    def __repr__(self):
        return str(self.value)

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

class Interpreter:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        print(method_name)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        return RTResult().success(
            Number(node.token.value).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node):
        res = RTResult()
        left = res.register(self.visit(node.left_node))
        if res.error: return res
        right = res.register(self.visit(node.right_node))
        if res.error: return res

        if node.token.type == T_PLUS:
            result, error = left.added_to(right)
        elif node.token.type == T_MINUS:
            result, error = left.subbed_by(right)
        elif node.token.type == T_MULTIPLY:
            result, error = left.multed_by(right)
        elif node.token.type == T_DIVIDE:
            result, error = left.dived_by(right)
        elif node.token.type == T_MODULO:
            result,error=left.modul_by(right)
        elif node.token.type == T_EE:
            result,error=left.get_comparison_eq(right)
        elif node.token.type == T_G:
            result,error=left.get_comparison_g(right)
        elif node.token.type == T_GE:
            result,error=left.get_comparison_ge(right)
        elif node.token.type == T_L:
            result,error=left.get_comparison_l(right)
        elif node.token.type == T_LE:
            result,error=left.get_comparison_le(right)
        elif node.token.type == T_NE:
            result,error=left.get_comparison_ne(right)
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node):
        res = RTResult()
        number = res.register(self.visit(node.node))
        if res.error: return res

        error = None

        if node.operation.type == T_MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))
