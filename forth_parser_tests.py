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
            : maior2 2dup > if swap . ." é o maior " else . ." é o maior " then ;
            77 156 maior2
            '''
        )
        self.assertEqual(a[0]['type'], 'palavra')
        self.assertEqual(a[0]['codigo'], [2.0, "dup", ">", {
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
     
if __name__ == "__main__":
    unittest.main()