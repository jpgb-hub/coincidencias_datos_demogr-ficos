from datetime import datetime
from Levenshtein import distance as levenshtein_distance

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

# Función de distancia de Levenshtein
def levenshtein_similarity(s1, s2):
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    return 1 - distance / max_len

# Función para comparar fechas
def compare_dates(date1, date2, date_format="%d/%m/%Y"):
    try:
        dt1 = datetime.strptime(date1, date_format)
        dt2 = datetime.strptime(date2, date_format)
    except ValueError:
        return 0
    day_sim = 1 if dt1.day == dt2.day else 0
    month_sim = 1 if dt1.month == dt2.month else 0
    year_sim = 1 if dt1.year == dt2.year else 0
    total_similarity = (day_sim + month_sim + year_sim) / 3
    return total_similarity

# Función para calcular la similitud total
def calculate_similarity(patient1, patient2, weights):
    name_sim = levenshtein_similarity(metaphone_es(patient1['nombre']), metaphone_es(patient2['nombre']))
    surname_sim = levenshtein_similarity(metaphone_es(patient1['apellido']), metaphone_es(patient2['apellido']))
    dob_sim = compare_dates(patient1['fecha_nacimiento'], patient2['fecha_nacimiento'])
    commune_sim = levenshtein_similarity(patient1['comuna'], patient2['comuna'])
    
    total_similarity = (
        weights['nombre'] * name_sim +
        weights['apellido'] * surname_sim +
        weights['fecha_nacimiento'] * dob_sim +
        weights['comuna'] * commune_sim
    )
    return total_similarity

# Ejemplo de datos de pacientes
patient1 = {
    'nombre': 'Carlos',
    'apellido': 'Perez',
    'fecha_nacimiento': '15/04/1985',
    'comuna': 'Santiago'
}

patient2 = {
    'nombre': 'Karlos',
    'apellido': 'Peres',
    'fecha_nacimiento': '15/04/1998',
    'comuna': 'Santiago'
}

# Pesos para cada variable
weights = {
    'nombre': 0.4,
    'apellido': 0.3,
    'fecha_nacimiento': 0.2,
    'comuna': 0.1
}

# Calcular la similitud
similarity_score = calculate_similarity(patient1, patient2, weights)
print(f"Puntuación de similitud entre los pacientes: {similarity_score:.2f}")

# Umbral para considerar una coincidencia
threshold = 0.9
if similarity_score >= threshold:
    print("Los pacientes coinciden.")
else:
    print("Los pacientes no coinciden.")
