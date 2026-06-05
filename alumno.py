import re

class Alumno:
    """
    Classe utilitzada per al tractament de les notes dels alumnes. Cadascun
    inclou els atributs següents:

    numIden:   Número d'identificació. És un número sencer que, en cas
               de no indicar-se, pren el valor per defecte 'numIden=-1'.
    nombre:    Nom complet de l'alumne.
    notas:     Llista de números reals amb les diferents notes de cada alumne.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Retorna un nou objecte 'Alumno' con una llista de notes ampliada amb
        el valor passat com a argument. D'aquesta manera, afegir una nota a un
        Alumno es realitza amb l'ordre 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Retorna la nota mitjana de l'alumne.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Retorna la representació 'oficial' de l'alumne. A partir de copiar
        i enganxar la cadena obtinguda és possible crear un nou Alumno idèntic.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Retorna la representació 'bonica' de l'alumne. Visualitza en tres
        columnes separades per tabulador el número d'identificació, el nom
        complet i la nota mitjana de l'alumne con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'


def leeAlumnos(ficAlum):
    """
    Llegeix un fitxer de text amb les dades dels alumnes i retorna un
    diccionari on la clau és el nom de cada alumne i el valor és
    l'objecte Alumno corresponent.

    >>> alumnos = leeAlumnos('alumnos.txt')
    >>> for alumno in alumnos:
    ...     print(alumnos[alumno])
    171\tBlanca Agirrebarrenetse\t9.5
    23\tCarles Balcell de Lara\t4.9
    68\tDavid Garcia Fuster\t7.0
    """
    diccionario_alumnos = {}
    
    # Expressió regular:
    # ^\s*(\d+)  -> Captura l'ID (un o més dígits) al principi
    # \s+(.+?)   -> Captura el nom (qualsevol caràcter, no cobdiciós)
    # \s+((?:\d+(?:\.\d+)?\s*)*)$ -> Captura la seqüència final de notes numèriques
    patron = re.compile(r'^\s*(\d+)\s+(.+?)\s+((?:\d+(?:\.\d+)?\s*)*)$')

    with open(ficAlum, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
                
            match = patron.match(linea)
            if match:
                num_iden = int(match.group(1))
                nombre = match.group(2).strip()
                # Extraurem totes les notes utilitzant una cerca de decimals/enters
                notas_txt = match.group(3)
                notas = [float(n) for n in re.findall(r'\d+(?:\.\d+)?', notas_txt)]
                
                # Crear l'objecte Alumno i desar-lo al diccionari
                diccionario_alumnos[nombre] = Alumno(nombre, num_iden, notas)
                
    return diccionario_alumnos


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)