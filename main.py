from parser import parse
from lexer import LexerError
import sys


def out_parse_result(definitions):
    for definition in definitions:
        print(definition)


def test():
    for i in range(5):
        print("Test " + str(i))
        file = open("tests/test" + str(i), 'r')
        out_parse_result(parse(file.read()))
    print("Expect some parse error:")
    for i in range(4):
        print("Test " + str(i + 5))
        file = open("tests/fail_test" + str(i), 'r')
        out_parse_result(parse(file.read()))


if len(sys.argv) < 2:
    test()
else:
    file = open(sys.argv[1], 'r')
    try:
        out_parse_result(parse(file.read()))
    except LexerError as error:
        print(error.args[0])
