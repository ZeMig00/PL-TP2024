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
        print(a)
     
if __name__ == "__main__":
    unittest.main()