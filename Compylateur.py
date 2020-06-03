# --------------------------------------------------
# Compylateur (Version dev)
# By Sha-Chan~ 
# from April to June 2020
#
# Code provided with licence (CC BY-NC-ND 4.0)
# For more informations about licence :
# https://creativecommons.org/licenses/by-nc-nd/4.0/
# --------------------------------------------------


# ==================================================
# Objects code
# ==================================================

# --- Tokens --- #

class Token():
    def __init__(self, token_type = "", token_value = ""):
        self.type = token_type
        self.value = token_value

class TokenList():
    def __init__(self):
        self.index = 0
        self.list = list()
        
    def add(self, token):
        self.list.append(token)

    def next(self):
        self.index += 1
        if self.index < len(self.list):
            return self.list[self.index]
        else:
            return Token()

    def generate(self):
        for i in self.list: print((i.type, i.value))

# --- Abstract Syntax Tree (AST) --- #

class Node():
    def __init__(self, node_type, node_value, *sub_node):
        self.type = node_type
        self.value = node_value
        self.sub_node = list(sub_node)

    def add_node(self, *sub_node):
        for i in sub_node: self.sub_node.append(i)

    def gen(self):
        return self.type, self.value, self.sub_node
    

def AST_gen(node, tab = 0):
    for i in node:
        print(tab * "  " + "{0} : {1}".format(i.gen()[0], i.gen()[1]))
        if i.gen()[2]: AST_gen(i.gen()[2], tab + 1)

# --- Parser --- #

class Parser():
    def __init__(self, l_token):
        self.l_token = l_token
        self.token_ahead = l_token.list[0]

    def expect(self, target = []):
        last = self.token_ahead
        self.token_ahead = self.l_token.next()
        if target != [] and last.type not in target:
            raise SyntaxError("This operand was not expected : '{0}' (for dev : {1})".format(last.value, target))
        return last

    def atome(self):
        return self.expect(["VAR", "NUM"])
        

# ==================================================
# Lexer
# ================================================== 

# --- Main function --- #

def lexer(prgm_src):    
    var_type = {"des réels", "un réel", "des entiers", "un entiers", "un entier naturel", "des entiers naturels", "un entier relatif", "des entiers relatifs", "une liste", "des listes", "un flottant", "des flottants", "une chaîne de caractères", "des chaînes de caractères"}
    cmnd = {"fin", "finsi", "fin si", "fintantque", "fin tantque", "fin tant que", "finpour", "fin pour", "afficher", "si", "alors", "sinon", "tant que", "tantque", "pour"}
    optr = {"+", "-", "/", "*", "^"}
    sptr = {"et", "(", ")", "[", "]", "{", "}", "\n", "à", "entre", "de", ",", ";", "faire"}
    comp = {"=", "<", "<=", ">", ">=", "est supérieur à", "est supérieur ou égal à", "est inférieur à", "est inférieur ou égal à", "est différent de", "est égal à"}
    user = {"saisir", "saisir la valeur de", "saisir les valeurs de", "demander la valeur de", "demander à l'utilisateur la valeur de"}
    logi = {"et que", "ou que"}
    assi = {"prend la valeur", "sont", "est"}
    rang = {"allant", "variant"}
    
    for i in {"=", "<", "<=", ">", ">=", "+", "-", "/", "*", "^", "(", ")", "[", "]", "{", "}", '"', "\n", ",", ";"}:
        prgm_src = prgm_src.replace(i, " " + i + " ")
    word = [i for i in prgm_src.lower().split(" ") if i != ""]

    l_token = TokenList()
    index, undef = 0, bool()

    token = (var_type, cmnd, optr, comp, user, logi, assi, sptr, rang)
    name = ("TYPE", "CMND", "OPTR", "COMP", "USER", "LOGI", "ASSI", "SPTR", "RANG")

    while True:
        undef = True
        for j in range(len(token)):
            for k in token[j]:
                
                target = k.split(" ")
                
                if index >= len(word): return l_token
                
                if word[index] in target and lexer_detect(word, index, target):
                        l_token.add(Token(name[j], k))
                        undef = False
                        index += len(target)
        

        if undef and word[index] == "\"":
            l_token, index = text_detecter(word, index, l_token)
        elif undef:
            l_token.add(Token(("VAR", "NUM")[word[index].isdigit()], word[index]))
            index += 1

# --- Secondary functions --- #

def lexer_detect(word, index, target):
    try:
        return not 0 in [target[i] == word[i + index] for i in range(len(target))]
    except:
        return 0

def text_detecter(word, index, l_token):
    txt = word[index]
    index += 1
    while word[index] != '"':
        txt = txt + " " + word[index]
        index += 1
    l_token.add(Token("TEXT", txt + ' "'))
    return l_token, index + 1

    

# ==================================================
# Parser
# ==================================================

# --- Main function --- #

def parser(l_token):
    parser = Parser(l_token)
    ast = Node("Programm", "")
    
    ast.add_node(expr(parser, []))
    
    return ast

# --- Grammar detection functions --- #
# (only test functions for the moment)


def expr(parser, expr_backward):
    expr_backward.append(parser.atome())
    expr_backward.append(parser.expect(["OPTR"]))
    expr_backward.append(parser.atome())
    
    return Node("Operation", expr_backward[1].value, Node(("Variable", "Number")[expr_backward[0].value.isdigit()], expr_backward[0].value), Node(("Variable", "Number")[expr_backward[2].value.isdigit()], expr_backward[2].value))
    

# --- Secondary functions --- #
# (empty for the moment)

# ==================================================
# Miscellaneous functions
# ==================================================

def compylateur(code):
    
    l_token = lexer(code)
    print("--- Tokens ---")
    l_token.generate()
    
    ast = parser(l_token)
    print("\n\n--- AST ---")
    AST_gen(ast.sub_node)
