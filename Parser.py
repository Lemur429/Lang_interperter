from Token import *
import Error
class NumberNode:
    def __init__(self,token):
        self.token=token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end
    def __repr__(self):
        return f'{self.token}'     

class BinOpNode:
    def __init__(self,left_node,token,right_node):
        self.left_node=left_node
        self.token=token
        self.right_node=right_node
        self.pos_start=self.left_node.pos_start
        self.pos_end=self.right_node.pos_end
    def __repr__(self):
        return f'({self.left_node} , {self.token} , {self.right_node})'
class UnaryOpNode:
    def __init__(self,operation,node):
        self.operation=operation
        self.node=node

        self.pos_start=self.operation.pos_start
        self.pos_end=node.pos_end

    def __repr__(self) -> str:
        return f'({self.operation}, {self.node})'
        
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self
     

class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.idx=-1
        self.advance()
    
    def advance(self):
        self.idx+=1
        if self.idx<len(self.tokens): self.current=self.tokens[self.idx]
        return self.current
    
    def parse(self):
        res=self.expr()
        if not res.error and self.current.type !=T_EOF:
            return res.failure(Error.InvalidSyntax(self.current.pos_start, self.current.pos_end, 'Expected Binary operation'))
        return res
    
    def factor(self):
        res=ParseResult()
        token=self.current
        if token.type in (T_PLUS, T_MINUS): 
            res.register_advancement()
            self.advance()
            factor=res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token,factor))
        
        elif token.type is T_INTEGER:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))
        
        elif token.type is T_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if self.current.type is T_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(Error.InvalidSyntax(self.current.pos_start,self.current.pos_end,'Expected \')\' '))
        return res.failure(Error.InvalidSyntax(token.pos_start,token.pos_end,"Expected Integer"))
    
    def term(self):
        return self.bin_op(self.factor,(T_MULTIPLY,T_DIVIDE,T_MODULO))
    def arith_expr(self):
        return self.bin_op(self.term,(T_PLUS,T_MINUS))
    def comp_expr(self):
        res = ParseResult()
        if self.current.type is T_NOT:
            operation=self.current
            res.register_advancement()
            self.advance()
            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(operation,node))
        node = res.register(self.bin_op(self.arith_expr, (T_EE, T_NE, T_L, T_G, T_LE, T_GE)))
        if res.error:
            return res.failure(Error.InvalidSyntax(
                self.current.pos_start, self.current.pos_end,
                "Expected int, identifier, '+', '-', '(' or '!'"
            ))
        return res.success(node)

    def expr(self):
        res=ParseResult()
        node = res.register(self.bin_op(self.comp_expr, (T_AND,T_OR)))
        if res.error: return res
        else: 
            return res.success(node)
                            
    def bin_op(self,func_a,ops,func_b=None):
        if func_b==None: func_b=func_a
        res=ParseResult()
        left=res.register(func_a())
        if res.error: return res
        while self.current.type in ops:
            operation=self.current
            res.register_advancement()
            self.advance()
            right=res.register(func_b())
            if res.error: return res
            left=BinOpNode(left,operation,right)
        return res.success(left)
   