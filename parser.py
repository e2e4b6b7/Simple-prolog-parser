from lexer import lex_it
from enum import Enum


def get_error_text(expected_text, find_text, line, position):
    return "Parse error. Expected: '" + str(expected_text) + "', got: '" + str(
        find_text) + "'. At line: " + str(line) + ", pos: " + str(position)


class ParserError(Exception):
    def __init__(self, text):
        self.txt = text


class Variable:
    def __init__(self, name):
        self.name = name


class OperatorType(Enum):
    DISJUNCTION = 1
    CONJUNCTION = 2


class Operator:
    def __init__(self, op_type, left, right):
        self.op_type = op_type
        self.left = left
        self.right = right


class Definition:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression


pos = 0
tokens = []


def parse_item():
    global tokens, pos
    if tokens[pos].type == 'IDENTIFIER':
        pos = pos + 1
        return Variable(tokens[pos - 1].value)
    elif tokens[pos].type == 'OBRACKET':
        pos = pos + 1
        expression = parse_disjunction()
        if tokens[pos].type == 'CBRACKET':
            pos = pos + 1
            return expression
        else:
            raise ParserError(get_error_text(')', tokens[pos].value, tokens[pos].lineno, tokens[pos].lexpos))
    else:
        raise ParserError(get_error_text('IDENTIFIER', tokens[pos].type, tokens[pos].lineno, tokens[pos].lexpos))


def parse_conjunction():
    global tokens, pos
    expression_l = parse_item()
    if tokens[pos].type == 'CONJUNCTION':
        pos += 1
        expression_r = parse_conjunction()
        return Operator(OperatorType.CONJUNCTION, expression_l, expression_r)
    else:
        return expression_l


def parse_disjunction():
    global tokens, pos
    expression_l = parse_conjunction()
    if tokens[pos].type == 'DISJUNCTION':
        pos += 1
        expression_r = parse_disjunction()
        return Operator(OperatorType.DISJUNCTION, expression_l, expression_r)
    else:
        return expression_l


def parse_identifier():
    global tokens, pos
    if tokens[pos].type == 'IDENTIFIER':
        pos += 1
        return tokens[pos - 1].value
    else:
        raise ParserError(get_error_text('IDENTIFIER', tokens[pos].type, tokens[pos].lineno, tokens[pos].lexpos))


def check_drop_corkscrew():
    global tokens, pos
    if tokens[pos].type == 'CORKSCREW':
        pos += 1
        return True
    else:
        return False


def check_drop_dot():
    global tokens, pos
    if tokens[pos].type == 'DOT':
        pos += 1
        return True
    else:
        return False


def parse_definition():
    global tokens, pos
    identifier = parse_identifier()
    if check_drop_corkscrew():
        expression = parse_disjunction()
    if not check_drop_dot():
        raise ParserError(get_error_text('.', tokens[pos].value, tokens[pos].lineno, tokens[pos].lexpos))
    # return Definition(identifier, expression)


def parse_it(text):
    global tokens, pos
    tokens = lex_it(text)
    pos = 0
    while pos < len(tokens):
        try:
            parse_definition()
        except IndexError:
            raise ParserError("Unexpected EOF")
