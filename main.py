nombres_premiers: list[int] = [2, 3, 5, 7, 11, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
debug: bool = True


def debug_print(*args):
    if debug:
        print(*args)


class Fraction:
    def __init__(self, dividende: int, diviseur: int = 1):
        debug_print("Début du traitement de la fraction", dividende, "/", diviseur)
        if dividende < 0 and diviseur < 0:
            dividende = dividende * -1
            diviseur = diviseur * -1
            debug_print("Fraction: La fraction est du type -", dividende, " / -", diviseur,
                        ", elle a été transformée en", dividende, "/", diviseur)

        dividende_avant = None
        while dividende != dividende_avant:
            dividende_avant = dividende
            for i in nombres_premiers:
                if diviseur % i == 0 and dividende % i == 0:
                    debug_print("Fraction: La fraction est simplifiée par ", i)
                    diviseur = int(diviseur / i)
                    dividende = int(dividende / i)

        debug_print("La fraction finale est", dividende, "/", diviseur, "\n")
        self.dividende = dividende
        self.diviseur = diviseur

    def get(self) -> tuple:
        return self.dividende, "/", self.diviseur

    def evaluate(self, precision: int):
        return round(self.dividende / self.diviseur, precision)


class Variable:
    def __init__(self, nombres: list[Fraction], variables: list[str]):
        self.partie_numerique = multiplier(nombres)
        if self.partie_numerique.get() == Fraction(0).get():
            self.partie_litterale = []
        else:
            self.partie_litterale = variables


class Addition:
    def __init__(self, params: list):
        self.params = params

    def get(self):
        resultat = []
        for i in self.params:
            resultat += i, "+"
        resultat.pop(len(resultat)-1)
        return resultat


class Multiplication:
    def __init__(self, params: list):
        self.params = params

    def get(self) -> tuple:
        resultat = []
        for i in self.params:
            resultat += i, "*"
        resultat.pop(len(resultat)-1)
        resultat = tuple(resultat)
        return resultat


class Puissance:
    def __init__(self, params: list):
        self.params = params

    def get(self) -> tuple:
        resultat = []
        for i in self.params:
            resultat += i, "^"
        resultat.pop(len(resultat)-1)
        resultat = tuple(resultat)
        return resultat


def ajouter(param: list[Fraction]) -> Fraction:
    debug_print("Début du traitement d'une addition")
    resultat: Fraction = Fraction(0)
    for i in param:
        resultat = Fraction((resultat.dividende * i.diviseur) + (i.dividende * resultat.diviseur),
                            resultat.diviseur * i.diviseur)
        debug_print("Ajouter: Le résultat est désormais", resultat.get())
    debug_print("Fin du traitement de l'addition\n")
    return resultat


def multiplier(param: list[Fraction]) -> Fraction:
    debug_print("Début du traitement d'une multiplication")
    resultat = Fraction(1)
    for i in param:
        if resultat.get() == Fraction(0).get() or i.get() == Fraction(0).get():
            debug_print("Multiplier: Multiplication par 0: le resultat est défini à 0")
            return Fraction(0)
        resultat = Fraction(resultat.dividende * i.dividende, resultat.diviseur * i.diviseur)
        debug_print("Multiplier: Le résultat est désormais", resultat.get())
    debug_print("Fin du traitement de la multiplication\n")
    return resultat


def exponent(param: list[Fraction] = [Fraction(0)]) -> Puissance:
    debug_print("Début du traitement d'une puissance")
    execute: bool = False
    fraction_originale = Fraction(param[0].dividende, param[0].diviseur)
    liste_exposants: list[Fraction] = []
    for i in param:
        if execute:
            liste_exposants.append(i)
        execute = True
    local_exponent = multiplier(liste_exposants)
    if local_exponent.diviseur == 1:
        resultat = Fraction(fraction_originale.dividende ** local_exponent.dividende, fraction_originale.diviseur ** local_exponent.dividende)
    debug_print("Fin du traitement de la puissance\n")
    return resultat


def conversion_fraction(nombre: float) -> Fraction:
    nombre_decimaux = len(str(nombre).split('.')[1])
    return Fraction(int(nombre * (10 ** nombre_decimaux)), int(10 ** nombre_decimaux))


if __name__ == '__main__':

    debug_print(exponent([Fraction(6, 2), Fraction(2)]).get())
    print('Programme terminé !')
