#---------------------------------------------------------------------------------------------------------------
# Programme de chiffrement / déchiffrement d'un message
# L'utilisateur choisit s'il veut chiffrer ou déchiffrer, puis une méthode
# (César, ROT13, Vigenère ou carré de Polybe), puis tape son message.
#---------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------
# Valeurs par défaut (utilisées si l'utilisateur appuie seulement sur Entrée)
#---------------------------------------------------------------------------------------------------------------
DECALAGE_DEFAUT = 4
CLE_DEFAUT = "BIRAH"

#---------------------------------------------------------------------------------------------------------------
# 1) Code César
#---------------------------------------------------------------------------------------------------------------

# Chiffrement : chaque lettre est décalée de s positions dans l'alphabet.
# Exemple avec s = 3 : A -> D, B -> E, ..., Z -> C (on revient au début grâce au modulo 26).
def encoder_code_cesar(text, s):
    result = ""
    for char in text:
        if 'A' <= char <= 'Z':
            # ord(char) - 65 : position de la lettre dans l'alphabet (A = 0, ..., Z = 25)
            # + s           : on décale
            # % 26          : on revient à A si on dépasse Z
            # + 65          : on retrouve le code ASCII de la nouvelle lettre majuscule
            result += chr((ord(char) - 65 + s) % 26 + 65)
        elif 'a' <= char <= 'z':
            # Même principe pour les minuscules (code ASCII de 'a' = 97)
            result += chr((ord(char) - 97 + s) % 26 + 97)
        else:
            # Espaces, ponctuation, chiffres, accents : on les garde tels quels
            result += char
    return result


# Déchiffrement : on décale dans l'autre sens, donc de -s.
# Le modulo 26 de Python donne toujours un résultat positif : (0 - 3) % 26 = 23, donc D -> A et A -> X.
def decoder_code_cesar(text, s):
    return encoder_code_cesar(text, -s)


#---------------------------------------------------------------------------------------------------------------
# 2) ROT13
#---------------------------------------------------------------------------------------------------------------

# ROT13 est un code César avec un décalage fixe de 13.
def encoder_rot13(text):
    return encoder_code_cesar(text, 13)


# Déchiffrement : 13 + 13 = 26, un tour complet de l'alphabet.
# Appliquer ROT13 une 2e fois redonne donc le message d'origine : c'est la même fonction.
def decoder_rot13(text):
    return encoder_rot13(text)


#---------------------------------------------------------------------------------------------------------------
# 3) Code de Vigenère
#---------------------------------------------------------------------------------------------------------------

# Fonction commune au chiffrement et au déchiffrement.
# sens = +1 pour chiffrer (on ajoute le décalage), -1 pour déchiffrer (on le retire).
# Le décalage change à chaque lettre : il est donné par les lettres de la clé, répétée autant que nécessaire.
# Exemple avec la clé "CLE" : 1re lettre décalée de C (2), 2e de L (11), 3e de E (4), 4e de C (2)...
def vigenere(message, key, sens):
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = key.upper()          # la clé est mise en majuscules pour être trouvée dans LETTERS
    res = ""
    key_index = 0              # position de la lettre de la clé à utiliser
    for s in message:
        num = LETTERS.find(s.upper())   # position de la lettre du message (-1 si ce n'est pas une lettre)
        if num != -1:
            decalage = LETTERS.find(key[key_index])   # décalage donné par la lettre de la clé
            num = (num + sens * decalage) % 26        # on ajoute (ou retire) le décalage en restant dans l'alphabet
            res += LETTERS[num]
            key_index = (key_index + 1) % len(key)    # lettre suivante de la clé ; on revient au début à la fin
        else:
            res += s           # les caractères qui ne sont pas des lettres sont gardés, et la clé n'avance pas
    return res


def encoder_code_vigenere(message, key):
    return vigenere(message, key, 1)


def decoder_code_vigenere(message, key):
    return vigenere(message, key, -1)


#---------------------------------------------------------------------------------------------------------------
# 4) Carré de Polybe
#---------------------------------------------------------------------------------------------------------------
# L'alphabet est rangé dans une grille 5 x 5. 25 cases pour 26 lettres : I et J partagent la même case.
#
#        1 2 3 4 5
#     1  A B C D E
#     2  F G H I K
#     3  L M N O P
#     4  Q R S T U
#     5  V W X Y Z
#
GRILLE = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'   # l'alphabet sans le J, lu ligne par ligne


# Chiffrement : chaque lettre devient son numéro de ligne suivi de son numéro de colonne.
# Exemple : B -> 12 (ligne 1, colonne 2), K -> 25, J -> 24 (comme I)
def encoder_carre_polybe(message):
    res = ""
    for s in message.upper():
        if s == 'J':
            s = 'I'                         # J est codé comme I
        pos = GRILLE.find(s)
        if pos != -1:
            ligne = pos // 5 + 1            # division entière : numéro de la ligne
            colonne = pos % 5 + 1           # reste : numéro de la colonne
            res += str(ligne) + str(colonne) + " "
        elif s == " ":
            res += "/ "                     # on marque la séparation entre les mots
    return res.strip()                      # on enlève l'espace en trop à la fin


