# schcls.py
#
# Proof of concept--not complete

from sly.docparse import DocParseMeta
from sly import Lexer, Parser

class SchLexer(Lexer):
    tokens   = { NUMBER, NAME, DEFINE, SET }
    ignore   = ' \t'
    literals = ['=','+','-','*','/','(',')','.']

    NAME     = '[a-zA-Z_!][a-zA-Z0-9_!]*'
    NAME['define'] = DEFINE
    NAME['set!'] = SET

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno = t.lineno + t.value.count('\n')

    def error(self, t):
        print(f"{self.cls_module}.{self.cls_name}:{self.lineno}: * Illegal character", repr(self.text[self.index]))
        self.index += 1

class SchParser(Parser):
    tokens = SchLexer.tokens
    precedence = ( 
        ('left', '+','-'),
        ('left', '*','/')
        )
    def __init__(self):
        self.env = { }

    @_('declarations',
       '')
    def program(self, p):
        return self.env

    @_('declarations declaration')
    def declarations(self, p):
        pass

    @_('declaration')
    def declarations(self, p):
        pass

    @_("'(' DEFINE NAME expression ')'")
    def declaration(self, p):
        self.env[p.NAME] = p.expression

    @_("'(' DEFINE '(' NAME arglist ')' exprlist ')'")
    def declaration(self, p):
        args = ','.join(p.arglist)
        self.env[p.NAME] = eval(f"lambda {args}: ({','.join(p.exprlist)},)[-1]")

    @_("'(' SET NAME '.' NAME expression ')'")
    def expression(self, p):
        return f'setattr({p.NAME0}, {p.NAME1!r}, {p.expression})'

    @_("")
    def arglist(self, p):
        return []

    @_("arglist_nonempty")
    def arglist(self, p):
        return p.arglist_nonempty

    @_("arglist_nonempty NAME")
    def arglist_nonempty(self, p):
        p.arglist_nonempty.append(p.NAME)
        return p.arglist_nonempty

    @_("NAME")
    def arglist_nonempty(self, p):
        return [ p.NAME ]

    @_("NUMBER")
    def expression(self, p):
        return str(p.NUMBER)

    @_("name")
    def expression(self, p):
        return p.name

    @_("'(' operator exprlist ')'")
    def expression(self, p):
        return '(' + p.operator.join(p.exprlist) + ')'
    
    @_("'+'", "'-'", "'*'", "'/'")
    def operator(self, p):
        return p[0]

    @_("'(' name exprlist ')'")
    def expression(self, p):
        return p.name + '(' + ','.join(p.exprlist) + ')'

    @_("'(' name ')'")
    def expression(self, p):
        return p.name + '()'

    @_('exprlist expression')
    def exprlist(self, p):
        p.exprlist.append(p.expression)
        return p.exprlist

    @_('expression')
    def exprlist(self, p):
        return [ p.expression ]

    @_("NAME '.' NAME")
    def name(self, p):
        return f'{p.NAME0}.{p.NAME1}'

    @_("NAME")
    def name(self, p):
        return p.NAME

    def error(self, p):
        print(f'{self.cls_module}.{self.cls_name}:{getattr(p,"lineno","")}: '
              f'Syntax error at {getattr(p,"value","EOC")}')

class SchMeta(DocParseMeta):
    lexer = SchLexer
    parser = SchParser

class Sch(metaclass=SchMeta):
    pass

class Rat(Sch):
    '''
    (define (__init__ self numer denom)
        (set! self.numer numer)
        (set! self.denom denom)
    )
    (define (__add__ self other)
        (Rat (+ (* self.numer other.denom)
                (* self.denom other.numer))
             (* self.denom other.denom)
        )
    )
    (define (__sub__ self other)
        (Rat (- (* self.numer other.denom)
                (* self.denom other.numer))
             (* self.denom other.denom)
        )
    )
    (define (__mul__ self other) 
        (Rat (* self.numer other.numer)
             (* self.denom other.denom)
        )
    )
    (define (__truediv__ self other) 
        (Rat (* self.numer other.denom)
             (* self.denom other.numer)
        )
    )
    '''
    def __repr__(self):
        return f'Rat({self.numer}, {self.denom})'

if __name__ == '__main__':
    a = Rat(2, 3)
    b = Rat(1, 4)
    print(a + b)
    print(a - b)
    print(a * b)
    print(a / b)





    
    
