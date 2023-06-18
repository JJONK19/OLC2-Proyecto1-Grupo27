from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
 
from Dato.Any import any
from Dato.Vector import vector
from Dato.Primitivo import primitivo
from Dato.Struct import struct


class DeclaracionAtributo(instruccion):
    '''
        Declara un atributo para la definicion del struct.
        - ID: Nombre del atributo
        - Expresion: Valor del atributo
        - TipoInstruccion: Indica que es una instruccion de tipo declaracion primitiva
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    #todo cambiar constructores
    def __init__(self, ID, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.DECLARACION_ATRIBUTO.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Declaracion Atributo\" ];\n"
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

        #Declarar expresion
        nodoExp = self.expresion.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoExp + ";\n"

        return padre
    
    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        #Extraer valores
        expresionContenido = self.expresion.analisis(SIMBOLOS, REPORTES)
        expresionContenido.id = self.id
        
        #Crear el objeto
        #Verificar que no sea nulo
        if expresionContenido.tipo == Tipo.NULL.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: El atributo recibio un valor NULL. \n"
            mensaje = "El atributo recibio un valor NULL."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno
        
        #Crear el objeto y añadir a la lista
        if expresionContenido.clase == Clases.PRIMITIVO.value:
            return primitivo(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.valor)  
        elif expresionContenido.clase == Clases.VECTOR.value:
            return vector(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.claseContenido, expresionContenido.valor)
        elif expresionContenido.clase == Clases.STRUCT.value:
            return struct(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.valor)
        elif expresionContenido.clase == Clases.ANY.value:
            return any(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.valor, expresionContenido.valorTipo, expresionContenido.valorClase, expresionContenido.claseContenido)

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

