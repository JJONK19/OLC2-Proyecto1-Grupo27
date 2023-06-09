from Simbolo import simbolo
from Ejecucion.Valor import valor
from Tipos.Tipos import *
from Reporte.Reporte import *

class vector(simbolo):
    '''
        Se usa para representar colecciones de datos (int, string, bool, vectores, etc). 
        - ID: Nombre de la variable (String)
        - Tipo: Tipado de la variable (string, int, bool, etc) (String).
        - Clase: Vector (String).
        - ClaseContenido: Indica si el contenido es de primitivos, structs, any, etc. 
        - Valor: Contenido de la variable (simbolo[])
    '''
    def __init__(self, ID, TIPO, CLASE, CLASE_CONTENIDO, VALOR):
        super().__init__(ID, TIPO, CLASE) 
        self.valor = VALOR
        self.claseContenido = CLASE_CONTENIDO
    
    def set(self, NUEVO):
        '''
            Asigna un nuevo vector a la variable.
            - Nuevo: Es un vector con los contenidos de la variable
        '''
        self.valor = NUEVO

    def get(self, POSICION, REPORTES, LINEA, COLUMNA):
        '''
            Retorna un objeto de tipo Simbolo, con el valor de en una posicion dada como string. Retorna NULL si la posicion es erronea.
            - Posicion: Posicion del vector a la que se quiere acceder.
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
            - Linea / Columna: Posiciones donde se esta ejecutando. Se usa en los errores.
        '''
        retorno = valor()
        #SI POSICION ES IGUAL A "", RETORNA EL MISMO VECTOR 
        if POSICION == "":
            retorno.id = self.id
            retorno.tipo = self.tipo
            retorno.valor = self.valor
            retorno.clase = self.clase
            retorno.claseContenido = self.claseContenido
            retorno.string = self.getString(REPORTES, LINEA, COLUMNA)
            return retorno

        #Verificar que la posicion respete los limites
        if (POSICION > len(self.valor) - 1) or POSICION < 0 :
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"

            #ERRORES
            REPORTES.salida += "ERROR: Indice fuera del rango del vector. \n"
            REPORTES.añadirError("Semantico", "Indice fuera del rango del vector", LINEA, COLUMNA)
            return retorno

        #Retornar la informacion
        return self.valor[POSICION]
    
    def getString(self, REPORTES, LINEA, COLUMNA):
        '''
            Retorna la variable como un string.
        '''
        cadena = "[ "
        for i in range(len(self.valor)):
            temp = self.valor[i]
            valor = ""
            
            if temp.clase == Clases.PRIMITIVO.value:
                valor = temp.get()
            elif temp.clase == Clases.VECTOR.value:
                valor = temp.get("", REPORTES, LINEA, COLUMNA)
            elif temp.clase == Clases.STRUCT.value:
                valor = temp.get("", REPORTES, LINEA, COLUMNA)

            cadena += valor.string

            if i != len(self.valor) - 1:
                cadena += ", "
            else:
                cadena += " ]"

            return cadena



