import unittest
from forth_to_vm_generate import VmGenerator

class Test_VmGenerator(unittest.TestCase):

    def setUp(self):
        self.vm_generator = VmGenerator()
    
    def assertEqualString(self, f, s):
        f = f.split("\n")
        s = list(filter(None, s.split("\n")))
        for idx in range(len(f)):
            self.assertEqual(f[idx].strip(), s[idx].strip())

    def generator_test(self, i, expected):
        r = self.vm_generator.convert(i)
        self.assertEqualString(r, expected)

    def test1(self):
        self.generator_test(
            '''
            2.0 11.0 +
            ''',
            '''
            pushf 2.0
            pushf 11.0
            add
            '''
        )
    
    def test2(self):
        self.generator_test(
            '''
            2 11 +
            ''',
            '''
            pushi 2
            pushi 11
            add
            '''
        )

    def test3(self):
        self.generator_test(
            '''
            2 11 *
            ''',
            '''
            pushi 2
            pushi 11
            mul
            '''
        )
    def test4(self):
        self.generator_test(
            '''
            2 11 /
            ''',
            '''
            pushi 2
            pushi 11
            div
            '''
        )
    def test5(self):
        self.generator_test(
            '''
            2 11 -
            ''',
            '''
            pushi 2
            pushi 11
            sub
            '''
        )
    def test6(self):
        self.generator_test(
            '''
            5 10 >
            ''',
            '''
            pushi 5
            pushi 10
            sup
            '''
        )
    def test7(self):
        self.generator_test(
            '''
            5 10 <
            ''',
            '''
            pushi 5
            pushi 10
            inf
            '''
        )
    def test8(self):
        self.generator_test(
            '''
            5 10 >=
            ''',
            '''
            pushi 5
            pushi 10
            supeq
            '''
        )
    def test9(self):
        self.generator_test(
            '''
            5 10 <=
            ''',
            '''
            pushi 5
            pushi 10
            infeq
            '''
        )

if __name__ == "__main__":
    unittest.main()