from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor

class DeclaracionPrimitiva(instruccion):
    '''
        Declara un primitivo.
        - ID: Nombre de la variable
        - Tipo: Tipo del primitivo
        - Expresion: Contiene el valor (5, true, false, etc).
        - TipoInstruccion: Indica que es una instruccion de tipo declaracion primitiva
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    def __init__(self, ID, TIPO, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.tipo = TIPO
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.DECLARACION_PRIMITIVA.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Declaracion Primitiva\" ];\n"
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

            #Definir valor por defecto
            if self.tipo == Tipo.BOOLEAN.value:
                nuevo.valor = "true"
            elif self.tipo == Tipo.STRING.value:
                nuevo.valor = ""
            elif self.tipo == Tipo.NUMBER.value:
                nuevo.valor = "0"

            nuevo.clase = Clases.PRIMITIVO.value
            nuevo.valorClase = nuevo.clase
            nuevo.valorTipo = nuevo.tipo

        else:
            #Extraer valores
            expresionEvaluar = self.expresion.analisis(SIMBOLOS, REPORTES)
            
            #Verificar que no sea nulo
            if expresionEvaluar.tipo == Tipo.NULL.value:
                REPORTES.salida += "ERROR: No se puede asignar NULL a un primitivo. \n"
                mensaje = "No se puede asignar NULL a un primitivo."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Comprobar que sea primitivo
            if expresionEvaluar.clase != Clases.PRIMITIVO.value:
                REPORTES.salida += "ERROR: Una variable primitiva solo recibe primitivos. \n"
                mensaje = "Una variable primitiva solo recibe primitivos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Comprobar que el tipo sea el mismo que la variable
            if expresionEvaluar.tipo != self.tipo:
                REPORTES.salida += "ERROR: Primitivo " + self.tipo + " no recibe " + expresionEvaluar.tipo + ". \n"
                mensaje = "Primitivo " + self.tipo + " no recibe " + expresionEvaluar.tipo + "."
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

