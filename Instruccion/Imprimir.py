from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
 
class imprimir(instruccion):
    '''
        Añade texto a la variable "salida" de los reportes.
        Siempre retorna un primitivo al ejecutarse.
        - Valor: Contiene el valor (5, true, false, etc).
        - TipoInstruccion: Indica que es una instruccion de tipo print
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.PRINT.value

    def grafo(self):
        pass

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        pass

    def c3d(self):
        pass

