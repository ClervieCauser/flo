"""
Affiche une chaine de caractère avec une certaine identation
"""
def afficher(s,indent=0):
    print(" "*indent+s)

class Programme:
    def __init__(self,listeInstructions):
        self.listeInstructions = listeInstructions
    def afficher(self,indent=0):
        afficher("<programme>",indent)
        self.listeInstructions.afficher(indent+1)
        afficher("</programme>",indent)

class ListeInstructions:
    def __init__(self):
        self.instructions = []
    def afficher(self,indent=0):
        afficher("<listeInstructions>",indent)
        for instruction in self.instructions:
            instruction.afficher(indent+1)
        afficher("</listeInstructions>",indent)

class Ecrire:
    def __init__(self,exp):
        self.exp = exp
    def afficher(self,indent=0):
        afficher("<ecrire>",indent)
        self.exp.afficher(indent+1)
        afficher("</ecrire>",indent)

class Operation:
    def __init__(self,op,exp1,exp2):
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2
    def afficher(self,indent=0):
        afficher("<operation>",indent)
        afficher(self.op,indent+1)
        self.exp1.afficher(indent+1)
        self.exp2.afficher(indent+1)
        afficher("</operation>",indent)
class Entier:
    def __init__(self,valeur):
        self.valeur = valeur
    def afficher(self,indent=0):
        afficher("[Entier:"+str(self.valeur)+"]",indent)

class Lire:
    def __init__(self):
        pass
    def afficher(self, indent=0):
        afficher("[Lire]", indent)

class Variable:
    def __init__(self, identifiant):
        self.identifiant = identifiant
    def afficher(self, indent=0):
        afficher("[Variable:" + self.identifiant + "]", indent)

class Bool:
    def __init__(self, valeur):
        self.valeur = valeur
    def afficher(self, indent=0):
        afficher("[Bool:" + str(self.valeur) + "]", indent)

class Negation:
    def __init__(self, booleen):
        self.booleen = booleen
    def afficher(self, indent=0):
        afficher("<negation>", indent)
        self.booleen.afficher(indent + 1)
        afficher("</negation>", indent)

class Conjonction:
    def __init__(self, booleen1, booleen2):
        self.booleen1 = booleen1
        self.booleen2 = booleen2
    def afficher(self, indent=0):
        afficher("<conjonction>", indent)
        self.booleen1.afficher(indent + 1)
        self.booleen2.afficher(indent + 1)
        afficher("</conjonction>", indent)

class Disjonction:
    def __init__(self, booleen1, booleen2):
        self.booleen1 = booleen1
        self.booleen2 = booleen2
    def afficher(self, indent=0):
        afficher("<disjonction>", indent)
        self.booleen1.afficher(indent + 1)
        self.booleen2.afficher(indent + 1)
        afficher("</disjonction>", indent)

class Comparaison:
    def __init__(self, op, exp1, exp2):
        self.op = op
        self.exp1 = exp1
        self.exp2 = exp2
    def afficher(self, indent=0):
        afficher("<comparaison>", indent)
        afficher(self.op, indent + 1)
        self.exp1.afficher(indent + 1)
        self.exp2.afficher(indent + 1)
        afficher("</comparaison>", indent)

class Declaration:
    def __init__(self, type_, identifiant):
        self.type = type_
        self.identifiant = identifiant
    def afficher(self, indent=0):
        afficher("<declaration>", indent)
        afficher(self.type, indent + 1)
        afficher(self.identifiant, indent + 1)
        afficher("</declaration>", indent)

class Affectation:
    def __init__(self, identifiant, expression):
        self.identifiant = identifiant
        self.expression = expression
    def afficher(self, indent=0):
        afficher("<affectation>", indent)
        afficher(self.identifiant, indent + 1)
        self.expression.afficher(indent + 1)
        afficher("</affectation>", indent)

class DeclarationAffectation:
    def __init__(self, type_, identifiant, expression):
        self.type = type_
        self.identifiant = identifiant
        self.expression = expression
    def afficher(self, indent=0):
        afficher("<declaration_affectation>", indent)
        afficher(self.type, indent + 1)
        afficher(self.identifiant, indent + 1)
        self.expression.afficher(indent + 1)
        afficher("</declaration_affectation>", indent)

class InstructionConditionnelle:
    def __init__(self, conditions, sinon):
        self.conditions = conditions
        self.sinon = sinon
    def afficher(self, indent=0):
        afficher("<instruction_conditionnelle>", indent)
        for condition in self.conditions:
            condition.afficher(indent + 1)
        if self.sinon:
            self.sinon.afficher(indent + 1)
        afficher("</instruction_conditionnelle>", indent)

class SinonSi:
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions
    def afficher(self, indent=0):
        afficher("<sinon_si>", indent)
        self.condition.afficher(indent + 1)
        self.instructions.afficher(indent + 1)
        afficher("</sinon_si>", indent)

class Sinon:
    def __init__(self, instructions):
        self.instructions = instructions
    def afficher(self, indent=0):
        afficher("<sinon>", indent)
        self.instructions.afficher(indent + 1)
        afficher("</sinon>", indent)

class InstructionBoucle:
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions
    def afficher(self, indent=0):
        afficher("<instruction_boucle>", indent)
        self.condition.afficher(indent + 1)
        self.instructions.afficher(indent + 1)
        afficher("</instruction_boucle>", indent)

class InstructionRetourner:
    def __init__(self, expression):
        self.expression = expression
    def afficher(self, indent=0):
        afficher("<instruction_retourner>", indent)
        self.expression.afficher(indent + 1)
        afficher("</instruction_retourner>", indent)

class AppelFonctionIgnorer:
    def __init__(self, identifiant, arguments):
        self.identifiant = identifiant
        self.arguments = arguments
    def afficher(self, indent=0):
        afficher("<appel_fonction_ignorer>", indent)
        afficher(self.identifiant, indent + 1)
        if self.arguments:
            self.arguments.afficher(indent + 1)
        afficher("</appel_fonction_ignorer>", indent)

class Condition:
    def __init__(self, condition, instructions):
        self.condition = condition
        self.instructions = instructions
    def afficher(self, indent=0):
        afficher("<condition>", indent)
        self.condition.afficher(indent + 1)
        self.instructions.afficher(indent + 1)
        afficher("</condition>", indent)