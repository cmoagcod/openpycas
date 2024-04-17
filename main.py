nombres_premiers: list[int] = [2, 3, 5, 7, 11, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
racines: dict = {1: 1, 4: 2, 9: 3, 16: 4, 25: 5, 36: 6, 49: 7, 64: 8, 81: 9, 100: 10, 121: 11, 144: 12, 169: 13,
                 196: 14, 225: 15, 256: 16, 289: 17, 324: 18, 361: 19, 400: 20, 441: 21, 484: 22, 529: 23, 576: 24,
                 625: 25, 676: 26, 729: 27, 784: 28, 841: 29, 900: 30, 961: 31, 1024: 32, 1089: 33, 1156: 34, 1225: 35,
                 1296: 36, 1369: 37, 1444: 38, 1521: 39, 1600: 40, 1681: 41, 1764: 42, 1849: 43, 1936: 44, 2025: 45,
                 2116: 46, 2209: 47, 2304: 48, 2401: 49, 2500: 50, 2601: 51, 2704: 52, 2809: 53, 2916: 54, 3025: 55,
                 3136: 56, 3249: 57, 3364: 58, 3481: 59, 3600: 60, 3721: 61, 3844: 62, 3969: 63, 4096: 64, 4225: 65,
                 4356: 66, 4489: 67, 4624: 68, 4761: 69, 4900: 70, 5041: 71, 5184: 72, 5329: 73, 5476: 74, 5625: 75,
                 5776: 76, 5929: 77, 6084: 78, 6241: 79, 6400: 80, 6561: 81, 6724: 82, 6889: 83, 7056: 84, 7225: 85,
                 7396: 86, 7569: 87, 7744: 88, 7921: 89, 8100: 90, 8281: 91, 8464: 92, 8649: 93, 8836: 94, 9025: 95,
                 9216: 96, 9409: 97, 9604: 98, 9801: 99, 10000: 100}
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


def ajouter(params: list[Fraction]) -> Fraction:
    debug_print("Début du traitement d'une addition")
    resultat: Fraction = Fraction(0)
    for i in params:
        resultat = Fraction((resultat.dividende * i.diviseur) + (i.dividende * resultat.diviseur),
                            resultat.diviseur * i.diviseur)
        debug_print("Ajouter: Le résultat est désormais", resultat.get())
    debug_print("Fin du traitement de l'addition\n")
    return resultat


def multiplier(params: list[Fraction]) -> Fraction:
    debug_print("Début du traitement d'une multiplication")
    resultat = Fraction(1)
    for i in params:
        if resultat.get() == Fraction(0).get() or i.get() == Fraction(0).get():
            debug_print("Multiplier: Multiplication par 0: le resultat est défini à 0")
            return Fraction(0)
        resultat = Fraction(resultat.dividende * i.dividende, resultat.diviseur * i.diviseur)
        debug_print("Multiplier: Le résultat est désormais", resultat.get())
    debug_print("Fin du traitement de la multiplication\n")
    return resultat


def exponent(params: list[Fraction]) -> object:
    debug_print("Début du traitement d'une puissance")
    execute: bool = False
    fraction_originale = Fraction(params[0].dividende, params[0].diviseur)
    liste_exposants: list[Fraction] = []
    for i in params:
        if execute:
            liste_exposants.append(i)
        execute = True
    local_exponent = multiplier(liste_exposants)
    if local_exponent.diviseur == 1:
        resultat = Fraction(fraction_originale.dividende ** local_exponent.dividende,
                            fraction_originale.diviseur ** local_exponent.dividende)
    else:
        racine = Fraction(1, local_exponent.diviseur)
        puissance = Fraction(local_exponent.dividende)
        partie_entiere: Fraction = exponent([fraction_originale, puissance])
        if partie_entiere.dividende == 1 and partie_entiere.diviseur == 1:
            local_exponent = Fraction(1)
            racine = Fraction(1)
        if partie_entiere.evaluate(1) < 10 ** 10:
            resultat = Puissance([partie_entiere, racine])
        else:
            resultat = Puissance([fraction_originale, local_exponent])
    debug_print("Fin du traitement de la puissance\n")
    return resultat


def conversion_fraction(nombre: float) -> Fraction:
    nombre_decimaux = len(str(nombre).split('.')[1])
    return Fraction(int(nombre * (10 ** nombre_decimaux)), int(10 ** nombre_decimaux))


if __name__ == '__main__':

    print('Programme terminé !')
