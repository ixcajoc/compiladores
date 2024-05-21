from tkinter import *
import tkinter as tk
from tkinter import filedialog
from Archivo import MetodosArchivo


objetoAbrir = MetodosArchivo()


def insertarContenido():
    limpiarContenido()
    info = objetoAbrir.abrirArchivo()
    txtCargarArchivo.delete("1.0", tk.END)
    txtCargarArchivo.insert(tk.END, info)

def obtenerInfo():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    if infoActual == "\n":
        tk.messagebox.showerror("Ningún Archivo Cargado",
                                 "Aún no ha cargado ningun archivo para obtener los tokens")
        return
    else:
        objetoAbrir.contenido = infoActual

def analize_file():
    obtenerInfo()
    objetoAbrir.analizadorSintactico()
    txtErrores.delete("1.0", tk.END)
    ventanaErrores()
    # texto = objetoAbrir.separarTokens()
    # enumerar()
    txtConvertirArchivo.delete("1.0", tk.END)
    # txtConvertirArchivo.insert(tk.END, texto)

def ventanaErrores():
    textoErrores = objetoAbrir.errores
    txtErrores.delete("1.0", tk.END)
    txtErrores.insert(tk.END, textoErrores)
    objetoAbrir.errores = ""
    
def Guardar():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.marcarCambios(infoActual)
    objetoAbrir.guardarArchivo(infoActual)

def guardarComo():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.guardarArchivoComo(infoActual)

def cerrar():
    infoActual = txtCargarArchivo.get("1.0", tk.END)
    objetoAbrir.marcarCambios(infoActual)
    # objetoAbrir.cerrarVentana(infoActual,interfaz)
    interfaz.protocol("WM_DELETE_WINDOW", 
                      objetoAbrir.cerrarVentana(infoActual,interfaz))

    # interfaz.destroy()

def limpiarContenido():
    txtErrores.delete("1.0", tk.END)
    txtConvertirArchivo.delete("1.0", tk.END)
    txtCargarArchivo.delete("1.0", tk.END)
    txtlineaNumerica.delete("1.0", tk.END)
    txtlineaNumerica.config(state="normal")
    objetoAbrir.limpiarVariables()

def enumerar():
    txtlineaNumerica.config(state="normal")
    txtlineaNumerica.delete("1.0", tk.END)

    for i in range(1,objetoAbrir.cantidadLineas+1):
        txtlineaNumerica.insert(tk.END, f"{i}\n")
    txtlineaNumerica.config(state="disabled")

   


interfaz = tk.Tk()
interfaz.title("Analizador Sintactico")
interfaz.geometry("1366x768")
interfaz.attributes('-fullscreen', True)
interfaz.config(background="white")

barraMenu = tk.Menu(interfaz)

subMenuArchivo = tk.Menu(barraMenu, tearoff=0)
subMenuArchivo.add_command(label="Abrir",command=insertarContenido)
subMenuArchivo.add_command(label="Guardar", command=Guardar)
subMenuArchivo.add_command(label="Guardar como...", command=guardarComo)
subMenuArchivo.add_command(label="Limpiar contenido", command=limpiarContenido)

subMenuTokens = tk.Menu(barraMenu, tearoff=0)
subMenuTokens.add_command(label="Obtener", command=analize_file)  
subMenuTokens.add_command(label="Clasificar")
subMenuTokens.add_command(label="Sistemas Numericos")

subMenuSalir = tk.Menu(barraMenu, tearoff=0)
subMenuSalir.add_command(label="Cerrar Programa",command=interfaz.destroy)  

#hago los menus
barraMenu.add_cascade(label="Archivo", menu=subMenuArchivo)
barraMenu.add_cascade(label="Tokens", menu=subMenuTokens)
barraMenu.add_cascade(label="Salir", menu=subMenuSalir)

interfaz.config(menu=barraMenu)

txtCargarArchivo = tk.Text(interfaz, wrap="none", width=80, height=32,
                           highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtCargarArchivo.place(x= 15, y = 10)
txtCargarArchivo.config(padx=10,pady=10)

txtConvertirArchivo = tk.Text(interfaz, wrap="none", width=80, height=32,
                            highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtConvertirArchivo.place(x= 693, y=10)
txtConvertirArchivo.config(padx= 10,pady=10)

txtlineaNumerica = tk.Text(interfaz, wrap="none", width=3, height=32,
                           highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtlineaNumerica.place(x= 673, y=10)
txtlineaNumerica.config(pady=10, fg="red")

def sincornizar(txtOrigen, txtDestino):
    def sincroDesplazamiento(*args):
        fraccion = txtOrigen.yview()[0]
        txtDestino.yview_moveto(fraccion)

    return sincroDesplazamiento

sincroConvertirAlinea = sincornizar(txtConvertirArchivo, txtlineaNumerica)
sincroLineaAconvertir = sincornizar(txtlineaNumerica, txtConvertirArchivo)

txtConvertirArchivo.config(yscrollcommand=sincroConvertirAlinea)
txtlineaNumerica.config(yscrollcommand=sincroLineaAconvertir)


txtErrores = tk.Text(interfaz, wrap="none", width=164, height=10,
                    highlightthickness=1,highlightbackground="#7D8081",bd=0)
txtErrores.place(x= 15, y=550)
txtErrores.config(padx=10,pady=10)



# interfaz.protocol("WM_DELETE_WINDOW", cerrar)
  
interfaz.mainloop()
