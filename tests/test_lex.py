import pytest
from sly import Lexer

class CalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = {
        'ID',
        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'ASSIGN',
        'LT',
        'LE',
        }

    literals = { '(', ')' }

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Ignored text
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    # Attached rule
    def ID(self, t):
        t.value = t.value.upper()
        return t

    def error(self, value):
        self.errors.append(value)
        self.index += 1

    def __init__(self):
        self.errors = []

# Test basic recognition of various tokens and literals
def test_tokens():
    lexer = CalcLexer()
    toks = list(lexer.tokenize('abc 123 + - * / = < <= ( )'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE','ASSIGN','LT','LE','(',')']
    assert vals == ['ABC', 123, '+', '-', '*', '/', '=', '<', '<=', '(', ')']

# Test ignored comments and newlines
def test_ignored():
    lexer = CalcLexer()
    toks = list(lexer.tokenize('\n\n# A comment\n123\nabc\n'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    linenos = [t.lineno for t in toks]
    assert types == ['NUMBER', 'ID']
    assert vals == [123, 'ABC']
    assert linenos == [4,5]
    assert lexer.lineno == 6

# Test error handling
def test_error():
    lexer = CalcLexer()
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'PLUS', 'MINUS']
    assert vals == [123, '+', '-']
    assert lexer.errors == [ ':+-' ]

    
    
    



