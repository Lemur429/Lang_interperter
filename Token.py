import string
T_EOF= 'EOF'
T_NEWLINE='NEWLINE'
DIGITS='0123456789'
ALPHABET=string.ascii_letters
T_INTEGER='INT'

##         ARITHMETIC OPERATIONS
T_PLUS='PLUS'
T_MINUS='MINUS'
T_MULTIPLY='MUL'
T_DIVIDE='DIV'
T_MODULO='MODULE'

##    BOOLEAN OPERATIONS
T_NE='NE'   # NOT EQUAL
T_EE='EE'  # EQUAL
T_G='GT'  ## GREATER THAN
T_GE='GE'  # GREATER OR EQUAL
T_L='LT' # LESS THAN
T_LE='LE' # LESS OR EQUAL
T_AND='AND'  # AND &&
T_OR='OR'  # OR ||
T_NOT='NOT'  # NOT !

T_LPAREN='LPAREN' #(
T_RPAREN='RPAREN'  # )
### MOSTLY USED FOR FUNCTION DEF AND CALLS
T_ARROW='ARROW'  #->
T_COMMA='COMMA'
T_KEYWORD='KEYWORD'  # ANY KNOWN WORDS SPECIFIED AT KEWORDS LIST
T_IDENTIFIER='IDENTIFIER'  # NOT LANGUAGE TOKEN
KEYWORDS =['FUNC','APPLY']

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

# USED FOR DEBUGGING PURPOSES
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        else: return f'{self.type}'
