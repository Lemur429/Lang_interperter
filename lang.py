import Error
T_CLOSE = 'CLOSE'

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
       

    def advance(self, current_char):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col,self.fn,self.ftxt)


class Token:
    def __init__(self,typ, value=None):
        self.type=typ
        self.value=value

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
        while self.current!=None and self.current in DIGITS :
            str+=self.current
            self.advance()
        return Token(T_INTEGER,int(str))
        
    def make_tokens(self):
        tokens=[]
        self.advance()
        while self.current!=None:
            
            if self.current == '\n' or self.current=='\t' or self.current==' ': 
                self.advance()
                continue
            elif self.current in DIGITS: tokens.append(self.make_num())
            elif self.current=='+': tokens.append(Token(T_PLUS)); self.advance()
            elif self.current=='-': tokens.append(Token(T_MINUS)); self.advance()
            elif self.current=='(': tokens.append(Token(T_LPAREN)); self.advance()
            elif self.current==')': tokens.append(Token(T_RPAREN)); self.advance()
            else: 
                char=self.current
                pos_start=self.pos.copy()
                self.advance()
                return [],Error.IllegalChracterError(pos_start,self.pos,f'Token Unknown \'{char}\'')
        return tokens,None


        

def run(text,fn=None):
    lex=Lexer(fn,text)
    tokens,error=lex.make_tokens()

    return tokens,error