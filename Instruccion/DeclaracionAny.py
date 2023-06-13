from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor

class DeclaracionAny(instruccion):
    '''
        Declara una variable any. Contiene primitivos y vectores
        - ID: Nombre de la variable
        - Tipo: Tipo ANY
        - Clase: Clase ANY
        - Expresion: Contiene el valor (5, true, false, etc).
        - TipoInstruccion: Indica que es una instruccion de tipo declaracion any
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    def __init__(self, ID, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.tipo= Tipo.ANY.value
        self.clase = Clases.ANY.value
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.DECLARACION_ANY.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Declaracion Any\" ];\n"
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

        if self.expresion != None:
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
        #TRABAJAR CON LA EXPRESION Y CREAR EL VALOR
        nuevo = ""
        if self.expresion == None:
            nuevo = valor()
            nuevo.tipo = self.tipo
            nuevo.valor = ""
            nuevo.clase = self.clase
            nuevo.valorClase = Clases.PRIMITIVO.value
            nuevo.valorTipo = Tipo.STRING.value

        else:
            #Extraer valores
            expresionEvaluar = self.expresion.analisis(SIMBOLOS, REPORTES)
            expresionEvaluar.tipo = Tipo.ANY.value
            expresionEvaluar.clase = Clases.ANY.value
            nuevo = expresionEvaluar

        #Añadir el id de la variable a valor
        nuevo.id = self.id
      
        #Enviar al entorno local
        local = SIMBOLOS[-1]
        salida = local.insertarSimbolo(nuevo, REPORTES)
        
        if salida == -1:
            return -1
        else:
            return None
        
    def c3d(self):
        pass