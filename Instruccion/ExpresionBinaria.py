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

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Expresion\" ];\n"
        REPORTES.cont += 1

        #Declarar operador izquiedo
        nodoIzquierdo = self.izquierda.grafo(REPORTES)

        #Declarar operador
        nodoOperador = "NODO" + str(REPORTES.cont)
        operador = ""
        if self.tipoOperacion == Expresion.SUMA.value:
            operador = "+"
        elif self.tipoOperacion == Expresion.RESTA.value:
            operador = "-"
        elif self.tipoOperacion == Expresion.MULTIPLICACION.value:
            operador = "*"
        elif self.tipoOperacion == Expresion.DIVISION.value:
            operador = "/"
        elif self.tipoOperacion == Expresion.POT.value:
            operador = "^"
        elif self.tipoOperacion == Expresion.MOD.value:
            operador = "%"
        elif self.tipoOperacion == Expresion.IGUALACION.value:
            operador = "==="
        elif self.tipoOperacion == Expresion.DISTINTO.value:
            operador = "!="
        elif self.tipoOperacion == Expresion.MAYORQ.value:
            operador = ">"
        elif self.tipoOperacion == Expresion.MENORQ.value:
            operador = "<"
        elif self.tipoOperacion == Expresion.MAYORIG.value:
            operador = ">="
        elif self.tipoOperacion == Expresion.MENORIG.value:
            operador = "<"
        elif self.tipoOperacion == Expresion.OR.value:
            operador = "||"
        elif self.tipoOperacion == Expresion.AND.value:
            operador = "&&"
        REPORTES.dot += nodoOperador + "[ label = \"" +  operador + "\" ];\n"
        REPORTES.cont += 1

        #Declarar operador derecho
        nodoDerecho = self.derecha.grafo(REPORTES)

        #Conectar con el padre
        REPORTES.dot += padre + "->" + nodoIzquierdo + ";\n"
        REPORTES.dot += padre + "->" + nodoOperador + ";\n"
        REPORTES.dot += padre + "->" + nodoDerecho + ";\n"
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
