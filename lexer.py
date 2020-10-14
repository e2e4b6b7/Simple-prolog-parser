import ply.lex as lex


def get_error_text(text, line, pos):
    return "Unrecognized symbol: '" + str(text) + "'. At line: " + str(line) + ", pos: " + str(pos)


class LexerError(Exception):
    def __init__(self, text):
        pass


tokens = [
    'IS',
    'AND',
    'OR',
    'ID',
    'LBR',
    'RBR',
    'DOT'
]

t_ID = r"[a-zA-Z_][a-zA-Z_0-9]*"
t_IS = ':-'
t_AND = ','
t_OR = ';'
t_LBR = r'\('
t_RBR = r'\)'
t_DOT = r'\.'

t_ignore = ' \t'


def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


def t_error(t):
    raise LexerError(get_error_text(t.value[0], t.lexer.lineno, t.lexer.lexpos))


lexer = lex.lex()


def lex_reset():
    global lexer
    lexer = lex.lex()
