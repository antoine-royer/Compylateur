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

    def expr(self): return self.sum()
    
    def atome(self, minus = False):
        atm = self.expect(["VAR", "NUM", "LPAR", "MINUS"])
        
        if atm.type == "MINUS": return self.atome(not minus)
        elif atm.type == "VAR":
            if self.token_ahead.type == "LPAR":
                self.expect()
                return Node("Function", atm.value, *self.fct())
            
            if minus: return Node("Operation", "--", Node("Variable", atm.value))
            else: return Node("Variable", atm.value)

        elif atm.type == "NUM":
            return Node("Number", (atm.value, -atm.value)[minus])
        else:
            e = self.expr()
            self.expect("RPAR")
            if minus: return Node("Operation", "--", e)
            else: return e

    def fct(self):
        param = list()
        while self.token_ahead.type != "RPAR":
            if self.token_ahead.type in ("VAR", "NUM", "MINUS"):
                param.append(Node("Parameter", "#{}".format(len(param)+1), self.expr()))
            else: self.expect(["COMMA", "RPAR"])
        return param
    
    def sum(self):
        atomes = [self.product()]

        while self.token_ahead.type in ("PLUS", "MINUS"):
            operator = self.expect()
            atome_after = self.product()
            atomes.append((atome_after, Node("Operation", "-", atome_after))[operator.type == "MINUS"])

        return (Node("Operation", "+", *atomes), atomes[0])[len(atomes) == 1]
            
    def product(self):
        atomes = [self.exp()]
        
        while self.token_ahead.type in ("MULTI", "DIVI"):
            operator = self.expect()
            atome_after = self.exp()
            atomes.append((atome_after, Node("Operation", "1/", atome_after))[operator.type == "DIVI"])

        return (Node("Operation", "*", *atomes), atomes[0])[len(atomes) == 1]

    def exp(self):
        atome_1 = self.atome()
        if self.token_ahead.type != "EXP":
            return atome_1
        op = self.expect()
        atome_2 = self.atome()
        return Node("Operation", op.value, atome_1, atome_2)

# ==================================================
# Lexer
# ================================================== 

# --- Main function --- #

def lexer(prgm_src):    
    token = {
        "(":"LPAR",
        ")":"RPAR",
        "+":"PLUS",
        "-":"MINUS",
        "*":"MULTI",
        "/":"DIVI",
        "^":"EXP",
        ",":"COMMA"}
    
    for i in {"=", "<", "<=", ">", ">=", "+", "-", "/", "*", "^", "(", ")", "[", "]", "{", "}", '"', "\n", ",", ";"}:
        prgm_src = prgm_src.replace(i, " " + i + " ")
    word = [i for i in prgm_src.lower().split(" ") if i != ""]

    l_token = TokenList()
    index, undef = 0, bool()

    while index < len(word):
        undef = True

        for target in token.keys():                
            name = token[target]
               
            if word[index] in target and lexer_detect(word, index, target):
                    l_token.add(Token(name, target))
                    undef = False
                    index += len(target)
                    break
        

        if undef and word[index] == "\"":
            l_token, index = text_detecter(word, index, l_token)
        elif undef:
            if word[index].isdigit():
                l_token.add(Token("NUM", eval(word[index])))
            else:
                l_token.add(Token("VAR", word[index]))
            index += 1
            
    return l_token

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
    par = Parser(l_token)
    ast = Node("Programm", "")
    ast.add_node(par.sum())
    
    
    return ast



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
