from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *

class DefinicionStruct(instruccion):
    '''
        Define como viene un struct.
        - ID: Nombre del struct
        - ListaAtributos: Lista de atributos del struct 
        - TipoInstruccion: Indica que es una instruccion de tipo declaracion primitiva
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    #todo cambiar constructores
    def __init__(self, ID, LISTA_ATRIBUTOS, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.listaAtributos = LISTA_ATRIBUTOS
        self.tipoInstruccion = Instrucciones.DECLARACION_STRUCT.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[color = \"brown\", style =\"radial\", fillcolor = \"gold:brown\", gradientangle = \"315\", label = \"Definicion Struct\" ];\n"
        REPORTES.cont += 1

        #Declarar palabra reservada interface
        nodoLet = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLet + "[ label = \"Interface\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLet + ";\n"

        nodoID = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoID + "[ label = \""+self.id+"\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoID + ";\n"

        #Nodo complementario :
        nodoLlA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlA + "[ label = \"{\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlA + ";\n"

        #Declarar atributos
        for i in self.listaAtributos:
            nodoAtributo = i.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoAtributo + ";\n"

        #Nodo complementario :
        nodoLlC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlC + "[ label = \"}\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlC + ";\n"

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
        atributos = []
        #Crear la lista de atributos
        for i in self.listaAtributos:
            atributos.append(i.analisis(SIMBOLOS, REPORTES))
        
        #Enviar al entorno global la estructura
        entornoGlobal = SIMBOLOS[0]
        salida = entornoGlobal.insertarEstructura(self.id, atributos, REPORTES, self.linea, self.columna)
        
        if salida == -1:
            return -1
        else:
            return None

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

