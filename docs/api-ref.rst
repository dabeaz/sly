SLY (Sly Lex Yacc) API reference
================================

``sly.yacc``
------------

.. automodule:: sly.yacc
    :members:
    :show-inheritance:
    :inherited-members:

Note: All above members are accessible in root ``sly`` package.


.. autoexception:: sly.yacc.YaccError
    :show-inheritance:

.. autoclass:: sly.yacc.SlyLogger
    :members:

    .. method:: warning(msg, *args, **kwargs)
    .. method:: info(msg, *args, **kwargs)
    .. method:: debug(msg, *args, **kwargs)
    .. method:: error(msg, *args, **kwargs)
    .. method:: critical(msg, *args, **kwargs)

        log something at the given level.

        :param msg: the message to log
        :param args: formatting arguments
        :param kwargs: by default, these are unused

        Note: old-style formatting is used

.. autoclass:: sly.yacc.YaccSymbol
    :members:
    :show-inheritance:
    :inherited-members:

.. autoclass:: sly.yacc.YaccProduction
    :members:
    :show-inheritance:
    :inherited-members:

.. autoclass:: sly.yacc.Production
    :members:
    :show-inheritance:
    :inherited-members:

.. autoclass:: sly.yacc.LRItem
    :members:
    :show-inheritance:
    :inherited-members:

.. autofunction:: sly.yacc.rightmost_terminal

.. autoexception:: sly.yacc.GrammarError
    :show-inheritance:

.. autoclass:: sly.yacc.Grammar
    :members:
    :show-inheritance:
    :inherited-members:

.. autofunction:: sly.yacc.digraph

.. autoexception:: sly.yacc.LALRError
    :show-inheritance:

.. autoclass:: sly.yacc.LRTable
    :members: write
    :show-inheritance:
    :inherited-members:

``sly.lex``
-----------

.. automodule:: sly.lex
    :members:
    :show-inheritance:
    :inherited-members:

Note: All above members are accessible in root ``sly`` package.

.. autoexception:: sly.lex.LexError
    :show-inheritance:

.. autoexception:: sly.lex.PatternError
    :show-inheritance:

.. autoexception:: sly.lex.LexerBuildError

.. autoclass:: sly.lex.Token
    :members:
    :show-inheritance:
    :inherited-members:

.. autoclass:: sly.lex.TokenStr
    :members:
    :show-inheritance:
    :inherited-members:


``sly.ast``
-----------

.. autoclass:: sly.ast.AST
    :members:
    :show-inheritance:
    :inherited-members:

``sly.docparse``
----------------

.. automodule:: sly.docparse
    :members:
    :show-inheritance:
