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
# Tokens and Abstract syntax tree
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
        print(tab * "    " + "{0} : {1}".format(i.gen()[0], i.gen()[1]))
        if i.gen()[2]: AST_gen(i.gen()[2], tab + 1)   

# ==================================================
# Lexer
# ================================================== 

# --- Main function --- #

def lexer(prgm_src):
    prgm_src = prgm_src.replace("\n", " ")
    token = {
        "(":"LPAR",
        ")":"RPAR",
        "+":"PLUS",
        "-":"MINUS",
        "*":"MULTI",
        "/":"DIVI",
        "^":"EXP",
        ",":"COMMA",
        "=":"EQUAL",
        "est supérieur à":"SUP", ">":"SUP", "est plus grand que":"SUP",
        "est supérieur ou égal à":"SUP_EGA", ">=":"SUP_EGA", "≥":"SUP_EGA", "est plus grand ou égal à":"SUP_EGA",
        "est inférieur à":"INF", "<":"INF", "≤":"INF_EGA", "est plus petit que":"INF",
        "est inférieur ou égal à":"INF_EGA", "<=":"INF_EGA", "est plus petit ou égal à":"INF_EGA",
        "est égal à":"EGA", "==":"EGA", "égal":"EGA", "égale":"EGA",
        "est différent de":"DIF", "!=":"DIF", "≠":"DIF",
        "ou":"OR",
        "et":"AND",
        "affecter à":"AFFECT", "prend la valeur":"TAKE", "est initialisé à":"TAKE",
        "afficher":"DISPLAY",
        "demander la valeur de":"REQUEST", "on demande la valeur de":"REQUEST", "saisir la valeur de":"REQUEST", "saisir":"REQUEST", "à l'utilisateur":"USER", "la valeur":"VALUE",
        "fin si":"END_IF", "fin pour":"END_FOR", "fin tant que":"END_WHILE", "fin tantque":"END_WHILE", "faire":"DO",
        "si":"IF", "alors":"THEN", "sinon , si":"ELIF", "sinon":"ELSE",
        "pour":"FOR", "allant de":"INTER_ST", "variant entre":"INTER_ST", "variant de":"INTER_ST", "à":"INTER_ED", "jusqu'à":"INTER_ED",
        "tant que":"WHILE", "tantque":"WHILE"}
    
    for i in {"=", "<", "<=", ">", ">=", "+", "-", "/", "*", "^", "(", ")", "[", "]", "{", "}", '"', "\n", ",", ";"}:
        prgm_src = prgm_src.replace(i, " " + i + " ")
    word = [i for i in prgm_src.lower().split(" ") if i != ""]

    l_token = TokenList()
    index, undef = 0, bool()

    while index < len(word):
        undef = True

        for target in token.keys():                
            name, value, target = token[target], target, target.split(" ")
        
            if word[index] == target[0] and lexer_detect(word, index, target):
                    l_token.add(Token(name, value))
                    undef = False
                    index += len(target)
                    break
        

        if undef and word[index] == '"':
            l_token, index = text_detecter(word, index + 1, l_token)
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
    l_token.add(Token("TEXT", '"' + txt + '"'))
    return l_token, index + 1

# ==================================================
# Parser
# ==================================================

