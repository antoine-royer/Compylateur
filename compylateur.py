# --------------------------------------------------
# Compylateur (Version 0.0)
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
        self.index = -1
        self.list = list()
        
    def add(self, token):
        self.list.append(token)

    def next(self, jump = 1):
        self.index += jump
        if self.index < len(self.list):
            return self.list[self.index]
        else:
            return self.list[-1]

    def generate(self):
        index = 0
        while index < len(self.list):
            print((self.list[index].type, self.list[index].value))
            index += 1

# --- Abstract Syntax Tree (AST) --- #

class AST():
    def __init__(self):
        self.branch = list()

    def add_branch(self, branch):
        self.branch.append(branch)

    def generate(self):
        for i in self.branch:
            print(i)

class Branch():
    def __init__(self, title, value, *sub_branch):
        self.title = title
        self.value = value
        self.sub_branch = list(sub_branch)

    def add_sub_branch(self, *sub_branch):
        for i in sub_branch: self.sub_branch.append(i)

    def generate(self):
        return self.title, self.value, self.sub_branch

# --- Parser --- #

class Parser():
    def __init__(self, l_token):
        self.l_token = l_token
        self.token_ahead = Token()

    def expect(self, target = []):
        last = self.token_ahead
        self.token_ahead = self.l_token.next()
        if target != [] and self.token_ahead.type not in target:
            raise SyntaxError("unknown operand, one of these is expected : " + ", ".join(target))
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
                
                if index >= len(word):
                    l_token.generate()
                    return l_token
                
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
    
    somme(parser)

# --- Grammar detection functions --- #
# (only tests function for the moment)


def somme(parser):
    atome_1 = parser.atome()
    if parser.token_ahead.value == "+":
        parser.expect(["OPTR"])
        atome_2 = atome()
        

# --- Secondary functions --- #
    

# ==================================================
# Tests functions
# ==================================================

def compylateur(code):
    l_token = lexer(code)
    print(parser(l_token))
