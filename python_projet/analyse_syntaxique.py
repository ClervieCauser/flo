import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait

class FloParser(Parser):
    # On récupère la liste des lexèmes de l'analyse lexicale
    tokens = FloLexer.tokens
    debugfile = "parser.out"
    # Règles gramaticales et actions associées

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p[0])

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p[0])
        return l

    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p[1].instructions.append(p[0])
        return p[1]

    @_('ecrire')
    def instruction(self, p):
        return p[0]

    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr) #p.expr = p[2]

    @_('somme "+" produit')
    def somme(self, p):
        return arbre_abstrait.Operation('+',p[0],p[2])

    @_('somme "-" produit')
    def somme(self, p):
        return arbre_abstrait.Operation('-',p[0],p[2])

    @_('produit "*" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('*',p[0],p[2])

    @_('produit "/" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('/',p[0],p[2])

    @_('produit "%" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('%', p[0], p[2])

    @_('produit')
    def somme(self,p):
        return p.produit

    @_('"(" expr ")"')
    def facteur(self, p):
        return p[1]

    @_('"-" facteur')
    def produit(self, p):
        return arbre_abstrait.Operation('*',arbre_abstrait.Entier(-1),p[1])

    @_('facteur')
    def produit(self, p):
        return p.facteur

    @_('ENTIER')
    def facteur(self, p):
        return arbre_abstrait.Entier(p.ENTIER) #p.ENTIER = p[0]

    @_('LIRE "(" ")"')
    def facteur(self, p):
        return arbre_abstrait.Lire()

    @_('conjonction')
    def expr(self, p):
        return p.conjonction
    
    @_('disjonction')
    def conjonction(self, p): 
        return p.disjonction
    
    @_('neg')
    def disjonction(self, p):
        return p.neg
    @_('booleen')
    def neg(self, p):
        return p.booleen

    @_('BOOLEAN')
    def booleen(self, p):
        return arbre_abstrait.Bool(p[0])

    @_('somme')
    def booleen(self, p):
        return p.somme

    @_('variable')
    def facteur(self, p):
        return p.variable

    @_('IDENTIFIANT')
    def variable(self, p):
        return arbre_abstrait.Variable(p.IDENTIFIANT)

    @_('NON neg')
    def neg(self, p):
        return arbre_abstrait.Negation(p[1])

    @_('disjonction ET neg')
    def disjonction(self, p):
        return arbre_abstrait.Disjonction(p[0], p[2])

    @_('conjonction OU disjonction')
    def conjonction(self, p):
        return arbre_abstrait.Conjonction(p[0], p[2])

    @_('somme INFERIEUR somme')
    def expr(self, p):
        return arbre_abstrait.Comparaison('<', p[0], p[2])

    @_('somme INFERIEUR_OU_EGAL somme')
    def expr(self, p):
        return arbre_abstrait.Comparaison('<=', p[0], p[2])

    @_('somme SUPERIEUR somme')
    def expr(self, p):
        return arbre_abstrait.Comparaison('>', p[0], p[2])

    @_('somme SUPERIEUR_OU_EGAL somme')
    def expr(self, p):
        return arbre_abstrait.Comparaison('>=', p[0], p[2])

    @_('somme EGAL somme')
    def expr(self, p):
        return arbre_abstrait.Comparaison('==', p[0], p[2])

    @_('somme DIFFERENT somme')
    def expr(self, p):
        return arbre_abstrait.Comparaison('!=', p[0], p[2])

if __name__ == '__main__':
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 2:
        print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1],"r") as f:
            data = f.read()
            try:
                arbre = parser.parse(lexer.tokenize(data))
                arbre.afficher()
            except EOFError:
                exit()
