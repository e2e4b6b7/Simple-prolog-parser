import ply.yacc as yacc
from lexer import tokens, lex_reset

definitions = []


class Identifier:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Atom:
    def __init__(self, identifier, atoms):
        self.identifier = identifier
        self.atoms = atoms

    def __str__(self):
        ret = "Atom (" + str(self.identifier) + ") ["
        for atom in self.atoms:
            ret += str(atom) + ", "
        if self.atoms:
            ret = ret[0:-2]
        ret += "]"
        return ret


class OperatorAnd:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "And (" + str(self.left) + ") (" + str(self.right) + ")"


class OperatorOr:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "Or (" + str(self.left) + ") (" + str(self.right) + ")"


class Definition:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

    def __str__(self):
        ret = "Definition (" + str(self.identifier) + ")"
        if self.expression:
            ret += " (" + str(self.expression) + ")"
        return ret


def p_definitions_list(p):
    """definitions_list : definition definitions_list
                        |"""
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]


def p_definition(p):
    """definition : atom DOT
                  | atom IS expression DOT"""
    if len(p) == 3:
        p[0] = Definition(p[1], None)
    else:
        p[0] = Definition(p[1], p[3])

    global definitions
    definitions += [p[0]]


def p_atom(p):
    """atom : ID braced_atoms_list"""
    p[0] = Atom(p[1], p[2])


def p_braced_atom(p):
    """braced_atom : LBR braced_atom RBR
                   | atom"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = p[1]


def p_braced_atoms_list(p):
    """braced_atoms_list : ID braced_atoms_list
                         | LBR braced_atom RBR braced_atoms_list
                         |"""
    if len(p) == 1:
        p[0] = []
    elif len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[2]] + p[4]


def p_expression(p):
    """expression : term OR expression
                  | term"""
    if len(p) == 4:
        p[0] = OperatorOr(p[1], p[3])
    else:
        p[0] = p[1]


def p_term(p):
    """term : factor AND term
            | factor"""
    if len(p) == 4:
        p[0] = OperatorAnd(p[1], p[3])
    else:
        p[0] = p[1]


def p_factor(p):
    """factor : atom
              | LBR expression RBR"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]


def p_error(p):
    if p:
        print("Parse error in line " + str(p.lineno))
        global parser
        while True:
            tok = parser.token()
            if not tok or tok.type == 'DOT':
                break
        parser.restart()
    else:
        print("Unexpected EOF in last definition")


parser = yacc.yacc()


def reset():
    global definitions
    lex_reset()
    definitions = []


def parse(text):
    reset()
    parser.parse(text)
    return definitions.copy()
