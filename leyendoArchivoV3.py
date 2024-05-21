# tabla_de_analisis.py

# Tabla de análisis sintáctico representada como un diccionario anidado
parsing_table = {
    'E': {
        '+': '',
        '*': '',
        '(': 'E -> T E\'',
        ')': '',
        'id': 'E -> T E\'',
        '$': ''
    },
    'E\'': {
        '+': 'E\' -> + T E\'',
        '*': '',
        '(': '',
        ')': 'E\' -> ε',
        'id': '',
        '$': 'E\' -> ε'
    },
    'T': {
        '+': '',
        '*': '',
        '(': 'T -> F T\'',
        ')': '',
        'id': 'T -> F T\'',
        '$': ''
    },
    'T\'': {
        '+': 'T\' -> ε',
        '*': 'T\' -> * F T\'',
        '(': '',
        ')': 'T\' -> ε',
        'id': '',
        '$': 'T\' -> ε'
    },
    'F': {
        '+': '',
        '*': '',
        '(': 'F -> ( E )',
        ')': '',
        'id': 'F -> id',
        '$': ''
    }
}

# Función para obtener la producción dada una entrada
def get_production(non_terminal, terminal):
    return parsing_table.get(non_terminal, {}).get(terminal, '')

# Función para analizar sintácticamente una cadena
def parse_string(input_string, line_num):
    input_tokens = input_string.split() + ['$']  # Añadimos el símbolo de fin de cadena
    stack = ['$', 'E']  # Inicializamos la pila con el símbolo de fin de cadena y el símbolo inicial
    index = 0

    while stack:
        top = stack.pop()
        current_token = input_tokens[index]

        if top == current_token:
            if top == '$':
                return "Cadena aceptada"
            index += 1
        elif top in parsing_table:
            production = get_production(top, current_token)
            if not production:
                return f"Cadena no aceptada: carácter inesperado '{current_token}' en posición {index+1}, en línea {line_num}"
            _, _, prod_rhs = production.partition(' -> ')
            if prod_rhs != 'ε':
                for symbol in reversed(prod_rhs.split()):
                    stack.append(symbol)
        else:
            return f"Cadena no aceptada: carácter inesperado '{current_token}' en posición {index+1}, en línea {line_num}"

    if index < len(input_tokens) - 1:
        return f"Cadena no aceptada: carácter inesperado '{input_tokens[index]}' en posición {index+1}, en línea {line_num}"

    return "Cadena no aceptada"

# Función para leer y analizar un archivo de texto
def analyze_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, 1):
                line = line.strip()  # Eliminar espacios en blanco al inicio y al final
                if line:  # Si la línea no está vacía
                    result = parse_string(line, line_num)
                    print(f'Línea {line_num}: {line}: {result}')
    except FileNotFoundError:
        print(f'Error: El archivo {filename} no fue encontrado.')

# Ejemplo de uso
if __name__ == "__main__":
    archivo = 'texto.txt'
    analyze_file(archivo)
