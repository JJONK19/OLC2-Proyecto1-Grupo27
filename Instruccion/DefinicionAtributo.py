from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Dato.Estructura import atributo

class DefinicionAtributo(instruccion):
    '''
        Define un atributo para la definicion del struct.
        - ID: Nombre del atributo
        - Tipo: Tipo del atributo 
        - Clase: Clase a la que pertenece el atributo
        - TipoInstruccion: Indica que es una instruccion de tipo dedinicion atrbuto
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    def __init__(self, ID, TIPO, CLASE, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.tipo = TIPO
        self.clase = CLASE
        self.tipoInstruccion = Instrucciones.DEFINICION_ATRIBUTO.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Atributo\" ];\n"
        REPORTES.cont += 1

        #Declarar nombre
        nodoID = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoID + "[ label = \""+self.id+"\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoID + ";\n"

        #Nodo complementario :
        nodoDospts = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoDospts + "[ label = \":\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoDospts + ";\n"

        #Declarar Tipado
        nodoTipado = "NODO" + str(REPORTES.cont)
        tipado = ""
        if self.tipo == Tipo.ANY.value:
            tipado = "Any"
        elif self.tipo == Tipo.NUMBER.value:
            tipado = "Number"
        elif self.tipo == Tipo.STRING.value:
            tipado = "String"
        elif self.tipo == Tipo.BOOLEAN.value:
            tipado = "Boolean"

        REPORTES.dot += nodoTipado + "[ label = \"" + tipado + "\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoTipado + ";\n"

        # Nodo complementario ;
        nodoPtcoma = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoPtcoma + "[ label = \";\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoPtcoma + ";\n"

        return padre
    
    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        #Para crear un atributo any, se debe ver si un atributo es de tipo any y clase primitiva
        #En la declaracion del arbol, era la forma facil sin ser redundante en la gramatica
        if self.tipo == Tipo.ANY.value and self.clase == Clases.PRIMITIVO.value:
            self.clase = Clases.ANY.value
        
        #Crear atributo con los valores y retornar
        return atributo(self.id, self.tipo, self.clase)
        
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

