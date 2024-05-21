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
        ')': 'E\' -> \'\'',
        'id': '',
        '$': 'E\' -> \'\''
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
        '+': 'T\' -> \'\'',
        '*': 'T\' -> * F T\'',
        '(': '',
        ')': 'T\' -> \'\'',
        'id': '',
        '$': 'T\' -> \'\''
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

# Ejemplo de uso
if __name__ == "__main__":
    ejemplos = [
        ('E', '('),
        ('E', 'id'),
        ('E\'', '+'),
        ('T\'', '*'),
        ('F', 'id'),
    ]
    
    for non_terminal, terminal in ejemplos:
        production = get_production(non_terminal, terminal)
        print(f'Producción para ({non_terminal}, {terminal}): {production}')
