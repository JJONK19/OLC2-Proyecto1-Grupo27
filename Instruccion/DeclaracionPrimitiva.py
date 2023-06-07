from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *


class DeclaracionPrimitiva(instruccion):
    '''
        Añade texto a la variable "salida" de los reportes.
        Siempre retorna un primitivo al ejecutarse.
        - Valor: Contiene el valor (5, true, false, etc).
        - TipoInstruccion: Indica que es una instruccion de tipo print
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    #todo cambiar constructores
    def __init__(self, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.PRINT.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Impresion\" ];\n"
        REPORTES.cont += 1

        # Declarar funcion
        nodoFuncionA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncionA + "[ label = \"Console.log(\" ];\n"
        REPORTES.cont += 1

        # Declarar operacion
        nodoExpresion = self.expresion.grafo(REPORTES)

        # Declarar cierre de funcion
        nodoFuncionC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncionC + "[ label = \")\" ];\n"
        REPORTES.cont += 1

        # Conectar con el padre
        REPORTES.dot += padre + "->" + nodoFuncionA + ";\n"
        REPORTES.dot += padre + "->" + nodoExpresion + ";\n"
        REPORTES.dot += padre + "->" + nodoFuncionC + ";\n"
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

