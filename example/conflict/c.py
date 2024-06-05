# -----------------------------------------------------------------------------
# c.py
# Sly version of the grammar extracted from the C 2x standard
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, '../..')

import sly

class CLexer(sly.Lexer):
    tokens = (
        "character-constant",
        "floating-constant",
        "identifier",
        "integer-constant",
        "|=",
        "^=",
        "&=",
        ">>=",
        "<<=",
        "-=",
        "+=",
        "%=",
        "/=",
        "*=",
        "...",
        "::",
        "||",
        "&&",
        "!=",
        "==",
        ">=",
        "<=",
        ">>",
        "<<",
        "--",
        "++",
        "->",
        "string-literal",
        "enumeration-constant",
        "auto",
        "break",
        "case",
        "char",
        "const",
        "continue",
        "default",
        "do",
        "double",
        "else",
        "enum",
        "extern",
        "float",
        "for",
        "goto",
        "if",
        "inline",
        "int",
        "long",
        "register",
        "restrict",
        "return",
        "short",
        "signed",
        "sizeof",
        "static",
        "struct",
        "switch",
        "typedef",
        "union",
        "unsigned",
        "void",
        "volatile",
        "while",
        "_Alignas",
        "_Alignof",
        "_Atomic",
        "_Bool",
        "_Complex",
        "_Decimal128",
        "_Decimal32",
        "_Decimal64",
        "_Generic",
        "_Imaginary",
        "_Noreturn",
        "_Static_assert",
        "_Thread_local",
    )
    literals = {
        ",",
        "=",
        ";",
        ":",
        "^",
        "|",
        ">",
        "<",
        "%",
        "/",
        "!",
        "~",
        "-",
        "&",
        ".",
        ")",
        "(",
        "+",
        "*",
        "}",
        "{",
        "]",
        "[",
        "?",
    }

