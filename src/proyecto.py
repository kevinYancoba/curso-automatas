import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import re

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Ventana Principal")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.create_menu()
        

        # Cuadro de texto 1 (izquierda)
        self.Cuadro_Texto = tk.Text(self.root, wrap=tk.NONE)
        self.Cuadro_Texto.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.scroll_texto = tk.Scrollbar(self.root, command=self.Cuadro_Texto.yview)
        self.scroll_texto.grid(row=0, column=1, sticky="ns")
        self.Cuadro_Texto.config(yscrollcommand=self.scroll_texto.set)

        # Cuadro de texto 2 (derecha)
        self.Cuadro_Tokens = tk.Text(self.root, wrap=tk.NONE)
        self.Cuadro_Tokens.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.scroll_Tokens = tk.Scrollbar(self.root, command=self.Cuadro_Tokens.yview)
        self.scroll_Tokens.grid(row=0, column=3, sticky="ns")
        self.Cuadro_Tokens.config(yscrollcommand=self.scroll_Tokens.set)

        # Cuadro de texto horizontal (inferior)
        self.Cuadro_Texto_Horizontal = tk.Text(self.root, wrap=tk.NONE)
        self.Cuadro_Texto_Horizontal.grid(row=2, column=0, columnspan=4, padx=5, pady=10, sticky="nsew")
        self.scroll_horizontal = tk.Scrollbar(self.root, command=self.Cuadro_Texto_Horizontal.xview, orient='horizontal')
        self.scroll_horizontal.grid(row=1, column=2, padx=10, sticky="ew")
        self.Cuadro_Texto_Horizontal.config(xscrollcommand=self.scroll_horizontal.set)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Abrir", command=self.abrir_archivo)
        archivo_menu.add_command(label="Guardar", command=self.guardar_archivo)
        archivo_menu.add_command(label="Guardar como", command=self.guardar_como_archivo)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Cerrar", command=self.cerrar)

        tokens_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tokens", menu=tokens_menu)
        tokens_menu.add_command(label="Obtener", command=self.obtener_tokens)
        tokens_menu.add_command(label="Clasificar", command=self.clasificar_tokens)

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos Visual Basics", "*.vb")])
        if archivo:
            with open(archivo, "r") as archivo_vb:
                contenido = archivo_vb.read()
                self.Cuadro_Texto.delete("1.0", tk.END)
                self.Cuadro_Texto.insert(tk.END, contenido)

    def guardar_archivo(self):
        contenido = self.Cuadro_Texto.get("1.0", tk.END)
        if not contenido.strip():
            tk.messagebox.showinfo("Error", "El cuadro de texto está vacío. No hay contenido para guardar.")
            return

        if hasattr(self, 'ruta_guardado'):
            ruta_guardado = self.ruta_guardado
        else:
            archivo_guardado = filedialog.asksaveasfilename(defaultextension=".vb", filetypes=[("Archivos Visual Basic", "*.vb")])
            if not archivo_guardado:
                return
            ruta_guardado = archivo_guardado
            self.ruta_guardado = ruta_guardado

        with open(ruta_guardado, "w") as archivo:
            archivo.write(contenido)
        tk.messagebox.showinfo("Éxito", f"Archivo guardado: {ruta_guardado}")


    def guardar_como_archivo(self):
        archivo = filedialog.asksaveasfilename()
        if archivo:
            print(f"Guardando archivo como: {archivo}")

    def cerrar(self):
        contenido_actual = self.Cuadro_Texto.get("1.0", tk.END).strip()

        if hasattr(self, 'ruta_guardado'):
            with open(self.ruta_guardado, "r") as archivo_guardado:
                contenido_guardado = archivo_guardado.read().strip()

            if contenido_actual != contenido_guardado:
                respuesta = tk.messagebox.askyesno("Cambios detectados", "¿Desea guardar los cambios antes de cerrar?")
                if respuesta:
                    self.guardar_archivo()
        else:
            if contenido_actual:
                respuesta = tk.messagebox.askyesno("Guardar cambios", "¿Desea guardar los cambios antes de cerrar?")
                if respuesta:
                    self.guardar_archivo()
        self.root.destroy()

    def obtener_tokens(self):
        programa = self.Cuadro_Texto.get("1.0", tk.END).strip()
        self.Cuadro_Tokens.delete("1.0", tk.END)
        if not programa.strip():
            messagebox.showinfo("Error", "Ingresar un archivo .vb para ejecutar esta función")
            return
        separar_lineas = programa.splitlines()
        for lineas in separar_lineas:
            tokens = lineas.split()
            for index in tokens:
                self.Cuadro_Tokens.insert(tk.END, f"{index},")
            self.Cuadro_Tokens.insert(tk.END, "\n")

    def automata(self, parametro):
        estado = 1
        for index in parametro:
            if estado == 1:
                if '0' <= index <= '9':
                    estado = 2
                elif index in ["+", "-"]:
                    estado = 2
                else:
                    return True
            elif estado == 2:
                if '0' <= index <= '9':
                    estado = 2
                elif index == '.':
                    estado = 3
                elif index == 'E':
                    estado = 5
                else:
                    return True
            elif estado == 3:
                if '0' <= index <= '9':
                    estado = 4
                else:
                    return True
            elif estado == 4:
                if '0' <= index <= '9':
                    estado = 4
                elif index == "E":
                    estado = 5
                else:
                    return True
            elif estado == 5:
                if '0' <= index <= '9':
                    estado = 7
                elif index in ["+", "-"]:
                    estado = 6
                else:
                    return True
            elif estado == 6:
                if '0' <= index <= '9':
                    estado = 7
                else:
                    return True
            elif estado == 7:
                if '0' <= index <= '9':
                    estado = 7
                else:
                    return True

        if estado == 2 or estado == 4 or estado == 7:
            return False
        else:
            return True


    def automata_identificadores(self, parametro):

        minusculas = "abcdefghijklmnopqrstuvwxyz"
        mayusculas = minusculas.upper()

        estado = 1
        for index in parametro:
            if estado == 1:
                if index in minusculas or index in mayusculas:
                    estado = 3
                elif index == '_':
                    estado = 3
                elif '0'<= index <= '9':
                    estado = 2
                else:
                    return True

            elif estado == 2:
                return True

            elif estado == 3:
                if index in minusculas or index in mayusculas:
                    estado = 3
                elif index == '_':
                    estado = 3
                elif '0'<= index <= '9':
                    estado = 3
                else:
                    return True
                
        if estado != 3:
            return True
        else:
            return False
        
    def automata_decimales(self, parametro):
        estado = 0
        for index in parametro:
            if estado == 0:
                if index == '0':
                    estado = 1
                elif index > '0':
                    estado = 5
                elif index == '.':
                    estado = 6
                else:
                    return True
                
            elif estado == 1:
                if '0' <= index <= '7':
                    estado = 8
                elif index in ['x', 'X']:
                    estado = 2
                elif index == '.':
                    estado = 6
                else:
                    return True
                
            elif estado == 2:
                if index in ['a','b','c','d','e','f']:
                    estado = 3
                elif index in ['A','B','C','D','E','F']:
                    estado = 3
                elif '0' <= index <= '9':
                    estado = 3
                else:
                    return True
                
            elif estado == 3:
                if index in ['a','b','c','d','e','f']:
                    estado = 4
                elif index in ['A','B','C','D','E','F']:
                    estado = 4
                elif '0' <= index <= '9':
                    estado = 4
                else:
                    return True
                               
            elif estado == 4:
                if index in ['a','b','c','d', 'e','f']:
                    estado = 3
                elif index in ['A','B','C','D','E','F']:
                    estado = 3
                elif '0' <= index <= '9':
                    estado = 3
                else:
                    return True
                
            elif estado == 5:
                if '0' <= index <= '9':
                    estado = 5
                elif index == '.':
                    estado = 6
                else:
                    return True
                
            elif estado == 6:
                if '0' <= index <= '9':
                    estado = 7
                else:
                    return True
                
            elif estado == 7:
                if '0' <= index <= '9':
                    estado = 7
                else:
                    return True
                
            elif estado == 8:
                if '0' <= index <= '7':
                    estado = 8
                else:
                    return True
        
        if estado != 8 or estado != 5 or estado != 7 or estado != 4:
            return True
        else:
            return False




    def clasificar_tokens(self):
        programa = self.Cuadro_Texto.get("1.0", tk.END).strip()
        self.Cuadro_Tokens.delete("1.0", tk.END)
        palabras_reservadas = [
            "AddHandler", "AddressOf", "Alias", "And", "AndAlso", "As", "Boolean",
            "ByRef", "Byte", "ByVal", "Call", "Case", "Catch", "CBool", "CByte",
            "CChar", "CDate", "CDec", "Char", "CInt", "Class", "CLng", "CObj",
            "Continue", "CSByte", "CShort", "CSng", "CStr", "CType", "Date",
            "Decimal", "Declare", "Default", "Delegate", "Dim", "DirectCast",
            "Do", "Double", "Each", "Else", "ElseIf", "End", "Enum", "Erase",
            "Error", "Event", "Exit", "False", "Finally", "For", "Friend",
            "Function", "Get", "GetType", "GoSub", "GoTo", "Handles", "If",
            "Implements", "Imports", "In", "Inherits", "Integer", "Interface",
            "Is", "Let", "Lib", "Like", "Long", "Loop", "Me", "Mod", "Module",
            "MustInherit", "MustOverride", "MyBase", "MyClass", "Namespace",
            "Narrowing", "New", "Next", "Not", "Nothing", "NotInheritable",
            "NotOverridable", "Object", "Of", "On", "Operator", "Option",
            "Optional", "Or", "OrElse", "Overloads", "Overridable", "Overrides",
            "ParamArray", "Partial", "Private", "Property", "Protected",
            "Public", "RaiseEvent", "ReadOnly", "ReDim", "REM", "RemoveHandler",
            "Resume", "Return", "SByte", "Select", "Set", "Shadows", "Shared",
            "Short", "Single", "Static", "Step", "Stop", "String", "Structure",
            "Sub", "SyncLock", "Then", "Throw", "To", "True", "Try", "TryCast",
            "TypeOf", "UInteger", "ULong", "UShort", "Using", "Variant",
            "Wend", "When", "While", "Widening", "With", "WithEvents", "WriteOnly",
            "Xor"
        ]
        operadores_comparacion = ["=", "+=", "-=", "/", "&", "*=", "/=", "&=", "^=",
                                  "<<=", ">>=", ">>>=", "(", ")","()"]
        operadores_logicos = ["And", "Or", "Not", "AndAlso", "OrElse"]

        separar_lineas = programa.splitlines()
        for i,linea in enumerate(separar_lineas):
            self.Cuadro_Tokens.insert(tk.END, f"{i}  ")
            tokens = linea.split()
            for index in tokens:
                if index in palabras_reservadas:
                    self.Cuadro_Tokens.insert(tk.END, f" ⫺ Pl.Resrv: {index},")
                elif re.match(r"^[0-9\+\-E\.]+$", index):
                    validacion = self.automata(index)
                    if validacion == False:
                        self.Cuadro_Tokens.insert(tk.END, f" ⫺ Nums: {index},")
                    else:
                        self.Cuadro_Tokens.insert(tk.END, f" ⫺ Nums: {index},")
                        self.Cuadro_Texto_Horizontal.insert(tk.END, f"❎ linea:{i} automata Nms: {index}\n")
                elif index in operadores_comparacion:
                    self.Cuadro_Tokens.insert(tk.END, f" ⫺ Opr.Com: {index},")
                elif index in operadores_logicos:
                    self.Cuadro_Tokens.insert(tk.END, f" ⫺ Opr.Logic: {index},")
                else:
                    validacion = self.automata_identificadores(index)
                    if validacion == False:
                        self.Cuadro_Tokens.insert(tk.END, f" ⫺ Id: {index},")
                    else:
                        self.Cuadro_Tokens.insert(tk.END, f" ⫺ Id: {index},")
                        self.Cuadro_Texto_Horizontal.insert(tk.END, f"❎ linea {i} automata Id: {index}\n")
            self.Cuadro_Tokens.insert(tk.END, "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaPrincipal(root)
    root.mainloop()