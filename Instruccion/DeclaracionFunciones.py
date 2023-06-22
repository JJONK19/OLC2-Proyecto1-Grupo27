from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *

class declaracionFuncion(instruccion):
    '''
        Define como viene una funcion.
        - ID: Nombre de la funcion
        - ListaAtributos: Lista de atributos de la funcion. Se reusa la clase atributo de los structs. 
        - Instrucciones: Lista de instrucciones de la funcion. 
        - TipoInstruccion: Indica que es una instruccion de declaracion de funcion
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    def __init__(self, ID, LISTA_ATRIBUTOS, INSTRUCCIONES, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.listaAtributos = LISTA_ATRIBUTOS
        self.instrucciones = INSTRUCCIONES
        self.tipoInstruccion = Instrucciones.DECLARACION_FUNCION.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Definicion Funcion\" ];\n"
        REPORTES.cont += 1

        #Declarar palabra reservada function
        nodoFunction = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunction + "[ label = \"function\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunction + ";\n"

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

        #Declarar instrucciones
        nodoFunctionB = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunctionB + "[ label = \") {\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunctionB + ";\n"

        #Declarar instrucciones
        for instruccion in self.instrucciones:
            nodoInstruccion = instruccion.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoInstruccion + ";\n"
        
        #Declarar while
        nodoFunctionC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunctionC + "[ label = \"} ;\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunctionC + ";\n"
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
        salida = entornoGlobal.insertarMetodo(self.id, atributos, self.instrucciones,  REPORTES, self.linea, self.columna)
        
        if salida == -1:
            return -1
        else:
            return None

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

