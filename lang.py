import Lexer
import Parser
import Interperter as Inter
###NODES
   
## CREATING GLOBAL "VARIABLES", 
global_symbol_table = Inter.SymbolTable()
global_symbol_table.set("NULL", Inter.Number.NULL)
 # IN THE END TRUE AND FALSE ARE JUST NUMBER 0 AND 1 LIKE MOST LOW-LEVEL LANGUAGES
global_symbol_table.set("FALSE", Inter.Number.FALSE)
global_symbol_table.set("TRUE", Inter.Number.TRUE)

def run(text,fn=None):
    ## MAKE TOKENS FROM LEXER
    lex=Lexer.Lexer(fn,text)
    tokens,error=lex.make_tokens()
    if error: return None,error
    print(tokens)
    ## PARSER CALL
    parser=Parser.Parser(tokens)
    ast=parser.parse()
    if ast.error: 
        print(ast.error)
    else:
    ## EACH ITEM IS A LINE 
        list_node=ast.node  

        context=Inter.Context('<program>')
        context.symbol_table=global_symbol_table
        inter=Inter.Interpreter()
    ## EXECUTING EACH LINE ONE BY ONE INDEPENDENT OF EACH OTHER SO WE GET IMEEDIATE RESPONSE FOR EACH LINE
        for item in list_node.element_nodes:
            result=inter.visit(item,context)
            if result.error: print(result.error)
            else: print(result.value)
 