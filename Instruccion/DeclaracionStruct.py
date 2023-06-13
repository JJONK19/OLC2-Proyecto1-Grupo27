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

    def __init__(self, ID, TIPO, LISTA_VALORES, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.tipo = TIPO
        self.listaValores = LISTA_VALORES
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

        #Nodo complementario :
        nodoLlA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlA + "[ label = \"{\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlA + ";\n"

        #Declarar atributos
        for i in self.listaValores:
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
        for i in self.listaValores:
            atributos.append(i.analisis(SIMBOLOS, REPORTES))

        nuevo = valor()
        nuevo.tipo = self.tipo
        nuevo.valor = atributos
        nuevo.clase = Clases.STRUCT.value
        nuevo.valorClase = nuevo.clase
        nuevo.valorTipo = nuevo.tipo

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

