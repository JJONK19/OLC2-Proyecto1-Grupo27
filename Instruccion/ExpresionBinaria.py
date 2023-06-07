from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *

class expresionBinaria(instruccion):
    '''
        Almacena el contenido de una operacion con dos valores (suma, mayor que, igual, etc).
        Siempre retorna un primitivo al ejecutarse.
        - Izquierda: Contiene una instruccion que puede ser otra operacion o un valor.
        - Derecha: Contiene una instruccion que puede ser otra operacion o un valor.
        - TipoOperacion: Contiene un string que indica que operacion se va a realizar (suma, resta, potencia, etc)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, IZQUIERDA, DERECHA, TIPO_OPERACION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.izquierda = IZQUIERDA
        self.derecha = DERECHA
        self.tipoOperacion = TIPO_OPERACION
        self.tipoInstruccion = Instrucciones.OPERACION.value

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
