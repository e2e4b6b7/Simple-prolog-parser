import ply.lex as lex


def get_error_text(text, line, pos):
    return "Unrecognized symbol: '" + str(text) + "'. At line: " + str(line) + ", pos: " + str(pos)


class LexerError(Exception):
    def __init__(self, text):
        pass


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
    raise LexerError(get_error_text(t.value[0], t.lexer.lineno, t.lexer.lexpos))


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
