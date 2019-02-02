try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

tests_require = ['pytest']

setup(name = "sly",
            description="SLY - Sly Lex Yacc",
            long_description = """
SLY is an implementation of lex and yacc for Python 3.
""",
            license="""BSD""",
            version = "0.4",
            author = "David Beazley",
            author_email = "dave@dabeaz.com",
            maintainer = "David Beazley",
            maintainer_email = "dave@dabeaz.com",
            url = "https://github.com/dabeaz/sly",
            packages = ['sly'],
            python_requires = ">=3.6",
            tests_require = tests_require,
            extras_require = {
                'test': tests_require,
              },
            classifiers = [
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7',
              ]
            )
