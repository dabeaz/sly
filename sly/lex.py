# -----------------------------------------------------------------------------
# sly: lex.py
#
# Copyright (C) 2016 - 2018
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

__version__    = '0.3'
__all__ = ['Lexer', 'LexerStateChange']

import re
import copy

class LexError(Exception):
    '''
    Exception raised if an invalid character is encountered and no default
    error handler function is defined.  The .text attribute of the exception
    contains all remaining untokenized text. The .error_index is the index
    location of the error.
    '''
    def __init__(self, message, text, error_index):
        self.args = (message,)
        self.text = text
        self.error_index = error_index

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

class LexerStateChange(Exception):
    '''
    Exception raised to force a lexing state change
    '''
    def __init__(self, newstate, tok=None):
        self.newstate = newstate
        self.tok = tok

class Token(object):
    '''
    Representation of a single token.
    '''
    __slots__ = ('type', 'value', 'lineno', 'index')
    def __repr__(self):
        return f'Token(type={self.type!r}, value={self.value!r}, lineno={self.lineno}, index={self.index})'

class TokenStr(str):
    @staticmethod
    def __new__(cls, value):
        self = super().__new__(cls, value)
        if isinstance(value, TokenStr):
            self.remap = dict(value.remap)
            self.before = value.before
        else:
            self.remap = { }
            self.before = None
        return self

    # Implementation of TOKEN[value] = NEWTOKEN
    def __setitem__(self, key, value):
        self.remap[key] = value

    # Implementation of del TOKEN[value]
    def __delitem__(self, key):
        del self.remap[key]


class LexerMetaDict(dict):
    '''
    Special dictionary that prohibits duplicate definitions in lexer specifications.
    '''
    def __setitem__(self, key, value):
        if isinstance(value, str):
            value = TokenStr(value)
            
        if key in self and not isinstance(value, property):
            prior = self[key]
            if isinstance(prior, str):
                if callable(value):
                    value.pattern = prior
                    value.remap = getattr(prior, 'remap', None)
                else:
                    pass
                    # raise AttributeError(f'Name {key} redefined')

        super().__setitem__(key, value)

    def __getitem__(self, key):
        if key not in self and key.split('ignore_')[-1].isupper() and key[:1] != '_':
            return key
        else:
            return super().__getitem__(key)

class LexerMeta(type):
    '''
    Metaclass for collecting lexing rules
    '''
    @classmethod
    def __prepare__(meta, name, bases):
        d = LexerMetaDict()

        def _(pattern, *extra):
            patterns = [pattern, *extra]
            def decorate(func):
                pattern = '|'.join(f'({pat})' for pat in patterns )
                if hasattr(func, 'pattern'):
                    func.pattern = pattern + '|' + func.pattern
                else:
                    func.pattern = pattern
                return func
            return decorate

        def before(tok, pattern):
            value = TokenStr(pattern)
            value.before = tok
            return value

        d['_'] = _
        d['before'] = before
        return d

    def __new__(meta, clsname, bases, attributes):
        del attributes['_']
        clsattributes = { key: str(val) if isinstance(val, TokenStr) else val
                       for key, val in attributes.items() }
        cls = super().__new__(meta, clsname, bases, clsattributes)
        # Record the original definition environment
        cls._attributes = attributes
        cls._build()
        return cls

class Lexer(metaclass=LexerMeta):
    # These attributes may be defined in subclasses
    tokens = set()
    literals = set()
    ignore = ''
    reflags = 0
    
    _token_funcs = {}
    _ignored_tokens = set()
    _remapping = {}

    # Internal attributes
    __state_stack = None
    __set_state = None

    @classmethod
    def _collect_rules(cls):
        '''
        Collect all of the rules from class definitions that look like tokens
        '''
        definitions = list(cls._attributes.items())
        rules = []

        # Collect all of the previous rules from base classes
        for base in cls.__bases__:
            if isinstance(base, LexerMeta):
                rules.extend(base._collect_rules())

        existing = dict(rules)

        for key, value in definitions:
            if (key in cls.tokens) or key.startswith('ignore_') or hasattr(value, 'pattern'):
                if key in existing:
                    n = rules.index((key, existing[key]))
                    rules[n] = (key, value)
                    existing[key] = value
                elif isinstance(value, TokenStr) and value.before in existing:
                    n = rules.index((value.before, existing[value.before]))
                    rules.insert(n, (key, value))
                    existing[key] = value
                else:
                    rules.append((key, value))
                    existing[key] = value
            elif isinstance(value, str) and not key.startswith('_') and key not in {'ignore'}:
                raise LexerBuildError(f'{key} does not match a name in tokens')

        return rules

    @classmethod
    def _build(cls):
        '''
        Build the lexer object from the collected tokens and regular expressions.
        Validate the rules to make sure they look sane.
        '''
        if 'tokens' not in vars(cls):
            raise LexerBuildError(f'{cls.__qualname__} class does not define a tokens attribute')

        cls._ignored_tokens = set(cls._ignored_tokens)
        cls._token_funcs = dict(cls._token_funcs)
        cls._remapping = dict(cls._remapping)
        cls._remapping.update({ key: val.remap for key, val in cls._attributes.items()
                           if getattr(val, 'remap', None) })

        # Build a set of all remapped tokens
        remapped_tokens = set()
        for toks in cls._remapping.values():
            remapped_tokens.update(toks.values())

        undefined = remapped_tokens - set(cls.tokens)
        if undefined:
            missing = ', '.join(undefined)
            raise LexerBuildError(f'{missing} not included in token(s)')

        parts = []
        for tokname, value in cls._collect_rules():
            if tokname.startswith('ignore_'):
                tokname = tokname[7:]
                cls._ignored_tokens.add(tokname)

            if isinstance(value, str):
                pattern = value

            elif callable(value):
                cls._token_funcs[tokname] = value
                pattern = getattr(value, 'pattern', None)
                if not pattern:
                    continue

            # Form the regular expression component
            part = f'(?P<{tokname}>{pattern})'

            # Make sure the individual regex compiles properly
            try:
                cpat = re.compile(part, cls.reflags)
            except Exception as e:
                raise PatternError(f'Invalid regex for token {tokname}') from e

            # Verify that the pattern doesn't match the empty string
            if cpat.match(''):
                raise PatternError(f'Regex for token {tokname} matches empty input')

            parts.append(part)

        if not parts:
            return

        # Form the master regular expression
        #previous = ('|' + cls._master_re.pattern) if cls._master_re else ''
        # cls._master_re = re.compile('|'.join(parts) + previous, cls.reflags)
        cls._master_re = re.compile('|'.join(parts), cls.reflags)

        # Verify that that ignore and literals specifiers match the input type
        if not isinstance(cls.ignore, str):
            raise LexerBuildError('ignore specifier must be a string')

        if not all(isinstance(lit, str) for lit in cls.literals):
            raise LexerBuildError('literals must be specified as strings')

    def begin(self, cls):
        '''
        Begin a new lexer state
        '''
        assert isinstance(cls, LexerMeta), "state must be a subclass of Lexer"
        if self.__set_state:
            self.__set_state(cls)
        self.__class__ = cls

    def push_state(self, cls):
        '''
        Push a new lexer state onto the stack
        '''
        if self.__state_stack is None:
            self.__state_stack = []
        self.__state_stack.append(type(self))
        self.begin(cls)

    def pop_state(self):
        '''
        Pop a lexer state from the stack
        '''
        self.begin(self.__state_stack.pop())

    def tokenize(self, text, lineno=1, index=0):
        _ignored_tokens = _master_re = _ignore = _token_funcs = _literals = _remapping = None

        def _set_state(cls):
            nonlocal _ignored_tokens, _master_re, _ignore, _token_funcs, _literals, _remapping
            _ignored_tokens = cls._ignored_tokens
            _master_re = cls._master_re
            _ignore = cls.ignore
            _token_funcs = cls._token_funcs
            _literals = cls.literals
            _remapping = cls._remapping

        self.__set_state = _set_state
        _set_state(type(self))
        self.text = text

        try:
            while True:
                try:
                    if text[index] in _ignore:
                        index += 1
                        continue
                except IndexError:
                    return

                tok = Token()
                tok.lineno = lineno
                tok.index = index
                m = _master_re.match(text, index)
                if m:
                    index = m.end()
                    tok.value = m.group()
                    tok.type = m.lastgroup
                    if tok.type in _remapping:
                        tok.type = _remapping[tok.type].get(tok.value, tok.type)

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
                        tok.type = 'ERROR'
                        tok.value = text[index:]
                        tok = self.error(tok)
                        if tok is not None:
                            yield tok

                        index = self.index
                        lineno = self.lineno

        # Set the final state of the lexer before exiting (even if exception)
        finally:
            self.text = text
            self.index = index
            self.lineno = lineno

    # Default implementations of the error handler. May be changed in subclasses
    def error(self, t):
        raise LexError(f'Illegal character {t.value[0]!r} at index {self.index}', t.value, self.index)
