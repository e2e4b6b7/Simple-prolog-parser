import ply.lex as lex


class LexerError(Exception):
    def __init__(self, text, line, pos):
        self.txt = "Unrecognized symbol: '" + str(text) + "'. At line: " + str(line) + ", pos: " + str(pos)


tokens = [
    'CORKSCREW',
    'CONJUNCTION',
    'DISJUNCTION',
    'IDENTIFIER',
    'OBRACKET',
    'CBRACKET',
    'DOT'
]

t_IDENTIFIER = r"[a-zA-Z_][a-zA-Z_0-9]*"
t_CORKSCREW = ':-'
t_CONJUNCTION = ','
t_DISJUNCTION = ';'
t_OBRACKET = r'\('
t_CBRACKET = r'\)'
t_DOT = r'\.'
t_ignore = ' \t'


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise LexerError(t.value[0], t.lexer.lineno, t.lexer.lexpos)


def lex_it(text):
    lexer = lex.lex()
    lexer.input(text)
    tokens_array = []
    while True:
        token = lexer.token()
        if not token:
            break
        tokens_array += [token]
    return tokens_array
