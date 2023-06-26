from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
 
from Dato.Any import any
from Dato.Vector import vector
from Dato.Primitivo import primitivo
from Dato.Struct import struct

class datoVector(instruccion):
    '''
        Almacena los datos para crear un valor de tipo vector (string, bool, number).
        Siempre retorna un vector al ejecutarse.
        - Valor: Contiene una lista de expresiones.
        - Tipo: Contiene el tipo del valor (number, string, bool)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, VALOR, TIPO, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.valor = VALOR
        self.tipo = TIPO
        self.clase = Clases.VECTOR.value
        self.tipoInstruccion = Instrucciones.DATO.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[color = \"brown\", style =\"radial\", fillcolor = \"gold:brown\", gradientangle = \"315\", label = \"ValorVector\" ];\n"
        REPORTES.cont += 1

        #Declarar funcion
        nodoFuncionA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncionA + "[ label = \"[\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFuncionA + ";\n"

        #Declarar operaciones
        for i in self.valor:
            nodoExpresion = i.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoExpresion + ";\n"

        #Declarar cierre de funcion
        nodoFuncionC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncionC + "[ label = \")\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFuncionC + ";\n"
        return padre    

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Contenido es un vector de instrucciones con las declaraciones de vectores
        contenido = []

        for i in self.valor:
            #Extraer valor
            expresionContenido = i.analisis(SIMBOLOS, REPORTES)

            #Verificar que no sea nulo
            if expresionContenido.tipo == Tipo.NULL.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: El vector recibio un valor NULL. \n"
                mensaje = "El vector recibio un valor NULL."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            #Crear el objeto y añadir a la lista
            if expresionContenido.clase == Clases.PRIMITIVO.value:
                contenido.append(primitivo(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.valor))    
            elif expresionContenido.clase == Clases.VECTOR.value:
                contenido.append(vector(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.claseContenido, expresionContenido.valor))
            elif expresionContenido.clase == Clases.STRUCT.value:
                contenido.append(struct(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.valor))
            elif expresionContenido.clase == Clases.ANY.value:
                contenido.append(any(expresionContenido.id, expresionContenido.tipo, expresionContenido.clase, expresionContenido.valor, expresionContenido.valorTipo, expresionContenido.valorClase, expresionContenido.claseContenido)) 
        
        
        #Por si se pide el string
        tempVector = vector("", Tipo.ANY.value, Clases.VECTOR.value, Clases.ANY, contenido)

        #Retorno           
        retorno = valor()
        retorno.id = ""
        retorno.tipo = self.tipo
        retorno.valor = contenido
        retorno.clase = self.clase
        retorno.string = tempVector.getString(REPORTES, self.linea, self.columna)
        retorno.claseContenido = Clases.ANY.value
        retorno.valorClase = retorno.clase
        retorno.valorTipo = retorno.tipo    
        return retorno     
        
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass
