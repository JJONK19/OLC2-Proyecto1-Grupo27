from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *

class expresionUnaria(instruccion):
    '''
        Almacena el contenido de una operacion con dos valores (suma, mayor que, igual, etc).
        Siempre retorna un primitivo al ejecutarse.
        - Expresion: Contiene una instruccion que puede ser otra operacion o un valor.
        - TipoOperacion: Contiene un string que indica que operacion se va a realizar (suma, resta, potencia, etc)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    
    def __init__(self, EXPRESION, TIPO_OPERACION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.expresion = EXPRESION
        self.tipoOperacion = TIPO_OPERACION
        self.tipoInstruccion = Instrucciones.OPERACION.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Expresion\" ];\n"
        REPORTES.cont += 1

        #Declarar operador
        nodoOperador = "NODO" + str(REPORTES.cont)
        operador = ""
        if self.tipoOperacion == Expresion.UNARIO.value:
            operador = "-"
        elif self.tipoOperacion == Expresion.UNARIO.value:
            operador = "!"
        REPORTES.dot += nodoOperador + "[ label = \"" +  operador + "\" ];\n"
        REPORTES.cont += 1

        #Declarar operacion
        nodoExpresion = self.expresion.grafo(REPORTES)

        #Conectar con el padre
        REPORTES.dot += padre + "->" + nodoOperador + ";\n"
        REPORTES.dot += padre + "->" + nodoExpresion + ";\n"
        return padre    

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        pass

    def c3d(self):
        pass
