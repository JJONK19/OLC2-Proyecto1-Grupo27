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
    def __init__(self, ID, TIPO, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.tipoDeclaracion = TIPO
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.DECLARACION_PRIMITIVA.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Declaración\" ];\n"
        REPORTES.cont += 1

        #Declarar palabra reservada Let
        nodoLet = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLet + "[ label = \"Let\" ];\n"
        REPORTES.cont += 1

        nodoID = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoID + "[ label = \""+self.id+"\" ];\n"
        REPORTES.cont += 1

        #Nodo complementario :
        nodoDospts = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoDospts + "[ label = \":\" ];\n"
        REPORTES.cont += 1

        #Declarar Tipado
        nodoTipado = "NODO" + str(REPORTES.cont)
        tipado = ""
        if self.tipoDeclaracion == Tipo.ANY.value:
            tipado = "Any"
        elif self.tipoDeclaracion == Tipo.NULL.value:
            tipado = "Null"
        elif self.tipoDeclaracion == Tipo.NUMBER.value:
            tipado = "Number"
        elif self.tipoDeclaracion == Tipo.STRING.value:
            tipado = "String"
        elif self.tipoDeclaracion == Tipo.BOOLEAN.value:
            tipado = "Boolean"
        else:
            tipado = "Any"

        REPORTES.dot += nodoTipado + "[ label = \"" + tipado + "\" ];\n"
        REPORTES.cont += 1

        # Nodo complementario =
        nodoIgual = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoIgual + "[ label = \"=\" ];\n"
        REPORTES.cont += 1

        nodoExp = self.expresion.grafo(REPORTES)

        # Nodo complementario ;
        nodoPtcoma = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoPtcoma + "[ label = \";\" ];\n"
        REPORTES.cont += 1

        #Conectar con el padre
        REPORTES.dot += padre + "->" + nodoLet + ";\n"
        REPORTES.dot += padre + "->" + nodoID + ";\n"
        REPORTES.dot += padre + "->" + nodoDospts + ";\n"
        REPORTES.dot += padre + "->" + nodoTipado + ";\n"
        REPORTES.dot += padre + "->" + nodoIgual + ";\n"
        REPORTES.dot += padre + "->" + nodoExp + ";\n"
        REPORTES.dot += padre + "->" + nodoPtcoma + ";\n"
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

