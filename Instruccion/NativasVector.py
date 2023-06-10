from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from Dato.Vector import vector
from Dato.Primitivo import primitivo

class nativasVector(instruccion):
    '''
        Funciones nativas que retornan un vector. Reciben un parametro.
        - Modificar: Contiene una expresion (llamada a variable, un string, etc).
        - Contenido: Contiene una expresion usada en la funcion nativa. Puede ser una expresion o un vector.
        - TipoInstruccion: String con el tipo de instruccion(toString, toUpper, etc).
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, MODIFICAR, CONTENIDO, TIPO_INSTRUCCION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.modificar = MODIFICAR
        self.contenido = CONTENIDO
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
        REPORTES.dot += padre + "->" + nodoModificar + ";\n"

        # Declarar funcion
        nodoFuncion = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncion + "[ label = \"." + self.tipoInstruccion +" (\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFuncion + ";\n"

        # Declarar operacion
        if self.tipoInstruccion == Expresion.SPLIT.value:
            nodoContenido = self.contenido.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoContenido + ";\n"
        elif self.tipoInstruccion == Expresion.CONCAT.value:
            for i in self.contenido:
                nodoContenido = i.grafo(REPORTES)
                REPORTES.dot += padre + "->" + nodoContenido + ";\n"

        # Declarar cierre de funcion
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
        
        #Clasificar por tipo de operacion y ejecutar
        if self.tipoInstruccion == Expresion.SPLIT.value:
            #Extraer valor
            expresionContenido = self.contenido.analisis(SIMBOLOS, REPORTES)

            #Verificar que no sea nulo
            if expresionContenido.tipo == Tipo.NULL.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La funcion nativa recibio un parametro NULL. \n"
                mensaje = "La funcion nativa recibio un parametro NULL."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
            #Comprobar que sean primitivos ambos
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
            
            if expresionContenido.clase != Clases.PRIMITIVO.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo recibe tipos Primitivos. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo recibe sobre tipos Primitivos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            #Verificar que reciba un string en la entrada y el parametro
            if expresionEvaluar.tipo != Tipo.STRING.value or expresionContenido.tipo != Tipo.STRING.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja numbers. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo maneja numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            #Ejecutar la funcion
            cadena = expresionEvaluar.valor
            separador = expresionContenido.valor
            split = cadena.split(separador)

            #Convertir la salida en un vector
            temp = []
            for i in split:
                temp.append(primitivo("", Tipo.STRING.value, Clases.PRIMITIVO.value, i))

            tempVector = vector("", Tipo.STRING.value, Clases.VECTOR.value, Clases.PRIMITIVO, temp)

            #Retorno
            retorno = valor()
            retorno.id = ""
            retorno.tipo = Tipo.STRING.value
            retorno.valor = temp
            retorno.clase = Clases.VECTOR.value
            retorno.string = tempVector.getString(REPORTES, self.linea, self.columna)
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno
        
        elif self.tipoInstruccion == Expresion.CONCAT.value:
            #Contenido es un vector de instrucciones con las declaraciones de vectores
            contenido = []

            for i in self.contenido:
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
                    
                    REPORTES.salida += "ERROR: La funcion nativa recibio un parametro NULL. \n"
                    mensaje = "La funcion nativa recibio un parametro NULL."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    return retorno
            
                #Comprobar que sea un vector
                if expresionContenido.clase != Clases.VECTOR.value:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo recibe tipos Vectores. \n"
                    mensaje = "La funcion " + self.tipoInstruccion + " solo recibe sobre tipos Vectores."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    return retorno
                
                #Añadir a la lista
                contenido.append(expresionContenido.valor)
            
            #Comprobar que sea vector el valor a evaluar 
            if expresionEvaluar.clase != Clases.VECTOR.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre Vectores. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo opera sobre Vectores."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            #Ejecutar la funcion
            concatenar = expresionEvaluar.valor.copy()

            for i in contenido:
                concatenar += i

            tempVector = vector("", Tipo.ANY.value, Clases.VECTOR.value, Clases.ANY, concatenar)

            #Retorno           
            retorno = valor()
            retorno.id = ""
            retorno.tipo = Tipo.ANY.value
            retorno.valor = concatenar
            retorno.clase = Clases.VECTOR.value
            retorno.string = tempVector.getString(REPORTES, self.linea, self.columna)
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno     
        
    def c3d(self):
        pass