# Déchiffrement : on lit les chiffres deux par deux (ligne, colonne) et on retrouve la lettre dans la grille.
# Accepte "43 11 31 / 12" comme "43113112" : les espaces sont ignorés, "/" sépare les mots.
# Attention : un I déchiffré peut avoir été un J à l'origine (même case).
def decoder_carre_polybe(message):
    mots = message.split("/")               # un morceau par mot
    res = []
    for mot in mots:
        chiffres = mot.replace(" ", "")     # on enlève les espaces : il ne reste que les chiffres
        if len(chiffres) % 2 != 0:
            return "Erreur : il faut un nombre pair de chiffres (ligne + colonne)"
        texte = ""
        for i in range(0, len(chiffres), 2):    # on avance de 2 en 2
            ligne = int(chiffres[i])
            colonne = int(chiffres[i + 1])
            if not (1 <= ligne <= 5 and 1 <= colonne <= 5):
                return "Erreur : lignes et colonnes doivent être entre 1 et 5"
            pos = (ligne - 1) * 5 + (colonne - 1)   # calcul inverse : position dans GRILLE
            texte += GRILLE[pos]
        res.append(texte)
    return " ".join(res)                    # on remet un espace entre les mots


#---------------------------------------------------------------------------------------------------------------
# Sous-programmes de dialogue avec l'utilisateur
#---------------------------------------------------------------------------------------------------------------

# Demande s'il faut chiffrer ou déchiffrer, renvoie le choix tapé (sous forme de chaîne)
def choix_mode():
    print("Que voulez-vous faire ?")
    print("  1 - Chiffrer")
    print("  2 - Déchiffrer")
    return input("Votre choix (1 ou 2) : ")


# Affiche le menu des méthodes et renvoie le choix tapé (sous forme de chaîne)
def choix_encodage():
    print("Choisissez une méthode :")
    print("  1 - Code César (décalage par défaut = " + str(DECALAGE_DEFAUT) + ")")
    print("  2 - ROT13")
    print("  3 - Code de Vigenère (clé par défaut = " + CLE_DEFAUT + ")")
    print("  4 - Carré de Polybe")
    return input("Votre choix (1 à 4) : ")


# Demande le message
def entrer_message():
    message = input("Entrez le message : ")
    if message == "":
        print("Le message est vide.")
    return message


# Demande le décalage ; Entrée seule = valeur par défaut
def entrer_decalage():
    s = input("Valeur de décalage (Entrée = " + str(DECALAGE_DEFAUT) + ") : ")
    if s == "":
        return DECALAGE_DEFAUT
    return int(s)       # provoque une ValueError si ce n'est pas un entier (capturée dans main)


# Demande la clé ; Entrée seule = clé par défaut
def entrer_cle():
    key = input("Clé, lettres uniquement (Entrée = " + CLE_DEFAUT + ") : ")
    if key == "":
        return CLE_DEFAUT
    if not key.isalpha():
        print("La clé ne doit contenir que des lettres (sans accent).")
        return ""
    return key


# Appelle la bonne fonction selon le mode (1 = chiffrer, 2 = déchiffrer) et la méthode choisie
def traiter(mode, choix, message):
    if choix == 1:
        s = entrer_decalage()
        if mode == 1:
            return encoder_code_cesar(message, s)
        return decoder_code_cesar(message, s)
    elif choix == 2:
        if mode == 1:
            return encoder_rot13(message)
        return decoder_rot13(message)
    elif choix == 3:
        key = entrer_cle()
        if key == "":
            return ""
        if mode == 1:
            return encoder_code_vigenere(message, key)
        return decoder_code_vigenere(message, key)
    else:
        if mode == 1:
            return encoder_carre_polybe(message)
        return decoder_carre_polybe(message)


#---------------------------------------------------------------------------------------------------------------
# Programme principal
#---------------------------------------------------------------------------------------------------------------
def main():
    try:
        mode = int(choix_mode())            # int() provoque une ValueError si ce n'est pas un nombre
        if mode != 1 and mode != 2:
            print("Vous devez choisir 1 ou 2")
            return
        choix = int(choix_encodage())
        if choix < 1 or choix > 4:
            print("Vous devez faire un choix entre 1 et 4")
            return
        message = entrer_message()
        if message == "":
            return
        res = traiter(mode, choix, message)
        if res == "":
            return
        if mode == 1:
            titre = "MESSAGE CRYPTE : "
        else:
            titre = "MESSAGE DECRYPTE : "
        print("\n####################################\n")
        print(titre + res)
        print("\n####################################\n")
    except ValueError:
        # Ne capture que l'erreur de conversion en entier (mode, choix ou décalage)
        print("Vous devez saisir un nombre entier")


# Ce bloc ne s'exécute que si on lance ce fichier directement (pas s'il est importé dans un autre)
if __name__ == "__main__":
    main()
