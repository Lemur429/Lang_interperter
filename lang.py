from Error import *
T_EOF= 'EOF'
DIGITS='0123456789'
T_INTEGER='INT'
T_BOOLEAN='BOOL'

T_PLUS='PLUS'
T_MINUS='MINUS'
T_MULTIPLY='MUL'
T_DIVIDE='DIV'
T_MODULO='MODULE'

T_AND='AND'
T_OR='OR'
T_NOT='NOT'

T_LPAREN='LPAREN'
T_RPAREN='RPAREN'



class Position:
    def __init__(self, idx, ln, col,fn,ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn=fn
        self.ftxt=ftxt
       

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col,self.fn,self.ftxt)
class Token:
    def __init__(self,typ, value=None,pos_start=None,pos_end=None):
        self.type=typ
        self.value=value
        if pos_start: 
            self.pos_start=pos_start
            self.pos_end=pos_start.copy()
            self.pos_end.advance()
        if pos_end: self.pos_end=pos_end
    def __repr__(self) -> str:
        if self.value: return f'{self.type}:{self.value}'
        else: return f'{self.type}'
class Lexer:
    def __init__(self,fn,text):
        self.fn=fn
        self.text=text
        self.pos=Position(-1,0,-1,fn,text)
        self.current=None

    def advance(self):
        self.pos.advance(self.current)
        if self.pos.idx<len(self.text): self.current=self.text[self.pos.idx]
        else: self.current=None
    def make_num(self):
        str=''
        pos_start=self.pos.copy()

        while self.current!=None and self.current in DIGITS :
            str+=self.current
            self.advance()
        return Token(T_INTEGER,int(str),pos_start,self.pos)
        
    def make_tokens(self):
        tokens=[]
        self.advance()
        while self.current!=None:
            
            if self.current == '\n' or self.current=='\t' or self.current==' ': 
                self.advance()
                continue
            elif self.current in DIGITS: tokens.append(self.make_num())
            elif self.current=='+': tokens.append(Token(T_PLUS, pos_start=self.pos)); self.advance()
            elif self.current=='-': tokens.append(Token(T_MINUS, pos_start=self.pos)); self.advance()
            elif self.current=='*': tokens.append(Token(T_MULTIPLY, pos_start=self.pos));self.advance()
            elif self.current=='/': tokens.append(Token(T_DIVIDE, pos_start=self.pos)); self.advance()
            elif self.current=='%': tokens.append(Token(T_MODULO, pos_start=self.pos)); self.advance()
            elif self.current=='(': tokens.append(Token(T_LPAREN, pos_start=self.pos)); self.advance()
            elif self.current==')': tokens.append(Token(T_RPAREN, pos_start=self.pos)); self.advance()
            else: 
                char=self.current
                pos_start=self.pos.copy()
                self.advance()
                return [],IllegalChracterError(pos_start,self.pos,f'Token Unknown \'{char}\'')
        tokens.append(Token(T_EOF,pos_start=self.pos))
        return tokens,None

###NODES
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
    def __repr__(self) -> str:
        return f'({self.operation}, {self.node})'
        
class ParseResult:
    def __init__(self):
        self.error=None
        self.node=None
    def register(self,res):
        if isinstance(res,ParseResult):
            if res.error: self.error=res.error
            return res.node
        return res
    
    def success(self,node):
        self.node=node
        return self
    def failure(self,error):
        self.error=error
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
            return res.failure(InvalidSyntax(self.current.pos_start, self.current.pos_end, 'Expected Binary operation'))
        return res
    def factor(self):
        res=ParseResult()
        token=self.current
        if token.type in (T_PLUS, T_MINUS): 
            res.register(self.advance())
            factor=res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token,factor))
        
        elif token.type is T_INTEGER:
            res.register(self.advance())
            return res.success(NumberNode(token))
        
        elif token.type is T_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if self.current.type is T_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntax(self.current.pos_start,self.current.pos_end,'Expected \')\' '))
        return res.failure(InvalidSyntax(token.pos_start,token.pos_end,"Expected Integer"))
    
    def term(self):
        return self.bin_op(self.factor,(T_MULTIPLY,T_DIVIDE,T_MODULO))
    def expr(self):
        return self.bin_op(self.term,(T_PLUS,T_MINUS))


    def bin_op(self,func,ops):
        res=ParseResult()
        left=res.register(func())
        if res.error: return res

        while self.current.type in ops:
            operation=self.current
            res.register(self.advance())
            right=res.register(func())
            if res.error: return res
            left=BinOpNode(left,operation,right)
        return res.success(left)
      


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
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
    def modul_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Number(self.value % other.value).set_context(self.context), None
        
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

#######################################
# CONTEXT
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

#######################################
# INTERPRETER
#######################################

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ###################################

    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
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

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None

        if node.token.type == T_MINUS:
            number, error = number.multed_by(Number(-1))

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))


def run(text,fn=None):
    lex=Lexer(fn,text)
    tokens,error=lex.make_tokens()
    if error: return None,error
    parser=Parser(tokens)
    ast=parser.parse()
    if ast.error: return None,ast.error

    inter=Interpreter()
    context=Context('<program>')
    result=inter.visit(ast.node,context)
    return result.value,result.error