from abc import ABC, abstractmethod

class instruccion(ABC):
    '''
        Funciona como la clase padre con la informacion general que almacenan los nodos del AST del codigo.
    '''
    def __init__(self, LINEA, COLUMNA):
        self.linea = LINEA              #Linea donde se encuentra la instruccion
        self.columna = COLUMNA          #Posicion de la fila donde se encuentra la instruccion
    
    @abstractmethod
    def grafo(self):
        pass

    @abstractmethod
    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        pass

    @abstractmethod
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
            - Codigo: Generador del C3D
        '''
        pass