import ply.yacc as yacc
import sys, re
from itertools import chain
from forth_lexer import tokens, Lexer

def flatten(S):
        if S == []:
            return S
        if isinstance(S[0], list):
            return flatten(S[0]) + flatten(S[1:])
        return S[:1] + flatten(S[1:])

def converter_lowercase_preservandostrings(text):
    # Function to replace non-quoted text with its lowercase version
    def lowercase_non_quoted(match):
        # If the match is a quoted string, return it unchanged
        if match.group(0).startswith('"') and match.group(0).endswith('"'):
            return match.group(0)
        # Otherwise, return the lowercase version of the match
        return match.group(0).lower()
    
    # Regular expression to match text inside quotes or any other text
    pattern = r'"[^"]*"|[^"]+'
    # Use re.sub() to apply the function to each match
    return re.sub(pattern, lowercase_non_quoted, text)

class Parser:
    tokens = tokens
    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)

    def parse(self, data):
        return self.parser.parse(converter_lowercase_preservandostrings(data), lexer=self.lexer)

    def p_instrucoes(self, p):
        '''
        instrucoes : execucao instrucoes
                   | execucao
        '''
        p[0] = p[1]
        if len(p) == 3:
            p[0] = flatten([p[1], [p[2]]])

    def p_execucao(self, p):
        '''
        execucao : funcao
                 | codigo 
                 | palavra
        '''
        p[0] = p[1]

    def p_palavra(self, p):
        '''
        palavra : DP NAME codigo PV
        '''
        p[0] = {"type": "palavra", "name": p[2], "codigo": p[3]}
    
    def p_funcao(self, p):
        """
        funcao : DP NAME PARAM codigo PV
        """
        p[0] = {"type": "funcao", "name": p[2], "param": p[3], "codigo": p[4]}
        
    def p_codigo(self, p):
        """
        codigo : valor codigo
               | valor
               | condicao
        """
        p[0] = [p[1]]
        if len(p) == 3:
            p[0] = flatten([[p[0]], [p[2]]])

    def p_condicao(self, p):
        """
        condicao : IF codigo THEN
                 | IF codigo ELSE codigo THEN
        """
        p[0] = {"type": "condicao", "codigo_true" : p[2], "codigo_false": []}
        if len(p) == 6:
            p[0]["codigo_false"] = p[4]

    def p_valor(self, p):
        """
        valor : NAME
              | NUMBER
              | PONTO
              | STRING
              | EMIT
              | KEY
              | SPACE
              | SPACES
              | CHAR
              | CR
              | DUP
              | 2DUP
              | MAIOR
              | MENOR
              | IGUAL
              | DIVIDIR
              | MULTIPLICAR
              | SOMAR
              | SUBTRAIR
              | MOD
        """
        p[0] = p[1]

    #def p_vars(self, p):
    #    """
    #    vars : NAME
    #    """
    #    p[0] = {"type": "input", "vars": p[1] + p[2]}

    def p_error(self, p):
        if p:
            # Contextual information
            error_context = self.get_error_context(p)
            # Print detailed error information
            print(f"Syntax error at token '{p.type}' on line {p.lineno} at position {p.lexpos}")
            print(f"Error near: '{p.value}'")
            print(f"Context: {error_context}")

            # Suggest corrections based on common mistakes
            suggested_corrections = self.suggest_corrections(p)
            if suggested_corrections:
                print("Did you mean:")
                for suggestion in suggested_corrections:
                    print(f"    {suggestion}")
        else:
            # Error at End Of File - possibly missing tokens or unclosed constructs
            print("Syntax error at EOF. Possibly incomplete input.")

    def get_error_context(self, p):
        """
        Fetch a context window around the error position to help diagnose issues.
        """
        line_start = max(p.lexpos - 10, 0)
        line_end = p.lexpos + 10
        return p.lexer.lexdata[line_start:line_end]

    def suggest_corrections(self, p):
        """
        Generate a list of possible corrections based on common syntax errors.
        """
        suggestions = []
        if p.type in ["NAME", "NUMBER"]:
            # Example: Add common keyword if NAME is often confused with a keyword
            suggestions.append(f"Check if '{p.value}' is misspelled or should be a keyword.")
        elif p.type in ["DP", "PV"]:
            # Missing colon or semicolon can be a common issue
            suggestions.append("Maybe a ':' or ';' is missing or misplaced.")
        return suggestions



def main():
    parser = Parser()
    for line in sys.stdin:
        try:
            result = parser.parse(line)
            print(result)
        except Exception as e:
            print(f"error exception: {e}")

if __name__ == "__main__":
    main()
