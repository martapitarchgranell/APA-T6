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