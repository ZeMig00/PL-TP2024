from forth_parser import Parser
import sys

class VmGenerator:
    
    parser = Parser()
    
    funcoes = ['emit', 
               'key', 
               'space', 
               'spaces', 
               'char', 
               'cr',
               'dup',
               '2dup']

    def funcao(self, f):
        if f['name'] in self.funcoes:
            raise Exception(f"{f['name']} already exists in {self.funcoes}")
        assembly = f"{f['name']}:\n"
        for i,v in enumerate(f['param'][0]):
            assembly += "\tpushfp\n"
            assembly += f"\tload {(i+1)*-1}\n"
        assembly += self.generate(f['codigo'], line_begin='\t')
        assembly += "\treturn\n"
        self.funcoes.append(f['name'])
        return assembly

    def generate(self, parser_result_dict, line_begin = ''):
        assembly = ""
        assembly_funcoes = ""
        last_element_type = None

        if line_begin == '':
            assembly = "start\n"
        for element in parser_result_dict:
            if element in self.funcoes:
                assembly += f"{line_begin}pusha {element}\n"
                assembly += f"{line_begin}call\n"
            elif type(element) == dict and element['type'] == 'funcao':
                assembly_funcoes += self.funcao(element)
            elif type(element) == float:
                assembly += f"{line_begin}pushf {element}\n"
                last_element_type = float
            elif type(element) == int:
                assembly += f"{line_begin}pushi {element}\n"
                last_element_type = int
            elif element == '+':
                assembly += f"{line_begin}add\n"
            elif element == '-':
                assembly += f"{line_begin}sub\n"
            elif element == '/':
                assembly += f"{line_begin}div\n"
            elif element == '*':
                assembly += f"{line_begin}mul\n"
            elif element == '>':
                assembly += f"{line_begin}sup\n"
            elif element == '>=':
                assembly += f"{line_begin}supeq\n"
            elif element == '<':
                assembly += f"{line_begin}inf\n"
            elif element == '<=':
                assembly += f"{line_begin}infeq\n"
            elif element == '.' and last_element_type != None:
                if last_element_type == int:
                    assembly += f'{line_begin}writei\n'
                elif last_element_type == float:
                    assembly += f'{line_begin}writef\n'
                elif last_element_type == str:
                    assembly += f'{line_begin}writes\n'
                else:
                    raise Exception(f"No last element type supported")
            else:
                raise Exception(f"Token {element} not supported")
        
        if line_begin == '':
            assembly += "stop\n"

        return assembly + assembly_funcoes

    def convert(self, code):
        result = self.parser.parse(code)
        return self.generate(result)    

def main():
    vm_generator = VmGenerator()
    for line in sys.stdin:
        try:
            result = vm_generator.convert(line)
            print(result)
        except Exception as e:
            print(f"error exception: {e}")

if __name__ == '__main__':
    main()