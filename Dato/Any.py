from Dato.Simbolo import simbolo
from Ejecucion.Valor import valor
from Tipos.Tipos import *

class any(simbolo):
    '''
        Contiene primitivos, arrays o structs y pueden intercarmbiarse estas clases.
        - ID: Nombre de la variable (String)
        - Tipo: Tipado de la variable (string, int, bool, etc) (String).
        - Clase: Primitivo (String).
        - Valor: Contenido de la variable 
        - TipoValor: Al ser una clase any, se necesita saber el tipo de su contenido
        - ClaseValor: Al ser una clase any, se necesita saber la clase de su contenido
    '''
    def __init__(self, ID, TIPO, CLASE, VALOR, TIPO_VALOR, CLASE_VALOR, CLASE_CONTENIDO):
        super().__init__(ID, TIPO, CLASE) 
        self.valor = VALOR
        self.tipoValor = TIPO_VALOR
        self.claseValor = CLASE_VALOR
        self.claseContenido = CLASE_CONTENIDO
    
    def set(self, NUEVO, TIPO_VALOR, CLASE_VALOR, CLASE_CONTENIDO):
        '''
            Asigna un nuevo valor a la variable.
            - Nuevo: Es el contenido de la variable
        '''
        self.valor = NUEVO
        self.tipoValor = TIPO_VALOR
        self.claseValor = CLASE_VALOR
        self.claseContenido = CLASE_CONTENIDO
        
    def get(self, POSICION, ATRIBUTO, REPORTES, LINEA, COLUMNA):
        '''
            Retorna un objeto de tipo Valor, con el valor de la variable como string.
        '''
        if self.claseValor == Clases.PRIMITIVO.value:
            retorno = valor()
            retorno.id = self.id
            retorno.tipo = self.tipoValor
            retorno.valor = self.valor
            retorno.clase = self.claseValor
            retorno.string = self.valor
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo
            return retorno
            
        elif self.claseValor == Clases.VECTOR.value:
            retorno = valor()
            #SI POSICION ES IGUAL A "", RETORNA EL MISMO VECTOR 
            if POSICION == "":
                retorno.id = self.id
                retorno.tipo = self.tipoValor
                retorno.valor = self.valor
                retorno.clase = self.claseValor
                retorno.claseContenido = self.claseContenido
                retorno.string = self.getString(REPORTES, LINEA, COLUMNA)
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
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
        
        elif self.claseValor == Clases.STRUCT.value:
            #Si no hay atributo se devuelve una copia del struct
            if ATRIBUTO == "" :
                retorno = valor()
                retorno.id = self.id
                retorno.tipo = self.tipoValor
                retorno.valor = self.valor
                retorno.clase = self.claseValor
                retorno.string = self.getString(REPORTES, LINEA, COLUMNA)
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            #Buscar el atributo
            posicion = -1
            for i in range(len(self.valor)):
                atributo_temp = self.valor[i]

                if ATRIBUTO == atributo_temp.id:
                    posicion == i
                    break

            if posicion == -1:
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: El atributo " + ATRIBUTO + " no existe. \n"
                mensaje = "El atributo " + ATRIBUTO + " no existe."
                REPORTES.añadirError("Semantico", mensaje, LINEA, COLUMNA)
                return retorno
            

            #Retornar el valor. 
            return self.valor[posicion]
    
    def getString(self, REPORTES, LINEA, COLUMNA):
        '''
            Retorna la variable vector como un string.
        '''
        if self.claseValor == Clases.VECTOR.value:
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
                elif temp.clase == Clases.ANY.value:
                    valor = temp.get("", "", REPORTES, LINEA, COLUMNA)

                cadena += valor.string

                if i != len(self.valor) - 1:
                    cadena += ", "
                else:
                    cadena += " ]"
            return cadena
        
        elif self.claseValor == Clases.STRUCT.value:
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
