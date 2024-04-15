import ply.yacc as yacc
import sys
from forth_lexer import tokens, Lexer

class Parser:
    def __init__(self):
        self.tokens = tokens
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer)

    def p_var_multiple(self, p):
        'var : CHAR'
        p[0] = {"type": "int", "vars": p[0]}

    def p_error(self, p):
        print("Syntax error in input!")

def main():
    parser = Parser()
    for line in sys.stdin:
        try:
            result = parser.parse(line)
            print(result)
        except Exception as e:
            print(f"error exception: {e}")

if __name__ == "__main__":
    main()
