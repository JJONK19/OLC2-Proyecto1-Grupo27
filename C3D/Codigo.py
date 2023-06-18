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

    def insertar_Modulo(self, res, izq, der):

        '''
            Inserta la operación Modulo con la librería Math.
            Recibe la expresión de la izquierda, derecha y el operador,
            almacenado en la variable resultado (res). Todos son temporales.
        '''

        entrada = f'{res} = math.Mod({izq}, {der})\n'
        self.insertar(entrada)

        #Insertar math a la lista de librerias
        self.libreriasGO("math")

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
        entrada = f"fmt.Printf(\"%{caracter}\", {casteo}({valor}))\n"
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
        entrada += "fmt.Printf(\"%c\", 66)"
        entrada += "fmt.Printf(\"%c\", 111)"
        entrada += "fmt.Printf(\"%c\", 117)"
        entrada += "fmt.Printf(\"%c\", 110)"
        entrada += "fmt.Printf(\"%c\", 100)"
        entrada += "fmt.Printf(\"%c\", 115)"
        entrada += "fmt.Printf(\"%c\", 69)"
        entrada += "fmt.Printf(\"%c\", 114)"
        entrada += "fmt.Printf(\"%c\", 114)"
        entrada += "fmt.Printf(\"%c\", 111)"
        entrada += "fmt.Printf(\"%c\", 114)"
        self.insertar(entrada)

    def insertar_MathError(self):
        # Insertar fmt
        self.libreriasGO("fmt")

        entrada = ""
        entrada += "Printf(\"%c\", 77)"
        entrada += "Printf(\"%c\", 97)"
        entrada += "Printf(\"%c\", 116)"
        entrada += "Printf(\"%c\", 104)"
        entrada += "Printf(\"%c\", 69)"
        entrada += "Printf(\"%c\", 114)"
        entrada += "Printf(\"%c\", 114)"
        entrada += "Printf(\"%c\", 111)"
        entrada += "Printf(\"%c\", 114)"
        self.insertar(entrada)