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

The first step of any parsing is to break the text into tokens where
each token has a type and value. For example, the above text might be
described by the following list of token tuples::

    [ ('ID','x'), ('EQUALS','='), ('NUMBER','3'), 
      ('PLUS','+'), ('NUMBER','42'), ('TIMES','*'),
      ('LPAREN','('), ('ID','s'), ('MINUS','-'),
      ('ID','t'), ('RPAREN',')' ]

The SLY ``Lexer`` class is used to do this.   Here is a sample of a simple
lexer::

    # ------------------------------------------------------------
    # calclex.py
    #
    # Lexer for a simple expression evaluator for
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

        # String containing ignored characters (spaces and tabs)
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
            print("Line %d: Illegal character '%s'" %
	          (self.lineno, value[0]))
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

A lexer only has one public method ``tokenize()``.  This is a generator
function that produces a stream of ``Token`` instances.
The ``type`` and ``value`` attributes of ``Token`` contain the
token type name and value respectively.  The ``lineno`` and ``index``
attributes contain the line number and position in the input text
where the token appears. 

The tokens list
^^^^^^^^^^^^^^^

Lexers must specify a ``tokens`` attribute that defines all of the possible token
type names that can be produced by the lexer.  This list is always required
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
^^^^^^^^^^^^^^^^^^^^^^^

Tokens are specified by writing a regular expression rule compatible
with Python's ``re`` module.  This is done by writing definitions that
match one of the names of the tokens provided in the ``tokens``
attribute.  For example::

    PLUS = r'\+'
    MINUS = r'-'

Sometimes you want to perform an action when a token is matched.  For example,
maybe you want to convert a numeric value or look up a symbol.  To do
this, write your action as a method and give the associated regular
expression using the ``@_()`` decorator like this::

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

The method always takes a single argument which is an instance of
``Token``.  By default, ``t.type`` is set to the name of the token
(e.g., ``'NUMBER'``).  The function can change the token type and
value as it sees appropriate.  When finished, the resulting token
object should be returned as a result. If no value is returned by the
function, the token is simply discarded and the next token read.

Internally, the ``Lexer`` class uses the ``re`` module to do its
pattern matching.  Patterns are compiled using the ``re.VERBOSE`` flag
which can be used to help readability.  However, be aware that
unescaped whitespace is ignored and comments are allowed in this mode.
If your pattern involves whitespace, make sure you use ``\s``.  If you
need to match the ``#`` character, use ``[#]``.

Controlling Match Order
^^^^^^^^^^^^^^^^^^^^^^^

Tokens are matched in the same order as patterns are listed in the
``Lexer`` class.  Be aware that longer tokens may need to be specified
before short tokens.  For example, if you wanted to have separate
tokens for "=" and "==", you need to make sure that "==" is listed
first.  For example::

    class MyLexer(Lexer):
        tokens = ('ASSIGN', 'EQUALTO', ...)
        ...
        EQUALTO = r'=='       # MUST APPEAR FIRST!
        ASSIGN  = r'='

To handle reserved words, you should write a single rule to match an
identifier and do a special name lookup in a function like this::

    class MyLexer(Lexer):
 
        reserved = { 'if', 'then', 'else', 'while' }
        tokens = ['LPAREN','RPAREN',...,'ID'] + [ w.upper() for w in reserved ]

        @_(r'[a-zA-Z_][a-zA-Z_0-9]*')
        def ID(self, t):
            # Check to see if the name is a reserved word
            # If so, change its type.
            if t.value in self.reserved:
                t.type = t.value.upper()
            return t

Note: You should avoid writing individual rules for reserved words.
For example, suppose you wrote rules like this::

    FOR   = r'for'
    PRINT = r'print'

In this case, the rules will be triggered for identifiers that include
those words as a prefix such as "forget" or "printed".  
This is probably not what you want.

Discarded text
^^^^^^^^^^^^^^
To discard text, such as a comment, simply define a token rule that returns no value.  For example::

    @_(r'\#.*')
    def COMMENT(self, t):
        pass
        # No return value. Token discarded

Alternatively, you can include the prefix ``ignore_`` in a token
declaration to force a token to be ignored.  For example::

    ignore_COMMENT = r'\#.*'

Line numbers and position tracking
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
backwards until you reach the previous newline::

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
as opposed to including it on each token.

Ignored characters
^^^^^^^^^^^^^^^^^^

The special ``ignore`` specification is reserved for characters that
should be completely ignored in the input stream.  Usually this is
used to skip over whitespace and other non-essential characters.
Although it is possible to define a regular expression rule for
whitespace in a manner similar to ``newline()``, the use of ``ignore``
provides substantially better lexing performance because it is handled
as a special case and is checked in a much more efficient manner than
the normal regular expression rules.

The characters given in ``ignore`` are not ignored when such
characters are part of other regular expression patterns.  For
example, if you had a rule to capture quoted text, that pattern can
include the ignored characters (which will be captured in the normal
way).  The main purpose of ``ignore`` is to ignore whitespace and
other padding between the tokens that you actually want to parse.

Literal characters
^^^^^^^^^^^^^^^^^^

Literal characters can be specified by defining a variable
``literals`` in the class.  For example::

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

It's possible to write token methods that perform additional actions
when literals are matched.  However, you'll need to set the token type
appropriately. For example::

     class MyLexer(Lexer):

          literals = [ '{', '}' ]

          def __init__(self):
              self.indentation_level = 0

          @_(r'\{')
          def lbrace(self, t):
              t.type = '{'      # Set token type to the expected literal
	      self.indentation_level += 1
              return t

          @_(r'\}')
          def rbrace(t):
              t.type = '}'      # Set token type to the expected literal
	      self.indentation_level -=1
              return t

Error handling
^^^^^^^^^^^^^^

The ``error()`` method is used to handle lexing errors that occur when
illegal characters are detected.  The error method receives a string
containing all remaining untokenized text.  A typical handler might
look at this text and skip ahead in some manner.  For example::

    class MyLexer(Lexer):
        ...
        # Error handling rule
        def error(self, value):
            print("Illegal character '%s'" % value[0])
            self.index += 1

In this case, we simply print the offending character and skip ahead
one character by updating the lexer position.   Error handling in a
parser is often a hard problem.  An error handler might scan ahead
to a logical synchronization point such as a semicolon, a blank line,
or similar landmark.

Maintaining extra state
^^^^^^^^^^^^^^^^^^^^^^^

In your lexer, you may want to maintain a variety of other state
information.  This might include mode settings, symbol tables, and
other details.  As an example, suppose that you wanted to keep track
of how many NUMBER tokens had been encountered.  You can do this by
adding an ``__init__()`` method and adding more attributes. For
example::

    class MyLexer(Lexer):
        def __init__(self):
            self.num_count = 0

        @_(r'\d+')
        def NUMBER(self,t):
            self.num_count += 1
            t.value = int(t.value)    
            return t

Please note that lexers already use the ``lineno`` and ``position``
attributes during parsing.

Writing a Parser
----------------

The ``Parser`` class is used to parse language syntax.  Before showing
an example, there are a few important bits of background that must be
mentioned.  First, *syntax* is usually specified in terms of a BNF
grammar.  For example, if you wanted to parse simple arithmetic
expressions, you might first write an unambiguous grammar
specification like this::

    expr       : expr + term
               | expr - term
               | term
 
    term       : term * factor
               | term / factor
               | factor

    factor     : NUMBER
               | ( expr )

In the grammar, symbols such as ``NUMBER``, ``+``, ``-``, ``*``, and
``/`` are known as *terminals* and correspond to raw input tokens.
Identifiers such as ``term`` and ``factor`` refer to grammar rules
comprised of a collection of terminals and other rules.  These
identifiers are known as *non-terminals*.

The semantic behavior of a language is often specified using a
technique known as syntax directed translation.  In syntax directed
translation, attributes are attached to each symbol in a given grammar
rule along with an action.  Whenever a particular grammar rule is
recognized, the action describes what to do.  For example, given the
expression grammar above, you might write the specification for a
simple calculator like this::

    Grammar                   Action
    ------------------------  -------------------------------- 
    expr0   : expr1 + term    expr0.val = expr1.val + term.val
            | expr1 - term    expr0.val = expr1.val - term.val
            | term            expr0.val = term.val

    term0   : term1 * factor  term0.val = term1.val * factor.val
            | term1 / factor  term0.val = term1.val / factor.val
            | factor          term0.val = factor.val

    factor  : NUMBER          factor.val = int(NUMBER.val)
            | ( expr )        factor.val = expr.val

A good way to think about syntax directed translation is to view each
symbol in the grammar as a kind of object. Associated with each symbol
is a value representing its "state" (for example, the ``val``
attribute above).  Semantic actions are then expressed as a collection
of functions or methods that operate on the symbols and associated
values.

SLY uses a parsing technique known as LR-parsing or shift-reduce
parsing.  LR parsing is a bottom up technique that tries to recognize
the right-hand-side of various grammar rules.  Whenever a valid
right-hand-side is found in the input, the appropriate action code is
triggered and the grammar symbols are replaced by the grammar symbol
on the left-hand-side.

LR parsing is commonly implemented by shifting grammar symbols onto a
stack and looking at the stack and the next input token for patterns
that match one of the grammar rules.  The details of the algorithm can
be found in a compiler textbook, but the following example illustrates
the steps that are performed if you wanted to parse the expression ``3
+ 5 * (10 - 20)`` using the grammar defined above.  In the example,
the special symbol ``$`` represents the end of input::

    Step Symbol Stack           Input Tokens            Action
    ---- ---------------------  ---------------------   -------------------------------
    1                           3 + 5 * ( 10 - 20 )$    Shift 3
    2    3                        + 5 * ( 10 - 20 )$    Reduce factor : NUMBER
    3    factor                   + 5 * ( 10 - 20 )$    Reduce term   : factor
    4    term                     + 5 * ( 10 - 20 )$    Reduce expr : term
    5    expr                     + 5 * ( 10 - 20 )$    Shift +
    6    expr +                     5 * ( 10 - 20 )$    Shift 5
    7    expr + 5                     * ( 10 - 20 )$    Reduce factor : NUMBER
    8    expr + factor                * ( 10 - 20 )$    Reduce term   : factor
    9    expr + term                  * ( 10 - 20 )$    Shift *
    10   expr + term *                  ( 10 - 20 )$    Shift (
    11   expr + term * (                  10 - 20 )$    Shift 10
    12   expr + term * ( 10                  - 20 )$    Reduce factor : NUMBER
    13   expr + term * ( factor              - 20 )$    Reduce term : factor
    14   expr + term * ( term                - 20 )$    Reduce expr : term
    15   expr + term * ( expr                - 20 )$    Shift -
    16   expr + term * ( expr -                20 )$    Shift 20
    17   expr + term * ( expr - 20                )$    Reduce factor : NUMBER
    18   expr + term * ( expr - factor            )$    Reduce term : factor
    19   expr + term * ( expr - term              )$    Reduce expr : expr - term
    20   expr + term * ( expr                     )$    Shift )
    21   expr + term * ( expr )                    $    Reduce factor : (expr)
    22   expr + term * factor                      $    Reduce term : term * factor
    23   expr + term                               $    Reduce expr : expr + term
    24   expr                                      $    Reduce expr
    25                                             $    Success!

When parsing the expression, an underlying state machine and the
current input token determine what happens next.  If the next token
looks like part of a valid grammar rule (based on other items on the
stack), it is generally shifted onto the stack.  If the top of the
stack contains a valid right-hand-side of a grammar rule, it is
usually "reduced" and the symbols replaced with the symbol on the
left-hand-side.  When this reduction occurs, the appropriate action is
triggered (if defined).  If the input token can't be shifted and the
top of stack doesn't match any grammar rules, a syntax error has
occurred and the parser must take some kind of recovery step (or bail
out).  A parse is only successful if the parser reaches a state where
the symbol stack is empty and there are no more input tokens.

It is important to note that the underlying implementation is built
around a large finite-state machine that is encoded in a collection of
tables. The construction of these tables is non-trivial and
beyond the scope of this discussion.  However, subtle details of this
process explain why, in the example above, the parser chooses to shift
a token onto the stack in step 9 rather than reducing the
rule ``expr : expr + term``.

Parsing Example
^^^^^^^^^^^^^^^
Suppose you wanted to make a grammar for simple arithmetic expressions as previously described.  
Here is how you would do it with SLY::


    from sly import Parser
    from calclex import CalcLexer

    class CalcParser(Parser):
        # Get the token list from the lexer (required)
        tokens = CalcLexer.tokens

        # Grammar rules and actions
        @_('expr PLUS term')
        def expr(self, p):
            p[0] = p[1] + p[3]

        @_('expr MINUS term')
        def expr(self, p):
            p[0] = p[1] - p[3]

        @_('term')
        def expr(self, p):
            p[0] = p[1]

        @_('term TIMES factor')
        def term(self, p):
            p[0] = p[1] * p[3]

        @_('term DIVIDE factor')
        def term(self, p):
            p[0] = p[1] / p[3]

        @_('factor')
        def term(self, p):
            p[0] = p[1]

        @_('NUMBER')
        def factor(self, p):
            p[0] = p[1]

        @_('LPAREN expr RPAREN')
        def factor(self, p):
            p[0] = p[2]

        # Error rule for syntax errors
        def error(self, p):
            print("Syntax error in input!")

    if __name__ == '__main__':
        lexer = CalcLexer()
        parser = CalcParser()

        while True:
            try:
                text = input('calc > ')
                result = parser.parse(lexer.tokenize(text))
                print(result)
            except EOFError:
                break

In this example, each grammar rule is defined by a Python function
where the docstring to that function contains the appropriate
context-free grammar specification.  The statements that make up the
function body implement the semantic actions of the rule. Each function
accepts a single argument ``p`` that is a sequence containing the
values of each grammar symbol in the corresponding rule.  The values
of ``p[i]`` are mapped to grammar symbols as shown here::

    #   p[1] p[2] p[3]   
    #    |    |    |
    @_('expr PLUS term')
    def expr(self, p):
        p[0] = p[1] + p[3]

For tokens, the "value" of the corresponding ``p[i]`` is the
*same* as the ``p.value`` attribute assigned in the lexer
module.  For non-terminals, the value is determined by whatever is
placed in ``p[0]`` when rules are reduced.  This value can be
anything at all.  However, it probably most common for the value to be
a simple Python type, a tuple, or an instance.  In this example, we
are relying on the fact that the ``NUMBER`` token stores an
integer value in its value field.  All of the other rules simply
perform various types of integer operations and propagate the result.

Note: The use of negative indices have a special meaning in
yacc---specially ``p[-1]`` does not have the same value
as ``p[3]`` in this example.  Please see the section on "Embedded
Actions" for further details.

The first rule defined in the yacc specification determines the
starting grammar symbol (in this case, a rule for ``expr``
appears first).  Whenever the starting rule is reduced by the parser
and no more input is available, parsing stops and the final value is
returned (this value will be whatever the top-most rule placed
in ``p[0]``). Note: an alternative starting symbol can be
specified using the ``start`` attribute in the class.

The ``error()`` method is defined to catch syntax errors.
See the error handling section below for more detail.

If any errors are detected in your grammar specification, SLY will
produce diagnostic messages and possibly raise an exception.  Some of
the errors that can be detected include:

- Duplicated grammar rules
- Shift/reduce and reduce/reduce conflicts generated by ambiguous grammars.
- Badly specified grammar rules.
- Infinite recursion (rules that can never terminate).
- Unused rules and tokens
- Undefined rules and tokens

The final part of the example shows how to actually run the parser.
To run the parser, you simply have to call the ``parse()`` method with
a sequence of the input tokens.  This will run all of the grammar
rules and return the result of the entire parse.  This result return
is the value assigned to ``p[0]`` in the starting grammar rule.

Combining Grammar Rule Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When grammar rules are similar, they can be combined into a single function.
For example, consider the two rules in our earlier example::

    @_('expr PLUS term')
    def expr(self, p):
        p[0] = p[1] + p[3]

    @_('expr MINUS term')
    def expr(self, p):
        p[0] = p[1] - p[3]

Instead of writing two functions, you might write a single function like this:

    @_('expr PLUS term',
       'expr MINUS term')
    def expr(self, p):
        if p[2] == '+':
            p[0] = p[1] + p[3]
        elif p[2] == '-':
            p[0] = p[1] - p[3]

In general, the ``@_()`` decorator for any given method can list
multiple grammar rules.  When combining grammar rules into a single
function though, it is usually a good idea for all of the rules to have a
similar structure (e.g., the same number of terms).  Otherwise, the
corresponding action code may be more complicated than necessary.
However, it is possible to handle simple cases using len().  For
example:

    @_('expr MINUS expr',
       'MINUS expression')
    def expr(self, p):
        if (len(p) == 4):
            p[0] = p[1] - p[3]
        elif (len(p) == 3):
            p[0] = -p[2]

If parsing performance is a concern, you should resist the urge to put
too much conditional processing into a single grammar rule as shown in
these examples.  When you add checks to see which grammar rule is
being handled, you are actually duplicating the work that the parser
has already performed (i.e., the parser already knows exactly what rule it
matched).  You can eliminate this overhead by using a
separate method for each grammar rule.

Character Literals
^^^^^^^^^^^^^^^^^^

If desired, a grammar may contain tokens defined as single character
literals.  For example::

    @_('expr "+" term')
    def expr(self, p):
        p[0] = p[1] + p[3]

    @_('expr "-" term')
    def expr(self, p):
        p[0] = p[1] - p[3]

A character literal must be enclosed in quotes such as ``"+"``.  In addition, if literals are used, they must be declared in the
corresponding lexer class through the use of a special ``literals`` declaration::

    class CalcLexer(Lexer):
        ...
        literals = ['+','-','*','/' ]
        ...

Character literals are limited to a single character.  Thus, it is not
legal to specify literals such as ``<=`` or ``==``.
For this, use the normal lexing rules (e.g., define a rule such as
``EQ = r'=='``).

Empty Productions
^^^^^^^^^^^^^^^^^

If you need an empty production, define a special rule like this::

    @_('')
    def empty(self, p):
        pass

Now to use the empty production, simply use 'empty' as a symbol.  For
example::

    @_('item')
    def optitem(self, p):
        ...

    @_('empty')
    def optitem(self, p):
        ...

Note: You can write empty rules anywhere by simply specifying an empty
string. However, I personally find that writing an "empty"
rule and using "empty" to denote an empty production is easier to read
and more clearly states your intentions.

Changing the starting symbol
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Normally, the first rule found in a yacc specification defines the
starting grammar rule (top level rule).  To change this, supply
a ``start`` specifier in your file.  For example::

    class CalcParser(Parser):
        start = 'foo'

        @_('A B')
        def bar(self, p):
            ...

        @_('bar X')
        def foo(self, p):     # Parsing starts here (start symbol above)
            ...

The use of a ``start`` specifier may be useful during debugging
since you can use it to work with a subset of a larger grammar.

Dealing With Ambiguous Grammars
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The expression grammar given in the earlier example has been written
in a special format to eliminate ambiguity.  However, in many
situations, it is extremely difficult or awkward to write grammars in
this format.  A much more natural way to express the grammar is in a
more compact form like this::

expr : expr PLUS expr
     | expr MINUS expr
     | expr TIMES expr
     | expr DIVIDE expr
     | LPAREN expr RPAREN
     | NUMBER

Unfortunately, this grammar specification is ambiguous.  For example,
if you are parsing the string "3 * 4 + 5", there is no way to tell how
the operators are supposed to be grouped.  For example, does the
expression mean "(3 * 4) + 5" or is it "3 * (4+5)"?

When an ambiguous grammar is given, you will get messages about
"shift/reduce conflicts" or "reduce/reduce conflicts".  A shift/reduce
conflict is caused when the parser generator can't decide whether or
not to reduce a rule or shift a symbol on the parsing stack.  For
example, consider the string "3 * 4 + 5" and the internal parsing
stack::

    Step Symbol Stack           Input Tokens            Action
    ---- ---------------------  ---------------------   -------------------------------
    1    $                                3 * 4 + 5$    Shift 3
    2    $ 3                                * 4 + 5$    Reduce : expr : NUMBER
    3    $ expr                             * 4 + 5$    Shift *
    4    $ expr *                             4 + 5$    Shift 4
    5    $ expr * 4                             + 5$    Reduce: expr : NUMBER
    6    $ expr * expr                          + 5$    SHIFT/REDUCE CONFLICT ????

In this case, when the parser reaches step 6, it has two options.  One
is to reduce the rule ``expr : expr * expr`` on the stack.  The other
option is to shift the token ``+`` on the stack.  Both options are
perfectly legal from the rules of the context-free-grammar.

By default, all shift/reduce conflicts are resolved in favor of
shifting.  Therefore, in the above example, the parser will always
shift the ``+`` instead of reducing.  Although this strategy
works in many cases (for example, the case of 
"if-then" versus "if-then-else"), it is not enough for arithmetic expressions.  In fact,
in the above example, the decision to shift ``+`` is completely
wrong---we should have reduced ``expr * expr`` since
multiplication has higher mathematical precedence than addition.

To resolve ambiguity, especially in expression
grammars, SLY allows individual tokens to be assigned a
precedence level and associativity.  This is done by adding a variable
``precedence`` to the grammar file like this::

    class CalcParser(Parser):
        ...
        precedence = (
           ('left', 'PLUS', 'MINUS'),
           ('left', 'TIMES', 'DIVIDE'),
        )
        ...

This declaration specifies that ``PLUS``/``MINUS`` have the
same precedence level and are left-associative and that
``TIMES``/``DIVIDE`` have the same precedence and are
left-associative.  Within the ``precedence`` declaration, tokens
are ordered from lowest to highest precedence. Thus, this declaration
specifies that ``TIMES``/``DIVIDE`` have higher precedence
than ``PLUS``/``MINUS`` (since they appear later in the
precedence specification).

The precedence specification works by associating a numerical
precedence level value and associativity direction to the listed
tokens.  For example, in the above example you get::

    PLUS      : level = 1,  assoc = 'left'
    MINUS     : level = 1,  assoc = 'left'
    TIMES     : level = 2,  assoc = 'left'
    DIVIDE    : level = 2,  assoc = 'left'

These values are then used to attach a numerical precedence value and
associativity direction to each grammar rule. *This is always
determined by looking at the precedence of the right-most terminal
symbol.*  For example::

    expr : expr PLUS expr                 # level = 1, left
         | expr MINUS expr                # level = 1, left
         | expr TIMES expr                # level = 2, left
         | expr DIVIDE expr               # level = 2, left
         | LPAREN expr RPAREN             # level = None (not specified)
         | NUMBER                         # level = None (not specified)

When shift/reduce conflicts are encountered, the parser generator
resolves the conflict by looking at the precedence rules and
associativity specifiers.

1. If the current token has higher precedence than the rule on the stack, it is shifted.

2. If the grammar rule on the stack has higher precedence, the rule is reduced.

3. If the current token and the grammar rule have the same precedence, the
rule is reduced for left associativity, whereas the token is shifted for right associativity.

4. If nothing is known about the precedence, shift/reduce conflicts are resolved in
favor of shifting (the default).

For example, if "expr PLUS expr" has been parsed and the
next token is "TIMES", the action is going to be a shift because
"TIMES" has a higher precedence level than "PLUS".  On the other hand,
if "expr TIMES expr" has been parsed and the next token is
"PLUS", the action is going to be reduce because "PLUS" has a lower
precedence than "TIMES."

When shift/reduce conflicts are resolved using the first three
techniques (with the help of precedence rules), SLY will
report no errors or conflicts in the grammar.

One problem with the precedence specifier technique is that it is
sometimes necessary to change the precedence of an operator in certain
contexts.  For example, consider a unary-minus operator in "3 + 4 *
-5".  Mathematically, the unary minus is normally given a very high
precedence--being evaluated before the multiply.  However, in our
precedence specifier, MINUS has a lower precedence than TIMES.  To
deal with this, precedence rules can be given for so-called "fictitious tokens"
like this::

    class CalcParser(Parser):
        ...
        precedence = (
            ('left', 'PLUS', 'MINUS'),
            ('left', 'TIMES', 'DIVIDE'),
            ('right', 'UMINUS'),            # Unary minus operator
        )

Now, in the grammar file, we can write our unary minus rule like this::

        @_('MINUS expr %prec UMINUS')
        def expr(p):
           p[0] = -p[2]

In this case, ``%prec UMINUS`` overrides the default rule precedence--setting it to that
of UMINUS in the precedence specifier.

At first, the use of UMINUS in this example may appear very confusing.
UMINUS is not an input token or a grammar rule.  Instead, you should
think of it as the name of a special marker in the precedence table.
When you use the ``%prec`` qualifier, you're simply telling SLY
that you want the precedence of the expression to be the same as for
this special marker instead of the usual precedence.

It is also possible to specify non-associativity in the ``precedence`` table. This would
be used when you *don't* want operations to chain together.  For example, suppose
you wanted to support comparison operators like ``<`` and ``>`` but you didn't want to allow
combinations like ``a < b < c``.   To do this, specify a rule like this::

    class MyParser(Parser):
         ...
         precedence = (
              ('nonassoc', 'LESSTHAN', 'GREATERTHAN'),  # Nonassociative operators
              ('left', 'PLUS', 'MINUS'),
              ('left', 'TIMES', 'DIVIDE'),
              ('right', 'UMINUS'),            # Unary minus operator
         )

If you do this, the occurrence of input text such as ``a < b < c``
will result in a syntax error.  However, simple expressions such as
``a < b`` will still be fine.

Reduce/reduce conflicts are caused when there are multiple grammar
rules that can be applied to a given set of symbols.  This kind of
conflict is almost always bad and is always resolved by picking the
rule that appears first in the grammar file.   Reduce/reduce conflicts
are almost always caused when different sets of grammar rules somehow
generate the same set of symbols.  For example::


    assignment :  ID EQUALS NUMBER
               |  ID EQUALS expr
           
    expr       : expr PLUS expr
               | expr MINUS expr
               | expr TIMES expr
               | expr DIVIDE expr
               | LPAREN expr RPAREN
               | NUMBER

In this case, a reduce/reduce conflict exists between these two rules::

    assignment  : ID EQUALS NUMBER
    expr        : NUMBER

For example, if you wrote "a = 5", the parser can't figure out if this
is supposed to be reduced as ``assignment : ID EQUALS NUMBER`` or
whether it's supposed to reduce the 5 as an expression and then reduce
the rule ``assignment : ID EQUALS expr``.

It should be noted that reduce/reduce conflicts are notoriously
difficult to spot simply looking at the input grammar.  When a
reduce/reduce conflict occurs, SLY will try to help by
printing a warning message such as this::

    WARNING: 1 reduce/reduce conflict
    WARNING: reduce/reduce conflict in state 15 resolved using rule (assignment -> ID EQUALS NUMBER)
    WARNING: rejected rule (expression -> NUMBER)

This message identifies the two rules that are in conflict.  However,
it may not tell you how the parser arrived at such a state.  To try
and figure it out, you'll probably have to look at your grammar and
the contents of the parser debugging file with an appropriately high
level of caffeination (see the next section).

Parser Debugging
^^^^^^^^^^^^^^^^

Tracking down shift/reduce and reduce/reduce conflicts is one of the
finer pleasures of using an LR parsing algorithm.  To assist in
debugging, SLY creates a debugging file called 'parser.out' when it
generates the parsing table.  The contents of this file look like the
following:

<blockquote>
<pre>
Unused terminals:


Grammar

Rule 1     expression -> expression PLUS expression
Rule 2     expression -> expression MINUS expression
Rule 3     expression -> expression TIMES expression
Rule 4     expression -> expression DIVIDE expression
Rule 5     expression -> NUMBER
Rule 6     expression -> LPAREN expression RPAREN

Terminals, with rules where they appear

TIMES                : 3
error                : 
MINUS                : 2
RPAREN               : 6
LPAREN               : 6
DIVIDE               : 4
PLUS                 : 1
NUMBER               : 5

Nonterminals, with rules where they appear

expression           : 1 1 2 2 3 3 4 4 6 0


Parsing method: LALR


state 0

    S' -> . expression
    expression -> . expression PLUS expression
    expression -> . expression MINUS expression
    expression -> . expression TIMES expression
    expression -> . expression DIVIDE expression
    expression -> . NUMBER
    expression -> . LPAREN expression RPAREN

    NUMBER          shift and go to state 3
    LPAREN          shift and go to state 2


state 1

    S' -> expression .
    expression -> expression . PLUS expression
    expression -> expression . MINUS expression
    expression -> expression . TIMES expression
    expression -> expression . DIVIDE expression

    PLUS            shift and go to state 6
    MINUS           shift and go to state 5
    TIMES           shift and go to state 4
    DIVIDE          shift and go to state 7


state 2

    expression -> LPAREN . expression RPAREN
    expression -> . expression PLUS expression
    expression -> . expression MINUS expression
    expression -> . expression TIMES expression
    expression -> . expression DIVIDE expression
    expression -> . NUMBER
    expression -> . LPAREN expression RPAREN

    NUMBER          shift and go to state 3
    LPAREN          shift and go to state 2


state 3

    expression -> NUMBER .

    $               reduce using rule 5
    PLUS            reduce using rule 5
    MINUS           reduce using rule 5
    TIMES           reduce using rule 5
    DIVIDE          reduce using rule 5
    RPAREN          reduce using rule 5


state 4

    expression -> expression TIMES . expression
    expression -> . expression PLUS expression
    expression -> . expression MINUS expression
    expression -> . expression TIMES expression
    expression -> . expression DIVIDE expression
    expression -> . NUMBER
    expression -> . LPAREN expression RPAREN

    NUMBER          shift and go to state 3
    LPAREN          shift and go to state 2


state 5

    expression -> expression MINUS . expression
    expression -> . expression PLUS expression
    expression -> . expression MINUS expression
    expression -> . expression TIMES expression
    expression -> . expression DIVIDE expression
    expression -> . NUMBER
    expression -> . LPAREN expression RPAREN

    NUMBER          shift and go to state 3
    LPAREN          shift and go to state 2


state 6

    expression -> expression PLUS . expression
    expression -> . expression PLUS expression
    expression -> . expression MINUS expression
    expression -> . expression TIMES expression
    expression -> . expression DIVIDE expression
    expression -> . NUMBER
    expression -> . LPAREN expression RPAREN

    NUMBER          shift and go to state 3
    LPAREN          shift and go to state 2


state 7

    expression -> expression DIVIDE . expression
    expression -> . expression PLUS expression
    expression -> . expression MINUS expression
    expression -> . expression TIMES expression
    expression -> . expression DIVIDE expression
    expression -> . NUMBER
    expression -> . LPAREN expression RPAREN

    NUMBER          shift and go to state 3
    LPAREN          shift and go to state 2


state 8

    expression -> LPAREN expression . RPAREN
    expression -> expression . PLUS expression
    expression -> expression . MINUS expression
    expression -> expression . TIMES expression
    expression -> expression . DIVIDE expression

    RPAREN          shift and go to state 13
    PLUS            shift and go to state 6
    MINUS           shift and go to state 5
    TIMES           shift and go to state 4
    DIVIDE          shift and go to state 7


state 9

    expression -> expression TIMES expression .
    expression -> expression . PLUS expression
    expression -> expression . MINUS expression
    expression -> expression . TIMES expression
    expression -> expression . DIVIDE expression

    $               reduce using rule 3
    PLUS            reduce using rule 3
    MINUS           reduce using rule 3
    TIMES           reduce using rule 3
    DIVIDE          reduce using rule 3
    RPAREN          reduce using rule 3

  ! PLUS            [ shift and go to state 6 ]
  ! MINUS           [ shift and go to state 5 ]
  ! TIMES           [ shift and go to state 4 ]
  ! DIVIDE          [ shift and go to state 7 ]

state 10

    expression -> expression MINUS expression .
    expression -> expression . PLUS expression
    expression -> expression . MINUS expression
    expression -> expression . TIMES expression
    expression -> expression . DIVIDE expression

    $               reduce using rule 2
    PLUS            reduce using rule 2
    MINUS           reduce using rule 2
    RPAREN          reduce using rule 2
    TIMES           shift and go to state 4
    DIVIDE          shift and go to state 7

  ! TIMES           [ reduce using rule 2 ]
  ! DIVIDE          [ reduce using rule 2 ]
  ! PLUS            [ shift and go to state 6 ]
  ! MINUS           [ shift and go to state 5 ]

state 11

    expression -> expression PLUS expression .
    expression -> expression . PLUS expression
    expression -> expression . MINUS expression
    expression -> expression . TIMES expression
    expression -> expression . DIVIDE expression

    $               reduce using rule 1
    PLUS            reduce using rule 1
    MINUS           reduce using rule 1
    RPAREN          reduce using rule 1
    TIMES           shift and go to state 4
    DIVIDE          shift and go to state 7

  ! TIMES           [ reduce using rule 1 ]
  ! DIVIDE          [ reduce using rule 1 ]
  ! PLUS            [ shift and go to state 6 ]
  ! MINUS           [ shift and go to state 5 ]

state 12

    expression -> expression DIVIDE expression .
    expression -> expression . PLUS expression
    expression -> expression . MINUS expression
    expression -> expression . TIMES expression
    expression -> expression . DIVIDE expression

    $               reduce using rule 4
    PLUS            reduce using rule 4
    MINUS           reduce using rule 4
    TIMES           reduce using rule 4
    DIVIDE          reduce using rule 4
    RPAREN          reduce using rule 4

  ! PLUS            [ shift and go to state 6 ]
  ! MINUS           [ shift and go to state 5 ]
  ! TIMES           [ shift and go to state 4 ]
  ! DIVIDE          [ shift and go to state 7 ]

state 13

    expression -> LPAREN expression RPAREN .

    $               reduce using rule 6
    PLUS            reduce using rule 6
    MINUS           reduce using rule 6
    TIMES           reduce using rule 6
    DIVIDE          reduce using rule 6
    RPAREN          reduce using rule 6
</pre>
</blockquote>

The different states that appear in this file are a representation of
every possible sequence of valid input tokens allowed by the grammar.
When receiving input tokens, the parser is building up a stack and
looking for matching rules.  Each state keeps track of the grammar
rules that might be in the process of being matched at that point.  Within each
rule, the "." character indicates the current location of the parse
within that rule.  In addition, the actions for each valid input token
are listed.  When a shift/reduce or reduce/reduce conflict arises,
rules <em>not</em> selected are prefixed with an !.  For example:

<blockquote>
<pre>
  ! TIMES           [ reduce using rule 2 ]
  ! DIVIDE          [ reduce using rule 2 ]
  ! PLUS            [ shift and go to state 6 ]
  ! MINUS           [ shift and go to state 5 ]
</pre>
</blockquote>

By looking at these rules (and with a little practice), you can usually track down the source
of most parsing conflicts.  It should also be stressed that not all shift-reduce conflicts are
bad.  However, the only way to be sure that they are resolved correctly is to look at <tt>parser.out</tt>.
  
<H3><a name="ply_nn29"></a>6.8 Syntax Error Handling</H3>


If you are creating a parser for production use, the handling of
syntax errors is important.  As a general rule, you don't want a
parser to simply throw up its hands and stop at the first sign of
trouble.  Instead, you want it to report the error, recover if possible, and
continue parsing so that all of the errors in the input get reported
to the user at once.   This is the standard behavior found in compilers
for languages such as C, C++, and Java.

In PLY, when a syntax error occurs during parsing, the error is immediately
detected (i.e., the parser does not read any more tokens beyond the
source of the error).  However, at this point, the parser enters a
recovery mode that can be used to try and continue further parsing.
As a general rule, error recovery in LR parsers is a delicate
topic that involves ancient rituals and black-magic.   The recovery mechanism
provided by <tt>yacc.py</tt> is comparable to Unix yacc so you may want
consult a book like O'Reilly's "Lex and Yacc" for some of the finer details.

<p>
When a syntax error occurs, <tt>yacc.py</tt> performs the following steps:

<ol>
<li>On the first occurrence of an error, the user-defined <tt>p_error()</tt> function
is called with the offending token as an argument. However, if the syntax error is due to
reaching the end-of-file, <tt>p_error()</tt> is called with an
  argument of <tt>None</tt>.
Afterwards, the parser enters
an "error-recovery" mode in which it will not make future calls to <tt>p_error()</tt> until it
has successfully shifted at least 3 tokens onto the parsing stack.

<p>
<li>If no recovery action is taken in <tt>p_error()</tt>, the offending lookahead token is replaced
with a special <tt>error</tt> token.

<p>
<li>If the offending lookahead token is already set to <tt>error</tt>, the top item of the parsing stack is
deleted.

<p>
<li>If the entire parsing stack is unwound, the parser enters a restart state and attempts to start
parsing from its initial state.

<p>
<li>If a grammar rule accepts <tt>error</tt> as a token, it will be
shifted onto the parsing stack.

<p>
<li>If the top item of the parsing stack is <tt>error</tt>, lookahead tokens will be discarded until the
parser can successfully shift a new symbol or reduce a rule involving <tt>error</tt>.
</ol>

<H4><a name="ply_nn30"></a>6.8.1 Recovery and resynchronization with error rules</H4>


The most well-behaved approach for handling syntax errors is to write grammar rules that include the <tt>error</tt>
token.  For example, suppose your language had a grammar rule for a print statement like this:

<blockquote>
<pre>
def p_statement_print(p):
     'statement : PRINT expr SEMI'
     ...
</pre>
</blockquote>

To account for the possibility of a bad expression, you might write an additional grammar rule like this:

<blockquote>
<pre>
def p_statement_print_error(p):
     'statement : PRINT error SEMI'
     print("Syntax error in print statement. Bad expression")

</pre>
</blockquote>

In this case, the <tt>error</tt> token will match any sequence of
tokens that might appear up to the first semicolon that is
encountered.  Once the semicolon is reached, the rule will be
invoked and the <tt>error</tt> token will go away.

<p>
This type of recovery is sometimes known as parser resynchronization.
The <tt>error</tt> token acts as a wildcard for any bad input text and
the token immediately following <tt>error</tt> acts as a
synchronization token.

<p>
It is important to note that the <tt>error</tt> token usually does not appear as the last token
on the right in an error rule.  For example:

<blockquote>
<pre>
def p_statement_print_error(p):
    'statement : PRINT error'
    print("Syntax error in print statement. Bad expression")
</pre>
</blockquote>

This is because the first bad token encountered will cause the rule to
be reduced--which may make it difficult to recover if more bad tokens
immediately follow.   

<H4><a name="ply_nn31"></a>6.8.2 Panic mode recovery</H4>


An alternative error recovery scheme is to enter a panic mode recovery in which tokens are
discarded to a point where the parser might be able to recover in some sensible manner.

<p>
Panic mode recovery is implemented entirely in the <tt>p_error()</tt> function.  For example, this
function starts discarding tokens until it reaches a closing '}'.  Then, it restarts the 
parser in its initial state.

<blockquote>
<pre>
def p_error(p):
    print("Whoa. You are seriously hosed.")
    if not p:
        print("End of File!")
        return

    # Read ahead looking for a closing '}'
    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'RBRACE': 
            break
    parser.restart()
</pre>
</blockquote>

<p>
This function simply discards the bad token and tells the parser that the error was ok.

<blockquote>
<pre>
def p_error(p):
    if p:
         print("Syntax error at token", p.type)
         # Just discard the token and tell the parser it's okay.
         parser.errok()
    else:
         print("Syntax error at EOF")
</pre>
</blockquote>

<P>
More information on these methods is as follows:
</p>

<p>
<ul>
<li><tt>parser.errok()</tt>.  This resets the parser state so it doesn't think it's in error-recovery
mode.   This will prevent an <tt>error</tt> token from being generated and will reset the internal
error counters so that the next syntax error will call <tt>p_error()</tt> again.

<p>
<li><tt>parser.token()</tt>.  This returns the next token on the input stream.

<p>
<li><tt>parser.restart()</tt>.  This discards the entire parsing stack and resets the parser
to its initial state. 
</ul>

<p>
To supply the next lookahead token to the parser, <tt>p_error()</tt> can return a token.  This might be
useful if trying to synchronize on special characters.  For example:

<blockquote>
<pre>
def p_error(p):
    # Read ahead looking for a terminating ";"
    while True:
        tok = parser.token()             # Get the next token
        if not tok or tok.type == 'SEMI': break
    parser.errok()

    # Return SEMI to the parser as the next lookahead token
    return tok  
</pre>
</blockquote>

<p>
Keep in mind in that the above error handling functions,
<tt>parser</tt> is an instance of the parser created by
<tt>yacc()</tt>.   You'll need to save this instance someplace in your
code so that you can refer to it during error handling.
</p>

<H4><a name="ply_nn35"></a>6.8.3 Signalling an error from a production</H4>


If necessary, a production rule can manually force the parser to enter error recovery.  This
is done by raising the <tt>SyntaxError</tt> exception like this:

<blockquote>
<pre>
def p_production(p):
    'production : some production ...'
    raise SyntaxError
</pre>
</blockquote>

The effect of raising <tt>SyntaxError</tt> is the same as if the last symbol shifted onto the
parsing stack was actually a syntax error.  Thus, when you do this, the last symbol shifted is popped off
of the parsing stack and the current lookahead token is set to an <tt>error</tt> token.   The parser
then enters error-recovery mode where it tries to reduce rules that can accept <tt>error</tt> tokens.  
The steps that follow from this point are exactly the same as if a syntax error were detected and 
<tt>p_error()</tt> were called.

<P>
One important aspect of manually setting an error is that the <tt>p_error()</tt> function will <b>NOT</b> be
called in this case.   If you need to issue an error message, make sure you do it in the production that
raises <tt>SyntaxError</tt>.

<P>
Note: This feature of PLY is meant to mimic the behavior of the YYERROR macro in yacc.

<H4><a name="ply_nn38"></a>6.8.4 When Do Syntax Errors Get Reported</H4>


<p>
In most cases, yacc will handle errors as soon as a bad input token is
detected on the input.  However, be aware that yacc may choose to
delay error handling until after it has reduced one or more grammar
rules first.  This behavior might be unexpected, but it's related to
special states in the underlying parsing table known as "defaulted
states."  A defaulted state is parsing condition where the same
grammar rule will be reduced regardless of what <em>valid</em> token
comes next on the input.  For such states, yacc chooses to go ahead
and reduce the grammar rule <em>without reading the next input
token</em>.  If the next token is bad, yacc will eventually get around to reading it and 
report a syntax error.  It's just a little unusual in that you might
see some of your grammar rules firing immediately prior to the syntax 
error.
</p>

<p>
Usually, the delayed error reporting with defaulted states is harmless
(and there are other reasons for wanting PLY to behave in this way).
However, if you need to turn this behavior off for some reason.  You
can clear the defaulted states table like this:
</p>

<blockquote>
<pre>
parser = yacc.yacc()
parser.defaulted_states = {}
</pre>
</blockquote>

<p>
Disabling defaulted states is not recommended if your grammar makes use
of embedded actions as described in Section 6.11.</p>

<H4><a name="ply_nn32"></a>6.8.5 General comments on error handling</H4>


For normal types of languages, error recovery with error rules and resynchronization characters is probably the most reliable
technique. This is because you can instrument the grammar to catch errors at selected places where it is relatively easy 
to recover and continue parsing.  Panic mode recovery is really only useful in certain specialized applications where you might want
to discard huge portions of the input text to find a valid restart point.

<H3><a name="ply_nn33"></a>6.9 Line Number and Position Tracking</H3>


Position tracking is often a tricky problem when writing compilers.
By default, PLY tracks the line number and position of all tokens.
This information is available using the following functions:

<ul>
<li><tt>p.lineno(num)</tt>. Return the line number for symbol <em>num</em>
<li><tt>p.lexpos(num)</tt>. Return the lexing position for symbol <em>num</em>
</ul>

For example:

<blockquote>
<pre>
def p_expression(p):
    'expression : expression PLUS expression'
    line   = p.lineno(2)        # line number of the PLUS token
    index  = p.lexpos(2)        # Position of the PLUS token
</pre>
</blockquote>

As an optional feature, <tt>yacc.py</tt> can automatically track line
numbers and positions for all of the grammar symbols as well.
However, this extra tracking requires extra processing and can
significantly slow down parsing.  Therefore, it must be enabled by
passing the
<tt>tracking=True</tt> option to <tt>yacc.parse()</tt>.  For example:

<blockquote>
<pre>
yacc.parse(data,tracking=True)
</pre>
</blockquote>

Once enabled, the <tt>lineno()</tt> and <tt>lexpos()</tt> methods work
for all grammar symbols.  In addition, two additional methods can be
used:

<ul>
<li><tt>p.linespan(num)</tt>. Return a tuple (startline,endline) with the starting and ending line number for symbol <em>num</em>.
<li><tt>p.lexspan(num)</tt>. Return a tuple (start,end) with the starting and ending positions for symbol <em>num</em>.
</ul>

For example:

<blockquote>
<pre>
def p_expression(p):
    'expression : expression PLUS expression'
    p.lineno(1)        # Line number of the left expression
    p.lineno(2)        # line number of the PLUS operator
    p.lineno(3)        # line number of the right expression
    ...
    start,end = p.linespan(3)    # Start,end lines of the right expression
    starti,endi = p.lexspan(3)   # Start,end positions of right expression

</pre>
</blockquote>

Note: The <tt>lexspan()</tt> function only returns the range of values up to the start of the last grammar symbol.  

<p>
Although it may be convenient for PLY to track position information on
all grammar symbols, this is often unnecessary.  For example, if you
are merely using line number information in an error message, you can
often just key off of a specific token in the grammar rule.  For
example:

<blockquote>
<pre>
def p_bad_func(p):
    'funccall : fname LPAREN error RPAREN'
    # Line number reported from LPAREN token
    print("Bad function call at line", p.lineno(2))
</pre>
</blockquote>

<p>
Similarly, you may get better parsing performance if you only
selectively propagate line number information where it's needed using
the <tt>p.set_lineno()</tt> method.  For example:

<blockquote>
<pre>
def p_fname(p):
    'fname : ID'
    p[0] = p[1]
    p.set_lineno(0,p.lineno(1))
</pre>
</blockquote>

PLY doesn't retain line number information from rules that have already been
parsed.   If you are building an abstract syntax tree and need to have line numbers,
you should make sure that the line numbers appear in the tree itself.

<H3><a name="ply_nn34"></a>6.10 AST Construction</H3>


<tt>yacc.py</tt> provides no special functions for constructing an
abstract syntax tree.  However, such construction is easy enough to do
on your own. 

<p>A minimal way to construct a tree is to simply create and
propagate a tuple or list in each grammar rule function.   There
are many possible ways to do this, but one example would be something
like this:

<blockquote>
<pre>
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = ('binary-expression',p[2],p[1],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = ('group-expression',p[2])

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ('number-expression',p[1])
</pre>
</blockquote>

<p>
Another approach is to create a set of data structure for different
kinds of abstract syntax tree nodes and assign nodes to <tt>p[0]</tt>
in each rule.  For example:

<blockquote>
<pre>
class Expr: pass

class BinOp(Expr):
    def __init__(self,left,op,right):
        self.type = "binop"
        self.left = left
        self.right = right
        self.op = op

class Number(Expr):
    def __init__(self,value):
        self.type = "number"
        self.value = value

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = BinOp(p[1],p[2],p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])
</pre>
</blockquote>

The advantage to this approach is that it may make it easier to attach more complicated
semantics, type checking, code generation, and other features to the node classes.

<p>
To simplify tree traversal, it may make sense to pick a very generic
tree structure for your parse tree nodes.  For example:

<blockquote>
<pre>
class Node:
    def __init__(self,type,children=None,leaf=None):
         self.type = type
         if children:
              self.children = children
         else:
              self.children = [ ]
         self.leaf = leaf
	 
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

    p[0] = Node("binop", [p[1],p[3]], p[2])
</pre>
</blockquote>

<H3><a name="ply_nn35"></a>6.11 Embedded Actions</H3>


The parsing technique used by yacc only allows actions to be executed at the end of a rule.  For example,
suppose you have a rule like this:

<blockquote>
<pre>
def p_foo(p):
    "foo : A B C D"
    print("Parsed a foo", p[1],p[2],p[3],p[4])
</pre>
</blockquote>

<p>
In this case, the supplied action code only executes after all of the
symbols <tt>A</tt>, <tt>B</tt>, <tt>C</tt>, and <tt>D</tt> have been
parsed. Sometimes, however, it is useful to execute small code
fragments during intermediate stages of parsing.  For example, suppose
you wanted to perform some action immediately after <tt>A</tt> has
been parsed. To do this, write an empty rule like this:

<blockquote>
<pre>
def p_foo(p):
    "foo : A seen_A B C D"
    print("Parsed a foo", p[1],p[3],p[4],p[5])
    print("seen_A returned", p[2])

def p_seen_A(p):
    "seen_A :"
    print("Saw an A = ", p[-1])   # Access grammar symbol to left
    p[0] = some_value            # Assign value to seen_A

</pre>
</blockquote>

<p>
In this example, the empty <tt>seen_A</tt> rule executes immediately
after <tt>A</tt> is shifted onto the parsing stack.  Within this
rule, <tt>p[-1]</tt> refers to the symbol on the stack that appears
immediately to the left of the <tt>seen_A</tt> symbol.  In this case,
it would be the value of <tt>A</tt> in the <tt>foo</tt> rule
immediately above.  Like other rules, a value can be returned from an
embedded action by simply assigning it to <tt>p[0]</tt>

<p>
The use of embedded actions can sometimes introduce extra shift/reduce conflicts.  For example,
this grammar has no conflicts:

<blockquote>
<pre>
def p_foo(p):
    """foo : abcd
           | abcx"""

def p_abcd(p):
    "abcd : A B C D"

def p_abcx(p):
    "abcx : A B C X"
</pre>
</blockquote>

However, if you insert an embedded action into one of the rules like this,

<blockquote>
<pre>
def p_foo(p):
    """foo : abcd
           | abcx"""

def p_abcd(p):
    "abcd : A B C D"

def p_abcx(p):
    "abcx : A B seen_AB C X"

def p_seen_AB(p):
    "seen_AB :"
</pre>
</blockquote>

an extra shift-reduce conflict will be introduced.  This conflict is
caused by the fact that the same symbol <tt>C</tt> appears next in
both the <tt>abcd</tt> and <tt>abcx</tt> rules.  The parser can either
shift the symbol (<tt>abcd</tt> rule) or reduce the empty
rule <tt>seen_AB</tt> (<tt>abcx</tt> rule).

<p>
A common use of embedded rules is to control other aspects of parsing
such as scoping of local variables.  For example, if you were parsing C code, you might
write code like this:

<blockquote>
<pre>
def p_statements_block(p):
    "statements: LBRACE new_scope statements RBRACE"""
    # Action code
    ...
    pop_scope()        # Return to previous scope

def p_new_scope(p):
    "new_scope :"
    # Create a new scope for local variables
    s = new_scope()
    push_scope(s)
    ...
</pre>
</blockquote>

In this case, the embedded action <tt>new_scope</tt> executes
immediately after a <tt>LBRACE</tt> (<tt>{</tt>) symbol is parsed.
This might adjust internal symbol tables and other aspects of the
parser.  Upon completion of the rule <tt>statements_block</tt>, code
might undo the operations performed in the embedded action
(e.g., <tt>pop_scope()</tt>).

<H3><a name="ply_nn36"></a>6.12 Miscellaneous Yacc Notes</H3>


<ul>

<li>By default, <tt>yacc.py</tt> relies on <tt>lex.py</tt> for tokenizing.  However, an alternative tokenizer
can be supplied as follows:

<blockquote>
<pre>
parser = yacc.parse(lexer=x)
</pre>
</blockquote>
in this case, <tt>x</tt> must be a Lexer object that minimally has a <tt>x.token()</tt> method for retrieving the next
token.   If an input string is given to <tt>yacc.parse()</tt>, the lexer must also have an <tt>x.input()</tt> method.

<p>
<li>By default, the yacc generates tables in debugging mode (which produces the parser.out file and other output).
To disable this, use

<blockquote>
<pre>
parser = yacc.yacc(debug=False)
</pre>
</blockquote>

<p>
<li>To change the name of the <tt>parsetab.py</tt> file,  use:

<blockquote>
<pre>
parser = yacc.yacc(tabmodule="foo")
</pre>
</blockquote>

<P>
Normally, the <tt>parsetab.py</tt> file is placed into the same directory as
the module where the parser is defined. If you want it to go somewhere else, you can
given an absolute package name for <tt>tabmodule</tt> instead.  In that case, the 
tables will be written there.
</p>

<p>
<li>To change the directory in which the <tt>parsetab.py</tt> file (and other output files) are written, use:
<blockquote>
<pre>
parser = yacc.yacc(tabmodule="foo",outputdir="somedirectory")
</pre>
</blockquote>

<p>
Note: Be aware that unless the directory specified is also on Python's path (<tt>sys.path</tt>), subsequent
imports of the table file will fail.   As a general rule, it's better to specify a destination using the
<tt>tabmodule</tt> argument instead of directly specifying a directory using the <tt>outputdir</tt> argument.
</p>

<p>
<li>To prevent yacc from generating any kind of parser table file, use:
<blockquote>
<pre>
parser = yacc.yacc(write_tables=False)
</pre>
</blockquote>

Note: If you disable table generation, yacc() will regenerate the parsing tables
each time it runs (which may take awhile depending on how large your grammar is).

<P>
<li>To print copious amounts of debugging during parsing, use:

<blockquote>
<pre>
parser = yacc.parse(debug=True)     
</pre>
</blockquote>

<p>
<li>Since the generation of the LALR tables is relatively expensive, previously generated tables are
cached and reused if possible.  The decision to regenerate the tables is determined by taking an MD5
checksum of all grammar rules and precedence rules.  Only in the event of a mismatch are the tables regenerated.

<p>
It should be noted that table generation is reasonably efficient, even for grammars that involve around a 100 rules
and several hundred states. </li>


<p>
<li>Since LR parsing is driven by tables, the performance of the parser is largely independent of the
size of the grammar.   The biggest bottlenecks will be the lexer and the complexity of the code in your grammar rules.
</li>
</p>

<p>
<li><tt>yacc()</tt> also allows parsers to be defined as classes and as closures (see the section on alternative specification of
lexers).  However, be aware that only one parser may be defined in a single module (source file).  There are various 
error checks and validation steps that may issue confusing error messages if you try to define multiple parsers
in the same source file.
</li>
</p>

<p>
<li>Decorators of production rules have to update the wrapped function's line number.  <tt>wrapper.co_firstlineno = func.__code__.co_firstlineno</tt>:

<blockquote>
<pre>
from functools import wraps
from nodes import Collection


def strict(*types):
    def decorate(func):
        @wraps(func)
        def wrapper(p):
            func(p)
            if not isinstance(p[0], types):
                raise TypeError

        wrapper.co_firstlineno = func.__code__.co_firstlineno
        return wrapper

    return decorate

@strict(Collection)
def p_collection(p):
    """
    collection  : sequence
                | map
    """
    p[0] = p[1]
</pre>
</blockquote>

</li>
</p>


</ul>
</p>


<H2><a name="ply_nn37"></a>7. Multiple Parsers and Lexers</H2>


In advanced parsing applications, you may want to have multiple
parsers and lexers. 

<p>
As a general rules this isn't a problem.   However, to make it work,
you need to carefully make sure everything gets hooked up correctly.
First, make sure you save the objects returned by <tt>lex()</tt> and
<tt>yacc()</tt>.  For example:

<blockquote>
<pre>
lexer  = lex.lex()       # Return lexer object
parser = yacc.yacc()     # Return parser object
</pre>
</blockquote>

Next, when parsing, make sure you give the <tt>parse()</tt> function a reference to the lexer it
should be using.  For example:

<blockquote>
<pre>
parser.parse(text,lexer=lexer)
</pre>
</blockquote>

If you forget to do this, the parser will use the last lexer
created--which is not always what you want.

<p>
Within lexer and parser rule functions, these objects are also
available.  In the lexer, the "lexer" attribute of a token refers to
the lexer object that triggered the rule. For example:

<blockquote>
<pre>
def t_NUMBER(t):
   r'\d+'
   ...
   print(t.lexer)           # Show lexer object
</pre>
</blockquote>

In the parser, the "lexer" and "parser" attributes refer to the lexer
and parser objects respectively.

<blockquote>
<pre>
def p_expr_plus(p):
   'expr : expr PLUS expr'
   ...
   print(p.parser)          # Show parser object
   print(p.lexer)           # Show lexer object
</pre>
</blockquote>

If necessary, arbitrary attributes can be attached to the lexer or parser object.
For example, if you wanted to have different parsing modes, you could attach a mode
attribute to the parser object and look at it later.

<H2><a name="ply_nn38"></a>8. Using Python's Optimized Mode</H2>


Because PLY uses information from doc-strings, parsing and lexing
information must be gathered while running the Python interpreter in
normal mode (i.e., not with the -O or -OO options).  However, if you
specify optimized mode like this:

<blockquote>
<pre>
lex.lex(optimize=1)
yacc.yacc(optimize=1)
</pre>
</blockquote>

then PLY can later be used when Python runs in optimized mode. To make this work,
make sure you first run Python in normal mode.  Once the lexing and parsing tables
have been generated the first time, run Python in optimized mode. PLY will use
the tables without the need for doc strings.

<p>
Beware: running PLY in optimized mode disables a lot of error
checking.  You should only do this when your project has stabilized
and you don't need to do any debugging.   One of the purposes of
optimized mode is to substantially decrease the startup time of
your compiler (by assuming that everything is already properly
specified and works).

<H2><a name="ply_nn44"></a>9. Advanced Debugging</H2>


<p>
Debugging a compiler is typically not an easy task. PLY provides some
advanced diagostic capabilities through the use of Python's
<tt>logging</tt> module.   The next two sections describe this:

<H3><a name="ply_nn45"></a>9.1 Debugging the lex() and yacc() commands</H3>


<p>
Both the <tt>lex()</tt> and <tt>yacc()</tt> commands have a debugging
mode that can be enabled using the <tt>debug</tt> flag.  For example:

<blockquote>
<pre>
lex.lex(debug=True)
yacc.yacc(debug=True)
</pre>
</blockquote>

Normally, the output produced by debugging is routed to either
standard error or, in the case of <tt>yacc()</tt>, to a file
<tt>parser.out</tt>.  This output can be more carefully controlled
by supplying a logging object.  Here is an example that adds
information about where different debugging messages are coming from:

<blockquote>
<pre>
# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

lex.lex(debug=True,debuglog=log)
yacc.yacc(debug=True,debuglog=log)
</pre>
</blockquote>

If you supply a custom logger, the amount of debugging
information produced can be controlled by setting the logging level.
Typically, debugging messages are either issued at the <tt>DEBUG</tt>,
<tt>INFO</tt>, or <tt>WARNING</tt> levels.

<p>
PLY's error messages and warnings are also produced using the logging
interface.  This can be controlled by passing a logging object
using the <tt>errorlog</tt> parameter.

<blockquote>
<pre>
lex.lex(errorlog=log)
yacc.yacc(errorlog=log)
</pre>
</blockquote>

If you want to completely silence warnings, you can either pass in a
logging object with an appropriate filter level or use the <tt>NullLogger</tt>
object defined in either <tt>lex</tt> or <tt>yacc</tt>.  For example:

<blockquote>
<pre>
yacc.yacc(errorlog=yacc.NullLogger())
</pre>
</blockquote>

<H3><a name="ply_nn46"></a>9.2 Run-time Debugging</H3>


<p>
To enable run-time debugging of a parser, use the <tt>debug</tt> option to parse. This
option can either be an integer (which simply turns debugging on or off) or an instance
of a logger object. For example:

<blockquote>
<pre>
log = logging.getLogger()
parser.parse(input,debug=log)
</pre>
</blockquote>

If a logging object is passed, you can use its filtering level to control how much
output gets generated.   The <tt>INFO</tt> level is used to produce information
about rule reductions.  The <tt>DEBUG</tt> level will show information about the
parsing stack, token shifts, and other details.  The <tt>ERROR</tt> level shows information
related to parsing errors.

<p>
For very complicated problems, you should pass in a logging object that
redirects to a file where you can more easily inspect the output after
execution.

<H2><a name="ply_nn39"></a>11. Where to go from here?</H2>


The <tt>examples</tt> directory of the PLY distribution contains several simple examples.   Please consult a
compilers textbook for the theory and underlying implementation details or LR parsing.

</body>
</html>







