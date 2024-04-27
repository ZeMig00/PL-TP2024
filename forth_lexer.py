import sys, re
import ply.lex as lex


# List of token names.   This is always required
tokens = (
    "DP",           #:
    "PV",           #;
    "STRING",       #"
    "PARAM",        #(vars--vars)
    "MAIOR",        #>
    "MENOR",        #<
    "MAIORIG",      #>=
    "MENORIG",      #<=
    "DIVIDIR",      #/
    "MULTIPLICAR",  #*
    "SOMAR",        #+
    "SUBTRAIR",     #-
    "MOD",          #%
    "IF",           #if
    "ELSE",         #else
    "THEN",         #the
    'EMIT',         #EMIT
    'KEY',          #KEY
    'SPACE',        #SPACE
    'SPACES',       #SPACES
    'CHAR',         #CHAR
    'CR',           #CR
    "PONTO",        #.
    "NUMBER",       #[0-9]
    'DUP',          #DUP
    '2DUP',         #2DUP
    "NAME",         #Var names | Function names ...
)

def Lexer():
    # Regular expression rules for simple tokens
    t_DP    =           r':'
    t_PV    =           r';'
    t_MAIOR =           r'>'
    t_MENOR =           r'<'
    t_MAIORIG =         r'>='
    t_MENORIG =         r'<='
    t_DIVIDIR =         r'\/'
    t_MULTIPLICAR =     r'\*'
    t_SOMAR =           r'\+'
    t_SUBTRAIR =        r'\-'
    t_MOD =             r'%'
    t_IF =              r'if'
    t_ELSE =            r'else'
    t_THEN =            r'then'
    t_EMIT =            r'emit'
    t_KEY =             r'key'
    t_SPACE =           r'space'
    t_SPACES =          r'spaces'
    t_CHAR =            r'char'
    t_CR =              r'cr'
    t_PONTO =           r'\.'
    t_DUP =             r'dup'
    t_2DUP =            r'2dup'

    reserved = {
        'if':       'IF',
        'else':     'ELSE',
        'then':     'THEN',
        'emit':     'EMIT',
        'key':      'KEY',
        'space':    'SPACE',
        'spaces':   'SPACES',
        'char':     'CHAR',
        'cr':       'CR',
        'dup':      'DUP',
        '2dup':     '2DUP'
    }

    def t_PARAM(t):
        r'\(.*--.*\)'
        l = Lexer()
        text = str(t.value)
        m = re.findall(r"\((.*)--(.*)\)", text)
        entradas =re.findall("[a-z][a-z0-9.-]*", m[0][0])
        saidas = re.findall("[a-z][a-z0-9.-]*", m[0][1])
        t.value = [entradas , saidas]
        return t
    
    def t_COMENTARIO(t):
        r'\(.+\)'

    def t_COMENTARIO2(t):
        r'\\.+'

    def t_NAME(t):
        r'[a-z][a-z0-9.-]*'
        if t.value in reserved:
            t.type = reserved.get(t.value)
        return t

    def t_STRING(t):
        r'\".*\"'
        t.value = t.value[1:-1]
        return t
    
    def t_NUMBER(t):
        r'[-|\+]?[0-9]+(\.[0-9]+)?'
        t.value = float(t.value)
        return t

    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)
    
    # Build the lexer from my environment and return it    
    return lex.lex()

def lex_input(lexer, str):
    lexer.input(str.lower())

def main():
    lexer = Lexer()
    for line in sys.stdin:
        # case insensitive
        lex_input(lexer, line.lower())
        for t in lexer:
            print(t)

if __name__ == "__main__":
    main()