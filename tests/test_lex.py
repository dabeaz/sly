import pytest
from sly import Lexer

try:
    import regex
except ImportError:
    regex = None

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

    def error(self, t):
        self.errors.append(t.value)
        self.index += 1
        if hasattr(self, 'return_error'):
            return t

    def __init__(self):
        self.errors = []

if regex is not None:
    class RegexModuleCalcLexer(Lexer):
        regex_module = regex

        tokens = { 'ID', 'PLUS', 'MINUS' }

        literals = { '(', ')' }
        ignore = ' \t'

        ID      = r'\p{Ll}+'  # Unicode lowercase letters, regex module feature
        PLUS    = r'\+'
        MINUS   = r'-'

        ignore_comment = r'\#.*'

        @_(r'\n+')
        def newline(self, t):
            self.lineno += t.value.count('\n')

        def ID(self, t):
            t.value = t.value.upper()
            return t

# Test basic recognition of various tokens and literals
def test_tokens():
    lexer = CalcLexer()
    toks = list(lexer.tokenize('abc 123 + - * / = < <= ( )'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['ID','NUMBER','PLUS','MINUS','TIMES','DIVIDE','ASSIGN','LT','LE','(',')']
    assert vals == ['ABC', 123, '+', '-', '*', '/', '=', '<', '<=', '(', ')']

# Test third-party regex module support
@pytest.mark.skipif(regex is None,
                    reason="third-party regex module not installed")
def test_3rd_party_regex_module():
    lexer = RegexModuleCalcLexer()
    toks = list(lexer.tokenize('a + b - c'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['ID','PLUS','ID','MINUS','ID']
    assert vals == ['A', '+', 'B', '-', 'C']

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

# Test error token return handling
def test_error_return():
    lexer = CalcLexer()
    lexer.return_error = True
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'ERROR', 'PLUS', 'MINUS']
    assert vals == [123, ':+-', '+', '-']
    assert lexer.errors == [ ':+-' ]


class ModernCalcLexer(Lexer):
    # Set of token names.   This is always required
    tokens = { ID, NUMBER, PLUS, MINUS, TIMES, DIVIDE, ASSIGN, LT, LE, IF, ELSE }
    literals = { '(', ')' }

    # String containing ignored characters between tokens
    ignore = ' \t'

    # Regular expression rules for tokens
    ID      = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE

    NUMBER  = r'\d+'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    ASSIGN  = r'='
    LE      = r'<='
    LT      = r'<'

    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    # Ignored text
    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # Attached rule
    def ID(self, t):
        t.value = t.value.upper()
        return t

    def error(self, t):
        self.errors.append(t.value)
        self.index += 1
        if hasattr(self, 'return_error'):
            return t

    def __init__(self):
        self.errors = []


# Test basic recognition of various tokens and literals
def test_modern_tokens():
    lexer = ModernCalcLexer()
    toks = list(lexer.tokenize('abc if else 123 + - * / = < <= ( )'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['ID','IF','ELSE', 'NUMBER','PLUS','MINUS','TIMES','DIVIDE','ASSIGN','LT','LE','(',')']
    assert vals == ['ABC','if','else', 123, '+', '-', '*', '/', '=', '<', '<=', '(', ')']

# Test ignored comments and newlines
def test_modern_ignored():
    lexer = ModernCalcLexer()
    toks = list(lexer.tokenize('\n\n# A comment\n123\nabc\n'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    linenos = [t.lineno for t in toks]
    assert types == ['NUMBER', 'ID']
    assert vals == [123, 'ABC']
    assert linenos == [4,5]
    assert lexer.lineno == 6

# Test error handling
def test_modern_error():
    lexer = ModernCalcLexer()
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'PLUS', 'MINUS']
    assert vals == [123, '+', '-']
    assert lexer.errors == [ ':+-' ]

# Test error token return handling
def test_modern_error_return():
    lexer = ModernCalcLexer()
    lexer.return_error = True
    toks = list(lexer.tokenize('123 :+-'))
    types = [t.type for t in toks]
    vals = [t.value for t in toks]
    assert types == ['NUMBER', 'ERROR', 'PLUS', 'MINUS']
    assert vals == [123, ':+-', '+', '-']
    assert lexer.errors == [ ':+-' ]

# Test Lexer Inheritance.  This class should inherit all of the tokens
# and features of ModernCalcLexer, but add two new tokens to it.  The
# PLUSPLUS token matches before the PLUS token.

if False:
    class SubModernCalcLexer(ModernCalcLexer):
        tokens |= { DOLLAR, PLUSPLUS }
        DOLLAR = r'\$'
        PLUSPLUS = r'\+\+'
        PLUSPLUS.before = PLUS

    def test_lexer_inherit():
        lexer = SubModernCalcLexer()
        toks = list(lexer.tokenize('123 + - $ ++ if'))
        types = [t.type for t in toks]
        vals = [t.value for t in toks]
        assert types == ['NUMBER', 'PLUS', 'MINUS', 'DOLLAR', 'PLUSPLUS', 'IF']
        assert vals == [123, '+', '-', '$', '++', 'if']


