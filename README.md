# Expresiones Regulares

## Nom i cognoms

> [!Important]
> Introduzca a continuación su nombre y apellidos:
>
> Marta Pitarch Granell

## Aviso Importante

> [!Caution]
> 
> El objetivo de esta tarea es aprender a usar las expresiones regulares. En concreto, su
> implementación en Python. A los profesores de la asignatura les importa un pimiento si
> usted conoce alguna biblioteca que hace el mismo trabajo de manera más sencilla y/o
> eficiente; su uso está prohibido.
>
> ¿Quiere saber más?, consulte con el profesorado.
 
## Fecha de entrega: 7 de junio a medianoche

## Tratamiento de ficheros de notas

Con el final de curso llega la ardua tarea de evaluar las tareas realizadas por los alumnos durante el
mismo. Para facilitar esta tarea, se dispone de la clase `Alumno` que proporciona los datos
fundamentales de cada alumno: su número de identificación (`numIden`), su nombre completo 
(`nombre`) y la lista de notas obtenidas a lo largo del curso (`notas`). La clase también
proporciona métodos para añadir una nota al expediente del alumno (`__add__()`), para obtener
la representación *oficial* del mismo (`__repr__()`) y para obtener la representación
*bonita* (`__str__()`).

La definición de la clase `Alumno`, disponible en `alumno.py`, es:

```python
class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separas por tabulador el número de identificación, el nombre
        completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden}\t{self.nombre}\t{self.media():.1f}'
```

A menudo, las notas de los alumnos se almacenan en ficheros de texto en los que los datos de cada alumno
ocupan una línea con los distintos valores separados por espacios y/o tabuladores.

El ejemplo siguiente muestra un fichero típico con las notas de tres alumnos:

```text
171 Blanca Agirrebarrenetse 10  	9 	  9.5
23  Carles Balcell de Lara  5 	    5 	  4.5  	5.2
68  David Garcia Fuster 	7.75    5.25  8   
```

Añada al fichero `alumno.py` la función `leeAlumnos(ficAlum)` que lea un fichero de texto con los datos de 
todos los alumnos y devuelva un diccionario en el que la clave sea el nombre de cada alumno y su contenido 
el objeto `Alumno` correspondiente.

La función deberá cumplir los requisitos siguientes:

- Sólo debe realizar lo que se indica; es decir, debe leer el fichero de texto que se le pasa como único
  argumento y devolver un diccionario con los datos de los alumnos.
- El análisis de cada línea de texto se realizará usando expresiones regulares.
- La función `leeAlumnos()` debe incluir, en su cadena de documentación, la prueba unitaria siguiente según
  el formato de la biblioteca `doctest`, donde el fichero `'alumnos.txt'` es el fichero mostrado como ejemplo
  al principio de este enunciado:

  ```python
  >>> alumnos = leeAlumnos('alumnos.txt')
  >>> for alumno in alumnos:
  ...     print(alumnos[alumno])
  ...
  171     Blanca Agirrebarrenetse 9.5
  23      Carles Balcells de Lara 4.9
  68      David Garcia Fuster     7.0
  ```

  - Evidentemente, es responsabilidad del autor comprobar que la prueba unitaria se pasa satisfactoriamente
    antes de la entrega de la tarea.

  - Para evitar que diferencias debidas a espacios en blanco o tabuladores den lugar a error, se recomienda
    efectuar las pruebas unitarias con la opción `doctest.NORMALIZE_WHITESPACE`. Por ejemplo,
    `doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)`.


## Análisis de expresiones horarias

En casi todos los idiomas más habituales, cualquier hora puede reducirse al formato estándar HH:MM, donde HH es 
un número de dos dígitos, que representa la hora y está comprendido entre 00 y 23, y MM es otro número de dos 
dígitos, que representa el minuto y está comprendido entre 00 y 59.

No obstante, en el lenguaje hablado, es raro usar este formato estándar. En el caso del castellano, existe una
gran variedad de formatos. La lista siguiente alguna de las posibilidades más frecuentes, aunque existen bastantes
más:

- **08:27**

  Es el formato estándar. Cuando la hora es menor que 10, es posible representarla con
  dos dígitos (08:27), o sólo uno (8:27). Los minutos se representan siempre con dos (8:05).

- **8h27m**

  Las horas o minutos menores que 10 pueden representarse usando uno o dos dígitos. Las horas
  *en punto* pueden indicarse sin minutos (8h).

- **8 en punto**

  Las horas exactas suelen indicarse con la partícula *'en punto'*. En ese caso, es
  habitual omitir la letra *h* después de la cifra.

  Otras alternativas semejantes son las *'8 y cuarto'*, las *'8 y media'* o las *'8 menos cuarto'*.

  En todos estos casos, el reloj empleado será de 12 horas y empezando en 1 (de 1 a 12). El
  resultado será ambiguo, ya que no sabremos si una cierta hora es AM o PM, pero así es cómo
  se suele hablar (la gente queda a *'las 11 en punto'* para ir a una fiesta, no a las
  *'las 23 en punto'*). El resultado se devolverá siempre en el rango de 00:00 a 11:59.