class CParser(sly.Parser):
    tokens = CLexer.tokens
    debugfile = 'c.out'
    dotfile = 'c.dot'
    start = 'translation_unit'


    @_('AND_expression "&" equality_expression')
    def AND_expression(self, p):
        pass

    @_('equality_expression')
    def AND_expression(self, p):
        pass

    @_('pointer direct_abstract_declarator')
    def abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator')
    def abstract_declarator(self, p):
        pass

    @_('pointer')
    def abstract_declarator(self, p):
        pass

    @_('additive_expression "-" multiplicative_expression')
    def additive_expression(self, p):
        pass

    @_('additive_expression "+" multiplicative_expression')
    def additive_expression(self, p):
        pass

    @_('multiplicative_expression')
    def additive_expression(self, p):
        pass

    @_('_Alignas "(" constant_expression ")"')
    def alignment_specifier(self, p):
        pass

    @_('_Alignas "(" type_name ")"')
    def alignment_specifier(self, p):
        pass

    @_('argument_expression_list "," assignment_expression')
    def argument_expression_list(self, p):
        pass

    @_('assignment_expression')
    def argument_expression_list(self, p):
        pass

    @_('direct_abstract_declarator "[" "*" "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" "*" "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "[" type_qualifier_list static assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" type_qualifier_list static assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "[" static type_qualifier_list assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" static type_qualifier_list assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "[" static assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" static assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "[" type_qualifier_list assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" type_qualifier_list assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "[" assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" assignment_expression "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "[" type_qualifier_list "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" type_qualifier_list "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "[" "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('"[" "]"')
    def array_abstract_declarator(self, p):
        pass

    @_('direct_declarator "[" type_qualifier_list "*" "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" "*" "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" type_qualifier_list static assignment_expression "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" static type_qualifier_list assignment_expression "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" static assignment_expression "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" type_qualifier_list assignment_expression "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" assignment_expression "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" type_qualifier_list "]"')
    def array_declarator(self, p):
        pass

    @_('direct_declarator "[" "]"')
    def array_declarator(self, p):
        pass

    @_('unary_expression assignment_operator assignment_expression')
    def assignment_expression(self, p):
        pass

    @_('conditional_expression')
    def assignment_expression(self, p):
        pass

    @_('"="')
    def assignment_operator(self, p):
        pass

    @_('*=')
    def assignment_operator(self, p):
        pass

    @_('/=')
    def assignment_operator(self, p):
        pass

    @_('%=')
    def assignment_operator(self, p):
        pass

    @_('+=')
    def assignment_operator(self, p):
        pass

    @_('-=')
    def assignment_operator(self, p):
        pass

    @_('<<=')
    def assignment_operator(self, p):
        pass

    @_('>>=')
    def assignment_operator(self, p):
        pass

    @_('&=')
    def assignment_operator(self, p):
        pass

    @_('^=')
    def assignment_operator(self, p):
        pass

    @_('|=')
    def assignment_operator(self, p):
        pass

    @_('_Atomic "(" type_name ")"')
    def atomic_type_specifier(self, p):
        pass

    @_('attribute_token attribute_argument_clause')
    def attribute(self, p):
        pass

    @_('attribute_token')
    def attribute(self, p):
        pass

    @_('"(" balanced_token_sequence ")"')
    def attribute_argument_clause(self, p):
        pass

    @_('"(" ")"')
    def attribute_argument_clause(self, p):
        pass

    @_('attribute_specifier_sequence ";"')
    def attribute_declaration(self, p):
        pass

    @_('attribute_list "," attribute')
    def attribute_list(self, p):
        pass

    @_('attribute_list ","')
    def attribute_list(self, p):
        pass

    @_('attribute')
    def attribute_list(self, p):
        pass

    @_('')
    def attribute_list(self, p):
        pass

    @_('identifier')
    def attribute_prefix(self, p):
        pass

    @_('attribute_prefix :: identifier')
    def attribute_prefixed_token(self, p):
        pass

    @_('"[" "[" attribute_list "]" "]"')
    def attribute_specifier(self, p):
        pass

    @_('attribute_specifier_sequence attribute_specifier')
    def attribute_specifier_sequence(self, p):
        pass

    @_('attribute_specifier')
    def attribute_specifier_sequence(self, p):
        pass

    @_('attribute_prefixed_token')
    def attribute_token(self, p):
        pass

    @_('standard_attribute')
    def attribute_token(self, p):
        pass

    @_('string-literal')
    def balanced_token(self, p):
        pass

    @_('character-constant')
    def balanced_token(self, p):
        pass

    @_('floating-constant')
    def balanced_token(self, p):
        pass

    @_('integer-constant')
    def balanced_token(self, p):
        pass

    @_('identifier')
    def balanced_token(self, p):
        pass

    @_('","')
    def balanced_token(self, p):
        pass

    @_('|=')
    def balanced_token(self, p):
        pass

    @_('^=')
    def balanced_token(self, p):
        pass

    @_('&=')
    def balanced_token(self, p):
        pass

    @_('>>=')
    def balanced_token(self, p):
        pass

    @_('<<=')
    def balanced_token(self, p):
        pass

    @_('-=')
    def balanced_token(self, p):
        pass

    @_('+=')
    def balanced_token(self, p):
        pass

    @_('%=')
    def balanced_token(self, p):
        pass

    @_('/=')
    def balanced_token(self, p):
        pass

    @_('*=')
    def balanced_token(self, p):
        pass

    @_('"="')
    def balanced_token(self, p):
        pass

    @_('...')
    def balanced_token(self, p):
        pass

    @_('";"')
    def balanced_token(self, p):
        pass

    @_('::')
    def balanced_token(self, p):
        pass

    @_('":"')
    def balanced_token(self, p):
        pass

    @_('"?"')
    def balanced_token(self, p):
        pass

    @_('||')
    def balanced_token(self, p):
        pass

    @_('&&')
    def balanced_token(self, p):
        pass

    @_('"|"')
    def balanced_token(self, p):
        pass

    @_('"^"')
    def balanced_token(self, p):
        pass

    @_('!=')
    def balanced_token(self, p):
        pass

    @_('==')
    def balanced_token(self, p):
        pass

    @_('>=')
    def balanced_token(self, p):
        pass

    @_('<=')
    def balanced_token(self, p):
        pass

    @_('">"')
    def balanced_token(self, p):
        pass

    @_('"<"')
    def balanced_token(self, p):
        pass

    @_('>>')
    def balanced_token(self, p):
        pass

    @_('<<')
    def balanced_token(self, p):
        pass

    @_('"%"')
    def balanced_token(self, p):
        pass

    @_('"/"')
    def balanced_token(self, p):
        pass

    @_('"!"')
    def balanced_token(self, p):
        pass

    @_('"~"')
    def balanced_token(self, p):
        pass

    @_('"-"')
    def balanced_token(self, p):
        pass

    @_('"+"')
    def balanced_token(self, p):
        pass

    @_('"*"')
    def balanced_token(self, p):
        pass

    @_('"&"')
    def balanced_token(self, p):
        pass

    @_('--')
    def balanced_token(self, p):
        pass

    @_('++')
    def balanced_token(self, p):
        pass

    @_('->')
    def balanced_token(self, p):
        pass

    @_('"."')
    def balanced_token(self, p):
        pass

    @_('_Thread_local')
    def balanced_token(self, p):
        pass

    @_('_Static_assert')
    def balanced_token(self, p):
        pass

    @_('_Noreturn')
    def balanced_token(self, p):
        pass

    @_('_Imaginary')
    def balanced_token(self, p):
        pass

    @_('_Generic')
    def balanced_token(self, p):
        pass

    @_('_Decimal64')
    def balanced_token(self, p):
        pass

    @_('_Decimal32')
    def balanced_token(self, p):
        pass

    @_('_Decimal128')
    def balanced_token(self, p):
        pass

    @_('_Complex')
    def balanced_token(self, p):
        pass

    @_('_Bool')
    def balanced_token(self, p):
        pass

    @_('_Atomic')
    def balanced_token(self, p):
        pass

    @_('_Alignof')
    def balanced_token(self, p):
        pass

    @_('_Alignas')
    def balanced_token(self, p):
        pass

    @_('while')
    def balanced_token(self, p):
        pass

    @_('volatile')
    def balanced_token(self, p):
        pass

    @_('void')
    def balanced_token(self, p):
        pass

    @_('unsigned')
    def balanced_token(self, p):
        pass

    @_('union')
    def balanced_token(self, p):
        pass

    @_('typedef')
    def balanced_token(self, p):
        pass

    @_('switch')
    def balanced_token(self, p):
        pass

    @_('struct')
    def balanced_token(self, p):
        pass

    @_('static')
    def balanced_token(self, p):
        pass

    @_('sizeof')
    def balanced_token(self, p):
        pass

    @_('signed')
    def balanced_token(self, p):
        pass

    @_('short')
    def balanced_token(self, p):
        pass

    @_('return')
    def balanced_token(self, p):
        pass

    @_('restrict')
    def balanced_token(self, p):
        pass

    @_('register')
    def balanced_token(self, p):
        pass

    @_('long')
    def balanced_token(self, p):
        pass

    @_('int')
    def balanced_token(self, p):
        pass

    @_('inline')
    def balanced_token(self, p):
        pass

    @_('if')
    def balanced_token(self, p):
        pass

    @_('goto')
    def balanced_token(self, p):
        pass

    @_('for')
    def balanced_token(self, p):
        pass

    @_('float')
    def balanced_token(self, p):
        pass

    @_('extern')
    def balanced_token(self, p):
        pass

    @_('enum')
    def balanced_token(self, p):
        pass

    @_('else')
    def balanced_token(self, p):
        pass

    @_('double')
    def balanced_token(self, p):
        pass

    @_('do')
    def balanced_token(self, p):
        pass

    @_('default')
    def balanced_token(self, p):
        pass

    @_('continue')
    def balanced_token(self, p):
        pass

    @_('const')
    def balanced_token(self, p):
        pass

    @_('char')
    def balanced_token(self, p):
        pass

    @_('case')
    def balanced_token(self, p):
        pass

    @_('break')
    def balanced_token(self, p):
        pass

    @_('auto')
    def balanced_token(self, p):
        pass

    @_('"{" balanced_token_sequence "}"')
    def balanced_token(self, p):
        pass

    @_('"{" "}"')
    def balanced_token(self, p):
        pass

    @_('"[" balanced_token_sequence "]"')
    def balanced_token(self, p):
        pass

    @_('"[" "]"')
    def balanced_token(self, p):
        pass

    @_('"(" balanced_token_sequence ")"')
    def balanced_token(self, p):
        pass

    @_('"(" ")"')
    def balanced_token(self, p):
        pass

    @_('balanced_token_sequence balanced_token')
    def balanced_token_sequence(self, p):
        pass

    @_('balanced_token')
    def balanced_token_sequence(self, p):
        pass

    @_('label')
    def block_item(self, p):
        pass

    @_('unlabeled_statement')
    def block_item(self, p):
        pass

    @_('declaration')
    def block_item(self, p):
        pass

    @_('block_item_list block_item')
    def block_item_list(self, p):
        pass

    @_('block_item')
    def block_item_list(self, p):
        pass

    @_('"(" type_name ")" cast_expression')
    def cast_expression(self, p):
        pass

    @_('unary_expression')
    def cast_expression(self, p):
        pass

    @_('"{" block_item_list "}"')
    def compound_statement(self, p):
        pass

    @_('"{" "}"')
    def compound_statement(self, p):
        pass

    @_('logical_OR_expression "?" expression ":" conditional_expression')
    def conditional_expression(self, p):
        pass

    @_('logical_OR_expression')
    def conditional_expression(self, p):
        pass

    @_('conditional_expression')
    def constant_expression(self, p):
        pass

    @_('static_assert_declaration attribute_declaration')
    def declaration(self, p):
        pass

    @_('attribute_specifier_sequence declaration_specifiers init_declarator_list ";"')
    def declaration(self, p):
        pass

    @_('declaration_specifiers init_declarator_list ";"')
    def declaration(self, p):
        pass

    @_('declaration_specifiers ";"')
    def declaration(self, p):
        pass

    @_('function_specifier')
    def declaration_specifier(self, p):
        pass

    @_('type_specifier_qualifier')
    def declaration_specifier(self, p):
        pass

    @_('storage_class_specifier')
    def declaration_specifier(self, p):
        pass

    @_('declaration_specifier declaration_specifiers')
    def declaration_specifiers(self, p):
        pass

    @_('declaration_specifier attribute_specifier_sequence')
    def declaration_specifiers(self, p):
        pass

    @_('declaration_specifier')
    def declaration_specifiers(self, p):
        pass

    @_('pointer direct_declarator')
    def declarator(self, p):
        pass

    @_('direct_declarator')
    def declarator(self, p):
        pass

    @_('designator_list "="')
    def designation(self, p):
        pass

    @_('"." identifier')
    def designator(self, p):
        pass

    @_('"[" constant_expression "]"')
    def designator(self, p):
        pass

    @_('designator_list designator')
    def designator_list(self, p):
        pass

    @_('designator')
    def designator_list(self, p):
        pass

    @_('function_abstract_declarator attribute_specifier_sequence')
    def direct_abstract_declarator(self, p):
        pass

    @_('function_abstract_declarator')
    def direct_abstract_declarator(self, p):
        pass

    @_('array_abstract_declarator attribute_specifier_sequence')
    def direct_abstract_declarator(self, p):
        pass

    @_('array_abstract_declarator')
    def direct_abstract_declarator(self, p):
        pass

    @_('"(" abstract_declarator ")"')
    def direct_abstract_declarator(self, p):
        pass

    @_('function_declarator attribute_specifier_sequence')
    def direct_declarator(self, p):
        pass

    @_('function_declarator')
    def direct_declarator(self, p):
        pass

    @_('array_declarator attribute_specifier_sequence')
    def direct_declarator(self, p):
        pass

    @_('array_declarator')
    def direct_declarator(self, p):
        pass

    @_('"(" declarator ")"')
    def direct_declarator(self, p):
        pass

    @_('identifier attribute_specifier_sequence')
    def direct_declarator(self, p):
        pass

    @_('identifier')
    def direct_declarator(self, p):
        pass

    @_('enum identifier')
    def enum_specifier(self, p):
        pass

    @_('enum attribute_specifier_sequence identifier "{" enumerator_list "," "}"')
    def enum_specifier(self, p):
        pass

    @_('enum identifier "{" enumerator_list "," "}"')
    def enum_specifier(self, p):
        pass

    @_('enum attribute_specifier_sequence "{" enumerator_list "," "}"')
    def enum_specifier(self, p):
        pass

    @_('enum "{" enumerator_list "," "}"')
    def enum_specifier(self, p):
        pass

    @_('enum attribute_specifier_sequence identifier "{" enumerator_list "}"')
    def enum_specifier(self, p):
        pass

    @_('enum identifier "{" enumerator_list "}"')
    def enum_specifier(self, p):
        pass

    @_('enum attribute_specifier_sequence "{" enumerator_list "}"')
    def enum_specifier(self, p):
        pass

    @_('enum "{" enumerator_list "}"')
    def enum_specifier(self, p):
        pass

    @_('enumeration-constant attribute_specifier_sequence "=" constant_expression')
    def enumerator(self, p):
        pass

    @_('enumeration-constant "=" constant_expression')
    def enumerator(self, p):
        pass

    @_('enumeration-constant attribute_specifier_sequence')
    def enumerator(self, p):
        pass

    @_('enumeration-constant')
    def enumerator(self, p):
        pass

    @_('enumerator_list "," enumerator')
    def enumerator_list(self, p):
        pass

    @_('enumerator')
    def enumerator_list(self, p):
        pass

    @_('equality_expression != relational_expression')
    def equality_expression(self, p):
        pass

    @_('equality_expression == relational_expression')
    def equality_expression(self, p):
        pass

    @_('relational_expression')
    def equality_expression(self, p):
        pass

    @_('expression "," assignment_expression')
    def expression(self, p):
        pass

    @_('assignment_expression')
    def expression(self, p):
        pass

    @_('attribute_specifier_sequence expression ";"')
    def expression_statement(self, p):
        pass

    @_('expression ";"')
    def expression_statement(self, p):
        pass

    @_('";"')
    def expression_statement(self, p):
        pass

    @_('declaration')
    def external_declaration(self, p):
        pass

    @_('function_definition')
    def external_declaration(self, p):
        pass

    @_('direct_abstract_declarator "(" parameter_type_list ")"')
    def function_abstract_declarator(self, p):
        pass

    @_('"(" parameter_type_list ")"')
    def function_abstract_declarator(self, p):
        pass

    @_('direct_abstract_declarator "(" ")"')
    def function_abstract_declarator(self, p):
        pass

    @_('"(" ")"')
    def function_abstract_declarator(self, p):
        pass

    @_('compound_statement')
    def function_body(self, p):
        pass

    @_('direct_declarator "(" parameter_type_list ")"')
    def function_declarator(self, p):
        pass

    @_('direct_declarator "(" ")"')
    def function_declarator(self, p):
        pass

    @_('attribute_specifier_sequence declaration_specifiers declarator function_body')
    def function_definition(self, p):
        pass

    @_('declaration_specifiers declarator function_body')
    def function_definition(self, p):
        pass

    @_('_Noreturn')
    def function_specifier(self, p):
        pass

    @_('inline')
    def function_specifier(self, p):
        pass

    @_('generic_assoc_list "," generic_association')
    def generic_assoc_list(self, p):
        pass

    @_('generic_association')
    def generic_assoc_list(self, p):
        pass

    @_('default ":" assignment_expression')
    def generic_association(self, p):
        pass

    @_('type_name ":" assignment_expression')
    def generic_association(self, p):
        pass

    @_('_Generic "(" assignment_expression "," generic_assoc_list ")"')
    def generic_selection(self, p):
        pass

    @_('inclusive_OR_expression "|" exclusive_OR_expression')
    def inclusive_OR_expression(self, p):
        pass

    @_('exclusive_OR_expression')
    def inclusive_OR_expression(self, p):
        pass

    @_('exclusive_OR_expression "^" AND_expression')
    def exclusive_OR_expression(self, p):
        pass

    @_('AND_expression')
    def exclusive_OR_expression(self, p):
        pass

    @_('declarator "=" initializer')
    def init_declarator(self, p):
        pass

    @_('declarator')
    def init_declarator(self, p):
        pass

    @_('init_declarator_list "," init_declarator')
    def init_declarator_list(self, p):
        pass

    @_('init_declarator')
    def init_declarator_list(self, p):
        pass

    @_('"{" initializer_list "," "}"')
    def initializer(self, p):
        pass

    @_('"{" initializer_list "}"')
    def initializer(self, p):
        pass

    @_('assignment_expression')
    def initializer(self, p):
        pass

    @_('initializer_list "," designation initializer')
    def initializer_list(self, p):
        pass

    @_('initializer_list "," initializer')
    def initializer_list(self, p):
        pass

    @_('designation initializer')
    def initializer_list(self, p):
        pass

    @_('initializer')
    def initializer_list(self, p):
        pass

    @_('for "(" declaration expression ";" expression ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" declaration ";" expression ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" declaration expression ";" ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" declaration ";" ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" expression ";" expression ";" expression ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" ";" expression ";" expression ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" expression ";" ";" expression ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" ";" ";" expression ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" expression ";" expression ";" ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" ";" expression ";" ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" expression ";" ";" ")" statement')
    def iteration_statement(self, p):
        pass

    @_('for "(" ";" ";" ")" statement')
    def iteration_statement(self, p):
        pass

    @_('do statement while "(" expression ")" ";"')
    def iteration_statement(self, p):
        pass

    @_('while "(" expression ")" statement')
    def iteration_statement(self, p):
        pass

    @_('return expression ";"')
    def jump_statement(self, p):
        pass

    @_('return ";"')
    def jump_statement(self, p):
        pass

    @_('break ";"')
    def jump_statement(self, p):
        pass

    @_('continue ";"')
    def jump_statement(self, p):
        pass

    @_('goto identifier ";"')
    def jump_statement(self, p):
        pass

    @_('attribute_specifier_sequence default ":"')
    def label(self, p):
        pass

    @_('default ":"')
    def label(self, p):
        pass

    @_('attribute_specifier_sequence case constant_expression ":"')
    def label(self, p):
        pass

    @_('case constant_expression ":"')
    def label(self, p):
        pass

    @_('attribute_specifier_sequence identifier ":"')
    def label(self, p):
        pass

    @_('identifier ":"')
    def label(self, p):
        pass

    @_('label statement')
    def labeled_statement(self, p):
        pass

    @_('logical_AND_expression && inclusive_OR_expression')
    def logical_AND_expression(self, p):
        pass

    @_('inclusive_OR_expression')
    def logical_AND_expression(self, p):
        pass

    @_('logical_OR_expression || logical_AND_expression')
    def logical_OR_expression(self, p):
        pass

    @_('logical_AND_expression')
    def logical_OR_expression(self, p):
        pass

    @_('static_assert_declaration')
    def member_declaration(self, p):
        pass

    @_('attribute_specifier_sequence specifier_qualifier_list member_declarator_list ";"')
    def member_declaration(self, p):
        pass

    @_('specifier_qualifier_list member_declarator_list ";"')
    def member_declaration(self, p):
        pass

    @_('attribute_specifier_sequence specifier_qualifier_list ";"')
    def member_declaration(self, p):
        pass

    @_('specifier_qualifier_list ";"')
    def member_declaration(self, p):
        pass

    @_('member_declaration_list member_declaration')
    def member_declaration_list(self, p):
        pass

    @_('member_declaration')
    def member_declaration_list(self, p):
        pass

    @_('declarator ":" constant_expression')
    def member_declarator(self, p):
        pass

    @_('":" constant_expression')
    def member_declarator(self, p):
        pass

    @_('declarator')
    def member_declarator(self, p):
        pass

    @_('member_declarator_list "," member_declarator')
    def member_declarator_list(self, p):
        pass

    @_('member_declarator')
    def member_declarator_list(self, p):
        pass

    @_('multiplicative_expression "%" cast_expression')
    def multiplicative_expression(self, p):
        pass

    @_('multiplicative_expression "/" cast_expression')
    def multiplicative_expression(self, p):
        pass

    @_('multiplicative_expression "*" cast_expression')
    def multiplicative_expression(self, p):
        pass

    @_('cast_expression')
    def multiplicative_expression(self, p):
        pass

    @_('attribute_specifier_sequence declaration_specifiers abstract_declarator')
    def parameter_declaration(self, p):
        pass

    @_('declaration_specifiers abstract_declarator')
    def parameter_declaration(self, p):
        pass

    @_('attribute_specifier_sequence declaration_specifiers')
    def parameter_declaration(self, p):
        pass

    @_('declaration_specifiers')
    def parameter_declaration(self, p):
        pass

    @_('attribute_specifier_sequence declaration_specifiers declarator')
    def parameter_declaration(self, p):
        pass

    @_('declaration_specifiers declarator')
    def parameter_declaration(self, p):
        pass

    @_('parameter_list "," parameter_declaration')
    def parameter_list(self, p):
        pass

    @_('parameter_declaration')
    def parameter_list(self, p):
        pass

    @_('parameter_list "," ...')
    def parameter_type_list(self, p):
        pass

    @_('parameter_list')
    def parameter_type_list(self, p):
        pass

    @_('"*" attribute_specifier_sequence type_qualifier_list pointer')
    def pointer(self, p):
        pass

    @_('"*" type_qualifier_list pointer')
    def pointer(self, p):
        pass

    @_('"*" attribute_specifier_sequence pointer')
    def pointer(self, p):
        pass

    @_('"*" pointer')
    def pointer(self, p):
        pass

    @_('"*" attribute_specifier_sequence type_qualifier_list')
    def pointer(self, p):
        pass

    @_('"*" type_qualifier_list')
    def pointer(self, p):
        pass

    @_('"*" attribute_specifier_sequence')
    def pointer(self, p):
        pass

    @_('"*"')
    def pointer(self, p):
        pass

    @_('"(" type_name ")" "{" initializer_list "," "}"')
    def postfix_expression(self, p):
        pass

    @_('"(" type_name ")" "{" initializer_list "}"')
    def postfix_expression(self, p):
        pass

    @_('postfix_expression --')
    def postfix_expression(self, p):
        pass

    @_('postfix_expression ++')
    def postfix_expression(self, p):
        pass

    @_('postfix_expression -> identifier')
    def postfix_expression(self, p):
        pass

    @_('postfix_expression "." identifier')
    def postfix_expression(self, p):
        pass

    @_('postfix_expression "(" argument_expression_list ")"')
    def postfix_expression(self, p):
        pass

    @_('postfix_expression "(" ")"')
    def postfix_expression(self, p):
        pass

    @_('postfix_expression "[" expression "]"')
    def postfix_expression(self, p):
        pass

    @_('primary_expression')
    def postfix_expression(self, p):
        pass

    @_('generic_selection')
    def primary_expression(self, p):
        pass

    @_('"(" expression ")"')
    def primary_expression(self, p):
        pass

    @_('string-literal')
    def primary_expression(self, p):
        pass

    @_('enumeration-constant')
    def primary_expression(self, p):
        pass

    @_('character-constant')
    def primary_expression(self, p):
        pass

    @_('floating-constant')
    def primary_expression(self, p):
        pass

    @_('integer-constant')
    def primary_expression(self, p):
        pass

    @_('identifier')
    def primary_expression(self, p):
        pass

    @_('relational_expression >= shift_expression')
    def relational_expression(self, p):
        pass

    @_('relational_expression <= shift_expression')
    def relational_expression(self, p):
        pass

    @_('relational_expression ">" shift_expression')
    def relational_expression(self, p):
        pass

    @_('relational_expression "<" shift_expression')
    def relational_expression(self, p):
        pass

    @_('shift_expression')
    def relational_expression(self, p):
        pass

    @_('switch "(" expression ")" statement')
    def selection_statement(self, p):
        pass

    @_('if "(" expression ")" statement else statement')
    def selection_statement(self, p):
        pass

    @_('if "(" expression ")" statement')
    def selection_statement(self, p):
        pass

    @_('shift_expression >> additive_expression')
    def shift_expression(self, p):
        pass

    @_('shift_expression << additive_expression')
    def shift_expression(self, p):
        pass

    @_('additive_expression')
    def shift_expression(self, p):
        pass

    @_('type_specifier_qualifier specifier_qualifier_list')
    def specifier_qualifier_list(self, p):
        pass

    @_('type_specifier_qualifier attribute_specifier_sequence')
    def specifier_qualifier_list(self, p):
        pass

    @_('type_specifier_qualifier')
    def specifier_qualifier_list(self, p):
        pass

    @_('identifier')
    def standard_attribute(self, p):
        pass

    @_('unlabeled_statement')
    def statement(self, p):
        pass

    @_('labeled_statement')
    def statement(self, p):
        pass

    @_('_Static_assert "(" constant_expression ")" ";"')
    def static_assert_declaration(self, p):
        pass

    @_('_Static_assert "(" constant_expression "," string-literal ")" ";"')
    def static_assert_declaration(self, p):
        pass

    @_('register')
    def storage_class_specifier(self, p):
        pass

    @_('auto')
    def storage_class_specifier(self, p):
        pass

    @_('_Thread_local')
    def storage_class_specifier(self, p):
        pass

    @_('static')
    def storage_class_specifier(self, p):
        pass

    @_('extern')
    def storage_class_specifier(self, p):
        pass

    @_('typedef')
    def storage_class_specifier(self, p):
        pass

    @_('union')
    def struct_or_union(self, p):
        pass

    @_('struct')
    def struct_or_union(self, p):
        pass

    @_('struct_or_union attribute_specifier_sequence identifier')
    def struct_or_union_specifier(self, p):
        pass

    @_('struct_or_union identifier')
    def struct_or_union_specifier(self, p):
        pass

    @_('struct_or_union attribute_specifier_sequence identifier "{" member_declaration_list "}"')
    def struct_or_union_specifier(self, p):
        pass

    @_('struct_or_union identifier "{" member_declaration_list "}"')
    def struct_or_union_specifier(self, p):
        pass

    @_('struct_or_union attribute_specifier_sequence "{" member_declaration_list "}"')
    def struct_or_union_specifier(self, p):
        pass

    @_('struct_or_union "{" member_declaration_list "}"')
    def struct_or_union_specifier(self, p):
        pass

    @_('translation_unit external_declaration')
    def translation_unit(self, p):
        pass

    @_('external_declaration')
    def translation_unit(self, p):
        pass

    @_('specifier_qualifier_list abstract_declarator')
    def type_name(self, p):
        pass

    @_('specifier_qualifier_list')
    def type_name(self, p):
        pass

    @_('_Atomic')
    def type_qualifier(self, p):
        pass

    @_('volatile')
    def type_qualifier(self, p):
        pass

    @_('restrict')
    def type_qualifier(self, p):
        pass

    @_('const')
    def type_qualifier(self, p):
        pass

    @_('type_qualifier_list type_qualifier')
    def type_qualifier_list(self, p):
        pass

    @_('type_qualifier')
    def type_qualifier_list(self, p):
        pass

    @_('typedef_name')
    def type_specifier(self, p):
        pass

    @_('enum_specifier')
    def type_specifier(self, p):
        pass

    @_('struct_or_union_specifier')
    def type_specifier(self, p):
        pass

    @_('atomic_type_specifier')
    def type_specifier(self, p):
        pass

    @_('_Decimal128')
    def type_specifier(self, p):
        pass

    @_('_Decimal64')
    def type_specifier(self, p):
        pass

    @_('_Decimal32')
    def type_specifier(self, p):
        pass

    @_('_Complex')
    def type_specifier(self, p):
        pass

    @_('_Bool')
    def type_specifier(self, p):
        pass

    @_('unsigned')
    def type_specifier(self, p):
        pass

    @_('signed')
    def type_specifier(self, p):
        pass

    @_('double')
    def type_specifier(self, p):
        pass

    @_('float')
    def type_specifier(self, p):
        pass

    @_('long')
    def type_specifier(self, p):
        pass

    @_('int')
    def type_specifier(self, p):
        pass

    @_('short')
    def type_specifier(self, p):
        pass

    @_('char')
    def type_specifier(self, p):
        pass

    @_('void')
    def type_specifier(self, p):
        pass

    @_('alignment_specifier')
    def type_specifier_qualifier(self, p):
        pass

    @_('type_qualifier')
    def type_specifier_qualifier(self, p):
        pass

    @_('type_specifier')
    def type_specifier_qualifier(self, p):
        pass

    @_('identifier')
    def typedef_name(self, p):
        pass

    @_('_Alignof "(" type_name ")"')
    def unary_expression(self, p):
        pass

    @_('sizeof "(" type_name ")"')
    def unary_expression(self, p):
        pass

    @_('sizeof unary_expression')
    def unary_expression(self, p):
        pass

    @_('unary_operator cast_expression')
    def unary_expression(self, p):
        pass

    @_('-- unary_expression')
    def unary_expression(self, p):
        pass

    @_('++ unary_expression')
    def unary_expression(self, p):
        pass

    @_('postfix_expression')
    def unary_expression(self, p):
        pass

    @_('"&"')
    def unary_operator(self, p):
        pass

    @_('"*"')
    def unary_operator(self, p):
        pass

    @_('"+"')
    def unary_operator(self, p):
        pass

    @_('"-"')
    def unary_operator(self, p):
        pass

    @_('"~"')
    def unary_operator(self, p):
        pass

    @_('"!"')
    def unary_operator(self, p):
        pass

    @_('attribute_specifier_sequence jump_statement')
    def unlabeled_statement(self, p):
        pass

    @_('jump_statement')
    def unlabeled_statement(self, p):
        pass

    @_('attribute_specifier_sequence iteration_statement')
    def unlabeled_statement(self, p):
        pass

    @_('iteration_statement')
    def unlabeled_statement(self, p):
        pass

    @_('attribute_specifier_sequence selection_statement')
    def unlabeled_statement(self, p):
        pass

    @_('selection_statement')
    def unlabeled_statement(self, p):
        pass

    @_('attribute_specifier_sequence compound_statement')
    def unlabeled_statement(self, p):
        pass

    @_('compound_statement')
    def unlabeled_statement(self, p):
        pass

    @_('expression_statement')
    def unlabeled_statement(self, p):
        pass

if __name__ == '__main__':
    lexer = CLexer()
    parser = CParser()
