SLY (Sly Lex Yacc)
==================

This document provides an overview of lexing and parsing with SLY.
Given the intrinsic complexity of parsing, I would strongly advise 
that you read (or at least skim) this entire document before jumping
into a big development project with SLY.  

SLY requires Python 3.5 or newer.  If you're using an older version,
you're out of luck. Sorry.

Introduction
------------
SLY is library for writing parsers and compilers.  It is loosely
based on the traditional compiler construction tools lex and yacc
and implements the same LALR(1) parsing algorithm.  Most of the
features available in lex and yacc are also available in SLY.
It should also be noted that SLY does not provide much in
the way of bells and whistles (e.g., automatic construction of
abstract syntax trees, tree traversal, etc.). Nor should you view it
as a parsing framework. Instead, you will find a bare-bones, yet
fully capable library for writing parsers in Python.

The rest of this document assumes that you are somewhat familiar with
parsing theory, syntax directed translation, and the use of compiler
construction tools such as lex and yacc in other programming
languages. If you are unfamiliar with these topics, you will probably
want to consult an introductory text such as "Compilers: Principles,
Techniques, and Tools", by Aho, Sethi, and Ullman.  O'Reilly's "Lex
and Yacc" by John Levine may also be handy.  In fact, the O'Reilly book can be
used as a reference for SLY as the concepts are virtually identical.

SLY Overview
------------

SLY provides two separate classes ``Lexer`` and ``Parser``.  The
``Lexer`` class is used to break input text into a collection of
tokens specified by a collection of regular expression rules.  The
``Parser`` class is used to recognize language syntax that has been
specified in the form of a context free grammar.    The two classes
are typically used together to make a parser.  However, this is not
a strict requirement--there is a great deal of flexibility allowed.
The next two parts describe the basics.

Writing a Lexer
---------------

Suppose you're writing a programming language and a user supplied the
following input string::

    x = 3 + 42 * (s - t)

