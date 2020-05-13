def lexer(prgm_src):    
    verbe = {"est", "sont", "prend", "demander", "saisir", "allant", "variant", "afficher", "affecter"}
    prep = {"à", "la", "le", "que", "de", "entre", "plus", "moins"}
    com = {"si", "alors", "sinon", "pour", "tant", "fin"}
    comp = {"supérieur", "inférieur", "égal", "différent", "grand", "petit", "<", "<=", ">", ">=", "="}
    logi = {"et", "ou"}
    oper = {"+", "-", "*", "/", "%", ",", "\"", "'", "(", ")", "[", "]", "{", "}", "\n", "^"}
    
    detect = [verbe, prep, com, comp, logi, oper]

    mot = prgm_src.split(" ")
    l_token, token = list(), str()
    
    for i in mot:
        for j in range(len(detect)):
            if i.lower() in detect[j]: token = ["VERBE", "PREP", "COM", "COMP", "LOGI", "OPER"][j]
        if i.isdigit(): token = "CHIFFRE"
        elif not len(token): token = "MOT"
        
        l_token.append((token, i))
    return l_token
