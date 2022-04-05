from token import DIGITS, KEYWORDS, LETTERS, LETTERS_DIGITS, TT_ARROW, TT_BW_AND, TT_BW_ANDE, TT_BW_LSHIFT, TT_BW_LSHIFTE, TT_BW_NOT, TT_BW_ORE, TT_BW_RSHIFT, TT_BW_RSHIFTE, TT_BW_XOR, TT_BW_XORE, TT_COMMA, TT_CONCAT, TT_DECR, TT_DIV, TT_DIVE, TT_EE, TT_EOF, TT_EQ, TT_FLOAT, TT_GT, TT_GTE, TT_IDENTIFIER, TT_INCR, TT_INT, TT_KEY, TT_KEYWORD, TT_LBRACE, TT_LPAREN, TT_LSQUARE, TT_LT, TT_LTE, TT_MINUS, TT_MINUSE, TT_MOD, TT_MODE, TT_MUL, TT_NE, TT_NEWLINE, TT_PLUS, TT_PLUSE, TT_POW, TT_POWE, TT_RBRACE, TT_RPAREN, TT_RSQUARE, TT_STRING, TT_BW_OR, Token
from errors import ExpectedCharError, IllegalCharError

from position import Position

########################################
# LEXER
########################################

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in ';\n':
                tokens.append(Token(TT_NEWLINE, pos_start=self.pos))
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS + '_':
                tokens.append(self.make_identifier())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(self.make_plus())
            elif self.current_char == '-':
                tokens.append(self.make_minus())
            elif self.current_char == '*':
                tokens.append(self.make_multiply())
            elif self.current_char == '/':
                tok = self.make_divide()
                if tok: tokens.append(tok)
            elif self.current_char == '%':
                tokens.append(self.make_op(TT_MOD, TT_MODE))
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(TT_LSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(TT_RSQUARE, pos_start=self.pos))
                self.advance()
            elif self.current_char == ':':
                token, error = self.make_colon()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '|':
                tokens.append(self.make_op(TT_BW_OR, TT_BW_ORE))
            elif self.current_char == '^':
                tokens.append(self.make_op(TT_BW_XOR, TT_BW_XORE))
            elif self.current_char == '&':
                tokens.append(self.make_op(TT_BW_AND, TT_BW_ANDE))
            elif self.current_char == '~':
                tokens.append(Token(TT_BW_NOT, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                token, error = self.make_not_equals()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_equals_or_arrow())
            elif self.current_char == '<':
                tokens.append(self.make_less_than())
            elif self.current_char == '>':
                tokens.append(self.make_greater_than())
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
            num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_plus(self):
        tok_type = TT_PLUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_PLUSE
        elif self.current_char == '+':
            self.advance()
            tok_type = TT_INCR

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_multiply(self):
        tok_type = TT_MUL
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_PLUSE
        elif self.current_char == '*':
            self.advance()
            tok_type = TT_POW

            if self.current_char == '=':
                self.advance()
                tok_type = TT_POWE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_minus(self):
        tok_type = TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_MINUSE
        elif self.current_char == '-':
            self.advance()
            tok_type = TT_DECR

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_op(self, tok_type1, tok_type2):
        tok_type = tok_type1
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = tok_type2

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        while self.current_char != None and (self.current_char != '"' or escape_character):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            else:
                if self.current_char == '\\':
                    escape_character = True
                else:
                    string += self.current_char
                    escape_character = False
            self.advance()

        self.advance()
        return Token(TT_STRING, string, pos_start, self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETTERS_DIGITS + '_':
            id_str += self.current_char
            self.advance()

        tok_type = TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
        return Token(tok_type, id_str, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals_or_arrow(self):
        tok_type = TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_EE
        elif self.current_char == '>':
            self.advance()
            tok_type = TT_ARROW

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        tok_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_LTE
        elif self.current_char == '<':
            self.advance()
            tok_type = TT_BW_LSHIFT

            if self.current_char == '=':
                self.advance()
                tok_type = TT_BW_LSHIFTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        tok_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '=':
            self.advance()
            tok_type = TT_GTE
        elif self.current_char == '>':
            self.advance()
            tok_type = TT_BW_RSHIFT

            if self.current_char == '=':
                self.advance()
                tok_type = TT_BW_RSHIFTE

        return Token(tok_type, pos_start=pos_start, pos_end=self.pos)

    def make_colon(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == ':':
            self.advance()
            return Token(TT_CONCAT, pos_start=pos_start, pos_end=self.pos), None
        
        return Token(TT_KEY, pos_start=pos_start, pos_end=self.pos), None

    def make_divide(self):
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == '/':
            self.skip_comment()
        elif self.current_char == '=':
            self.advance()
            return Token(TT_DIVE, pos_start=pos_start, pos_end=self.pos)
        else:
            return Token(TT_DIV, pos_start=self.pos)

    def skip_comment(self):
        self.advance()

        while self.current_char != '\n':
            self.advance()

        self.advance()