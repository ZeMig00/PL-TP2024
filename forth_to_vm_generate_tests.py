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
            start
            pushf 2.0
            pushf 11.0
            add
            stop
            '''
        )
    
    def test2(self):
        self.generator_test(
            '''
            2 11 +
            ''',
            '''
            start
            pushi 2
            pushi 11
            add
            stop
            '''
        )

    def test3(self):
        self.generator_test(
            '''
            2 11 *
            ''',
            '''
            start
            pushi 2
            pushi 11
            mul
            stop
            '''
        )
    def test4(self):
        self.generator_test(
            '''
            2 11 /
            ''',
            '''
            start
            pushi 2
            pushi 11
            div
            stop
            '''
        )
    def test5(self):
        self.generator_test(
            '''
            2 11 -
            ''',
            '''
            start
            pushi 2
            pushi 11
            sub
            stop
            '''
        )
    def test6(self):
        self.generator_test(
            '''
            5 10 >
            ''',
            '''
            start
            pushi 5
            pushi 10
            sup
            stop
            '''
        )
    def test7(self):
        self.generator_test(
            '''
            5 10 <
            ''',
            '''
            start
            pushi 5
            pushi 10
            inf
            stop
            '''
        )
    def test8(self):
        self.generator_test(
            '''
            5 10 >=
            ''',
            '''
            start
            pushi 5
            pushi 10
            supeq
            stop
            '''
        )
    def test9(self):
        self.generator_test(
            '''
            5 10 <=
            ''',
            '''
            start
            pushi 5
            pushi 10
            infeq
            stop
            '''
        )

    def test10(self):
        self.generator_test(
            '''
            5 10 <= 2 + 1 - .
            ''',
            '''
            start
            pushi 5
            pushi 10
            infeq
            pushi 2
            add
            pushi 1
            sub
            writei
            stop
            '''
        )

    def test11(self):
        self.generator_test(
            '''
            5.0 .
            ''',
            '''
            start
            pushf 5.0
            writef
            stop
            '''
        )

    def test12(self):
        self.generator_test(
            '''
            : AVERAGE ( a b -- avg ) + 2/ ;
            10 20 AVERAGE .
            ''',
            '''
            start
            pushi 10
            pushi 20
            pusha average
            call
            writei
            stop
            average:
                pushfp
                load -1
                pushfp
                load -2
                add
                pushi 2
                div
                return
            '''
        )

if __name__ == "__main__":
    unittest.main()