from parser import parse_it, ParserError
from lexer import LexerError
import sys


def test():
    for i in range(4):
        file = open("tests/test" + str(i), 'r')
        try:
            parse_it(file.read())
            print("test " + str(i) + ", successful")
        except LexerError as error:
            print(error.args[0])
        except ParserError as error:
            print(error.args[0])

    print("Expect parse error:")
    for i in range(3):
        file = open("tests/fail_test" + str(i), 'r')
        try:
            parse_it(file.read())
        except LexerError as error:
            print(error.args[0])
        except ParserError as error:
            print(error.args[0])
            print("fail test " + str(i) + ", successful")


if len(sys.argv) < 2:
    test()
else:
    file = open(sys.argv[1], 'r')
    try:
        parse_it(file.read())
        print("parsing successfully completed")
    except LexerError as error:
        print(error.args[0])
    except ParserError as error:
        print(error.args[0])