- **... de la mañana**

  Las expresiones horarias entre las 4 y las 12 pueden ir seguidas de la partícula *'de la mañana'*.

  Análogamente, las horas entre las 12 y las 3 pueden ir seguidas de *'del mediodía'*, las horas entre
  las 3 y las 8 pueden serlo de *'de la tarde'*, entre 8 y 4 de *'de la noche'* y entre 1 y
  6 de *'de la madrugada'*.

  En estos casos, el reloj empleado es siempre de 12 horas (nunca se dice *'las 18 de la tarde'*, sino
  *'las 6 de la tarde'*). Además la hora no puede ser cero, sino que, en ese caso, se usaría 12.

### Tarea: normalización de las expresiones horarias de un texto

Escriba el fichero `horas.py` con la función `normalizaHoras(ficText, ficNorm)`, que lee el fichero de
texto `ficText`, lo analiza en busca de expresiones horarias y escribe el fichero `ficNorm` en el que
éstas se expresan según el formato normalizado, con las horas y los minutos indicados por dos dígitos
y separados por dos puntos (08:27).

Cada línea del fichero puede contener, o no, una o más expresiones horarias, pero éstas nunca aparecerán
partidas en más de una línea.

Las horas con expresión incorrecta, por ejemplo, *'17:5'* (en la expresión normalizada deben usarse dos
dígitos para expresar los minutos) u *'11 de la tarde'* (la tarde nunca llega hasta esa hora), deben
dejarse tal cual.

Para la evaluación de la tarea se usará un texto con unas cien expresiones horarias, que incluirán tanto
expresiones correctas como incorrectas. Una parte de la nota dependerá de la precisión en su normalización.

Se recomienda empezar normalizando textos que sólo contengan expresiones correctas del tipo más sencillo;
es decir, con la forma *'18h45m'*. La consecución de este objetivo garantiza una nota mínima de notable
bajo (7). La extensión al resto de formatos indicados y la detección de expresiones incorrectas serán
necesarias para alcanzar la nota máxima (10).

La tabla siguiente muestra un ejemplo de texto antes y después de su normalización, incluyendo tanto
expresiones horarias **correctas** como <span style="color:red">**incorrectas**</span>.

### Ejemplo de normalización de las expresiones horarias de un texto

Las líneas siguientes muestran ejemplos de expresiones horarias, tanto correctas como incorrectas. Las
mismas expresiones se encuentran en el fichero `horas.txt`, que puede usar para comprobar el correcto
funcionamiento de su función.

#### Expresiones válidas

> - La llegada del tren está prevista a las **18:30**
> - La llegada del tren está prevista a las **18:30**

> - Tenía su clase entre las **8h** y las **10h30m**
> - Tenía su clase entre las **08:00** y las **10:30**

> - Se acaba a las **4 y media de la tarde**
> - Se acaba a las **16:30**

> - Empieza a trabajar a las **7h de la mañana**
> - Empieza a trabajar a las **07:00**

> - Es lo mismo **5 menos cuarto** que **4:45**
> - Es lo mismo **04:45** que **04:45**

> - Tenemos descanso hasta las **17h5m**
> - Tenemos descanso hasta las **17:05**

> - Las campanadas son a las **12 de la noche**
> - Las campanadas son a las **00:00**

#### Expresiones incorrectas

> - Son exactamente las $\textbf{\color{red}17:5}$
> - Son exactamente las $\textbf{\color{red}17:5}$

> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$
> - Cuando llegó, ya eran las $\textbf{\color{red}11 de la tarde}$

> - El examen es a las $\textbf{\color{red}17 de la tarde}$
> - El examen es a las $\textbf{\color{red}17 de la tarde}$

> - Cenamos en las $\textbf{\color{red}7}$ puertas
> - Cenamos en las $\textbf{\color{red}7}$ puertas

> - No llegará antes de las $\textbf{\color{red}1h78m}$
> - No llegará antes de las $\textbf{\color{red}1h78m}$

> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó
> - *Corrió* la maratón en $\textbf{\color{red}32h31m}$, pero no ganó

> - Quedamos a las $\textbf{\color{red}23 en punto}$
> - Quedamos a las $\textbf{\color{red}23 en punto}$


#### Entrega

##### Ficheros `alumno.py` y `horas.py`

- Ambos ficheros deben incluir una cadena de documentación con el nombre del alumno o alumnos
  y una descripción de su contenido.

- Se valorará lo pythónico de la solución; en concreto, su claridad y sencillez, y el
  uso de los estándares marcados por PEP-ocho.

##### Ejecución de los tests unitarios de `alumno.py`

Inserte a continuación una captura de pantalla que muestre el resultado de ejecutar el
fichero `alumno.py` con la opción *verbosa*, de manera que se muestre el
resultado de la ejecución de los tests unitarios.

##### Código desarrollado
```python
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
```
Inserte a continuación los códigos fuente desarrollados en esta tarea, usando los
comandos necesarios para que se realice el realce sintáctico en Python del mismo (no
vale insertar una imagen o una captura de pantalla, debe hacerse en formato *markdown*).
```python
import re

def procesar_hora(match):
    """
    Funció auxiliar que rep un 'match' d'expressió regular d'una hora,
    valida si és correcta segons les regles del text i retorna la cadena normalitzada
    o el text original si és invàlida.
    """
    texto_original = match.group(0)
    
    # 1. CAS: Format HH:MM o H:MM (ex: 18:30, 17:5, 08:00)
    if ':' in texto_original and 'de la' not in texto_original and 'del' not in texto_original:
        parts = texto_original.split(':')
        h = int(parts[0])
        m = int(parts[1])
        if h < 24 and m < 60 and len(parts[1]) == 2:
            return f"{h:02d}:{m:02d}"
        return texto_original

    # Captura de grups generals de l'expressió regular expandida
    h_str = match.group('h1') or match.group('h2') or match.group('h3') or match.group('h4')
    if not h_str:
        return texto_original
    
    h = int(h_str)
    m = 0
    
    # Determinar els minuts segons el format de text o lletra
    if match.group('m1'):
        m = int(match.group('m1'))
    elif match.group('m2'):
        m = int(match.group('m2'))
    elif match.group('mod'):
        mod = match.group('mod')
        if 'en punto' in mod:
            m = 0
        elif 'y cuarto' in mod:
            m = 15
        elif 'y media' in mod:
            m = 30
        elif 'menos cuarto' in mod:
            m = 45
            h -= 1  # Ajustem l'hora enrere (ex: 5 menos cuarto -> s'avalua sobre les 4)

    # Validació de minuts de seguretat
    if m >= 60 or m < 0:
        return texto_original

    # Detectar sufixos de franja horària
    sufijo = match.group('sufijo')
    
    if sufijo:
        # Totes les franges de text funcionen en format de 12 hores (1 a 12)
        if h < 1 or h > 12:
            return texto_original
            
        if 'mañana' in sufijo:
            if h < 4 or h > 12: return texto_original
            # Excepció: 12 de la mañana és migdia, però s'ajusta a 12
            if h == 12: h = 12
        elif 'mediodía' in sufijo:
            if h != 12 and (h < 1 or h > 3): return texto_original
            if h != 12: h += 12
        elif 'tarde' in sufijo:
            if h < 3 or h > 8: return texto_original
            if h != 12: h += 12
        elif 'noche' in sufijo:
            if (h < 8 or h > 12) and (h < 1 or h > 4): return texto_original
            if h == 12: h = 0
            elif 8 <= h < 12: h += 12
            else: h = h  # 1 a 4 de la nit/matinada s'interpreta com 01h a 04h
        elif 'madrugada' in sufijo:
            if h < 1 or h > 6: return texto_original
            if h == 12: return texto_original
            
        return f"{h:02d}:{m:02d}"
    
    # Si no té sufix, comprovem formats compactes sense franja com '10h30m' o '8h'
    else:
        # Si és un format purament de 24h sense text
        if h < 24 and m < 60:
            return f"{h:02d}:{m:02d}"
            
    return texto_original


def normalizaHoras(ficText, ficNorm):
    """
    Lee ficText, busca expresiones horarias, las normaliza al formato HH:MM
    y escribe el resultado en ficNorm.
    """
    # Patró regex complex per fer match de totes les casuístiques descrites
    # Cobreix: formats digitals, lletres 'h' i 'm', modificadors text i franges.
    patron_completo = re.compile(
        r'\b(?P<h1>\d{1,2}):(?P<m1>\d{1,2})\b|'  # 18:30, 17:5
        r'\b(?P<h2>\d{1,2})h(?P<m2>\d{1,2})m\b|'  # 10h30m, 17h5m
        r'\b(?P<h3>\d{1,2})h\b|'  # 8h
        r'\b(?P<h4>\d{1,2})\s+(?P<mod>en punto|y cuarto|y media|menos cuarto)?\s*(?P<sufijo>de la mañana|del mediodía|de la tarde|de la noche|de la madrugada)\b|'
        r'\b(?P<h5>\d{1,2})\s+(?P<mod2>en punto)\b' # 8 en punto (sense franja)
    , re.IGNORECASE)

    # Nota: per a simplificar la unió de grups al mètode auxiliar, readaptem la regex
    # fent servir una única estructura unificada per franges o buscant fragments de text:
    
    patron_textual = (
        r'\b(?P<h1>\d{1,2}):(?P<m1>\d{1,2})\b|'
        r'\b(?P<h2>\d{1,2})h(?P<m2>\d{1,2})m\b|'
        r'\b(?P<h3>\d{1,2})h\b|'
        r'\b(?P<h4>\d{1,2})(?:\s+(?P<mod>en punto|y cuarto|y media|menos cuarto))?(?:\s+(?P<sufijo>de la mañana|del mediodía|de la tarde|de la noche|de la madrugada))\b|'
        r'\b(?P<h5>\d{1,2})\s+(?P<mod2>en punto)\b'
    )
    
    regex = re.compile(patron_textual, re.IGNORECASE)

    def sustituir(match):
        # Normalització mitjançant anàlisi de grups
        original = match.group(0)
        
        # Format HH:MM
        if match.group('h1') and match.group('m1'):
            h, m = int(match.group('h1')), int(match.group('m1'))
            if h < 24 and m < 60 and len(match.group('m1')) == 2:
                return f"{h:02d}:{m:02d}"
            return original
            
        # Format XhYm
        if match.group('h2') and match.group('m2'):
            h, m = int(match.group('h2')), int(match.group('m2'))
            if h < 24 and m < 60:
                return f"{h:02d}:{m:02d}"
            return original
            
        # Format Xh
        if match.group('h3'):
            h = int(match.group('h3'))
            if h < 24:
                return f"{h:02d}:00"
            return original
            
        # Format X en punto (sense sufix de franja)
        if match.group('h5'):
            h = int(match.group('h5'))
            if h < 24:
                return f"{h:02d}:00"
            return original

        # Format Textual Complex amb Franja d'hores (h4)
        if match.group('h4'):
            h = int(match.group('h4'))
            m = 0
            mod = match.group('mod')
            sufijo = match.group('sufijo')
            
            if mod:
                if 'en punto' in mod: m = 0
                elif 'y cuarto' in mod: m = 15
                elif 'y media' in mod: m = 30
                elif 'menos cuarto' in mod:
                    m = 45
                    h -= 1

            if h < 1 or h > 12:
                # El rellotge de franges ha d'estar en format 1 a 12 (excepte si h-1 va donar 0 per 'menos cuarto')
                if not (mod and 'menos cuarto' in mod and h == 0):
                    return original
            
            # Reajustem h=0 a 12 per simplificar la lògica de comprovació de franja
            h_comprobar = 12 if h == 0 else h

            if 'mañana' in sufijo:
                if h_comprobar < 4 or h_comprobar > 12: return original
                h_res = 12 if h_comprobar == 12 else h_comprobar
            elif 'mediodía' in sufijo:
                if h_comprobar != 12 and (h_comprobar < 1 or h_comprobar > 3): return original
                h_res = 12 if h_comprobar == 12 else h_comprobar + 12
            elif 'tarde' in sufijo:
                if h_comprobar < 3 or h_comprobar > 8: return original
                h_res = 12 if h_comprobar == 12 else h_comprobar + 12
            elif 'noche' in sufijo:
                if (h_comprobar < 8 or h_comprobar > 12) and (h_comprobar < 1 or h_comprobar > 4): return original
                if h_comprobar == 12: h_res = 0
                elif 8 <= h_comprobar < 12: h_res = h_comprobar + 12
                else: h_res = h_comprobar
            elif 'madrugada' in sufijo:
                if h_comprobar < 1 or h_comprobar > 6: return original
                h_res = h_comprobar
            
            if h_res < 0 or h_res > 23 or m < 0 or m >= 60:
                return original
                
            return f"{h_res:02d}:{m:02d}"

        return original

    with open(ficText, 'r', encoding='utf-8') as f_in, open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            linea_modificada = regex.sub(sustituir, linea)
            f_out.write(linea_modificada)
```
##### Subida del resultado al repositorio GitHub y *pull-request*

La entrega se formalizará mediante *pull request* al repositorio de la tarea.

El fichero `README.md` deberá respetar las reglas de los ficheros Markdown y
visualizarse correctamente en el repositorio, incluyendo la imagen con la ejecución de
los tests unitarios y el realce sintáctico del código fuente insertado.

##### Y NADA MÁS

Sólo se corregirá el contenido de este fichero `README.md` y los códigos fuente `alumno.py`
y `horas.py`. No incluya otros ficheros con código fuente, notebooks de Jupyter o explicaciones
adicionales; simplemente, no se tendrán en cuenta para la evaluación de la tarea. Evidentemente,
sí puede añadir ficheros con las imágenes solicitadas en el enunciado, pero éstas deberán ser
visualizadas correctamente desde este mismo fichero al acceder al repositorio de la tarea.
