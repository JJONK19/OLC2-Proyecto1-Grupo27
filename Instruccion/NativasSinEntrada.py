from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor

class nativaSinValor(instruccion):
    '''
        Funciones nativas que retornan un primitivo. No reciben parametros.
        - Modificar: Contiene una expresion (llamada a variable, un string, etc).
        - Contenido: Contiene una expresion usada en la funcion nativa (una variable, un string, etc)
        - TipoInstruccion: String con el tipo de instruccion(toString, toUpper, etc).
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, MODIFICAR, TIPO_INSTRUCCION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.modificar = MODIFICAR
        self.tipoInstruccion = TIPO_INSTRUCCION

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"" + self.tipoInstruccion + "\" ];\n"
        REPORTES.cont += 1

        #Declarar el valor a operar

        nodoModificar = self.modificar.grafo(REPORTES)

        # Declarar funcion
        nodoFuncion = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncion + "[ label = \"." + self.tipoInstruccion +" ( )\" ];\n"
        REPORTES.cont += 1

        # Conectar con el padre
        REPORTES.dot += padre + "->" + nodoModificar + ";\n"
        REPORTES.dot += padre + "->" + nodoFuncion + ";\n"
        return padre

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        #Extraer valores
        expresionEvaluar = self.modificar.analisis(SIMBOLOS, REPORTES)

        #VErificar que no sea nulo
        if expresionEvaluar.tipo == Tipo.NULL.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: La funcion nativa se esta ejecutando sobre un NULL. \n"
            mensaje = "La funcion nativa se esta ejecutando sobre un NULL."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno
        
        #Comprobar que sea primitivo
        if expresionEvaluar.clase != Clases.PRIMITIVO.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre tipos Primitivos. \n"
            mensaje = "La funcion " + self.tipoInstruccion + " solo opera sobre tipos Primitivos."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno
        
        #Clasificar por tipo de operacion y ejecutar
        if self.tipoInstruccion == Expresion.TOSTRING.value:
            #Los valores vienen en string. Solo se cambia el tipo. 
            retorno = valor()
            retorno.id = expresionEvaluar.id
            retorno.tipo = Tipo.STRING.value
            retorno.valor = expresionEvaluar.valor
            retorno.clase = expresionEvaluar.clase
            retorno.string = expresionEvaluar.valor
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno

        elif self.tipoInstruccion == Expresion.TOLOWERCASE.value:
            #Verificar que reciba un string en la entrada y el parametro
            if expresionEvaluar.tipo != Tipo.STRING.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo maneja strings."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno

            #Ejecutar la funcion. El numero de decimales es contenido y el valor que se trabaja es modificar
            cadena = expresionEvaluar.valor
            lower = cadena.lower()

            retorno = valor()
            retorno.id = expresionEvaluar.id
            retorno.tipo = Tipo.STRING.value
            retorno.valor = lower
            retorno.clase = expresionEvaluar.clase
            retorno.string = lower
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno
        
        elif self.tipoInstruccion == Expresion.TOUPPERCASE.value:
            #Verificar que reciba un number en la entrada y el parametro
            if expresionEvaluar.tipo != Tipo.STRING.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo maneja strings."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno

            #Ejecutar la funcion. El numero de decimales es contenido y el valor que se trabaja es modificar
            cadena = expresionEvaluar.valor
            upper = cadena.upper()

            retorno = valor()
            retorno.id = expresionEvaluar.id
            retorno.tipo = Tipo.STRING.value
            retorno.valor = upper
            retorno.clase = expresionEvaluar.clase
            retorno.string = upper
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno
        
    def c3d(self):
        pass