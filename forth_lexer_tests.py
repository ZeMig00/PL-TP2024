import unittest
from forth_lexer import *

class Test_Lexer(unittest.TestCase):

    def setUp(self):
        self.lexer = Lexer()

    def verify_tokens(self, list_tokens, list_expected_tokens):
        self.assertEqual(len(list_tokens), len(list_expected_tokens))
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
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'SUBTRAIR', 'PONTO'])

    def test_6(self):
        lex_input(self.lexer, '30 5 / . ( 6=30/5 )')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'DIVIDIR', 'PONTO'])
    
    def test_7(self):
        lex_input(self.lexer, '30 5 * . ( 6=30/5 )')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'MULTIPLICAR', 'PONTO'])
    
    def test_8(self):
        lex_input(self.lexer, '30 5 + 7 / .(5=(30+5)/7)')
        r = list(self.lexer)
        self.verify_tokens(r, ['NUMBER', 'NUMBER', 'SOMAR', 'NUMBER', 'DIVIDIR', 'PONTO'])

    def test_9(self):
        lex_input(self.lexer, ': AVERAGE ( a b -- avg ) + 2/ ;')
        r = list(self.lexer)
        self.verify_tokens(r, ['DP', 'NAME', 'PARAM', 'SOMAR', 'NUMBER', 'DIVIDIR', 'PV'])
        self.assertEqual(r[2].value, [['a','b'],['avg']])

    def test_10(self):
        lex_input(self.lexer, 'CHAR W . CHAR % DUP . EMIT CHAR A DUP . 32 + EMIT')
        r = list(self.lexer)
        self.verify_tokens(r, ['CHAR', 'PONTO', 'CHAR', 'DUP', 'PONTO', 'EMIT', 'CHAR', 'DUP', 'PONTO', 'NUMBER', 'SOMAR', 'EMIT'])

    def test_11(self):
        program = '''
            : SPROUTS ." Miniature vegetables." ;
            : MENU
            CR TOFU CR SPROUTS CR
            ;
            MENU
        '''
        lex_input(self.lexer, program)
        r = list(self.lexer)
        self.verify_tokens(r, ["DP", "NAME", "PONTO", "STRING", "PV", "DP", "NAME", "CR",
                               "NAME", "CR", "NAME", "CR", "PV", "NAME"])
        
    def test_12(self):
        program = '''
            : TESTKEY ( -- )
            ." Hit a key: " KEY CR
            ." That = " . CR
            ;
            TESTKEY
        '''
        lex_input(self.lexer, program)
        r = list(self.lexer)
        self.verify_tokens(r, ["DP", "NAME", "PARAM",
                               "PONTO", "STRING", "KEY", "CR",
                               "PONTO", "STRING", "PONTO", "CR",
                               "PV", "NAME"])
        self.assertEqual(r[2].value, [[],[]])
        
    def test_13(self):
        program = '''
        ( May the Forth be with you)
        : STAR 42 EMIT ;
        : STARS 0 DO STAR LOOP ;
        : MARGIN CR 30 SPACES ;
        : BLIP MARGIN STAR ;
        : IOI MARGIN STAR 3 SPACES STAR ;
        : IIO MARGIN STAR STAR 3 SPACES ;
        : OIO MARGIN 2 SPACES STAR 2 SPACES ;
        : BAR MARGIN 5 STARS ;
        : F BAR BLIP BAR BLIP BLIP CR ;
        : O BAR IOI IOI IOI BAR CR ;
        : R BAR IOI BAR IIO IOI CR ;
        : T BAR OIO OIO OIO OIO CR ;
        : H IOI IOI BAR IOI IOI CR ;
        '''
        lex_input(self.lexer, program)
        r = list(self.lexer)
        self.assertEqual(len(r), 99)

    def test_14(self):
        program = '''
        : TESTKEY ( -- ) \\asdsad
            ." Hit a key: " KEY CR  \\ test
            ." That = " . CR
            ;
            TESTKEY
        '''
        lex_input(self.lexer, program)
        r = list(self.lexer)
        self.verify_tokens(r, ["DP", "NAME", "PARAM",
                               "PONTO", "STRING", "KEY", "CR",
                               "PONTO", "STRING", "PONTO", "CR",
                               "PV", "NAME"])
        self.assertEqual(r[2].value, [[],[]])

    def test_15(self):
        program = '''
            : maior2 2dup > if swap . ." é o maior " else . ." é o maior " then ;
            77 156 maior2
        '''
        lex_input(self.lexer, program)
        r = list(self.lexer)
        self.verify_tokens(r, ["DP", "NAME",
                               "2DUP", "MAIOR", "IF", "NAME",
                               "PONTO", "PONTO", "STRING", "ELSE", "PONTO", "PONTO", "STRING", "THEN",
                               "PV", "NUMBER", "NUMBER", "NAME"])
        
    def test_16(self):
        program = '''
            CHAR w .
        '''
        lex_input(self.lexer, program)
        r = list(self.lexer)
        self.verify_tokens(r, ["CHAR", "PONTO"])

if __name__ == "__main__":
    unittest.main()