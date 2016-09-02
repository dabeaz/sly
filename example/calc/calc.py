# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

from sly import Lexer, Parser

class CalcLexer(Lexer):
    tokens = (
        'NAME', 'NUMBER',
        )
    ignore = ' \t'
    literals = ['=', '+', '-', '*', '/', '(', ')']

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, value):
        print("Illegal character '%s'" % value[0])
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens
    
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.names = { }

    @_('statement : NAME "=" expression')
    def statement_assign(self, p):
        self.names[p[1]] = p[3]

    @_('statement : expression')
    def statement_expr(self, p):
        print(p[1])

    @_('''expression : expression '+' expression
                     | expression '-' expression
                     | expression '*' expression
                     | expression '/' expression''')
    def expression_binop(self, p):
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]
        elif p[2] == '*':
            p[0] = p[1] * p[3]
        elif p[2] == '/':
            p[0] = p[1] / p[3]

    @_('expression : "-" expression %prec UMINUS')
    def expression_uminus(self, p):
        p[0] = -p[2]

    @_('expression : "(" expression ")"')
    def expression_group(self, p):
        p[0] = p[2]

    @_('expression : NUMBER')
    def expression_number(self, p):
        p[0] = p[1]

    @_('expression : NAME')
    def expression_name(self, p):
        try:
            p[0] = self.names[p[1]]
        except LookupError:
            print("Undefined name '%s'" % p[1])
            p[0] = 0


if __name__ == '__main__':
    parser = CalcParser()
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if s:
            parser.parse(CalcLexer(s))
