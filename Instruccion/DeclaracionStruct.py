from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor

class DeclaracionStruct(instruccion):
    '''
        Declara el struct. Almacena una lista con los valores y los nombres
        - Valor: Contiene el valor (5, true, false, etc).
        - TipoInstruccion: Indica que es una instruccion de tipo print
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    def __init__(self, ID, TIPO, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.tipo = TIPO
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.DECLARACION_STRUCT.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Declaracion Struct\" ];\n"
        REPORTES.cont += 1

        #Declarar palabra reservada Let
        nodoLet = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLet + "[ label = \"Let\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLet + ";\n"

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
        REPORTES.dot += nodoTipado + "[ label = \"" + self.tipo + "\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoTipado + ";\n"

        nodoIgual = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoIgual + "[ label = \"=\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoIgual + ";\n"

        nodoExp = self.expresion.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoExp + ";\n"

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
        #Extraer valores
        expresionEvaluar = self.expresion.analisis(SIMBOLOS, REPORTES)
        
        #Verificar que no sea nulo
        if expresionEvaluar.tipo == Tipo.NULL.value:
            REPORTES.salida += "ERROR: No se puede asignar NULL a un primitivo. \n"
            mensaje = "No se puede asignar NULL a un primitivo."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return -1
        
        #Comprobar que sea primitivo
        if expresionEvaluar.clase != Clases.STRUCT.value:
            REPORTES.salida += "ERROR: Una variable struct solo recibe structs. \n"
            mensaje = "Una variable struct solo recibe structs."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return -1
        
        #Comprobar que el tipo sea el mismo que la variable
        if expresionEvaluar.tipo != self.tipo:
            REPORTES.salida += "ERROR: Struct " + self.tipo + " no recibe " + expresionEvaluar.tipo + ". \n"
            mensaje = "Struct " + self.tipo + " no recibe " + expresionEvaluar.tipo + "."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return -1
        
        nuevo = expresionEvaluar

        #Añadir el id de la variable a valor
        nuevo.id = self.id
        nuevo.linea = self.linea
        nuevo.columna = self.columna

        #Enviar al entorno local
        local = SIMBOLOS[-1]
        salida = local.insertarSimbolo(nuevo, REPORTES)
        
        if salida == -1:
            return -1
        else:
            return None

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

