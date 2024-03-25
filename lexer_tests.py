import unittest
from lexer import *

class Test_Lexer(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()

    def verify_tokens(self, list_tokens, list_expected_tokens):
        for i,t in enumerate(list_tokens):
            self.assertEqual(t.type, list_expected_tokens[i])
    
    def verify_tokens_value(self, list_tokens, list_expected_tokens):
        for i,t in enumerate(list_tokens):
            self.assertEqual(t.value, list_expected_tokens[i])

    def test_1(self):
        lex_input(self.lexer, "WAKE.UP EAT.BREAKFAST WORK EAT.DINNER PLAY SLEEP")
        self.verify_tokens(list(self.lexer), ["NAME", "NAME", "NAME", "NAME", "NAME", "NAME"])

    def test_2(self):
        lex_input(self.lexer, '." #S SWAP ! @ ACCEPT . *"')
        r = list(self.lexer)
        self.verify_tokens(r, ['PONTO', 'STRING'])
        self.verify_tokens_value(r, ['.',' #s swap ! @ accept . *'])

    def test_3(self):
        lex_input(self.lexer, '17 34 23')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'NUMBER'])
        self.verify_tokens_value(r, [17,34,23])

    def test_4(self):
        lex_input(self.lexer, '2 3 + 10 + .')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'SOMAR', 'NUMBER', 'SOMAR', 'PONTO'])
        self.verify_tokens_value(r, [2,3,"+",10,"+","."])

    def test_5(self):
        lex_input(self.lexer, '30 5 - . ( 25=30-5 )')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'SUBTRAIR', 'PONTO', 'COMENTARIO'])

    def test_6(self):
        lex_input(self.lexer, '30 5 / . ( 6=30/5 )')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'DIVIDIR', 'PONTO', 'COMENTARIO'])
    
    def test_7(self):
        lex_input(self.lexer, '30 5 * . ( 6=30/5 )')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'MULTIPLICAR', 'PONTO', 'COMENTARIO'])
    
    def test_8(self):
        lex_input(self.lexer, '30 5 + 7 / .(5=(30+5)/7)')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'SOMAR', 'NUMBER', 'DIVIDIR', 'PONTO', 'COMENTARIO'])

    def test_9(self):
        lex_input(self.lexer, ': AVERAGE ( a b -- avg ) + 2/ ;')
        r = list(self.lexer)
        self.verify_tokens(r, ['DP', 'NAME', 'COMENTARIO', 'SOMAR', 'NUMBER', 'DIVIDIR', 'PV'])

    def test_10(self):
        lex_input(self.lexer, 'CHAR W . CHAR % DUP . EMIT CHAR A DUP . 32 + EMIT')
        r = list(self.lexer)
        self.verify_tokens(r, ['CHAR', 'NAME', 'PONTO', 'CHAR', 'MOD', 'DUP', 'PONTO', 'EMIT', 'CHAR', 'NAME', 'DUP', 'PONTO', 'NUMBER', 'SOMAR', 'EMIT'])

if __name__ == "__main__":
    unittest.main()