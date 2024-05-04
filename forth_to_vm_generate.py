from forth_parser import Parser
import sys

class VmGenerator:
    
    parser = Parser()
    
    def generate(self, parser_result_dict):
        assembly = ""
        last_element_type = None
        for element in parser_result_dict:
            if type(element) == float:
                assembly += f"pushf {element}\n"
                last_element_type = float
            elif type(element) == int:
                assembly += f"pushi {element}\n"
                last_element_type = int
            elif element == '+':
                assembly += f"add\n"
            elif element == '-':
                assembly += f"sub\n"
            elif element == '/':
                assembly += f"div\n"
            elif element == '*':
                assembly += f"mul\n"
            elif element == '>':
                assembly += f"sup\n"
            elif element == '>=':
                assembly += f"supeq\n"
            elif element == '<':
                assembly += f"inf\n"
            elif element == '<=':
                assembly += f"infeq\n"
            elif element == '.' and last_element_type != None:
                if last_element_type == int:
                    assembly += 'writei\n'
                elif last_element_type == float:
                    assembly += 'writef\n'
                elif last_element_type == str:
                    assembly += 'writes\n'
                else:
                    raise Exception(f"No last element type supported")
            else:
                raise Exception(f"Token {element} not supported")
        
        return assembly

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