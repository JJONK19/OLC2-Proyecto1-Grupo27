from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor

from Dato.Any import any
from C3D.Valor3D import valor3D

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
        REPORTES.dot += padre + "[color = \"brown\", style =\"radial\", fillcolor = \"gold:brown\", gradientangle = \"315\", label = \"Declaracion Any\" ];\n"
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

            #Si es vector convertir a any sus contenidos
            if expresionEvaluar.clase == Clases.VECTOR.value:
                expresionEvaluar.valor = DeclaracionAny.convertirAny(expresionEvaluar.valor)

            #Asignar tipos
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
    
    @staticmethod
    def convertirAny(VECTOR):
        salida = []
        for i in range(len(VECTOR)):
            temp = VECTOR[i]

            if temp.clase == Clases.PRIMITIVO.value:
                salida.append(any(temp.id, Tipo.ANY.value, Clases.ANY.value, temp.valor, temp.tipo, temp.clase, ""))    
            elif temp.clase == Clases.VECTOR.value:
                nuevo = DeclaracionAny.convertirAny(temp.valor)
                salida.append(any(temp.id, Tipo.ANY.value, Clases.ANY.value, nuevo, temp.tipo, temp.clase, temp.claseContenido))
            elif temp.clase == Clases.STRUCT.value:
                salida.append(any(temp.id, Tipo.ANY.value, Clases.ANY.value, temp.valor, temp.tipo, temp.clase, "")) 
            elif temp.clase == Clases.ANY.value:
                salida.append(temp)
        return salida
    
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        CODIGO.insertar_Comentario("////////// INICIA DECLARACION ANY //////////")
        #TRABAJAR CON LA EXPRESION Y CREAR EL VALOR
        nuevo = ""
       
        if self.expresion == None:
            #Se define un string como valor por defecto
            temporal = CODIGO.nuevoTemporal()
            heap  = True
            CODIGO.insertar_Asignacion(temporal, "H")
            CODIGO.insertar_SetearHeap('H', ord(""))   
            CODIGO.insertar_MoverHeap()
            CODIGO.insertar_SetearHeap('H', '-1')            
            CODIGO.insertar_MoverHeap()  

            nuevo =  valor3D(temporal, True, self.tipo, self.clase, TIPO_VALOR=Tipo.STRING.value,
                             CLASE_VALOR=Clases.PRIMITIVO.value, HEAP=heap)

        else:
            #Extraer valores
            expresionEvaluar = self.expresion.c3d(SIMBOLOS, REPORTES, CODIGO) 
            expresionEvaluar.tipoValor = expresionEvaluar.tipo
            expresionEvaluar.claseValor = expresionEvaluar.clase 
            expresionEvaluar.tipo = Tipo.ANY.value
            expresionEvaluar.clase = Clases.ANY.value
            nuevo = expresionEvaluar

        #Añadir el id de la variable a valor
        nuevo.id = self.id
        nuevo.linea = self.linea
        nuevo.columna = self.columna

        #Enviar al entorno local
        local = SIMBOLOS[-1]
        salida = local.insertarSimbolo(nuevo, REPORTES, CODIGO)
        
        if salida == -1:
            return 
        
        #Añadir al stack el valor
        tempStack = CODIGO.nuevoTemporal()
        CODIGO.insertar_Expresion(tempStack, "P", "+", salida.posicionStack)
        CODIGO.insertar_SetearStack(tempStack, nuevo.valor)

