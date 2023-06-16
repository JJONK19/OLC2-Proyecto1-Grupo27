class codigo:
    '''
        Contenedor y creador del C3D. Posee metodos que facilitan el añadir informacion a la creacion del metodo.
    '''
    def __init__(self):
        self.codigo = ""                    #Contenedor del C3D
        self.labels = 1                     #Maneja el número de labels en la ejecucion
        self.temporales = 1                 #Maneja el numero de temporales en la ejecucion
        self.listaTemporales = []           #Almacena los temporales que se van a declarar en el archivo
        

    