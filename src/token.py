########################################
# CONSTANTS
########################################

import string

DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

########################################
# TOKENS
########################################

TT_INT          = 'INT'
TT_FLOAT        = 'FLOAT'
TT_STRING       = 'STRING'
TT_IDENTIFIER   = 'IDENTIFIER'
TT_KEYWORD      = 'KEYWORD'
TT_PLUS         = 'PLUS'
TT_PLUSE        = 'PLUSE'
TT_MINUS        = 'MINUS'
TT_MINUSE       = 'MINUSE'
TT_MUL          = 'MUL'
TT_MULE         = 'MULE'
TT_DIV          = 'DIV'
TT_DIVE         = 'DIVE'
TT_POW          = 'POW'
TT_POWE         = 'POWE'
TT_MOD          = 'MOD'
TT_MODE         = 'MODE'
TT_EQ           = 'EQ'
TT_LPAREN       = 'LPAREN'
TT_RPAREN       = 'RPAREN'
TT_LBRACE       = 'LBRACE'
TT_RBRACE       = 'RBRACE'
TT_LSQUARE      = 'LSQUARE'
TT_RSQUARE      = 'RSQUARE'
TT_KEY          = 'KEY'
TT_CONCAT       = 'CONCAT'
TT_EE           = 'EE'
TT_NE           = 'NE'
TT_LT           = 'LT'
TT_GT           = 'GT'
TT_LTE          = 'LTE'
TT_GTE          = 'GTE'
TT_COMMA        = 'COMMA'
TT_ARROW        = 'ARROW'
TT_NEWLINE      = 'NEWLINE'
TT_EOF          = 'EOF'
TT_INCR         = 'INCR'
TT_DECR         = 'DECR'

TT_BW_AND       = 'BW_AND'
TT_BW_ANDE      = 'BW_ANDE'
TT_BW_OR        = 'BW_OR'
TT_BW_ORE       = 'BW_ORE'
TT_BW_NOT       = 'BW_NOT'
TT_BW_NOTE      = 'BW_NOTE'
TT_BW_XOR       = 'BW_XOR'
TT_BW_XORE      = 'BW_XORE'
TT_BW_RSHIFT    = 'BW_RSHIFT'
TT_BW_RSHIFTE   = 'BW_RSHIFTE'
TT_BW_LSHIFT    = 'BW_LSHIFT'
TT_BW_LSHIFTE   = 'BW_LSHIFTE'

KEYWORDS = [
    'let',
    'const',
    'and',
    'or',
    'not',
    'if',
    'elif',
    'else',
    'for',
    'to',
    'step',
    'while',
    'func',
    'then',
    'end',
    'ret',
    'continue',
    'break',
    'import',
    'true',
    'false',
    'null',
    'do',
    'delete',
    'in',
]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'