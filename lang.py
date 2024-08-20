import Lexer
import Parser
import Interperter as Inter
###NODES
   


def run(text,fn=None):
    lex=Lexer.Lexer(fn,text)
    tokens,error=lex.make_tokens()
    if error: return None,error

    #print(tokens)
    parser=Parser.Parser(tokens)
    ast=parser.parse()
    if ast.error: return None,ast.error
    print(f'COOL: {ast.node}')
    #return ast.node,ast.error
    inter=Inter.Interpreter()
    result=inter.visit(ast.node)
    return result.value,result.error