class Parser():
    def __init__(self, l_token):
        self.l_token = l_token
        self.token_ahead = l_token.list[0]

    def expect(self, *target):
        last = self.token_ahead
        self.token_ahead = self.l_token.next()
        if target != () and last.type not in target:
            raise SyntaxError("This operand was not expected : '{0}' (for dev : {1})".format(last.value, target))
        return last

    # --- Arithmetic's rules --- #
    
    def expr(self): return self.sum()
    
    def atome(self, minus = False):
        atm = self.expect("VAR", "NUM", "LPAR", "MINUS")
        
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
        param.append(self.expr())
        if self.token_ahead.type == "RPAR":
          break
        self.expect("COMMA")
      self.expect("RPAR")
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

    # --- Comparison and Condition's rules --- #
    
    def condition(self): return self.condition_or()

    def condition_or(self):
        elmnt_1 = self.condition_and()
        if self.token_ahead.type != "OR": return elmnt_1
        self.expect()
        elmnt_2 = self.condition_and()
        return Node("Condition", "OR", elmnt_1, elmnt_2)

    def condition_and(self):
        elmnt_1 = self.comparison_1()
        if self.token_ahead.type != "AND": return elmnt_1
        self.expect()
        elmnt_2 = self.comparison_1()
        return Node("Condition", "AND", elmnt_1, elmnt_2)

    def comparison_1(self):
        elmnt_1 = self.comparison_2()
        if self.token_ahead.type not in ("EGA", "DIF"): return elmnt_1
        comp = self.expect()
        elmnt_2 = self.comparison_2()
        return Node("Comparison", comp.type, elmnt_1, elmnt_2)
        
    def comparison_2(self):
        elmnt_1 = self.expr()
        if self.token_ahead.type not in ("SUP", "SUP_EGA", "INF", "INF_EGA"): return elmnt_1
        comp = self.expect()
        elmnt_2 = self.expr()
        return Node("Comparison", comp.type, elmnt_1, elmnt_2)

    # --- Statements's rules --- #

    def block(self):
        ast = Node("Block", "")
        while self.token_ahead.type in ("AFFECT", "REQUEST", "VAR", "DISPLAY", "IF", "FOR", "WHILE"):
            ast.add_node(self.statement())
        return ast
        
    
    def statement(self):
        if self.token_ahead.type in ("AFFECT", "REQUEST", "VAR"): return self.assignement()
        elif self.token_ahead.type == "DISPLAY": return self.display()
        elif self.token_ahead.type == "IF": return self.statement_if()
        elif self.token_ahead.type == "FOR": return self.statement_for()
        elif self.token_ahead.type == "WHILE": return self.statement_while()

    def assignement(self):
        value = None
        
        if self.token_ahead.type == "REQUEST":
            self.expect()
            var = self.expect("VAR")
            if self.token_ahead.type == "USER": self.expect()
            return Node("User's request", "", Node("Variable", var.value))

        if self.token_ahead.type == "AFFECT":
            self.expect()
            var = self.expect("VAR")
            self.expect("VALUE")
            value = self.expr()
        
        elif self.token_ahead.type == "VAR":
            var = self.expect()
            self.expect("TAKE")
            value = self.expr()
            
        return Node("Assignement","", Node("Variable", var.value), value)

    def display(self):
        self.expect()
        text = Node("Display", "")
        if self.token_ahead.type in ("VAR", "NUM", "LPAR"):
            text.add_node(Node("Expression", "", self.expr()))
        else:
            text.add_node(Node("Text", self.expect("TEXT").value))
        
        while self.token_ahead.type == "COMMA":
            self.expect()
            if self.token_ahead.type in ("VAR", "NUM", "LPAR"):
                text.add_node(Node("Expression", "", self.expr()))
            else:
                text.add_node(Node("Text", self.expect("TEXT").value))
        return text

    def statement_if(self):
        self.expect()
        cond_1 = self.condition()
        self.expect("THEN", "COMMA", "DO")
        block_1 = self.block()
        ast = [cond_1, block_1]
        while self.token_ahead.type == "ELIF":
            self.expect()
            ast.append(self.condition())
            self.expect("THEN", "COMMA", "DO")
            ast.append(self.block())
        if self.token_ahead.type == "ELSE":
            self.expect()
            ast.append((self.block()))
        
        self.expect("END_IF")
        return Node("Statement", "if", *ast)

        

    def statement_for(self):
        self.expect()
        it_var = self.expect("VAR")
        self.expect("INTER_ST")
        start_value = self.expr()
        self.expect("INTER_ED")
        end_value = self.expr()
        self.expect("COMMA", "DO")
        ast = Node("Statement", "for", Node("Incremented variable", it_var.value), Node("Start value", start_value.value), Node("End value", end_value.value))
        ast.add_node(self.block())
        self.expect("END_FOR")
        return ast

    def statement_while(self):
        self.expect()
        condition = self.condition()
        self.expect("COMMA", "DO")
        block = self.block()
        self.expect("END_WHILE")
        return Node("Statement", "while", condition, block)            

# --- Secondary functions --- #

def parser(l_token):
    par = Parser(l_token)
    ast = Node("Programm", "")
    ast.add_node(par.block())
    
    return ast

# ==================================================
# Miscellaneous functions
# ==================================================

def compylateur(code, file = False):
    if file: code = open(code + ".txt", 'r').read()
    
    l_token = lexer(code)
    print("--- Tokens ---")
    l_token.generate()
    
    ast = parser(l_token)
    print("\n\n--- AST ---")
    AST_gen(ast.sub_node)
