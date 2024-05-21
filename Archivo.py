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

    def get_production(self, non_terminal, terminal):
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
        return parsing_table.get(non_terminal, {}).get(terminal, '')

    def parse_string(self, input_string, line_num):
        input_tokens = input_string.split() + ['$']  # Añadimos el símbolo de fin de cadena
        stack = ['$', 'E']  # Inicializamos la pila con el símbolo de fin de cadena y el símbolo inicial
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
    
    
    
