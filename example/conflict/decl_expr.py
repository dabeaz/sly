# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, '../..')

from sly import Lexer, Parser

class DeclExprLexer(Lexer):
    tokens = { IDENTIFIER, TYPENAME }
    ignore = ' \t'
    literals = {'=','+',';', '(', ')'}

    # Tokens
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENTIFIER['typename'] = TYPENAME

    # Ignored pattern
    ignore_newline = r'\n+'

    # Extra action for newlines
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class DeclExprParser(Parser):
    tokens = DeclExprLexer.tokens
    debugfile = 'decl_expr.out'

    def __init__(self):
        pass

    @_('prog stmt')
    @_('')
    def prog(self, p):
        pass

    @_('expr ";"')
    @_('decl')
    def stmt(self, p):
        pass

    @_('IDENTIFIER')
    @_('TYPENAME "(" expr ")"')
    @_('expr "+" expr')
    @_('expr "=" expr')
    def expr(self, p):
        pass

    @_('TYPENAME declarator ";"')
    @_('TYPENAME declarator "=" expr ";"')
    def decl(self, p):
        pass

    @_('IDENTIFIER')
    @_('"(" declarator ")"')
    def declarator(self, p):
        pass


if __name__ == '__main__':
    lexer = DeclExprLexer()
    parser = DeclExprParser()

