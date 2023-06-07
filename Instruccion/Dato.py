from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
 
class dato(instruccion):
    '''
        Almacena los datos para crear un valor de tipo primitivo (string, bool, number).
        Siempre retorna un primitivo al ejecutarse.
        - Valor: Contiene el valor (5, true, false, etc). Siempre es un string.
        - Tipo: Contiene el tipo del valor (number, string, bool)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, VALOR, TIPO, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.valor = VALOR
        self.tipo = TIPO
        self.clase = Clases.PRIMITIVO.value
        self.tipoInstruccion = Instrucciones.DATO.value

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

