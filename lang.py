import Lexer
import Parser
import Interperter as Inter
###NODES
   

global_symbol_table = Inter.SymbolTable()
global_symbol_table.set("NULL", Inter.Number.NULL)
global_symbol_table.set("FALSE", Inter.Number.FALSE)
global_symbol_table.set("TRUE", Inter.Number.TRUE)
def run(text,fn=None):
    lex=Lexer.Lexer(fn,text)
    tokens,error=lex.make_tokens()
    if error: return None,error

    parser=Parser.Parser(tokens)
    ast=parser.parse()
    if ast.error: return None,ast.error
    list_node=ast.node
    context=Inter.Context('<program>')
    context.symbol_table=global_symbol_table
    inter=Inter.Interpreter()
    for item in list_node.element_nodes:
        result=inter.visit(item,context)
        if result.error: print(result.error)
        else: print(result.value)
 