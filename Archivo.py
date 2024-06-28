import tkinter as tk
from tkinter import filedialog


class MetodosArchivo:
    def __init__(self):

        self.contenido = "\n"
        self.listaErrores = {}
        self.cantidadLineas = 0

        self.cambiosRealizados = False
        self.direccionArchivo = None 
        
    def limpiarVariables(self):
        self.contenido = ""
        self.errores = ""
        self.listaErrores = {}
        self.cantidadLineas = 0

    def abrirArchivo(self):
        direccionArchivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
        if direccionArchivo:
            with open(direccionArchivo, 'r') as archivo:
                contenido = archivo.read()
            self.direccionArchivo = direccionArchivo
            self.cambiosRealizados = False
            self.vacio = False
            self.cantidadLineas = len(contenido.splitlines())

        return contenido
    
    def marcarCambios(self, contenidoCaja):
        if self.contenido != contenidoCaja:
            self.cambiosRealizados = True 
        else:
            self.cambiosRealizados = False

    def cerrarVentana(self,contenidoCaja,ventana):
        contenido = contenidoCaja
        ventana = ventana

        if self.cambiosRealizados:
            respuesta = tk.messagebox.askyesnocancel("Guardar Cambios", "Deseas guardar los cambios antes de cerrar?")
            if respuesta is None:
                return
            elif respuesta:
                self.guardarArchivo(contenido)
        ventana.destroy()

    def guardarArchivoComo(self,contenidoCaja):
        direccionArchivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if direccionArchivo:
            contenido = contenidoCaja
            with open(direccionArchivo, "w") as archivo:
                archivo.write(contenido)
            self.direccionArchivo = direccionArchivo
            self.cambiosRealizados = False

    def guardarArchivo(self, contenidoCaja):
        if self.direccionArchivo:
            contenido = contenidoCaja
            with open(self.direccionArchivo, "w") as archivo:
                archivo.write(contenido)
            self.cambiosRealizados = False
        else:
            contenido = contenidoCaja
            self.guardarArchivoComo(contenido)
 
    def analizadorSintactico(self):
        line_num = 0
        lines = self.contenido.splitlines()
        self.cantidadLineas = len(lines)
        for line in lines:
            line_num += 1
            line = line.strip()  # Eliminar espacios en blanco al inicio y al final
            if line:  # Si la línea no está vacía
                result = self.parse_string(line, line_num)
                # print(f'Línea {line_num}: {line}: {result}')

        line_num = 0

    # def get_production(self, non_terminal, terminal):
    #     parsing_table = {
    #         'E': {
    #             '+': '',
    #             '*': '',
    #             '(': 'E -> T E\'',
    #             ')': '',
    #             'id': 'E -> T E\'',
    #             '$': ''
    #         },
    #         'E\'': {
    #             '+': 'E\' -> + T E\'',
    #             '*': '',
    #             '(': '',
    #             ')': 'E\' -> ε',
    #             'id': '',
    #             '$': 'E\' -> ε'
    #         },
    #         'T': {
    #             '+': '',
    #             '*': '',
    #             '(': 'T -> F T\'',
    #             ')': '',
    #             'id': 'T -> F T\'',
    #             '$': ''
    #         },
    #         'T\'': {
    #             '+': 'T\' -> ε',
    #             '*': 'T\' -> * F T\'',
    #             '(': '',
    #             ')': 'T\' -> ε',
    #             'id': '',
    #             '$': 'T\' -> ε'
    #         },
    #         'F': {
    #             '+': '',
    #             '*': '',
    #             '(': 'F -> ( E )',
    #             ')': '',
    #             'id': 'F -> id',
    #             '$': ''
    #         }
    #     }
    #     return parsing_table.get(non_terminal, {}).get(terminal, '')

    def get_production(self, non_terminal, terminal):
        parsing_table = {
            'S': {
                'CREATE': 'S -> SQLIns',
                'SELECT': 'S -> SQLIns',
                'INSERT': 'S -> SQLIns',
                'UPDATE': 'S -> SQLIns',
                'DELETE': 'S -> SQLIns',
                'EOF': ''
            },
            'SQLIns': {
                'CREATE': 'SQLIns -> Instruccion_Crear',
                'SELECT': 'SQLIns -> Instruccion_Listar',
                'INSERT': 'SQLIns -> Instruccion_Insertar',
                'UPDATE': 'SQLIns -> Instruccion_Actualizar',
                'DELETE': 'SQLIns -> Instruccion_Eliminar',
                'EOF': ''
            },
            'Instruccion_Crear': {
                'CREATE': 'Instruccion_Crear -> Crear_BD | Crear_TBL | Crear_IDX'
            },
            'Crear_BD': {
                'CREATE': 'Crear_BD -> CREATE DATABASE <nombre_BD>;'
            },
            'Crear_TBL': {
                'CREATE': 'Crear_TBL -> CREATE TABLE <nombre_TBL> (<Columnas_TBL>);'
            },
            'Crear_IDX': {
                'CREATE': 'Crear_IDX -> CREATE INDEX <nombre_IDX> ON <nombre_TBL>(<nombre_COL> <order>);'
            },
            'order': {
                'ASC': 'order -> ASC',
                'DESC': 'order -> DESC',
                'EOF': 'order -> ε',
                '<nombre_COL>': 'order -> ε'
            },
            'Columnas_TBL': {
                '<nombre_COL>': 'Columnas_TBL -> Columna_TBL , Columnas_TBL | Columna_TBL'
            },
            'Columna_TBL': {
                '<nombre_COL>': 'Columna_TBL -> <nombre_COL> <SPACE> <column_definition>'
            },
            'column_definition': {
                'TINYINT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'SMALLINT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'MEDIUMINT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'INT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'INTEGER': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'BIGINT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'REAL': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'DOUBLE': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'FLOAT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'DECIMAL': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'NUMERIC': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'DATE': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'TIME': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'DATETIME': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'VARCHAR': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'TINYTEXT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'TEXT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'MEDIUMTEXT': 'column_definition -> <data_type> <SPACE> <data_type_options>',
                'LONGTEXT': 'column_definition -> <data_type> <SPACE> <data_type_options>'
            },
            'data_type_options': {
                'NOT': 'data_type_options -> NOT NULL',
                'NULL': 'data_type_options -> NULL',
                'AUTO_INCREMENT PRIMARY KEY': 'data_type_options -> AUTO_INCREMENT PRIMARY KEY',
                'PRIMARY KEY': 'data_type_options -> PRIMARY KEY',
                'EOF': 'data_type_options -> ε',
                ')': 'data_type_options -> ε'
            },
            'data_type': {
                'TINYINT': 'data_type -> TINYINT(<length>)',
                'SMALLINT': 'data_type -> SMALLINT(<length>)',
                'MEDIUMINT': 'data_type -> MEDIUMINT(<length>)',
                'INT': 'data_type -> INT(<length>)',
                'INTEGER': 'data_type -> INTEGER(<length>)',
                'BIGINT': 'data_type -> BIGINT(<length>)',
                'REAL': 'data_type -> REAL(<length>,<decimals>)',
                'DOUBLE': 'data_type -> DOUBLE(<length>,<decimals>)',
                'FLOAT': 'data_type -> FLOAT(<length>,<decimals>)',
                'DECIMAL': 'data_type -> DECIMAL(<length>,<decimals>)',
                'NUMERIC': 'data_type -> NUMERIC(<length>,<decimals>)',
                'DATE': 'data_type -> DATE',
                'TIME': 'data_type -> TIME',
                'DATETIME': 'data_type -> DATETIME',
                'VARCHAR': 'data_type -> VARCHAR(<length>)',
                'TINYTEXT': 'data_type -> TINYTEXT',
                'TEXT': 'data_type -> TEXT',
                'MEDIUMTEXT': 'data_type -> MEDIUMTEXT',
                'LONGTEXT': 'data_type -> LONGTEXT'
            },
            'Instruccion_Listar': {
                'SELECT': 'Instruccion_Listar -> SELECT <list_FLD> FROM <table_references> <Where> <Group> <OrderBY>'
            },
            'Where': {
                'WHERE': 'Where -> WHERE <SPACE> <condition>',
                'EOF': 'Where -> ε',
                'GROUP BY': 'Where -> ε',
                'ORDER BY': 'Where -> ε'
            },
            'Group': {
                'GROUP BY': 'Group -> GROUP BY <SPACE> <lista_Columnas>',
                'EOF': 'Group -> ε',
                'ORDER BY': 'Group -> ε'
            },
            'OrderBY': {
                'ORDER BY': 'OrderBY -> ORDER BY <SPACE> <lista_Columnas> <SPACE> <order>',
                'EOF': 'OrderBY -> ε'
            },
            'lista_Columnas': {
                '<nombre_COL>': 'lista_Columnas -> <nombre_COL> , <lista_Columnas> | <nombre_COL>'
            },
            'list_FLD': {
                '<nombre_FLD>': 'list_FLD -> <nombre_FLD> , <list_FLD> | <nombre_FLD>'
            },
            'table_references': {
                '<table_reference>': 'table_references -> <table_reference> , <table_references> | <table_reference>'
            },
            'table_reference': {
                '<table_factor>': 'table_reference -> <table_factor>',
                '<joined_table>': 'table_reference -> <joined_table>'
            },
            'table_factor': {
                '<nombre_TBL>': 'table_factor -> <nombre_TBL> <alias>'
            },
            'alias': {
                'AS': 'alias -> AS <alias_name>',
                '<alias_name>': 'alias -> <alias_name>',
                'EOF': 'alias -> ε'
            },
            'joined_table': {
                'INNER JOIN': 'joined_table -> INNER JOIN <table_factor> <join_specification>',
                'LEFT JOIN': 'joined_table -> LEFT JOIN <table_factor> <join_specification>',
                'RIGHT JOIN': 'joined_table -> RIGHT JOIN <table_factor> <join_specification>'
            },
            'join_specification': {
                'ON': 'join_specification -> ON <condition>',
                'EOF': 'join_specification -> ε'
            },
            'condition': {
                '<expr>': 'condition -> <expr> OR <expr> | <expr> || <expr> | <expr> XOR <expr> | <expr> AND <expr> | <expr> && <expr> | NOT <expr> | ! <expr> | <boolean_primary>',
                'NOT': 'condition -> NOT <expr>',
                '!': 'condition -> ! <expr>',
                '<boolean_primary>': 'condition -> <boolean_primary>'
            },
            'boolean_primary': {
                '<boolean_primary>': 'boolean_primary -> <boolean_primary> IS [NOT] NULL | <boolean_primary> <COMPARISON_OPERATOR> <simple_expr> | <boolean_primary> <COMPARISON_OPERATOR> (<subquery>) | <simple_expr>'
            },
            'simple_expr': {
                '<literal>': 'simple_expr -> <literal>',
                '<identifier>': 'simple_expr -> <identifier>',
                '<variable>': 'simple_expr -> <variable>'
            },
            'Instruccion_Insertar': {
                'INSERT': 'Instruccion_Insertar -> INSERT INTO <nombre_TBL> (<lista_Columnas>) VALUES (value_list)'
            },
            'value_list': {
                '<numeric_literal>': 'value_list -> <value>,<value_list> | <value>',
                '<string_literal>': 'value_list -> <value>,<value_list> | <value>'
            },
            'Instruccion_Actualizar': {
                'UPDATE': 'Instruccion_Actualizar -> UPDATE <SPACE> <nombre_TBL_UPD> <SPACE> SET <SPACE> <assignment_list> <Where>'
            },
            'assignment_list': {
                '<Assignment>': 'assignment_list -> <Assignment>,<assignment_list> | <Assignment>'
            },
            'Assignment': {
                '<nombre_COL>': 'Assignment -> <nombre_COL> = <expr_update>'
            },
            'expr_update': {
                '<literal>': 'expr_update -> <literal>',
                '<identifier>': 'expr_update -> <identifier>',
                '<variable>': 'expr_update -> <variable>'
            },
            'Instruccion_Eliminar': {
                'DELETE': 'Instruccion_Eliminar -> DELETE FROM <SPACE> <nombre_TBL> <Where>'
            },
            'nombre_BD': {
                '<char_sequence>': 'nombre_BD -> <char_sequence>'
            },
            'nombre_TBL': {
                '<char_sequence>': 'nombre_TBL -> <char_sequence>'
            },
            'nombre_IDX': {
                '<char_sequence>': 'nombre_IDX -> <char_sequence>'
            },
            'nombre_COL': {
                '<char_sequence>': 'nombre_COL -> <char_sequence>'
            },
            'nombre_FLD': {
                '<char_sequence>': 'nombre_FLD -> <char_sequence>'
            },
            'nombre_TBL_UPD': {
                '<char_sequence>': 'nombre_TBL_UPD -> <char_sequence>'
            },
            'alias_name': {
                '<char_sequence>': 'alias_name -> <char_sequence>'
            },
            'char_sequence': {
                '<char>': 'char_sequence -> <char><char_sequence> | <char>'
            },
            'char': {
                '<LETTER>': 'char -> <LETTER>',
                '<DIGIT>': 'char -> <DIGIT>',
                '_': 'char -> _'
            },
            'Length': {
                '<DIGITS>': 'Length -> <DIGITS>'
            },
            'DIGITS': {
                '<DIGIT>': 'DIGITS -> <DIGIT> | <DIGIT><DIGITS>'
            },
            'expr': {
                '<char_sequence>': 'expr -> <char_sequence> | <numeric_expr>'
            },
            'numeric_expr': {
                '<numeric_literal>': 'numeric_expr -> <numeric_literal> | <arithmetic_expr>'
            },
            'numeric_literal': {
                '<DIGITS>': 'numeric_literal -> <DIGITS><fraction_part>'
            },
            'fraction_part': {
                '.': 'fraction_part -> .<DIGITS>'
            },
            'arithmetic_expr': {
                '<expr>': 'arithmetic_expr -> <expr><ARITHMETIC_OPERATOR><expr>'
            },
            'value': {
                '<numeric_literal>': 'value -> <numeric_literal>',
                '<string_literal>': 'value -> <string_literal>'
            },
            'string_literal': {
                '"': 'string_literal -> "<CHAR_SEQUENCE_EXT>"'
            },
            'CHAR_SEQUENCE_EXT': {
                '<char_ext>': 'CHAR_SEQUENCE_EXT -> <char_ext><CHAR_SEQUENCE_EXT> | <char_ext>'
            },
            'char_ext': {
                '<LETTER>': 'char_ext -> <LETTER>',
                '<DIGIT>': 'char_ext -> <DIGIT>',
                '<OTHER_CHAR>': 'char_ext -> <OTHER_CHAR>',
                '<SPACE>': 'char_ext -> <SPACE>'
            },
            'literal': {
                '<numeric_literal>': 'literal -> <numeric_literal>',
                '<string_literal>': 'literal -> <string_literal>'
            },
            'identifier': {
                '<char_sequence>': 'identifier -> <char_sequence>'
            },
            'variable': {
                '<char_sequence>': 'variable -> <char_sequence>'
            },
            'SPACE': {
                ' ': 'SPACE -> " "'
            },
            'OTHER_CHAR': {
                '#': 'OTHER_CHAR -> #',
                '$': 'OTHER_CHAR -> $',
                '%': 'OTHER_CHAR -> %',
                '&': 'OTHER_CHAR -> &',
                '(': 'OTHER_CHAR -> (',
                ')': 'OTHER_CHAR -> )',
                ',': 'OTHER_CHAR -> ,',
                ';': 'OTHER_CHAR -> ;',
                '.': 'OTHER_CHAR -> .',
                '?': 'OTHER_CHAR -> ?',
                '¡': 'OTHER_CHAR -> ¡'
            },
            'ARITHMETIC_OPERATOR': {
                '+': 'ARITHMETIC_OPERATOR -> +',
                '-': 'ARITHMETIC_OPERATOR -> -',
                '*': 'ARITHMETIC_OPERATOR -> *',
                '/': 'ARITHMETIC_OPERATOR -> /'
            },
            'LETTER': {
                'a': 'LETTER -> a',
                'b': 'LETTER -> b',
                'c': 'LETTER -> c',
                'd': 'LETTER -> d',
                'e': 'LETTER -> e',
                'f': 'LETTER -> f',
                'g': 'LETTER -> g',
                'h': 'LETTER -> h',
                'i': 'LETTER -> i',
                'j': 'LETTER -> j',
                'k': 'LETTER -> k',
                'l': 'LETTER -> l',
                'm': 'LETTER -> m',
                'n': 'LETTER -> n',
                'o': 'LETTER -> o',
                'p': 'LETTER -> p',
                'q': 'LETTER -> q',
                'r': 'LETTER -> r',
                's': 'LETTER -> s',
                't': 'LETTER -> t',
                'u': 'LETTER -> u',
                'v': 'LETTER -> v',
                'w': 'LETTER -> w',
                'x': 'LETTER -> x',
                'y': 'LETTER -> y',
                'z': 'LETTER -> z',
                'A': 'LETTER -> A',
                'B': 'LETTER -> B',
                'C': 'LETTER -> C',
                'D': 'LETTER -> D',
                'E': 'LETTER -> E',
                'F': 'LETTER -> F',
                'G': 'LETTER -> G',
                'H': 'LETTER -> H',
                'I': 'LETTER -> I',
                'J': 'LETTER -> J',
                'K': 'LETTER -> K',
                'L': 'LETTER -> L',
                'M': 'LETTER -> M',
                'N': 'LETTER -> N',
                'O': 'LETTER -> O',
                'P': 'LETTER -> P',
                'Q': 'LETTER -> Q',
                'R': 'LETTER -> R',
                'S': 'LETTER -> S',
                'T': 'LETTER -> T',
                'U': 'LETTER -> U',
                'V': 'LETTER -> V',
                'W': 'LETTER -> W',
                'X': 'LETTER -> X',
                'Y': 'LETTER -> Y',
                'Z': 'LETTER -> Z'
            },

            'DIGIT': {
                '0': 'DIGIT -> 0',
                '1': 'DIGIT -> 1',
                '2': 'DIGIT -> 2',
                '3': 'DIGIT -> 3',
                '4': 'DIGIT -> 4',
                '5': 'DIGIT -> 5',
                '6': 'DIGIT -> 6',
                '7': 'DIGIT -> 7',
                '8': 'DIGIT -> 8',
                '9': 'DIGIT -> 9'
            },

            'COMPARISON_OPERATOR': {
                '=': 'COMPARISON_OPERATOR -> =',
                '>=': 'COMPARISON_OPERATOR -> >=',
                '>': 'COMPARISON_OPERATOR -> >',
                '<=': 'COMPARISON_OPERATOR -> <=',
                '<': 'COMPARISON_OPERATOR -> <',
                '<>': 'COMPARISON_OPERATOR -> <>',
                '!=': 'COMPARISON_OPERATOR -> !='
            }
        }
                
        return parsing_table.get(non_terminal, {}).get(terminal, '')

    # def get_production(self, non_terminal, terminal):
    #     parsing_table = {
    #         "S": {
    #             "CREATE": "S -> SQLIns",
    #             "SELECT": "S -> SQLIns",
    #             "INSERT": "S -> SQLIns",
    #             "UPDATE": "S -> SQLIns",
    #             "DELETE": "S -> SQLIns",
    #             "EOF": ""
    #         },
    #         "SQLIns": {
    #             "CREATE": "Instruccion_Crear",
    #             "SELECT": "Instruccion_Listar",
    #             "INSERT": "Instruccion_Insertar",
    #             "UPDATE": "Instruccion_Actualizar",
    #             "DELETE": "Instruccion_Eliminar",
    #             "EOF": ""
    #         },
    #         "Instruccion_Crear": {
    #             "CREATE": "Crear_BD",
    #             "SELECT": "Crear_TBL",
    #             "INSERT": "Crear_IDX",
    #             "UPDATE": "Crear_IDX",
    #             "DELETE": "Crear_IDX",
    #             "EOF": ""
    #         },
    #         "Crear_BD": {
    #             "CREATE": "Crear_BD -> CREATE <nombre_BD> '(' lista_Columnas ')' EOF",
    #             "SELECT": "",
    #             "INSERT": "",
    #             "UPDATE": "",
    #             "DELETE": "",
    #             "EOF": ""
    #         },
    #         "Crear_TBL": {
    #             "CREATE": "Crear_TBL -> CREATE <nombre_TBL> '(' Columnas_TBL ')' EOF",
    #             "SELECT": "",
    #             "INSERT": "",
    #             "UPDATE": "",
    #             "DELETE": "",
    #             "EOF": ""
    #         },
    #         "Crear_IDX": {
    #             "CREATE": "Crear_IDX -> CREATE INDEX <nombre_IDX> ON <nombre_TBL> '(' list_FLD ')' EOF",
    #             "SELECT": "",
    #             "INSERT": "",
    #             "UPDATE": "",
    #             "DELETE": "",
    #             "EOF": ""
    #         },
    #         "order": {
    #             "<nombre_COL>": "",
    #             "ε": ""
    #         },
    #         "Columnas_TBL": {
    #             ")": "Columnas_TBL -> ε",
    #             "EOF": ""
    #         },
    #         "Columna_TBL": {
    #             ",": "Columna_TBL -> ε",
    #             ")": "Columna_TBL -> ε",
    #             "EOF": ""
    #         },
    #         # Continuará...

    #         # ... Tabla anterior ...

    #         "column_definition": {
    #             ",": "column_definition -> ε",
    #             ")": "column_definition -> ε",
    #             "EOF": ""
    #         },
    #         "data_type_options": {
    #             ")": "data_type_options -> ε",
    #             "EOF": ""
    #         },
    #         "data_type": {
    #             "(": "data_type -> <tipo_DATOS> data_type_options",
    #             "EOF": ""
    #         },
    #         "Instruccion_Listar": {
    #             "SELECT": "Instruccion_Listar -> SELECT lista_Columnas FROM table_references Where Group OrderBY EOF",
    #             "EOF": ""
    #         },
    #         "Where": {
    #             "GROUP BY": "Where -> WHERE condition",
    #             "ORDER BY": "Where -> WHERE condition",
    #             "EOF": ""
    #         },
    #         "Group": {
    #             "ORDER BY": "Group -> GROUP BY lista_Columnas",
    #             "EOF": ""
    #         },
    #         "OrderBY": {
    #             "EOF": "OrderBY -> ε"
    #         },
    #         "lista_Columnas": {
    #             "<nombre_COL>": "lista_Columnas -> Columna_TBL lista_Columnas",
    #             "EOF": ""
    #         },
    #         "list_FLD": {
    #             "<nombre_FLD>": "list_FLD -> FLD list_FLD",
    #             "EOF": ""
    #         },
    #         "table_references": {
    #             "WHERE": "table_references -> table_reference join_specification",
    #             "GROUP BY": "",
    #             "ORDER BY": "",
    #             "EOF": ""
    #         },
    #         "table_reference": {
    #             ",": "table_reference -> ε",
    #             "EOF": ""
    #         },
    #         "table_factor": {
    #             "INNER JOIN": "table_factor -> <nombre_TBL> alias",
    #             "LEFT JOIN": "table_factor -> <nombre_TBL> alias",
    #             "RIGHT JOIN": "table_factor -> <nombre_TBL> alias",
    #             "EOF": ""
    #         },
    #         "alias": {
    #             "ON": "alias -> AS <alias_name>",
    #             ",": "alias -> ε",
    #             "EOF": "alias -> ε"
    #         },
    #         "joined_table": {
    #             "WHERE": "joined_table -> joined_table join_specification",
    #             "GROUP BY": "",
    #             "ORDER BY": "",
    #             "EOF": ""
    #         },
    #         "join_specification": {
    #             "WHERE": "join_specification -> ε",
    #             "GROUP BY": "",
    #             "ORDER BY": "",
    #             "EOF": ""
    #         },
    #         "condition": {
    #             "AND": "condition -> boolean_primary AND condition",
    #             "OR": "condition -> boolean_primary OR condition",
    #             ",": "condition -> ε",
    #             ")": "condition -> ε",
    #             "EOF": "condition -> ε"
    #         },
    #         "boolean_primary": {
    #             "<expr>": "boolean_primary -> simple_expr",
    #             "NOT": "boolean_primary -> NOT simple_expr",
    #             "!": "boolean_primary -> ! simple_expr",
    #             "<literal>": "boolean_primary -> simple_expr",
    #             "<identifier>": "boolean_primary -> simple_expr",
    #             "<variable>": "boolean_primary -> simple_expr",
    #             "EOF": ""
    #         },
    #         "simple_expr": {
    #             "<literal>": "simple_expr -> value",
    #             "<identifier>": "simple_expr -> value",
    #             "<variable>": "simple_expr -> value",
    #             "EOF": ""
    #         },
    #         "value_list": {
    #             ")": "value_list -> ε",
    #             "EOF": ""
    #         },
    #         "value": {
    #             "<numeric_literal>": "value -> <numeric_literal>",
    #             "<string_literal>": "value -> <string_literal>",
    #             "EOF": ""
    #         },
    #         "Instruccion_Actualizar": {
    #             "UPDATE": "Instruccion_Actualizar -> UPDATE <nombre_TBL> assignment_list Where EOF",
    #             "EOF": ""
    #         },
    #         "assignment_list": {
    #             "WHERE": "assignment_list -> Assignment assignment_list",
    #             "EOF": ""
    #         },
    #         "Assignment": {
    #             "<nombre_COL>": "Assignment -> <nombre_COL> '=' expr_update",
    #             "EOF": ""
    #         },
    #         "expr_update": {
    #             "<literal>": "expr_update -> value",
    #             "<identifier>": "expr_update -> value",
    #             "<variable>": "expr_update -> value",
    #             "EOF": ""
    #         },
    #         "Instruccion_Eliminar": {
    #             "DELETE": "Instruccion_Eliminar -> DELETE FROM <nombre_TBL> Where EOF",
    #             "EOF": ""
    #         }
    #     }
    #     # Tabla completada

    #     return parsing_table.get(non_terminal, {}).get(terminal, '')

    def parse_string(self, input_string, line_num):
        input_tokens = input_string.split() + ['$']  # Añadimos el símbolo de fin de cadena
        stack = ['$', 'S']  # Inicializamos la pila con el símbolo de fin de cadena y el símbolo inicial
        # stack = ['$', 'E']  # Inicializamos la pila con el símbolo de fin de cadena y el símbolo inicial
        index = 0

        while stack:
            top = stack.pop()
            current_token = input_tokens[index]

            if top == current_token:
                if top == '$':
                    # return "Cadena aceptada"
                    return
                index += 1
            elif top in self.get_production(top, current_token):
                production = self.get_production(top, current_token)
                if not production:

                    self.listaErrores[line_num] = f"Cadena no aceptada: carácter inesperado '{current_token}' en posición {index+1}, en línea {line_num}"
                    # return f"Cadena no aceptada: carácter inesperado '{current_token}' en posición {index+1}, en línea {line_num}"
                    return
                _, _, prod_rhs = production.partition(' -> ')
                if prod_rhs != 'ε':
                    for symbol in reversed(prod_rhs.split()):
                        stack.append(symbol)
            else:
                self.listaErrores[line_num] = f"Cadena no aceptada: carácter inesperado '{current_token}' en posición {index+1}, en línea {line_num}\n"
                
                # return f"Cadena no aceptada: carácter inesperado '{current_token}' en posición {index+1}, en línea {line_num}"
                return

        if index < len(input_tokens) - 1:
            
            self.listaErrores[line_num] = f"Cadena no aceptada: carácter inesperado '{input_tokens[index]}' en posición {index+1}, en línea {line_num}"

            # return f"Cadena no aceptada: carácter inesperado '{input_tokens[index]}' en posición {index+1}, en línea {line_num}"
            return
        
        self.listaErrores[line_num] = "Cadena no aceptada"

        # return "Cadena no aceptada"
        return

    def exportarSQL(self, contenido):
        archivo = filedialog.asksaveasfilename(defaultextension=".sql", filetypes=[("SQL files", "*.sql"), ("All files", "*.*")])
    
        if archivo:
            # Guardar el contenido formateado en un archivo .sql
            with open(archivo, 'w') as f:
                f.write(contenido)
            
            tk.messagebox.showinfo("Correcto", "El archivo se ha exportado correctamente")

# Ejemplo de uso
# if __name__ == "__main__":
#     archivo = 'texto.txt'
#     analyze_file(archivo)

    
# if __name__ == "__main__":
#     miObjeto = MetodosArchivo()
    
#     miObjeto.contenido = miObjeto.abrirArchivo()
#     miObjeto.analizadorSintactico()
    
    
    
