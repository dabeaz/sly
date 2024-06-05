# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, '../..')

from sly import Lexer, Parser

class IfElseLexer(Lexer):
    tokens = { IDENTIFIER, IF, ELSE, SEMI, LPAREN, RPAREN }
    ignore = ' \t'

    # Tokens
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE

    # Special symbols
    SEMI = r'\;'
    LPAREN = r'\('
    RPAREN = r'\)'

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class IfElseParser(Parser):
    tokens = IfElseLexer.tokens
    debugfile = 'ifelse.out'
    dotfile = 'ifelse.dot'

    #precedence = (
    #    ('left', ELSE),
    #    )

    def __init__(self):
        pass

    @_('statement')
    def prog(self, p):
        pass

    @_('if_statement')
    def statement(self, p):
        pass

    @_('IF LPAREN expr RPAREN statement')
    def if_statement(self, p):
        pass

    @_('IF LPAREN expr RPAREN statement ELSE statement')
    def if_statement(self, p):
        pass

    @_('expr SEMI')
    def statement(self, p):
        pass

    @_('IDENTIFIER')
    def expr(self, p):
        pass

if __name__ == '__main__':
    lexer = IfElseLexer()
    parser = IfElseParser()
    parser.parse(lexer.tokenize("if (x) if (y) z; else w;"))
