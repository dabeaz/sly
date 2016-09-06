# -----------------------------------------------------------------------------
# sly: lex.py
#
# Copyright (C) 2016
# David M. Beazley (Dabeaz LLC)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the David Beazley or Dabeaz LLC may be used to
#   endorse or promote products derived from this software without
#  specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# -----------------------------------------------------------------------------

__version__    = '0.0'
__all__ = ['Lexer']

import re
from collections import OrderedDict

class LexError(Exception):
    '''
    Exception raised if an invalid character is encountered and no default
    error handler function is defined.  The .text attribute of the exception
    contains all remaining untokenized text.
    '''
    def __init__(self, message, text):
        self.args = (message,)
        self.text = text

class PatternError(Exception):
    '''
    Exception raised if there's some kind of problem with the specified
    regex patterns in the lexer.
    '''
    pass

class LexerBuildError(Exception):
    '''
    Exception raised if there's some sort of problem building the lexer.
    '''
    pass

class Token(object):
    '''
    Representation of a single token.
    '''
    __slots__ = ('type', 'value', 'lineno', 'index')
    def __repr__(self):
        return 'Token(%s, %r, %d, %d)' % (self.type, self.value, self.lineno, self.index)

class NoDupeDict(OrderedDict):
    '''
    Special dictionary that prohits duplicate definitions.
    '''
    def __setitem__(self, key, value):
        if key in self and not isinstance(value, property):
            raise AttributeError('Name %s redefined' % (key))
        super().__setitem__(key, value)

class LexerMeta(type):
    '''
    Metaclass for collecting lexing rules
    '''
    @classmethod
    def __prepare__(meta, *args, **kwargs):
        d = NoDupeDict()
        def _(pattern):
            def decorate(func):
                if hasattr(func, 'pattern'):
                    if isinstance(pattern, str):
                        func.pattern = ''.join(['(', pattern, ')|(', func.pattern, ')'])
                    else:
                        func.pattern = b''.join([b'(', pattern, b')|(', func.pattern, b')'])
                else:
                    func.pattern = pattern
                return func
            return decorate
        d['_'] = _
        return d

    def __new__(meta, clsname, bases, attributes):
        del attributes['_']
        cls = super().__new__(meta, clsname, bases, attributes)
        cls._build(list(attributes.items()))
        return cls

class Lexer(metaclass=LexerMeta):
    # These attributes may be defined in subclasses
    tokens = set()
    literals = set()
    ignore = None
    reflags = 0

    # These attributes are constructed automatically by the associated metaclass
    _master_re = None
    _token_names = set()
    _literals = set()
    _token_funcs = { }
    _ignored_tokens = set()
    _input_type = str

    @classmethod
    def _collect_rules(cls, definitions):
        '''
        Collect all of the rules from class definitions that look like tokens
        '''
        rules = []
        for key, value in definitions:
            if (key in cls.tokens) or key.startswith('ignore_') or hasattr(value, 'pattern'):
                rules.append((key, value))
        return rules

    @classmethod
    def _build(cls, definitions):
        '''
        Build the lexer object from the collected tokens and regular expressions.
        Validate the rules to make sure they look sane.
        '''
        if 'tokens' not in vars(cls):
            raise LexerBuildError('%s class does not define a tokens attribute' % cls.__qualname__)

        cls._token_names = cls._token_names | set(cls.tokens)
        cls._literals = cls._literals | set(cls.literals)
        cls._ignored_tokens = set(cls._ignored_tokens)
        cls._token_funcs = dict(cls._token_funcs)

        parts = []
        for tokname, value in cls._collect_rules(definitions):
            if tokname.startswith('ignore_'):
                tokname = tokname[7:]
                cls._ignored_tokens.add(tokname)

            if isinstance(value, (str, bytes)):
                pattern = value

            elif callable(value):
                pattern = value.pattern
                cls._token_funcs[tokname] = value

            # Form the regular expression component 
            if isinstance(pattern, str):
                part = '(?P<%s>%s)' % (tokname, pattern)
            else:
                part = b'(?P<%s>%s)' % (tokname.encode('ascii'), pattern)

            # Make sure the individual regex compiles properly
            try:
                cpat = re.compile(part, cls.reflags)
            except Exception as e:
                raise PatternError('Invalid regex for token %s' % tokname) from e

            # Verify that the pattern doesn't match the empty string
            if cpat.match(type(pattern)()):
                raise PatternError('Regex for token %s matches empty input' % tokname)

            parts.append(part)

        # If no parts collected, then no rules to process
        if not parts:
            return

        # Verify that all of the patterns are of the same type
        if not all(type(part) == type(parts[0]) for part in parts):
            raise LexerBuildError('Tokens are specified using both bytes and strings.')

        # Form the master regular expression
        if parts and isinstance(parts[0], bytes):
            previous = (b'|' + cls._master_re.pattern) if cls._master_re else b''
            cls._master_re = re.compile(b'|'.join(parts) + previous, cls.reflags)
            cls._input_type = bytes
        else:
            previous = ('|' + cls._master_re.pattern) if cls._master_re else ''
            cls._master_re = re.compile('|'.join(parts) + previous, cls.reflags)
            cls._input_type = str

        # Verify that that ignore and literals specifiers match the input type
        if cls.ignore is not None and not isinstance(cls.ignore, cls._input_type):
            raise LexerBuildError("ignore specifier type doesn't match token types (%s)" %
                                  cls._input_type.__name__)
        
        if not all(isinstance(lit, cls._input_type) for lit in cls.literals):
            raise LexerBuildError("literals specifier not using same type as tokens (%s)" %
                                  cls._input_type.__name__)


    def tokenize(self, text, lineno=1, index=0):
        # Local copies of frequently used values
        _ignored_tokens = self._ignored_tokens
        _master_re = self._master_re
        _ignore = self.ignore
        _token_funcs = self._token_funcs
        _literals = self._literals

        self.text = text
        try:
            while True:
                try:
                    if text[index] in _ignore:
                        index += 1
                        continue
                except IndexError:
                    if self.eof:
                        text = self.eof()
                        if text is not None:
                            index = 0
                            continue
                    break

                tok = Token()
                tok.lineno = lineno
                tok.index = index
                m = _master_re.match(text, index)
                if m:
                    index = m.end()
                    tok.value = m.group()
                    tok.type = m.lastgroup
                    if tok.type in _token_funcs:
                        self.index = index
                        self.lineno = lineno
                        tok = _token_funcs[tok.type](self, tok)
                        index = self.index
                        lineno = self.lineno
                        if not tok:
                            continue

                    if tok.type in _ignored_tokens:
                        continue

                    yield tok

                else:
                    # No match, see if the character is in literals
                    if text[index] in _literals:
                        tok.value = text[index]
                        tok.type = tok.value
                        index += 1
                        yield tok
                    else:
                        # A lexing error
                        self.index = index
                        self.lineno = lineno
                        self.error(text[index:])
                        index = self.index
                        lineno = self.lineno

        # Set the final state of the lexer before exiting (even if exception)
        finally:
            self.text = text
            self.index = index
            self.lineno = lineno

    # Default implementations of methods that may be subclassed by users
    def error(self, value):
        raise LexError("Illegal character %r at index %d" % (value[0], self.index), value)

    def eof(self):
        pass
