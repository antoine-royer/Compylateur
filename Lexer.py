def lexer(prgm_src):
    word = prgm_src.lower().split(" ")
    l_token = list()
    index, undef = 0, bool()
    
    var_type = {"un entier naturel", "des entiers naturels", "un entier relatif", "des entiers relatifs", "une liste", "des listes", "un flottant", "des flottants", "une chaîne de caractères", "des chaînes de caractères"}
    cmnd = {"si", "alors", "sinon", "tant que", "tantque", "pour"}
    optr = {"+", "-", "/", "*", "^"}
    sptr = {"et", ",", ";", "(", ")", "[", "]", "{", "}", "\"", "\n"}
    comp = {"est supérieur à", "est supérieur ou égal à", "est inférieur à", "est inférieur ou égal à", "est différent de", "est égal à"}
    user = {"saisir", "saisir la valeur de", "saisir les valeurs de", "demander la valeur de", "demander à l'utilisateur la valeur de"}
    logi = {"et que", "ou que"}
    assi = {"prend la valeur", "sont", "est"}
    
    rang = {"allant de # à", "variant entre # et", "variant de # à"}
    

    token = (var_type, cmnd, optr, comp, user, logi, assi, sptr)
    name = ("TYPE", "CMND", "OPTR", "COMP", "USER", "LOGI", "ASSI", "SPTR")

    while index < len(word):
        undef = True
        for j in range(len(token)):
            for k in token[j]:
                
                target = k.split(" ")
        
                if word[index] in target and detect(word, index, target):
                    l_token.append((name[j], k))
                    undef = False
                    index += len(target)-1
                    
        if undef:l_token.append(("UNDEF", word[index]))
        index += 1         
    
    return l_token
 
def detect(mot, index, target):
    try:
        return not 0 in [target[i] == mot[i + index] for i in range(len(target))]
    except:
        return 0

