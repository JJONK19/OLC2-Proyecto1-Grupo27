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

    ##===========================================  ENCABEZADO ============================================================

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

        #Declarar los imports