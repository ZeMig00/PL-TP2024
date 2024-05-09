from forth_parser import Parser
import sys

class VmGenerator:
    
    parser = Parser()
    
    def __init__(self):
        self.funcoes = {
            'emit': False,      #feito
            'spaces': False,    #feito
            'char': False, 
            'cr': False,
            '2dup': False       #feito
        }

        self.macros = {
            'dup': ['dup 1'],
            'key': ['read', 'chrcode'],
            'space': ['writes " "'],
        }

    def gerar_emit(self):
        assembly = ""
        if self.funcoes['emit'] == True:
            assembly = f"emit:\n"
            assembly += "\tpushfp\n"
            assembly += "\tload -1\n"

            assembly += "\twritechr\n"

            assembly += "\treturn\n"
        return assembly

    def gerar_2dup(self):
        assembly = ""
        if self.funcoes['2dup'] == True:
            assembly = f"2dup:\n"
            assembly += "\tpushfp\n"
            assembly += "\tload -1\n"
            assembly += "\tpushfp\n"
            assembly += "\tload -2\n"

            assembly += "\treturn\n"

        return assembly
    
    def gerar_spaces(self):
        assembly = ""
        if self.funcoes['spaces'] == True:
            assembly = f"spaces:\n"
            assembly += "\tpushfp\n"
            assembly += "\tload -1\n"

            assembly += "spaces_loop:\n"
            assembly += "\tjz spaces_fim\n"
            assembly += "\twrites \" \"\n"
            assembly += "\tpushi 1\n"
            assembly += "\tsub\n"
            assembly += "\tjump spaces_loop\n"

            assembly += "spaces_fim:\n"
            assembly += "\treturn\n"

        return assembly

    def gerar_funcoes_standard(self):
        assembly = ""
        assembly += self.gerar_emit()
        assembly += self.gerar_2dup()
        assembly += self.gerar_spaces()
        return assembly

    def funcao(self, f):
        if f['name'] in self.funcoes:
            raise Exception(f"{f['name']} already exists in {self.funcoes}")
        
        assembly = f"{f['name']}:\n"
        for i,v in enumerate(f['param'][0]):
            assembly += "\tpushfp\n"
            assembly += f"\tload {(i+1)*-1}\n"

        if len(f['param'][0]) == 0:
            assembly += "\tpushfp\n"
        
        assembly += self.generate(f['codigo'], line_begin='\t')

        assembly += "\treturn\n"
        self.funcoes[f['name']] = True
        return assembly

    def generate(self, parser_result_dict, line_begin = ''):
        assembly = ""
        assembly_funcoes = ""
        last_element_type = None

        if line_begin == '':
            assembly = "start\n"
        for element in parser_result_dict:
            if type(element) == str and element in self.macros:
                for macro_line in self.macros[element]:
                    assembly += f"{line_begin}{macro_line}\n"
            elif type(element) == str and element in self.funcoes:
                self.funcoes[element] = True
                assembly += f"{line_begin}pusha {element}\n"
                assembly += f"{line_begin}call\n"
            elif type(element) == dict and element['type'] == 'funcao':
                assembly_funcoes += self.funcao(element)
            elif type(element) == dict and element['type'] == 'char':
                assembly += f"{line_begin}pushs \"{element['param']}\"\n"
                assembly += f"chrcode\n"
                last_element_type = int
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

        return assembly + assembly_funcoes + self.gerar_funcoes_standard()

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