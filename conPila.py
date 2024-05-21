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
def parse_string(input_string):
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
                return "Cadena no aceptada"
            _, _, prod_rhs = production.partition(' -> ')
            if prod_rhs != 'ε':
                for symbol in reversed(prod_rhs.split()):
                    stack.append(symbol)
        else:
            return "Cadena no aceptada"

    return "Cadena no aceptada"

# Ejemplo de uso
if __name__ == "__main__":
    cadena = "id + id"
    resultado = parse_string(cadena)
    print(resultado)
