from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor

class expresionBinaria(instruccion):
    '''
        Almacena el contenido de una operacion con dos valores (suma, mayor que, igual, etc).
        Siempre retorna un primitivo al ejecutarse.
        - Izquierda: Contiene una instruccion que puede ser otra operacion o un valor.
        - Derecha: Contiene una instruccion que puede ser otra operacion o un valor.
        - TipoOperacion: Contiene un string que indica que operacion se va a realizar (suma, resta, potencia, etc)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, IZQUIERDA, DERECHA, TIPO_OPERACION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.izquierda = IZQUIERDA
        self.derecha = DERECHA
        self.tipoOperacion = TIPO_OPERACION
        self.tipoInstruccion = Instrucciones.OPERACION.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Expresion\" ];\n"
        REPORTES.cont += 1

        #Declarar operador izquiedo
        nodoIzquierdo = self.izquierda.grafo(REPORTES)

        #Declarar operador
        nodoOperador = "NODO" + str(REPORTES.cont)
        operador = ""
        if self.tipoOperacion == Expresion.SUMA.value:
            operador = "+"
        elif self.tipoOperacion == Expresion.RESTA.value:
            operador = "-"
        elif self.tipoOperacion == Expresion.MULTIPLICACION.value:
            operador = "*"
        elif self.tipoOperacion == Expresion.DIVISION.value:
            operador = "/"
        elif self.tipoOperacion == Expresion.POT.value:
            operador = "^"
        elif self.tipoOperacion == Expresion.MOD.value:
            operador = "%"
        elif self.tipoOperacion == Expresion.IGUALACION.value:
            operador = "==="
        elif self.tipoOperacion == Expresion.DISTINTO.value:
            operador = "!=="
        elif self.tipoOperacion == Expresion.MAYORQ.value:
            operador = ">"
        elif self.tipoOperacion == Expresion.MENORQ.value:
            operador = "<"
        elif self.tipoOperacion == Expresion.MAYORIG.value:
            operador = ">="
        elif self.tipoOperacion == Expresion.MENORIG.value:
            operador = "<="
        elif self.tipoOperacion == Expresion.OR.value:
            operador = "||"
        elif self.tipoOperacion == Expresion.AND.value:
            operador = "&&"
        REPORTES.dot += nodoOperador + "[ label = \"" +  operador + "\" ];\n"
        REPORTES.cont += 1

        #Declarar operador derecho
        nodoDerecho = self.derecha.grafo(REPORTES)

        #Conectar con el padre
        REPORTES.dot += padre + "->" + nodoIzquierdo + ";\n"
        REPORTES.dot += padre + "->" + nodoOperador + ";\n"
        REPORTES.dot += padre + "->" + nodoDerecho + ";\n"
        return padre

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Obtener el valor de las expresiones
        expresionIzquierda = self.izquierda.analisis(SIMBOLOS, REPORTES)
        expresionDerecha = self.derecha.analisis(SIMBOLOS, REPORTES)

        #Comprobar que no sea NUll
        if expresionIzquierda.tipo == Tipo.NULL.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: El operador izquierdo es de tipo Null. \n"
            mensaje = "El operador izquierdo es de tipo Null."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno

        if expresionDerecha.tipo == Tipo.NULL.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: El operador derecho es de tipo Null. \n"
            mensaje = "El operador derecho es de tipo Null."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno

        #Comprobar que sea primitivo
        if expresionIzquierda.clase != Clases.PRIMITIVO.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: El operador izquierdo no es de tipo Primitivo. \n"
            mensaje = "El operador izquierdo no es de tipo Primitivo."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno
        
        if expresionDerecha.clase != Clases.PRIMITIVO.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: El operador derecho no es de tipo Primitivo. \n"
            mensaje = "El operador derecho no es de tipo Primitivo."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno
        
        #Separacion de instruccion
        #Aritmeticas-------------------------------------------------------------------------------------
        if self.tipoOperacion == Expresion.SUMA.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                numero = float(expresionIzquierda.valor) + float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = expresionIzquierda.tipo
                retorno.valor = str(numero)
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
    
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Concatenar los strings
                cadena = expresionIzquierda.valor + expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = expresionIzquierda.tipo
                retorno.valor = cadena
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
    
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion suma solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion suma solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
        elif self.tipoOperacion == Expresion.RESTA.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                numero = float(expresionIzquierda.valor) - float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = expresionIzquierda.tipo
                retorno.valor = str(numero)
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
    
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion resta solo recibe numbers. \n"
                mensaje = "La operacion resta solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
        elif self.tipoOperacion == Expresion.MULTIPLICACION.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                numero = float(expresionIzquierda.valor) * float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = expresionIzquierda.tipo
                retorno.valor = str(numero)
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
    
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion multiplicación solo recibe numbers. \n"
                mensaje = "La operacion multiplicación solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno

        elif self.tipoOperacion == Expresion.DIVISION.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Validar division entre 0
                if float(expresionDerecha.valor) == 0:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: División entre 0. \n"
                    mensaje = "División entre 0."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    return retorno

                #Convertir el numero
                numero = float(expresionIzquierda.valor) / float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = expresionIzquierda.tipo
                retorno.valor = str(numero)
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
    
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion división solo recibe numbers. \n"
                mensaje = "La operacion división solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
        elif self.tipoOperacion == Expresion.POT.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                numero = float(expresionIzquierda.valor) ** float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = expresionIzquierda.tipo
                retorno.valor = str(numero)
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
    
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion potencia solo recibe numbers. \n"
                mensaje = "La operacion potencia solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
        elif self.tipoOperacion == Expresion.MOD.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Validar division entre 0
                if float(expresionDerecha.valor) == 0:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: Modulo entre 0. \n"
                    mensaje = "Modulo entre 0."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    return retorno

                #Convertir el numero
                numero = float(expresionIzquierda.valor) % float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = expresionIzquierda.tipo
                retorno.valor = str(numero)
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
    
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion modulo solo recibe numbers. \n"
                mensaje = "La operacion modulo solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
        #Relacionales-------------------------------------------------------------------------------------
        elif self.tipoOperacion == Expresion.MAYORQ.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                booleano = float(expresionIzquierda.valor) > float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor > expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion mayor que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion mayor que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno

        elif self.tipoOperacion == Expresion.MENORQ.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                booleano = float(expresionIzquierda.valor) < float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor < expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion menor que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion menor que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
        elif self.tipoOperacion == Expresion.MAYORIG.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                booleano = float(expresionIzquierda.valor) >= float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor >= expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion mayor igual solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion mayor igual solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno

        elif self.tipoOperacion == Expresion.MENORIG.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                booleano = float(expresionIzquierda.valor) <= float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor <= expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion menor igual solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion menor igual que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
        elif self.tipoOperacion == Expresion.IGUALACION.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                booleano = float(expresionIzquierda.valor) == float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor == expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor == expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion igualacion que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion igualacion que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
        elif self.tipoOperacion == Expresion.DISTINTO.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Convertir el numero
                booleano = float(expresionIzquierda.valor) != float(expresionDerecha.valor) 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor != expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            elif expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Evaluar los strings
                booleano = expresionIzquierda.valor == expresionDerecha.valor 
                
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if booleano:
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
            
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion distinto que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion distinto que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
        # Logicas -----------------------------------------------------------------------------------
        elif self.tipoOperacion == Expresion.AND.value:
            #Evaluar el caso en que ambos sean boolean
            if expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if expresionIzquierda.valor == "true" and expresionDerecha.valor == "true":
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
                
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion and que solo recibe booleanos. \n"
                mensaje = "La operacion and que solo recibe booleanos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
        elif self.tipoOperacion == Expresion.OR.value:
            #Evaluar el caso en que ambos sean boolean
            if expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Retorno
                retorno = valor()
                retorno.tipo = Tipo.BOOLEAN.value
                if expresionIzquierda.valor == "true" and expresionDerecha.valor == "true":
                    retorno.valor = "true"
                else:
                    retorno.valor = "false"
                retorno.clase = expresionIzquierda.clase
                retorno.string = retorno.valor
                retorno.valorClase = retorno.clase
                retorno.valorTipo = retorno.tipo
                return retorno
                
            else:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operacion or que solo recibe booleanos. \n"
                mensaje = "La operacion or que solo recibe booleanos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
        
    def c3d(self):
        pass
