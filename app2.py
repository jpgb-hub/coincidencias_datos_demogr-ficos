import jellyfish
from datetime import datetime

# Función Metaphone adaptada para español
def metaphone_es(word):
    word = word.lower()
    word = word.replace("h", "")
    word = word.replace("gue", "ge").replace("gui", "gi").replace("güe", "gue").replace("güi", "gui")
    word = word.replace("ll", "y").replace("ch", "x").replace("v", "b")
    word = word.replace("ce", "se").replace("ci", "si").replace("ge", "je").replace("gi", "ji")
    word = word.replace("z", "s")
    word = word.replace("rr", "r")
    result = ""
    prev_char = ""
    for char in word:
        if char != prev_char:
            result += char
        prev_char = char
    return result.upper()

# Función para comparar fechas
def compare_dates(date1, date2, date_format="%d/%m/%Y"):
    try:
        dt1 = datetime.strptime(date1, date_format)
        dt2 = datetime.strptime(date2, date_format)
    except ValueError:
        return 0
    return 1 if dt1 == dt2 else 0

# Función para evaluar coincidencias
def evaluate_match(patient1, patient2):
    results = {}

    # Metaphone Comparisons
    firstname_meta_sim = metaphone_es(patient1['firstname']) == metaphone_es(patient2['firstname'])
    lastname_meta_sim = metaphone_es(patient1['lastname']) == metaphone_es(patient2['lastname'])
    birthday_sim = compare_dates(patient1['birthday'], patient2['birthday'])
    phone_sim = patient1['phone'] == patient2['phone']
    org_name_sim = patient1['org-name'] == patient2['org-name']
    
    # Verificar y usar la función Jaro-Winkler adecuada
    if hasattr(jellyfish, 'jaro_winkler'):
        jaro_winkler = jellyfish.jaro_winkler
    elif hasattr(jellyfish, 'jaro_winkler_similarity'):
        jaro_winkler = jellyfish.jaro_winkler_similarity
    else:
        raise AttributeError("No se encontró una función Jaro-Winkler en jellyfish.")
    
    # Jaro-Winkler Comparisons
    firstname_jaro_sim = jaro_winkler(patient1['firstname'], patient2['firstname']) > 0.85
    lastname_jaro_sim = jaro_winkler(patient1['lastname'], patient2['lastname']) > 0.85
    
    # Define match rules
    results["firstname-meta,lastname-meta,birthday"] = "MATCH" if firstname_meta_sim and lastname_meta_sim and birthday_sim else "NO_MATCH"
    results["firstname-meta,lastname-meta,phone"] = "MATCH" if firstname_meta_sim and lastname_meta_sim and phone_sim else "NO_MATCH"
    results["firstname-jaro,lastname-jaro,birthday"] = "POSSIBLE_MATCH" if firstname_jaro_sim and lastname_jaro_sim and birthday_sim else "NO_MATCH"
    results["firstname-jaro,lastname-jaro,phone"] = "POSSIBLE_MATCH" if firstname_jaro_sim and lastname_jaro_sim and phone_sim else "NO_MATCH"
    results["lastname-jaro,phone,birthday"] = "POSSIBLE_MATCH" if lastname_jaro_sim and phone_sim and birthday_sim else "NO_MATCH"
    results["firstname-jaro,phone,birthday"] = "POSSIBLE_MATCH" if firstname_jaro_sim and phone_sim and birthday_sim else "NO_MATCH"
    results["org-name"] = "MATCH" if org_name_sim else "NO_MATCH"
    
    return results

# Ejemplo de datos de pacientes
patient1 = {
    'firstname': 'Carlos',
    'lastname': 'Perez',
    'birthday': '15/04/1985',
    'phone': '123456789',
    'org-name': 'Hospital ABC'
}

patient2 = {
    'firstname': 'Karlos',
    'lastname': 'Peres',
    'birthday': '15/04/1985',
    'phone': '123456789',
    'org-name': 'Hospital ABC'
}

# Evaluar coincidencias
results = evaluate_match(patient1, patient2)
for key, value in results.items():
    print(f"{key}: {value}")
