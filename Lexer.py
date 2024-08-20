from Token import *
import Error
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
  
    def make_greater(self):
        pos_start=self.pos.copy()
        self.advance()
        if self.current =='=':
            token=Token(T_GE,pos_start=pos_start,pos_end=self.pos)
            self.advance()
        else:
            token=Token(T_G,pos_start=pos_start)
        return token
    def make_less(self):
        pos_start=self.pos.copy()
        self.advance()
        if self.current =='=':
            token=Token(T_LE,pos_start=pos_start,pos_end=self.pos)
            self.advance()
        else:
            token=Token(T_L,pos_start=pos_start)
        return token
    def make_not(self):
        pos_start=self.pos.copy()
        self.advance()
        if self.current =='=':
            token=Token(T_NE,pos_start=pos_start,pos_end=self.pos)
            self.advance()
        else:
            token=Token(T_NOT,pos_start=pos_start)
        return token
 
    def make_char_error(self,token_type,char):
        pos_start=self.pos.copy()
        self.advance()
        if self.current == char:
            token=Token(token_type,pos_start=pos_start,pos_end=self.pos)
            self.advance()
            return token,None
        else:
            return [],Error.ExpectedChar(pos_start,self.pos,char)
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
            elif self.current=='=': 
                token,error=self.make_char_error(T_EE,'=')
                if error: return [],error 
                else: tokens.append(token)
            elif self.current=='&': 
                token,error=self.make_char_error(T_AND,'&')
                if error: return [],error 
                else: tokens.append(token)
            elif self.current== '>':tokens.append(self.make_greater())
            elif self.current== '<':tokens.append(self.make_less())
            elif self.current== '!':tokens.append(self.make_not())
            else: 
                char=self.current
                pos_start=self.pos.copy()
                self.advance()
                return [],Error.IllegalChracterError(pos_start,self.pos,f'Token Unknown \'{char}\'')
        tokens.append(Token(T_EOF,pos_start=self.pos))
        return tokens,None
