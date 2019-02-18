# -----------------------------------------------------------------------------
# expr.py
#
# Proof-of-concept encoding of functions/expressions into Wasm.
#
# This file implements a mini-language for writing Wasm functions as expressions.
# It only supports integers.
#
# Here's a few examples:
#
# # Some basic function definitions
# add(x, y) = x + y;
# mul(x, y) = x * y;
# dsquare(x, y) = mul(x, x) + mul(y, y);
#
# # A recursive function
# fact(n) = if n < 1 then 1 else n*fact(n-1);
#
# The full grammar:
#
#     functions : functions function
#               | function
#
#     function : NAME ( parms ) = expr ;
#     
#     expr : expr + expr
#          | expr - expr
#          | expr * expr
#          | expr / expr
#          | expr < expr
#          | expr <= expr
#          | expr > expr
#          | expr >= expr
#          | expr == expr
#          | expr != expr
#          | ( expr )
#          | NAME (exprs)
#          | if expr then expr else expr
#          | NUMBER
#
# Note: This is implemented as one-pass compiler with no intermediate AST.
# Some of the grammar rules have to be written in a funny way to make this 
# work.  If doing this for real, I'd probably build an AST and construct
# Wasm code through AST walking.  
# -----------------------------------------------------------------------------

import sys
sys.path.append('../..')

from sly import Lexer, Parser
import wasm

class ExprLexer(Lexer):
    tokens = { NAME, NUMBER, PLUS, TIMES, MINUS, DIVIDE, LPAREN, RPAREN, COMMA,
               LT, LE, GT, GE, EQ, NE, IF, THEN, ELSE, ASSIGN, SEMI }
    ignore = ' \t'

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    NAME['if'] = IF
    NAME['then'] = THEN
    NAME['else'] = ELSE

    NUMBER = r'\d+'

    # Special symbols
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    COMMA = r','
    LE = r'<='
    LT = r'<'
    GE = r'>='
    GT = r'>'
    EQ = r'=='
    NE = r'!='
    ASSIGN = r'='
    SEMI = ';'

    # Ignored pattern
    ignore_newline = r'\n+'
    ignore_comment = r'#.*\n'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class ExprParser(Parser):
    tokens = ExprLexer.tokens

    precedence = (
        ('left', IF, ELSE),
        ('left', EQ, NE, LT, LE, GT, GE),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS)
        )

    def __init__(self):
        self.functions = { }
        self.module = wasm.Module()

    @_('functions function')
    def functions(self, p):
        pass

    @_('function')
    def functions(self, p):
        pass

    @_('function_decl ASSIGN expr SEMI')
    def function(self, p):
        self.function.block_end()
        self.function = None

    @_('NAME LPAREN parms RPAREN')
    def function_decl(self, p):
        self.locals = { name:n for n, name in enumerate(p.parms) }
        self.function = self.module.add_function(p.NAME, [wasm.i32]*len(p.parms), [wasm.i32])
        self.functions[p.NAME] = self.function

    @_('NAME LPAREN RPAREN')
    def function_decl(self, p):
        self.locals = { }
        self.function = self.module.add_function(p.NAME, [], [wasm.i32])
        self.functions[p.NAME] = self.function

    @_('parms COMMA parm')
    def parms(self, p):
        return p.parms + [p.parm]

    @_('parm')
    def parms(self, p):
        return [ p.parm ]

    @_('NAME')
    def parm(self, p):
        return p.NAME

    @_('expr PLUS expr')
    def expr(self, p):
        self.function.i32.add()

    @_('expr MINUS expr')
    def expr(self, p):
        self.function.i32.sub()

    @_('expr TIMES expr')
    def expr(self, p):
        self.function.i32.mul()

    @_('expr DIVIDE expr')
    def expr(self, p):
        self.function.i32.div_s()

    @_('expr LT expr')
    def expr(self, p):
        self.function.i32.lt_s()

    @_('expr LE expr')
    def expr(self, p):
        self.function.i32.le_s()

    @_('expr GT expr')
    def expr(self, p):
        self.function.i32.gt_s()

    @_('expr GE expr')
    def expr(self, p):
        self.function.i32.ge_s()

    @_('expr EQ expr')
    def expr(self, p):
        self.function.i32.eq()

    @_('expr NE expr')
    def expr(self, p):
        self.function.i32.ne()

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        pass

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        pass

    @_('NUMBER')
    def expr(self, p):
        self.function.i32.const(int(p.NUMBER))

    @_('NAME')
    def expr(self, p):
        self.function.local.get(self.locals[p.NAME])

    @_('NAME LPAREN exprlist RPAREN')
    def expr(self, p):
        self.function.call(self.functions[p.NAME])

    @_('NAME LPAREN RPAREN')
    def expr(self, p):
        self.function.call(self.functions[p.NAME])

    @_('IF expr thenexpr ELSE expr')
    def expr(self, p):
        self.function.block_end()

    @_('exprlist COMMA expr')
    def exprlist(self, p):
        pass

    @_('expr')
    def exprlist(self, p):
        pass

    @_('startthen expr')
    def thenexpr(self, p):
        self.function.else_start()
    
    @_('THEN')
    def startthen(self, p):
        self.function.if_start(wasm.i32)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        raise SystemExit(f'Usage: {sys.argv[0]} module')
    
    lexer = ExprLexer()
    parser = ExprParser()
    parser.parse(lexer.tokenize(open(sys.argv[1]).read()))

    name = sys.argv[1].split('.')[0]
    parser.module.write_wasm(name)
    parser.module.write_html(name)
    print(f'Wrote: {name}.wasm')
    print(f'Wrote: {name}.html')
    print('Use python3 -m http.server to test')
