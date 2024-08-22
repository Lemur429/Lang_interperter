import Lexer
import Parser
import Interperter as Inter
###NODES
   

global_symbol_table = Inter.SymbolTable()
global_symbol_table.set("NULL", Inter.Number(0))
global_symbol_table.set("FALSE", Inter.Number(0))
global_symbol_table.set("TRUE", Inter.Number(1))
def run(text,fn=None):
    lex=Lexer.Lexer(fn,text)
    tokens,error=lex.make_tokens()
    if error: return None,error
    parser=Parser.Parser(tokens)
    ast=parser.parse()
    if ast.error: return None,ast.error
    #return ast.node,ast.error
    context=Inter.Context('<program>')
    context.symbol_table=global_symbol_table
    inter=Inter.Interpreter()
    result=inter.visit(ast.node,context)
    return result.value,result.error