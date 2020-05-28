def lexer(prgm_src):    
    var_type = {"un entier naturel", "des entiers naturels", "un entier relatif", "des entiers relatifs", "une liste", "des listes", "un flottant", "des flottants", "une chaîne de caractères", "des chaînes de caractères"}
    cmnd = {"afficher", "si", "alors", "sinon", "tant que", "tantque", "pour", "fin", "finsi", "fin si", "fintantque", "fin tantque", "fin tant que", "finpour", "fin pour"}
    optr = {"+", "-", "/", "*", "^"}
    sptr = {"et", "(", ")", "[", "]", "{", "}", "\"", "\n", "à", "entre", "de", ",", ";", "faire"}
    comp = {"est supérieur à", "est supérieur ou égal à", "est inférieur à", "est inférieur ou égal à", "est différent de", "est égal à"}
    user = {"saisir", "saisir la valeur de", "saisir les valeurs de", "demander la valeur de", "demander à l'utilisateur la valeur de"}
    logi = {"et que", "ou que"}
    assi = {"prend la valeur", "sont", "est"}
    rang = {"allant", "variant"}
    
    for i in {"+", "-", "/", "*", "^", "(", ")", "[", "]", "{", "}", "\"", "\n", ",", ";"}:
        prgm_src = prgm_src.replace(i, " " + i + " ")
    word = [i for i in prgm_src.lower().split(" ") if i != ""]

    l_token = list()
    index, undef = 0, bool()

    token = (var_type, cmnd, optr, comp, user, logi, assi, sptr, rang)
    name = ("TYPE", "CMND", "OPTR", "COMP", "USER", "LOGI", "ASSI", "SPTR", "RANG")

    while True:
        undef = True
        for j in range(len(token)):
            for k in token[j]:
                
                target = k.split(" ")
                
                if index >= len(word): return l_token
                
                if word[index] in target and detect(word, index, target):
                        l_token.append((name[j], k))
                        undef = False
                        index += len(target)
        

        if undef:
            l_token.append((("UNDEF", "NUM")[word[index].isdigit()], word[index]))
            index += 1


def detect(mot, index, target):
    try:
        return not 0 in [target[i] == mot[i + index] for i in range(len(target))]
    except:
        return 0

