from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from Dato.Any import any

class DeclaracionVector(instruccion):
    '''
        Declara un primitivo.
        - ID: Nombre de la variable
        - Tipo: Tipo del vector
        - Expresion: Contiene el vector
        - TipoInstruccion: Indica que es una instruccion de tipo declaracion vector
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, ID, TIPO, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.tipo = TIPO
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.DECLARACION_VECTOR.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Declaracion Vector\" ];\n"
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

        #Nodo complementario :
        nodoCorA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoCorA + "[ label = \"[ ]\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoCorA + ";\n"

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
            nuevo.valor = []
            nuevo.clase = Clases.VECTOR.value
            nuevo.valorClase = nuevo.clase
            nuevo.valorTipo = nuevo.tipo
            if self.tipo != Tipo.ANY.value:
                nuevo.claseContenido = Clases.PRIMITIVO.value
            else: 
                nuevo.claseContenido = Clases.ANY.value

        else:
            #Extraer valores
            expresionEvaluar = self.expresion.analisis(SIMBOLOS, REPORTES)
            
            #Verificar que no sea nulo
            if expresionEvaluar.tipo == Tipo.NULL.value:
                REPORTES.salida += "ERROR: No se puede asignar NULL a un vector. \n"
                mensaje = "No se puede asignar NULL a un vector."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Comprobar que sea vector
            if expresionEvaluar.clase != Clases.VECTOR.value:
                REPORTES.salida += "ERROR: Una variable vector solo recibe vectores. \n"
                mensaje = "Una variable vector solo recibe vectores."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Si tipo no es ANY, comparar contenido con el tipo del vector
            if self.tipo != Tipo.ANY.value:
                for i in expresionEvaluar.valor:
                    if i.tipo != self.tipo:
                        REPORTES.salida += "ERROR: Uno o mas valores del vector no cumple con el tipo. \n"
                        mensaje = "Uno o mas valores del vector no cumple con el tipo."
                        REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                        return -1
            
            #Asignar el tipo
            expresionEvaluar.tipo = self.tipo
            
            #Asignar la clase del contenido
            if self.tipo != Tipo.ANY.value:
                if self.tipo == Tipo.STRING.value or self.tipo == Tipo.NUMBER.value or self.tipo == Tipo.BOOLEAN.value:
                    expresionEvaluar.claseContenido = Clases.PRIMITIVO.value
                else:
                    expresionEvaluar.claseContenido = Clases.STRUCT.value
            else: 
                expresionEvaluar.claseContenido = Clases.ANY.value

            #Convertir todos los objetos a Anys en caso sea de tipo any
            anyLista = []
            if self.tipo == Tipo.ANY.value:
                for i in expresionEvaluar.valor:

                    if i.clase == Clases.PRIMITIVO.value:
                        anyLista.append(any(i.id, Tipo.ANY.value, Clases.ANY.value, i.valor, i.tipo, i.clase, ""))    
                    elif i.clase == Clases.VECTOR.value:
                        anyLista.append(any(i.id, Tipo.ANY.value, Clases.ANY.value, i.valor, i.tipo, i.clase, i.claseContenido))
                    elif i.clase == Clases.STRUCT.value:
                        anyLista.append(any(i.id, Tipo.ANY.value, Clases.ANY.value, i.valor, i.tipo, i.clase, "")) 
                
                expresionEvaluar.valor = anyLista
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

    def c3d(self):
        pass

