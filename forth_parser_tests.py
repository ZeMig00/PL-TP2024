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
                ." Hello, World!" cr ;
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
            : hello-world ( -- )
            ." Hello, World!" cr ;
            hello-world \ Call the defined word
            '''
        )
     
if __name__ == "__main__":
    unittest.main()