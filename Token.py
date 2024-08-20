T_EOF= 'EOF'
DIGITS='0123456789'
T_INTEGER='INT'
T_BOOLEAN='BOOL'

T_PLUS='PLUS'
T_MINUS='MINUS'
T_MULTIPLY='MUL'
T_DIVIDE='DIV'
T_MODULO='MODULE'

T_NE='NE'
T_EE='Equal'
T_G='Greater'
T_GE='GreaterEq'
T_L='Less'
T_LE='LessEq'

T_AND='AND'
T_OR='OR'
T_NOT='NOT'

T_LPAREN='LPAREN'
T_RPAREN='RPAREN'

KEYWORDS=['FALSE','TRUE']

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
