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
        self.encabezado =  "package main;\n"

        # Declarar los imports
        for libreria in self.librerias:
            self.encabezado += f"import \"{libreria}\"\n"

        #Declarar el stack y la pila
        self.encabezado += "var stack [10000000] float64 \nvar heap [10000000]float64\n"

        #Declarar los apuntadores
        self.encabezado += "var P, H float64 \n"

        #Declarar los tokens
        self.encabezado += "var "
        for posicion in range(len(self.listaTemporales)):
            self.encabezado += self.listaTemporales[posicion]
            if posicion == (len(self.listaTemporales) - 1):
                break
            self.encabezado += ", "
        self.encabezado += " float64;\n"

    def generarCodigo(self):
        '''
            Concatena el codigo de las cuatro secciones del archivo:
            1. Encabezado
            2. Nativas
            3. Funciones
            4. Nativas
        '''
        codigo = f'{self.generarEncabezado()}{self.nativas}\n{self.funciones}\nfunc main(){{\n{self.main}\n}}'
        return codigo

    # Insertar ---------------------------------------------------------------------------------------------------------
    def insertar(self, code):
            

    # Temporales -------------------------------------------------------------------------------------------------------
    def agregarTemporal(self):
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
        lbl = f't{self.labels}'
        self.labels += 1
        return lbl

    def colocarLabel(self, lbl):
        '''
            Agrega un Label al código de salida
        '''
        self.codigo += f"{lbl}:\n"
        #codeIn

    # Goto --------------------------------------------------------------------------------
    def agregarGoto(self, lbl):
        '''
            Crea y retorna un nuevo Label destino para la ejecución
        '''
        self.codigo += f"goto {lbl}:\n"
        # codeIn


