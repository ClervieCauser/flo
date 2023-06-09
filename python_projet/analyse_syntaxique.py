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
        return arbre_abstrait.Programme([], p[0])

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

    @_('declaration')
    def instruction(self, p):
        return p.declaration

    @_('affectation')
    def instruction(self, p):
        return p.affectation

    @_('declaration_affectation')
    def instruction(self, p):
        return p.declaration_affectation

    @_('instruction_conditionnelle')
    def instruction(self, p):
        return p.instruction_conditionnelle

    # Action associée à la règle 'declaration'
    @_('TYPE IDENTIFIANT ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.TYPE, p.IDENTIFIANT)

    # Action associée à la règle 'affectation'
    @_('IDENTIFIANT "=" expr ";"')
    def affectation(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expr)

    # Action associée à la règle 'declaration_affectation'
    @_('TYPE IDENTIFIANT "=" expr ";"')
    def declaration_affectation(self, p):
        return arbre_abstrait.DeclarationAffectation(p.TYPE, p.IDENTIFIANT, p.expr)

    # Action associée à la règle 'instruction_conditionnelle'
    @_('SI "(" expr ")" "{" listeInstructions "}"')
    def instruction_conditionnelle(self, p):
        conditions = [arbre_abstrait.Condition(p.expr, p.listeInstructions)]
        return arbre_abstrait.InstructionConditionnelle(conditions, None)

    # Action associée à la règle 'sinon_si'
    @_('sinon_si SINON_SI "(" expr ")" "{" listeInstructions "}"')
    def sinon_si(self, p):
        p.sinon_si.conditions.append(arbre_abstrait.Condition(p.expr, p.listeInstructions))
        return p.sinon_si

    # Action associée à la règle 'sinon'
    @_('SINON "{" listeInstructions "}"')
    def sinon(self, p):
        return arbre_abstrait.Sinon(p.listeInstructions)

    @_('SI "(" expr ")" "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.InstructionConditionnelle([arbre_abstrait.Condition(p.expr, p.listeInstructions)], None)

    @_('SI "(" expr ")" "{" listeInstructions "}" sinon')
    def instruction(self, p):
        return arbre_abstrait.InstructionConditionnelle([arbre_abstrait.Condition(p.expr, p.listeInstructions)],p.sinon)

    @_('instruction_conditionnelle SINON_SI "(" expr ")" "{" listeInstructions "}"')
    def sinon_si(self, p):
        p.instruction_conditionnelle.conditions.append(arbre_abstrait.Condition(p.expr, p.listeInstructions))
        return p.instruction_conditionnelle

    @_('TANTQUE "(" expr ")" "{" listeInstructions "}"')
    def instruction(self, p):
        return arbre_abstrait.InstructionBoucle(p.expr, p.listeInstructions)

    @_('RETOURNER expr ";"')
    def instruction(self, p):
        return arbre_abstrait.InstructionRetourner(p.expr)

    @_('expr')
    def arguments(self,p):
        return p.expr

    @_('IDENTIFIANT "(" arguments ")" ";"')
    def instruction(self, p):
        return arbre_abstrait.AppelFonctionIgnorer(p.IDENTIFIANT, p.arguments)

    @_('listeFonctions listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.listeFonctions, p.listeInstructions)

    @_('fonction')
    def listeFonctions(self, p):
        return [p.fonction]

    @_('fonction listeFonctions')
    def listeFonctions(self, p):
        p.listeFonctions.append(p.fonction)
        return p.listeFonctions

    @_('TYPE IDENTIFIANT "(" arguments ")" "{" listeInstructions "}"')
    def fonction(self, p):
        return arbre_abstrait.Fonction(p.TYPE, p.IDENTIFIANT, p.arguments, p.listeInstructions)

    @_('TYPE IDENTIFIANT')
    def arguments(self, p):
        return [(p.TYPE, p.IDENTIFIANT)]

    @_('TYPE IDENTIFIANT "," arguments')
    def arguments(self, p):
        return [arbre_abstrait.Argument(p.TYPE, p.IDENTIFIANT)] + p.arguments


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
