import sys
from sly import Lexer

class FloLexer(Lexer):
    # Noms des lexèmes (sauf les litéraux). En majuscule. Ordre non important
    tokens = { IDENTIFIANT, ENTIER, BOOLEAN, ECRIRE , SI, SINON_SI, SINON, TANTQUE, RETOURNER, INFERIEUR_OU_EGAL, EGAL, INFERIEUR, SUPERIEUR, SUPERIEUR_OU_EGAL, DIFFERENT, ET, OU, NON, LIRE, TYPE }

    #Les caractères litéraux sont des caractères uniques qui sont retournés tel quel quand rencontré par l'analyse lexicale.
    #Les litéraux sont vérifiés en dernier, après toutes les autres règles définies par des expressions régulières.
    #Donc, si une règle commence par un de ces littérals (comme INFERIEUR_OU_EGAL), cette règle aura la priorité.
    literals = { '+','*','(',')',';','/','%','-','{','}' }

    # chaines contenant les caractères à ignorer. Ici espace et tabulation
    ignore = ' \t'

    # Expressions régulières correspondant aux différents Lexèmes par ordre de priorité
    #arithmetique

    #comparateur
    EGAL= r'=='
    INFERIEUR= r'<'
    INFERIEUR_OU_EGAL= r'<='
    SUPERIEUR= r'>'
    SUPERIEUR_OU_EGAL= r'>='
    DIFFERENT= r'!='

    @_(r'0|[1-9][0-9]*')
    def ENTIER(self, t):
        t.value = int(t.value)
        return t

    @_(r'Vrai|Faux')
    def BOOLEAN(self, t):
        t.value = "Vrai" if (t.value == "Faux") else "Faux"
        return t

    # cas général
    IDENTIFIANT = r'[a-zA-Z][a-zA-Z0-9_]*' #en général, variable ou nom de fonction

    # cas spéciaux:
    IDENTIFIANT['ecrire'] = ECRIRE
    IDENTIFIANT['si'] = SI
    IDENTIFIANT['sinon si'] = SINON_SI
    IDENTIFIANT['sinon'] = SINON
    IDENTIFIANT['tant que'] = TANTQUE
    IDENTIFIANT['retourner'] = RETOURNER
    IDENTIFIANT['lire'] = LIRE
    IDENTIFIANT['ou'] = OU
    IDENTIFIANT['et'] = ET
    IDENTIFIANT['non'] = NON
    IDENTIFIANT['TYPE'] = TYPE

    #Syntaxe des commentaires à ignorer
    ignore_comment = r'\#.*'

    # Permet de conserver les numéros de ligne. Utile pour les messages d'erreurs
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    # En cas d'erreur, indique où elle se trouve
    def error(self, t):
        print(f'Ligne{self.lineno}: caractère inattendu "{t.value[0]}"')
        self.index += 1

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1],"r") as f:
            data = f.read()
            lexer = FloLexer()
            for tok in lexer.tokenize(data):
                print(tok)
