code = str()

def enter(nb_ligne = 1):
  decod = {"est superieur a@est superieur ou":">", "est inferieur a@est inferieur ou":"<", "est different de":"!=", "=@est egal a":"==", " egal,1+":"& ", "saisir la valeur de @saisir @demander la valeur de ":"float(input('", "prend la valeur@la valeur":"&", "tant que ":"while ", "si ":"if ", "pour ":"for ", "allant de @variant de @de ":"in range(", " a @ jusque ":",1+", "afficher ":"print(", "alors @ faire@affecter,1+":"", "sinon ":"else:"}
  ligne, debut = ['from math import *'], list()
  for i in range(nb_ligne):ligne.append(input("\nligne {0} / {1}\n".format(i+1, nb_ligne)))

  for i in range(len(ligne)):
    for j in decod.keys():
      for k in j.split("@"):
        ligne[i] = ligne[i].replace(k, decod[j])
    ligne[i] = ligne[i].replace("&","=")
    if " est " in ligne[i] or " sont " in ligne[i]: 
      ligne[i] = (ligne[i][:(ligne[i].find("est"), ligne[i].find("sont"))["sont" in ligne[i]]] + "=").replace(" et ", ", ")
      for j in range(len(ligne[i].split(","))):ligne[i] += " int(),"
      ligne[i] = ligne[i][:-1]
      
    if not ligne[i].find("float(input("):
      k = str()
      ligne[i] = ligne[i].replace(" et ",",")
      for j in range(len(ligne[i][13:].split(","))):
        k += ligne[i][13:].split(",")[j].replace(" ","") + " = float(input('" + ligne[i][13:].split(",")[j].replace(" ","") + " : '))\n"
      ligne[i] = k[:-1]
    if "if" in ligne[i] or "while" in ligne[i]:
      ligne[i] += ":"
      debut.append(i)
    if "for" in ligne[i]:
      ligne[i] += "):"
      debut.append(i)
    if "print" in ligne[i]:
      ligne[i] += ")"
  
  if len(debut):ligne = alinea(ligne, debut)
  rslt = str()
  for i in ligne:
    if len(i):rslt += "\n"+i
  return rslt[1:]
    
def alinea(ligne, debut):
  for i in range(len(ligne)):
    if not ligne[i].find("fin"):break
  ligne[i] = ""
  for j in debut:
    for k in range(j+1, i):
      ligne[k] = "  " + ligne[k]
      if "else:" in ligne[k]:ligne[k] = "else:\n  " + ligne[k][7:] 
  return ligne

def run():
  global code
  code = enter(int(input("Nombre de ligne du code :\n> ")))
  print("\n'go()' pour executer le code\nApercu du code python :\n")
  print(code)

def go():
  exec(code)
  
print("Entrez 'run()' pour enregistrer\nle code\nEntrez 'go()' pour l'executer")