import unittest, logging, sys
from forth_to_vm_generate import VmGenerator

class Test_VmGenerator(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.level = logging.DEBUG
        self.stream_handler = logging.StreamHandler(sys.stdout)
        self.logger.addHandler(self.stream_handler)
        self.stream_handler.stream = sys.stdout
        self.vm_generator = VmGenerator()
    
    def assertEqualString(self, f, s):
        f = f.split("\n")
        s = list(filter(None, s.split("\n")))
        for idx in range(len(f)):
            if f[idx].strip() != s[idx].strip():
                print("")
                print("Return Value:-------")
                print("\n".join(f))
                print("-------------------")
                print("Expected Value:-----")
                print("\n".join(s))
                print("-------------------")
                print("TESTE STE\nTEADSA\nasdsad")
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

    def test13(self):
        self.generator_test(
            '''
            CHAR W .
            ''',
            '''
            start
            pushs "w"
            chrcode
            writei
            stop
            '''
        )
    
    def test14(self):
        self.generator_test(
            '''
            CHAR % DUP . EMIT
            ''',
            '''
            start
            pushs "%"
            chrcode
            pusha dup
            call
            writei
            pusha emit
            call
            stop
            '''
        )

if __name__ == "__main__":
    unittest.main()