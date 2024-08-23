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
##  NODE CONTAINING ALL THE NODES AT LIST USEFUL FOR FILES    
class ListNode:
  def __init__(self, element_nodes, pos_start, pos_end):
    self.element_nodes = element_nodes

    self.pos_start = pos_start
    self.pos_end = pos_end
## DEFINE NEW FUNCTION NODE
class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end
    def __repr__(self) -> str:
        return f'({self.var_name_tok} takes [{self.arg_name_toks} -> {self.body_node}])'
## "VARIABLE" ACCESS NODE - ONLY FUNCTIONS!
class VarAccessNode: 
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end
    def __repr__(self) -> str:
        return f'VAR:{self.var_name_tok}'
# CALL TO FUNCTION NODE
class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
## CLASS TO IDENTIFY ERRORS IN PARSING
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self

# PARSER CLASS
class Parser:
    def __init__(self,tokens):
        self.tokens=tokens
        self.idx=-1
        self.advance()
    ## MOVING TO THE NEXT TOKEN 
    def advance(self):
        self.idx+=1
        if self.idx<len(self.tokens): self.current=self.tokens[self.idx]
        return self.current
    ## REVERSE TO PAST TOKEN IF ERROR HAPPEND, NEEDED FOR FILES READ
    def reverse(self, amount=1):
        self.idx -= amount
        if self.idx>0 and self.idx<len(self.tokens): self.current=self.tokens[self.idx]
        return self.current
##  MAIN PARSE FUNCTION
    def parse(self):
        res=self.statements()
        
        return res
## FOR EACH LINE CREATING PARSING
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current.pos_start.copy()

        while self.current.type == T_NEWLINE: # skip all empty lines
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())  # recieve statement
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
          newline_count = 0
          while self.current.type == T_NEWLINE:
            res.register_advancement()
            self.advance()
            newline_count += 1
          if newline_count == 0:
            more_statements = False

          if not more_statements: break
          statement = res.try_register(self.statement())
          if not statement:
            self.reverse(res.to_reverse_count)
            more_statements = False
            continue
          statements.append(statement)

        return res.success(ListNode(
          statements,
          pos_start,
          self.current.pos_end.copy()
        ))
## CREATE PARSE FOR ONE LINE
    def statement(self):
        res = ParseResult()
        expr = res.register(self.expr())
        if res.error:
          return res
        return res.success(expr)

# EACH FUNCTION HERE IS A PART OF THE BNF GRAMMER MAKING A NODE ACCORDING TO EACH EXPRESSION GRAMMER
    def expr(self):
        res=ParseResult()
        node = res.register(self.bin_op(self.comp_expr, (T_AND,T_OR)))
        if res.error: return res
        else: 
            return res.success(node)
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
                "Expected identifier,int, '+', '-', '(' or '!'"
            ))
        return res.success(node)
    def arith_expr(self):
        return self.bin_op(self.term,(T_PLUS,T_MINUS))
    def term(self):
        return self.bin_op(self.factor,(T_MULTIPLY,T_DIVIDE,T_MODULO))
    def factor(self):
        res=ParseResult()
        token=self.current
        if token.type in (T_PLUS, T_MINUS): 
            res.register_advancement()
            self.advance()
            factor=res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token,factor))
        return self.call()
    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: 
            return res
        
        if self.current.type == T_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current.type == T_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(Error.InvalidSyntax(
                        self.current.pos_start, self.current.pos_end,
                        "Expected ')', 'FUNC', int,identifier, '+', '-', '(' or '!'"
                    ))

                while self.current.type == T_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current.type != T_RPAREN:
                    return res.failure(Error.InvalidSyntax(
                        self.current.pos_start, self.current.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)
    def atom(self):
        res =ParseResult()
        token=self.current
        if token.type is T_INTEGER:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(token))
        elif token.type is T_LPAREN:
            res.register_advancement()
            self.advance()
            expr=res.register(self.expr())
            if self.current.type ==T_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(Error.ExpectedChar(self.current.pos_start,self.current.pos_end,f'Expected \')\''))
        elif token.type is T_KEYWORD and token.value =='FUNC':
             func_def=res.register(self.func_def())
             if res.error: return res
             return res.success(func_def)
        elif token.type is T_KEYWORD and token.value =='APPLY':
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))
        elif token.type is T_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(token))
        return res.failure(Error.InvalidSyntax(token.pos_start,token.pos_end,"Expected Integer,+,-,(,! or func definition"))
    def func_def(self):
        res=ParseResult()
        # if arrived here we got FUNC keyword so we advance
        res.register_advancement()
        self.advance() 
        if self.current.type == T_IDENTIFIER:
             func_name_token = self.current
             res.register_advancement()
             self.advance()
             if self.current.type != T_LPAREN:
                  return res.failure(Error.InvalidSyntax(self.current.pos_start ,self.current.pos_end,'Expected \'(\''))
        else:
             func_name_token=None
             if self.current.type != T_LPAREN:
                  return res.failure(Error.InvalidSyntax(self.current.pos_start ,self.current.pos_end,'Expected identifier or \'(\''))
        res.register_advancement()
        self.advance()
        arg_name_tokens = []
        if self.current.type ==T_IDENTIFIER:
            arg_name_tokens.append(self.current)
            res.register_advancement()
            self.advance()
            while self.current.type==T_COMMA:
                res.register_advancement()
                self.advance()
                if self.current.type ==T_IDENTIFIER:
                    arg_name_tokens.append(self.current)
                    res.register_advancement()
                    self.advance()
                else:
                     return res.failure(Error.InvalidSyntax(self.current.pos_start,self.current.pos_end,'Expected identifier after \',\''))
            if self.current.type!=T_RPAREN:
                return res.failure(Error.InvalidSyntax(self.current.pos_start ,self.current.pos_end,'Expected \')\' or \',\''))
        else:
             if self.current.type!= T_RPAREN:
                return res.failure(Error.InvalidSyntax(self.current.pos_start ,self.current.pos_end,'Expected identifier or \')\''))
        res.register_advancement()
        self.advance()
        if self.current.type != T_ARROW:
             return res.failure(Error.InvalidSyntax(self.current.pos_start,self.current.pos_end,"Expected '->'"))
        res.register_advancement()
        self.advance()
        node=res.register(self.expr())
        if res.error: return res
        return res.success(FuncDefNode(func_name_token,arg_name_tokens,node))

    
    
    
## GENERAL FUNCTION USED FOR BINARY OPERATIONS , ARITHMETIC AND BOOLEAN
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
   