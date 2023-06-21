from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from Dato.Struct import struct

class datoStruct(instruccion):
    '''
        Almacena los datos para crear un valor de tipo STRUCT.
        Siempre retorna un vector al ejecutarse.
        - Valor: Contiene una lista de atributos.
        - Tipo: Contiene el tipo del valor (number, string, bool)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, VALOR, TIPO, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.valor = VALOR
        self.tipo = TIPO
        self.clase = Clases.STRUCT.value
        self.tipoInstruccion = Instrucciones.DATO.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Dato Struct\" ];\n"
        REPORTES.cont += 1

        #Nodo complementario :
        nodoLlA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlA + "[ label = \"{\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlA + ";\n"

        #Declarar atributos
        for i in self.valor:
            nodoAtributo = i.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoAtributo + ";\n"

        #Nodo complementario :
        nodoLlC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlC + "[ label = \"}\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlC + ";\n"

        return padre

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        atributos = []
        #Crear la lista de atributos
        for i in self.valor:
            atributos.append(i.analisis(SIMBOLOS, REPORTES))
    
        nuevo = valor()
        nuevo.valor = atributos
        nuevo.clase = Clases.STRUCT.value
        nuevo.valorClase = nuevo.clase

        #Extraer el nombre de la clase
        local = SIMBOLOS[-1]
        salida = local.determinarStruct(nuevo.valor)
        
        if salida == -1:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: La estructura declarada no existe. \n"
            mensaje = "La estructura declarada no existe."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno
        
        #Asignar el tipo
        nuevo.tipo = salida
        nuevo.valorTipo = nuevo.tipo

        #Por si se pide el string
        tempStruct = struct("", salida, Clases.STRUCT.value, atributos)

        #Retorno           
        retorno = valor()
        retorno.id = ""
        retorno.tipo = salida
        retorno.valor = atributos
        retorno.clase = Clases.STRUCT.value
        retorno.string = tempStruct.getString(REPORTES, self.linea, self.columna)
        retorno.claseContenido = ""
        retorno.valorClase = retorno.clase
        retorno.valorTipo = retorno.tipo    
        return retorno     

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

 