A tokenizer splits the string into individual tokens where each token
has a name and value.  For example, the above text might be described
by the following token list::

    [ ('ID','x'), ('EQUALS','='), ('NUMBER','3'), 
      ('PLUS','+'), ('NUMBER','42), ('TIMES','*'),
      ('LPAREN','('), ('ID','s'), ('MINUS','-'),
      ('ID','t'), ('RPAREN',')' ]

The ``Lexer`` class is used to do this.   Here is a sample of a simple
tokenizer::

    # ------------------------------------------------------------
    # calclex.py
    #
    # tokenizer for a simple expression evaluator for
    # numbers and +,-,*,/
    # ------------------------------------------------------------

    from sly import Lexer

    class CalcLexer(Lexer):
        # List of token names.   This is always required
        tokens = (
            'NUMBER',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'LPAREN',
            'RPAREN',
            )

        # String containining ignored characters (spaces and tabs)
        ignore = ' \t'

        # Regular expression rules for simple tokens
        PLUS    = r'\+'
        MINUS   = r'-'
        TIMES   = r'\*'
        DIVIDE  = r'/'
        LPAREN  = r'\('
        RPAREN  = r'\)'

        # A regular expression rule with some action code
        @_(r'\d+')
        def NUMBER(self, t):
            t.value = int(t.value)    
            return t

        # Define a rule so we can track line numbers
        @_(r'\n+')
        def newline(self, t):
            self.lineno += len(t.value)

        # Error handling rule (skips ahead one character)
        def error(self, value):
            print("Line %d: Illegal character '%s'" % (self.lineno, value[0]))
            self.index += 1

    if __name__ == '__main__':
        data = '''
                 3 + 4 * 10
                   + -20 * ^ 2
               '''

        lexer = CalcLexer()
        for tok in lexer.tokenize(data):
            print(tok)

When executed, the example will produce the following output::

    Token(NUMBER, 3, 2, 14)
    Token(PLUS, '+', 2, 16)
    Token(NUMBER, 4, 2, 18)
    Token(TIMES, '*', 2, 20)
    Token(NUMBER, 10, 2, 22)
    Token(PLUS, '+', 3, 40)
    Token(MINUS, '-', 3, 42)
    Token(NUMBER, 20, 3, 43)
    Token(TIMES, '*', 3, 46)
    Line 3: Illegal character '^'
    Token(NUMBER, 2, 3, 50)

The tokens produced by the ``lexer.tokenize()`` methods are instances
of type ``Token``.  The ``type`` and ``value`` attributes contain the
token name and value respectively.  The ``lineno`` and ``index``
attributes contain the line number and position in the input text
where the token appears. Here is an example of accessing these
attributes::

    for tok in lexer.tokenize(data):
        print(tok.type, tok.value,  tok.lineno, tok.index)


The tokens list
---------------

All lexers must provide a list ``tokens`` that defines all of the possible token
names that can be produced by the lexer.  This list is always required
and is used to perform a variety of validation checks.  

In the example, the following code specified the token names::

    class CalcLexer(Lexer):
        ...
        # List of token names.   This is always required
        tokens = (
            'NUMBER',
            'PLUS',
            'MINUS',
            'TIMES',
            'DIVIDE',
            'LPAREN',
            'RPAREN',
            )
        ...

Specification of tokens
-----------------------
Each token is specified by writing a regular expression rule compatible with Python's ``re`` module.  Each of these rules
are defined by making declarations that match the names of the tokens provided in the tokens list.
For simple tokens, the regular expression is specified as a string such as this::

    PLUS = r'\+'
    MINUS = r'-'
    
If some kind of action needs to be performed when a token is matched,
a token rule can be specified as a function.  In this case, the
associated regular expression is given using the ``@_` decorator like
this::

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

The function always takes a single argument which is an instance of
``Token``.  By default, ``t.type`` is set to the name of the
definition (e.g., ``'NUMBER'``).  The function can change the token
type and value as it sees appropriate.  When finished, the resulting
token object should be returned. If no value is returned by the
function, the token is simply discarded and the next token read.

Internally, the ``Lexer`` class uses the ``re`` module to do its pattern matching.  Patterns are compiled
using the ``re.VERBOSE`` flag which can be used to help readability.  However, be aware that unescaped
whitespace is ignored and comments are allowed in this mode.  If your pattern involves whitespace, make sure you
use ``\s``.  If you need to match the ``#`` character, use ``[#]``.

When building the master regular expression, rules are added in the
same order as they are listed in the ``Lexer`` class.  Be aware that
longer tokens may need to be specified before short tokens.  For
example, if you wanted to have separate tokens for "=" and "==", you
need to make sure that "==" is listed first.

To handle reserved words, you should write a single rule to match an
identifier and do a special name lookup in a function like this::

    class CalcLexer(Lexer):
 
        reserved = { 'if', 'then', 'else', 'while' }
        tokens = ['LPAREN','RPAREN',...,'ID'] + [ w.upper() for w in reserved ]

        @_(r'[a-zA-Z_][a-zA-Z_0-9]*')
        def ID(self, t):
            if t.value in self.reserved:
                t.type = t.value.upper()
            return t

Note: You should avoid writing individual rules for reserved words.
For example, suppose you wrote rules like this::

    FOR   = r'for'
    PRINT = r'print'

In this case, the rules will be triggered for identifiers that include
those words as a prefix such as "forget" or "printed".  This is
probably not what you want.

Discarded tokens
----------------
To discard a token, such as a comment, simply define a token rule that returns no value.  For example::

    @_(r'\#.*')
    def COMMENT(self, t):
        pass
        # No return value. Token discarded

Alternatively, you can include the prefix "ignore_" in the token declaration to force a token to be ignored.  For example:

    ignore_COMMENT = r'\#.*'


Line numbers and positional information
---------------------------------------

By default, lexers know nothing about line numbers.  This is because
they don't know anything about what constitutes a "line" of input
(e.g., the newline character or even if the input is textual data).
To update this information, you need to write a special rule.  In the
example, the ``newline()`` rule shows how to do this::

    # Define a rule so we can track line numbers
    @_(r'\n+')
    def newline(self, t):
        self.lineno += len(t.value)

Within the rule, the lineno attribute of the lexer is updated.  After
the line number is updated, the token is simply discarded since
nothing is returned.

Lexers do not perform and kind of automatic column tracking.  However,
it does record positional information related to each token in the
``index`` attribute.  Using this, it is usually possible to compute
column information as a separate step.  For instance, you could count
backwards until you reach a newline::

    # Compute column. 
    #     input is the input text string
    #     token is a token instance
    def find_column(text, token):
        last_cr = text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        column = (token.index - last_cr) + 1
        return column

Since column information is often only useful in the context of error
handling, calculating the column position can be performed when needed
as opposed to doing it for each token.

Ignored characters
------------------

The special ``ignore`` rule is reserved for characters that should be
completely ignored in the input stream.  Usually this is used to skip
over whitespace and other non-essential characters.  Although it is
possible to define a regular expression rule for whitespace in a
manner similar to ``newline()``, the use of ``ignore`` provides
substantially better lexing performance because it is handled as a
special case and is checked in a much more efficient manner than the
normal regular expression rules.

The characters given in ``ignore`` are not ignored when such
characters are part of other regular expression patterns.  For
example, if you had a rule to capture quoted text, that pattern can
include the ignored characters (which will be captured in the normal
way).  The main purpose of ``ignore`` is to ignore whitespace and
other padding between the tokens that you actually want to parse.

Literal characters
------------------

Literal characters can be specified by defining a variable ``literals`` in the class.
For example::

     class MyLexer(Lexer):
         ...
         literals = [ '+','-','*','/' ]
         ...

A literal character is simply a single character that is returned "as
is" when encountered by the lexer.  Literals are checked after all of
the defined regular expression rules.  Thus, if a rule starts with one
of the literal characters, it will always take precedence.

When a literal token is returned, both its ``type`` and ``value``
attributes are set to the character itself. For example, ``'+'``.

It's possible to write token functions that perform additional actions
when literals are matched.  However, you'll need to set the token type
appropriately. For example::

     class MyLexer(Lexer):

          literals = [ '{', '}' ]

          @_(r'\{')
          def lbrace(self, t):
              t.type = '{'      # Set token type to the expected literal
              return t

          @_(r'\}')
          def rbrace(t):
              t.type = '}'      # Set token type to the expected literal
              return t

Error handling
--------------

The ``error()``
function is used to handle lexing errors that occur when illegal
characters are detected.  The error function receives a string containing
all remaining untokenized text.  A typical handler might skip ahead 
in the input. For example::

    # Error handling rule
    def error(self, value):
        print("Illegal character '%s'" % value[0])
        self.index += 1

In this case, we simply print the offending character and skip ahead one character by updating the
lexer position.

EOF Handling
------------

An optional ``eof()`` method can be used to handle an end-of-file (EOF) condition in the input.   
Write me::

    # EOF handling rule
    def eof(self):
        # Get more input (Example)
        more = raw_input('... ')
        if more:
            self.lexer.input(more)
            return self.lexer.token()
        return None

Maintaining state
-----------------
In your lexer, you may want to maintain a variety of state
information.  This might include mode settings, symbol tables, and
other details.  As an example, suppose that you wanted to keep
track of how many NUMBER tokens had been encountered.  
You can do this by adding an ``__init__()`` method. For example::

class MyLexer(Lexer):
    def __init__(self):
        self.num_count = 0

    @_(r'\d+')
    def NUMBER(self,t):
        self.num_count += 1
        t.value = int(t.value)    
        return t

