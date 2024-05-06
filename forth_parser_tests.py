import unittest
from forth_parser import Parser

class Test_Parser(unittest.TestCase):

    def setUp(self):
        self.parser = Parser()
   
    def test1(self):
        a = self.parser.parse(':FUNCAO (a b c -- out) . 9 8 8 ;')
        self.assertEqual(a['type'], 'funcao')
        self.assertEqual(a['name'], 'funcao')
        self.assertEqual(a['param'], [['a','b','c'],['out']])
        self.assertEqual(a["codigo"], ['.', 9,8,8])
    
    def test2(self):
        a = self.parser.parse(':PALAVRA ."ola Mundo!" ;')
        self.assertEqual(a['type'], 'palavra')
        self.assertEqual(a['name'], 'palavra')
        self.assertEqual(a["codigo"], ['.', "ola Mundo!"])
    
    def test3(self):
        a = self.parser.parse(
            '''
            : hello-world ( -- )
                ." Hello, World!" cr ; \ Call the defined word
                hello-world 9 3 + 
            '''
        )
        self.assertEqual(a[0]['type'], 'funcao')
        self.assertEqual(a[0]['param'][0], []) # entrada
        self.assertEqual(a[0]['param'][1], []) # saida
        self.assertEqual(a[0]['codigo'][0], '.')
        self.assertEqual(a[0]['codigo'][1], ' Hello, World!')
        self.assertEqual(a[0]['codigo'][2], 'cr')

        self.assertEqual(a[1], 'hello-world')
        self.assertEqual(a[2], 9.0)
        self.assertEqual(a[3], 3.0)
        self.assertEqual(a[4], '+')

    def test4(self):
        a = self.parser.parse(
            '''
            : maior2 2dup >= if swap . ." é o maior " else . ." é o maior " then ;
            77 156 maior2
            '''
        )
        self.assertEqual(a[0]['type'], 'palavra')
        self.assertEqual(a[0]['codigo'], [2.0, "dup", ">=", {
            "type": "condicao", 
            "codigo_true": ["swap", ".", ".", " é o maior "],
            "codigo_false": [".", ".", " é o maior "]
        }])
        self.assertEqual(a[1], 77.0)
        self.assertEqual(a[2], 156.0)
        self.assertEqual(a[3],"maior2")

    def test5(self):
        a = self.parser.parse(
            '''
            : maior2 2dup > if swap then ;
            : maior3 maior2 maior2 . ;
            2 11 3 maior3
            '''
        )
        self.assertEqual(a[0]['type'], 'palavra')
        self.assertEqual(a[0]['codigo'], [2.0, "dup", ">", {
            "type": "condicao", 
            "codigo_true": ["swap"],
            "codigo_false": []
        }])

        self.assertEqual(a[1]['type'], 'palavra')
        self.assertEqual(a[1]['codigo'], ['maior2', 'maior2', '.'])

        self.assertEqual(a[2], 2.0)
        self.assertEqual(a[3], 11.0)
        self.assertEqual(a[4], 3.0)
        self.assertEqual(a[5], 'maior3')
     
    def test6(self):
        a = self.parser.parse(
            '''
            : maior2 2dup > if drop else swap drop then ;
            : maior3 maior2 maior2 ;
            : maiorN depth 1 do maior2 loop ;
            2 11 3 4 45 8 19 maiorN .
            '''
        )

        self.assertEqual(a[0]['type'], 'palavra')
        self.assertEqual(a[1]['type'], 'palavra')
        self.assertEqual(a[2]['type'], 'palavra')
        self.assertEqual(a[3], 2.0)
        self.assertEqual(a[4], 11.0)
        self.assertEqual(a[5], 3.0)
        self.assertEqual(a[6], 4.0)
        self.assertEqual(a[7], 45.0)
        self.assertEqual(a[8], 8.0)
        self.assertEqual(a[9], 19.0)
        self.assertEqual(a[10], 'maiorn')
        self.assertEqual(a[11], '.')

    def test7(self):
        a = self.parser.parse(
            '''
            : factorial ( n -- n! )
            dup 0 = if
            drop 1
            else
            dup 1 - recurse *
            then ;
            \ Example usage:
            5 factorial . \ Calculate factorial of 5 and print result
            '''
        )

        self.assertEqual(a[0]['type'], 'funcao')
        self.assertEqual(a[1], 5.0)
        self.assertEqual(a[2], 'factorial')
        self.assertEqual(a[3], '.')

    def test8(self):
        a = self.parser.parse(
            '''
            CHAR w .
            '''
        )
        self.assertEqual(a[0]['type'], 'char')
        self.assertEqual(a[0]['param'], 'w')
        self.assertEqual(a[1], '.')

        
if __name__ == "__main__":
    unittest.main()