from Dato.Metodo import metodo
from Tipos.Tipos import *

class codigo:
    '''
        Contenedor y creador del C3D. Posee metodos que facilitan el añadir informacion a la creacion del metodo.
        Se va pasando durante toda la ejecucion.
    '''
    def __init__(self):
        self.codigo = ""                    #Contenedor del C3D
        self.encabezado = ""                #Codigo con el encabezado del archivo
        self.main = ""                      #Codigo del entorno global (main)
        self.funciones = ""                 #Codigo con las definiciones de la funcion
        self.nativas = ""                   #Codigo con las definiciones de las nativas
        self.labels = 1                     #Maneja el número de labels en la ejecucion
        self.temporales = 1                 #Maneja el numero de temporales en la ejecucion
        self.listaTemporales = []           #Almacena los temporales que se van a declarar en el archivo
        self.librerias = []                 #Nombre de las librerias de GO que se van a imprimir en el archivo
        self.posicionEscritura = 0          #0 esta en main, 1 esta en funciones, 2 esta en nativas
        self.listaFunciones = {}            #Lista de funciones declaradas en la ejecucion

    # Limpiar ----------------------------------------------------------------------------------
    def limpiar(self):
        self.codigo = ""                    #Contenedor del C3D
        self.encabezado = ""                #Codigo con el encabezado del archivo
        self.main = ""                      #Codigo del entorno global (main)
        self.funciones = ""                 #Codigo con las definiciones de la funcion
        self.nativas = ""                   #Codigo con las definiciones de las nativas
        self.labels = 1                     #Maneja el número de labels en la ejecucion
        self.temporales = 1                 #Maneja el numero de temporales en la ejecucion
        self.listaTemporales = []           #Almacena los temporales que se van a declarar en el archivo
        self.librerias = []                 #Nombre de las librerias de GO que se van a imprimir en el archivo
        self.posicionEscritura = 0          #0 esta en main, 1 esta en funciones, 2 esta en nativas
        self.listaFunciones = {}            #Lista de funciones declaradas en la ejecucion

    #Funciones --------------------------------------------------------------------------------------------------------
    def insertarMetodo(self, ID, PARAMETROS, RETURN, CLASE_RETURN,INSTRUCCIONES, REPORTES, LINEA, COLUMNA):
        '''
            Añade un nuevo metodo al diccionario de metodos y a la lista del reporte.
            - ID: Nombre del metodo.
            - Parametros: Lista de parametros que pide el metodo (atributos[])
            - Instrucciones: Lista de instrucciones (instruccion[])
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        #Verificar que no exista
        if ID in self.listaFunciones:
            REPORTES.salida += "ERROR: El método " + ID + " ya existe. \n"
            mensaje = "El método " + ID + " ya existe. \n"
            REPORTES.añadirError("Semantico", mensaje, LINEA, COLUMNA)
            self.insertar_Comentario("ERROR: El método " + ID + " ya existe.")
            return -1

        #Añadir el metodo a los reportes y a la lista de metodos
        REPORTES.añadirMetodo(ID, Tipo.ANY.value, LINEA, COLUMNA)
        self.listaFunciones[ID] = metodo(ID, PARAMETROS, RETURN, CLASE_RETURN, INSTRUCCIONES)

    def getMetodo(self, ID, REPORTES, LINEA, COLUMNA):
        '''
            Retorna una instancia de metodo.
            - ID: Nombre del metodo.
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
            - Linea: Linea de la instruccion. Para el error.
            - Columna: Columna donde esta el error.
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        if ID in self.listaFunciones:
            retorno = self.listaFunciones[ID]
            return retorno
        else:
            REPORTES.salida += "ERROR: El metodo " + ID + " no existe. \n"
            mensaje = "El metodo " + ID + " no existe."
            REPORTES.añadirError("Semantico", mensaje, LINEA, COLUMNA)
            self.insertar_Comentario("ERROR: El método " + ID + " no existe.")
            return -1
    
 
    #Encabezado --------------------------------------------------------------------------------------------------------
    def libreriasGO(self, LIBRERIA):
        '''
            Recibe el nombre de una libreria en go (fmt, math, etc) y la añade a la lista de librerias. Si esta no existe,
            la añade a la lista.
        '''
        if LIBRERIA not in self.librerias:
            self.librerias.append(LIBRERIA)

    def generarEncabezado(self):
        '''
            Modifica la variable encabezado con el codigo correspondiente.
        '''
        self.encabezado = "package main\n"

        # Declarar los imports
        for libreria in self.librerias:
            self.encabezado += f"import \"{libreria}\"\n"

        #Declarar el stack y la pila
        self.encabezado += "var STACK [10000000]float64 \nvar HEAP [10000000]float64\n"

        #Declarar los apuntadores
        self.encabezado += "var P, H float64 \n"

        #Declarar los tokens
        self.encabezado += "var "
        for posicion in range(len(self.listaTemporales)):
            self.encabezado += self.listaTemporales[posicion]
            if posicion == (len(self.listaTemporales) - 1):
                break
            self.encabezado += ", "
        self.encabezado += " float64\n"
        return self.encabezado

    def generarCodigo(self):
        '''
            Concatena el codigo de las cuatro secciones del archivo:
            1. Encabezado
            2. Nativas
            3. Funciones
            4. Nativas
        '''
        self.codigo = f'{self.generarEncabezado()}{self.nativas}\n{self.funciones}\nfunc main(){{\n{self.main}\n}}'
        return self.codigo

    # Insertar ---------------------------------------------------------------------------------------------------------
    def insertar(self, codigo):
        '''
            Inserta el codigo en la variable correspondiente:
            - 0: Main
            - 1: Funciones
            - 2: Nativas
        '''
        if self.posicionEscritura == 0:
            self.main += codigo
        elif self.posicionEscritura == 1:
            self.funciones += codigo
        else:
            self.nativas += codigo

    # Temporales -------------------------------------------------------------------------------------------------------
    def nuevoTemporal(self):
        '''
            Agrega un temporal nuevo a la lista de temporales y retorna el temporal para su uso.
        '''
        tmp = f't{self.temporales}'
        self.temporales += 1
        self.listaTemporales.append(tmp)
        return tmp

    # Labels --------------------------------------------------------------------------------
    def nuevoLabel(self):
        '''
            Crea y retorna un nuevo Label destino para la ejecución
        '''
        lbl = f'L{self.labels}'
        self.labels += 1
        return lbl

    def insertar_Label(self, lbl):
        '''
            Agrega un Label al código de salida
        '''
        entrada = f"{lbl}:\n"
        self.insertar(entrada)

    # Expresiones --------------------------------------------------------------------------------
    def insertar_Expresion(self, res, izq, op, der):
        '''
            Inserta una expresión al codigo. Recibe la expresión de la izquierda, derecha y el operador,
            almacenado en la variable resultado (res). Todos son temporales.
        '''
        entrada = f'{res} = {izq} {op} {der}\n'
        self.insertar(entrada)

    def insertar_Asignacion(self, res, izq):
        '''
            Asigna una expresión a una variable. Recibe la expresión de la izquierda
            almacenada en la variable resultado (res). Todos son temporales.
        '''
        entrada = f'{res} = {izq}\n'
        self.insertar(entrada)

    # If --------------------------------------------------------------------------------
    def insertar_If(self, izq, operador, der, lbl):
        '''
            Inserta un if en el codigo.
        '''
        entrada = f'if {izq} {operador} {der} {{goto {lbl}}}\n'
        self.insertar(entrada)

    # Goto --------------------------------------------------------------------------------
    def insertar_Goto(self, lbl):
        '''
            Inserta un goto en el codigo. Recibe un label.
        '''
        entrada = f"goto {lbl}\n"
        self.insertar(entrada)

    # Extras -------------------------------------------------------------------------------------------------------
    def insertar_Comentario(self, comentario):
        entrada = "/*" + comentario + "*/\n"
        self.insertar(entrada)

    def insertar_NuevaLinea(self):
        entrada = "fmt.Printf(\"%c\", 10)\n"
        self.insertar(entrada)

    def insertar_Print(self, caracter, valor, casteo = ""):
        #Añadir la libreria
        self.libreriasGO("fmt")
        entrada = f"fmt.Printf(\"%{caracter}\", {casteo}({valor}))\n"
        self.insertar(entrada)
    
    def insertar_Abs(self, res, num):
        #Añadir la libreria
        self.libreriasGO("math")
        entrada = f"{res} = math.Abs({num})\n"
        self.insertar(entrada)

    def insertar_Floor(self, res, num):
        #Añadir la libreria
        self.libreriasGO("math")
        entrada = f"{res} = math.Floor({num})\n"
        self.insertar(entrada)
    
    def insertar_Pow(self, res, a, b):
        #Añadir la libreria
        self.libreriasGO("math")
        entrada = f"{res} = math.Pow({a}, {b} )\n"
        self.insertar(entrada)

    def insertar_Round(self, res, valor):
        #Añadir la libreria
        self.libreriasGO("math")
        entrada = f"{res} = math.Round({valor})\n"
        self.insertar(entrada)

    def insertar_Mod(self, res, valor1, valor2):
        #Añadir la libreria
        self.libreriasGO("math")
        entrada = f"{res} = math.Mod({valor1}, {valor2})\n"
        self.insertar(entrada)

    # Stack / Heap ------------------------------------------------------------------------------------
    # H = H + 1
    def insertar_MoverHeap(self):
        self.insertar("H = H + 1\n")

    # P = P + i
    def insertar_MoverStack(self, index):
        self.insertar(f"P = P + {index}\n")

    # P = P - i
    def insertar_RegresarStack(self, index):
        self.insertar(f"P = P - {index}\n")

    # heap[i]
    def insertar_ObtenerHeap(self, target, index):
        self.insertar(f"{target} = HEAP[int({index})]\n")

    # heap[i] = val
    def insertar_SetearHeap(self, index, value):
        self.insertar(f'HEAP[int({index})] = {value}\n')

    # stack[i]
    def insertar_ObtenerStack(self, target, index):
        self.insertar(f'{target} = STACK[int({index})]\n')

    # heap[i] = val
    def insertar_SetearStack(self, index, value):
        self.insertar(f'STACK[int({index})] = {value}\n')

    # Funciones --------------------------------------------------------------------------------
    def insertar_AperturaFuncion(self, nombre):
        #Mover a la variable de funcioens
        self.posicionEscritura = 1

        entrada = f'func {nombre}(){{\n'
        self.insertar(entrada)

    def insertar_CierreFuncion(self):
        entrada = 'return\n}\n'
        self.insertar(entrada)

        # Mover a la variable de main
        self.posicionEscritura = 0

    def insertar_llamadaFuncion(self, nombre):
        entrada = f'{nombre}()\n'
        self.insertar(entrada)

    # Errores ----------------------------------------------------------------------------------

    def insertar_BoundedError(self):
        #Insertar fmt
        self.libreriasGO("fmt")
        entrada = ""
        entrada += "fmt.Printf(\"%c\", 66)\n"
        entrada += "fmt.Printf(\"%c\", 111)\n"
        entrada += "fmt.Printf(\"%c\", 117)\n"
        entrada += "fmt.Printf(\"%c\", 110)\n"
        entrada += "fmt.Printf(\"%c\", 100)\n"
        entrada += "fmt.Printf(\"%c\", 115)\n"
        entrada += "fmt.Printf(\"%c\", 69)\n"
        entrada += "fmt.Printf(\"%c\", 114)\n"
        entrada += "fmt.Printf(\"%c\", 114)\n"
        entrada += "fmt.Printf(\"%c\", 111)\n"
        entrada += "fmt.Printf(\"%c\", 114)\n"
        entrada += "fmt.Printf(\"%c\", 10)\n"     #Salto de linea despues del print
        self.insertar(entrada)

    def insertar_MathError(self):
        # Insertar fmt
        self.libreriasGO("fmt")

        entrada = ""
        entrada += "fmt.Printf(\"%c\", 77)\n"
        entrada += "fmt.Printf(\"%c\", 97)\n"
        entrada += "fmt.Printf(\"%c\", 116)\n"
        entrada += "fmt.Printf(\"%c\", 104)\n"
        entrada += "fmt.Printf(\"%c\", 69)\n"
        entrada += "fmt.Printf(\"%c\", 114)\n"
        entrada += "fmt.Printf(\"%c\", 114)\n"
        entrada += "fmt.Printf(\"%c\", 111)\n"
        entrada += "fmt.Printf(\"%c\", 114)\n"
        entrada += "fmt.Printf(\"%c\", 10)\n"     #Salto de linea despues del print
        self.insertar(entrada)