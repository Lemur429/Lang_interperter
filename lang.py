import Error
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

class Token:
    def __init__(self,typ, value=None):
        self.type=typ
        self.value=value

    def __repr__(self) -> str:
        if self.value: return f'{self.type}:{self.value}'
        else: return f'{self.type}'

class Command:
    def __init__(self,text):
        self.text=text
        self.pos=-1
        self.current=None

    def advance(self):
        self.pos+=1
        if self.pos<len(self.text): self.current=self.text[self.pos]
        else: self.current=None
    def makeNumber(self):
        str=''
        while(self.current!=None and self.current in DIGITS):
            str+=self.current
            self.advance()
        return Token(T_INTEGER,int(str))
        
    def ToToken(self):
        tokens=[]
        self.advance()
        while self.current!=None:
           
            if(self.current == '\n' or self.current=='\t' or self.current==' '): 
                self.advance()
                continue
            elif(self.current in DIGITS): tokens.append(self.makeNumber())
            elif(self.current=='+'): tokens.append(Token(T_PLUS)); self.advance()
            elif(self.current=='-'): tokens.append(Token(T_MINUS)); self.advance()
            else: print(str(Error.IllegalChracterError(f'Token Unknown {self.current}'))); return []
        print('neiw')
        return tokens


        

        