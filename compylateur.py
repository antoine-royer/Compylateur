# --------------------------------------------------
# Compylateur (Version 0.0)
# By Sha-Chan
# April - May 2020
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
    def __init_(self, token_type, token_value):
        self.type = token_type
        self.value = token_value

    def type(self):
        return self.type

    def value(self):
        return self.value

class TokenList():
    def __init__(self, l_token = []):
        self.index = -1
        self.list = l_token
        
    def add(self, token):
        self.list.append(token)

    def get(self, jump = 1):
        self.index += jump
        if self.index < len(self.list):
            return self.list[self.index]
        else:
            return False

# --- Abstract Syntax Tree (AST) --- #

class AST():
    def __init__(self):
        self.branch = list()

    def add_branch(self, branch):
        self.branch.append(branch)

class Branch():
    def __init__(self, title, value, *sub_branch):
        self.title = title
        self.value = value
        self.sub_branch = list(sub_branch)

    def add_sub_branch(self, *sub_branch):
        for i in sub_branch: self.sub_branch.append(i)

    def generate(self):
        return self.title, self.value, self.sub_branch

# ==================================================
# Lexer
# ================================================== 

# --- Main function --- #

def lexer(prgm_src):    
    var_type = {"des réels", "un réel", "des entiers", "un entiers", "un entier naturel", "des entiers naturels", "un entier relatif", "des entiers relatifs", "une liste", "des listes", "un flottant", "des flottants", "une chaîne de caractères", "des chaînes de caractères"}
    cmnd = {"fin", "finsi", "fin si", "fintantque", "fin tantque", "fin tant que", "finpour", "fin pour", "afficher", "si", "alors", "sinon", "tant que", "tantque", "pour"}
    optr = {"+", "-", "/", "*", "^"}
    sptr = {"et", "(", ")", "[", "]", "{", "}", "\"", "\n", "à", "entre", "de", ",", ";", "faire"}
    comp = {"=", "<", "<=", ">", ">=", "est supérieur à", "est supérieur ou égal à", "est inférieur à", "est inférieur ou égal à", "est différent de", "est égal à"}
    user = {"saisir", "saisir la valeur de", "saisir les valeurs de", "demander la valeur de", "demander à l'utilisateur la valeur de"}
    logi = {"et que", "ou que"}
    assi = {"prend la valeur", "sont", "est"}
    rang = {"allant", "variant"}
    
    for i in {"=", "<", "<=", ">", ">=", "+", "-", "/", "*", "^", "(", ")", "[", "]", "{", "}", "\"", "\n", ",", ";"}:
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
        

        if undef:
            l_token.add(Token(("UNDEF", "NUM")[word[index].isdigit()], word[index]))
            index += 1

# --- Secondary functions --- #

def lexer_detect(mot, index, target):
    try:
        return not 0 in [target[i] == mot[i + index] for i in range(len(target))]
    except:
        return 0

# ==================================================
# Parser
# ==================================================

# --- Main function --- #

def parser(l_token):
    token_see = l_token.get()

# --- Secondary functions --- #

def expect(target = [], l_token):
    last = token_see
    token_see = l_token.get()
    if target != [] and last.type() not in target:
        raise SyntaxError("unknown operand, one of these is expected : " + ", ".join(target))
    return last

