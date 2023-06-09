from Dato.Simbolo import simbolo
from Ejecucion.Valor import valor
from Tipos.Tipos import *
from Reporte.Reporte import *

class struct(simbolo):
    '''
        Coleccion de variables. Almacena una lista con instancias de la clase atributo.
        - ID: Nombre de la variable (String)
        - Tipo: Tipado de la variable (string, int, bool, etc) (String).
        - Clase: Struct (String).
        - Valor: Contenido de la variable ((Primitivo, Vector o Struct)[])
    '''
    def __init__(self, ID, TIPO, CLASE, VALOR):
        super().__init__(ID, TIPO, CLASE) 
        self.valor = VALOR
    
    def set(self, NUEVO):
        '''
            Asigna un nuevo conjunto de atributos a la variable.
            - Nuevo: Es un vector con los contenidos de la variable
        '''
        self.valor = NUEVO

    def get(self, ATRIBUTO, REPORTES, LINEA, COLUMNA):
        '''
            Retorna un objeto de tipo Valor, con el valor del atributos. Retorna NULL si no existe.
            - Atributo: Nombre del atributo al que se quiere acceder.
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
            - Linea: Linea donde se encuentra la instruccion.
            - Columna: Posicion en la linea donde se encuentra la instruccion.
        '''
        retorno = valor()

        #Si no hay atributo se devuelve una copia del struct
        if ATRIBUTO == "" :
            retorno.id = self.id
            retorno.tipo = self.tipo
            retorno.valor = self.valor
            retorno.clase = Clases.STRUCT.value
            retorno.string = self.getString(REPORTES, LINEA, COLUMNA)
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo
            return retorno
        
        #Buscar el atributo
        posicion = -1
        for i in range(len(self.valor)):
            atributo_temp = self.valor[i]

            if ATRIBUTO == atributo_temp.nombre:
                posicion == i
                break

        if posicion == -1:
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: El atributo " + ATRIBUTO + " no existe. \n"
            mensaje = "El atributo " + ATRIBUTO + " no existe. \n"
            REPORTES.añadirError("Semantico", mensaje, LINEA, COLUMNA)
            return retorno
        

        #Retornar el valor. 
        return self.valor[posicion]
    
    def getString(self, REPORTES, LINEA, COLUMNA):
        '''
            Retorna la variable como un string.
        '''
        cadena = "[ "
        for i in range(len(self.valor)):
            temp = self.valor[i]
            valor = ""
            cadena += "{ "
            
            if temp.clase == Clases.PRIMITIVO.value:
                valor = temp.get()
            elif temp.clase == Clases.VECTOR.value:
                valor = temp.get("", REPORTES, LINEA, COLUMNA)
            elif temp.clase == Clases.STRUCT.value:
                valor = temp.get("", REPORTES, LINEA, COLUMNA)

            cadena += valor.id + " : " + valor.string

            if i != len(self.valor) - 1:
                cadena += " }, "
            else:
                cadena += " ]"

            return cadena