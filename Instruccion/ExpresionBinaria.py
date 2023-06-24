import math

from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from C3D.Valor3D import valor3D

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
                #numero = float(expresionIzquierda.valor) % float(expresionDerecha.valor)
                numero = math.fmod(float(expresionIzquierda.valor), float(expresionDerecha.valor))

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
                if expresionIzquierda.valor == "true" or expresionDerecha.valor == "true":
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
        
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        #Obtener el valor de las expresiones
        expresionIzquierda = self.izquierda.c3d(SIMBOLOS, REPORTES, CODIGO)
        expresionDerecha = self.derecha.c3d(SIMBOLOS, REPORTES, CODIGO)

        #Comprobar que sea primitivo
        if expresionIzquierda.clase != Clases.PRIMITIVO.value:
            CODIGO.insertar_Comentario("ERROR: El operador izquierdo no es de tipo Primitivo")
            REPORTES.salida += "ERROR: El operador izquierdo no es de tipo Primitivo. \n"
            mensaje = "El operador izquierdo no es de tipo Primitivo."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        
        if expresionDerecha.clase != Clases.PRIMITIVO.value:
            CODIGO.insertar_Comentario("ERROR: El operador derecho no es de tipo Primitivo.")
            REPORTES.salida += "ERROR: El operador derecho no es de tipo Primitivo. \n"
            mensaje = "El operador derecho no es de tipo Primitivo."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        #Separacion de instruccion
        #Aritmeticas-------------------------------------------------------------------------------------
        if self.tipoOperacion == Expresion.SUMA.value:
            #Evaluar el caso en que ambos sean number
            CODIGO.insertar_Comentario("////////// INICIA SUMA //////////")
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal y añadirle la suma de los temporales
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Expresion(tempResultado, expresionIzquierda.valor, "+", expresionDerecha.valor)

                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
    
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Crear el temporal y guardar la posicion del heap
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "H")

                #Ciclo de variable izquierda. Almacen guarda el ascii del caracter.
                #Concatena las variables en una nueva posicion del heap.
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                tempAlmacen = CODIGO.nuevoTemporal()

                CODIGO.insertar_Label(labelCiclo)
                CODIGO.insertar_ObtenerHeap(tempAlmacen, expresionIzquierda.valor)
                CODIGO.insertar_If(tempAlmacen, "==", "-1", labelSalida)
                CODIGO.insertar_SetearHeap('H', tempAlmacen)   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_Expresion(expresionIzquierda.valor, expresionIzquierda.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)
                CODIGO.insertar_Label(labelSalida)

                #Ciclo de variable derecha. Almacen guarda el ascii del caracter.
                #Concatena las variables en una nueva posicion del heap.
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                tempAlmacen = CODIGO.nuevoTemporal()

                CODIGO.insertar_Label(labelCiclo)
                CODIGO.insertar_ObtenerHeap(tempAlmacen, expresionDerecha.valor)
                CODIGO.insertar_If(tempAlmacen, "==", "-1", labelSalida)
                CODIGO.insertar_SetearHeap('H', tempAlmacen)   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)
                CODIGO.insertar_Label(labelSalida)

                #Guardar el fin de la cadena y mover el heap a una posicion vacia
                CODIGO.insertar_SetearHeap('H', '-1')            
                CODIGO.insertar_MoverHeap()

                return valor3D(tempResultado, True, Tipo.STRING.value, Clases.PRIMITIVO.value)
                
            else:
                CODIGO.insertar_Comentario("ERROR: La operacion suma solo recibe strings o numbers (un solo tipo a la vez). ")
                REPORTES.salida += "ERROR: La operacion suma solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion suma solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                
                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.RESTA.value:
            CODIGO.insertar_Comentario("////////// INICIA RESTA //////////")
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal y añadirle la resta de los temporales
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Expresion(tempResultado, expresionIzquierda.valor, "-", expresionDerecha.valor)

                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
    
            else:
                CODIGO.insertar_Comentario("ERROR: La operacion resta solo recibe numbers.")
                REPORTES.salida += "ERROR: La operacion resta solo recibe numbers. \n"
                mensaje = "La operacion resta solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.MULTIPLICACION.value:
            CODIGO.insertar_Comentario("////////// INICIA MULTIPLICACION //////////")
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal y añadirle la multiplicacion de los temporales
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Expresion(tempResultado, expresionIzquierda.valor, "*", expresionDerecha.valor)

                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
    
            else:
                CODIGO.insertar_Comentario("ERROR: La operacion multiplicación solo recibe numbers.")
                REPORTES.salida += "ERROR: La operacion multiplicación solo recibe numbers. \n"
                mensaje = "La operacion multiplicación solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                
                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.DIVISION.value:
            CODIGO.insertar_Comentario("////////// INICIA DIVISION //////////")
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal y añadirle la division de los temporales
                tempResultado = CODIGO.nuevoTemporal()

                #Validar division entre 0
                #---Crear label de error y de salida
                labelSalida = CODIGO.nuevoLabel()
                labelError = CODIGO.nuevoLabel()

                CODIGO.insertar_If(expresionDerecha.valor , "!=", "0", labelSalida)
                CODIGO.insertar_MathError()
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelError)
                
                #--Ejecutar division
                CODIGO.insertar_Label(labelSalida)
                CODIGO.insertar_Expresion(tempResultado, expresionIzquierda.valor, "/", expresionDerecha.valor)

                #--Label del error
                CODIGO.insertar_Label(labelError)
                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

            else:
                CODIGO.insertar_Comentario("ERROR: La operacion división solo recibe numbers.")
                REPORTES.salida += "ERROR: La operacion división solo recibe numbers. \n"
                mensaje = "La operacion división solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                
                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.POT.value:
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                CODIGO.insertar_Comentario("////////// INICIA POTENCIA //////////")

                #Crear el temporal y añadirle como valor 0. Resulatdo almacena el resultado en la iteracion.
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #Ciclo para el for. Se multiplica el valor izquierdo el numero de veces del derecho.
                #---Crear label de error y de salida
                labelCicloMayor = CODIGO.nuevoLabel()
                labelCicloMenor = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #--Comprobar si es mayor o menor o cero
                CODIGO.insertar_If(expresionDerecha.valor, "==", "0", labelSalida)
                CODIGO.insertar_If(expresionDerecha.valor, ">", "0", labelCicloMayor)
                CODIGO.insertar_If(expresionDerecha.valor, "<", "0", labelCicloMenor)

                #--Iniciar Ciclo Mayor. Se da con exponente positivo.
                CODIGO.insertar_Label(labelCicloMayor)
                CODIGO.insertar_If(expresionDerecha.valor, "==", "0", labelSalida)
                CODIGO.insertar_Expresion(tempResultado, tempResultado, "*", expresionIzquierda.valor)
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "-", "1")
                CODIGO.insertar_Goto(labelCicloMayor)

                #--Iniciar Ciclo Menor. Se da con exponente negativo.
                CODIGO.insertar_Label(labelCicloMenor)
                CODIGO.insertar_If(expresionDerecha.valor, "==", "0", labelSalida)
                CODIGO.insertar_Expresion(tempResultado, tempResultado, "/", expresionIzquierda.valor)
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCicloMenor)

                #--Salida de la operacion
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
    
            else:
                CODIGO.insertar_Comentario("ERROR: La operacion potencia solo recibe numbers.")
                REPORTES.salida += "ERROR: La operacion potencia solo recibe numbers. \n"
                mensaje = "La operacion potencia solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                
                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.MOD.value:
            CODIGO.insertar_Comentario("////////// INICIA MODULO //////////")
            #Evaluar el caso en que ambos sean number
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal y añadirle la division de los temporales
                tempResultado = CODIGO.nuevoTemporal()

                #Validar division entre 0
                #---Crear label de error y de salida
                labelSalida = CODIGO.nuevoLabel()
                labelError = CODIGO.nuevoLabel()



                CODIGO.insertar_If(expresionDerecha.valor , "!=", "0", labelSalida)
                CODIGO.insertar_MathError()
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelError)
                
                #--Ejecutar MODULO. Se calcula a pasito restando al dividendo el cociente por el divisor
                CODIGO.insertar_Label(labelSalida)
                CODIGO.insertar_Mod(tempResultado, expresionIzquierda.valor, expresionDerecha.valor)

                #--Label del error
                CODIGO.insertar_Label(labelError)
                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

            else:
                CODIGO.insertar_Comentario("ERROR: La operacion modulo solo recibe numbers.")
                REPORTES.salida += "ERROR: La operacion modulo solo recibe numbers. \n"
                mensaje = "La operacion división solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                
                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
        #Relacionales-------------------------------------------------------------------------------------
        elif self.tipoOperacion == Expresion.MAYORQ.value:
            #Evaluar el caso en que ambos sean number
            CODIGO.insertar_Comentario("////////// INICIA MAYOR QUE //////////")
   
            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, ">", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)

            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                
                #Declarar label
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                labelIzquierdaNulo = CODIGO.nuevoLabel()
                labelDerechaNulo = CODIGO.nuevoLabel()
                labelMayor = CODIGO.nuevoLabel()
                labelMenor = CODIGO.nuevoLabel()
                tempIzquierda = CODIGO.nuevoTemporal()
                tempDerecha = CODIGO.nuevoTemporal()

                #Ciclo de comparacion
                CODIGO.insertar_Label(labelCiclo)
                  #--- Leer el caracter del heap
                CODIGO.insertar_ObtenerHeap(tempIzquierda, expresionIzquierda.valor)
                CODIGO.insertar_ObtenerHeap(tempDerecha, expresionDerecha.valor)
                  #-- Si viene -1 o es menor se sale
                CODIGO.insertar_If(tempIzquierda, "==", "-1", labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelDerechaNulo)
                CODIGO.insertar_If(tempIzquierda, "<", tempDerecha, labelMenor)
                CODIGO.insertar_If(tempIzquierda, ">", tempDerecha, labelMayor)
                  #--Se itera hasta que encuentre de los casos anteriores
                CODIGO.insertar_Expresion(expresionIzquierda.valor, expresionIzquierda.valor, "+", "1")
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                #Label Mayor
                CODIGO.insertar_Label(labelMayor)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)

                #Label Menor
                CODIGO.insertar_Label(labelMenor)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)
                
                #Label Izquierdo Nulo
                CODIGO.insertar_Label(labelIzquierdaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)

                #Label Derecho Nulo
                CODIGO.insertar_Label(labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)
                
                #--Salida de la operacion
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
            
            else:
                CODIGO.insertar_Comentario("ERROR: La operacion mayor que solo recibe strings o numbers (un solo tipo a la vez).")
                REPORTES.salida += "ERROR: La operacion mayor que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion mayor que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                
                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.MENORQ.value:
            #Evaluar el caso en que ambos sean number
            CODIGO.insertar_Comentario("////////// INICIA MENOR QUE //////////")

            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "<", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)

            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                
                #Declarar label
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                labelIzquierdaNulo = CODIGO.nuevoLabel()
                labelDerechaNulo = CODIGO.nuevoLabel()
                labelMayor = CODIGO.nuevoLabel()
                labelMenor = CODIGO.nuevoLabel()
                tempIzquierda = CODIGO.nuevoTemporal()
                tempDerecha = CODIGO.nuevoTemporal()

                #Ciclo de comparacion
                CODIGO.insertar_Label(labelCiclo)
                  #--- Leer el caracter del heap
                CODIGO.insertar_ObtenerHeap(tempIzquierda, expresionIzquierda.valor)
                CODIGO.insertar_ObtenerHeap(tempDerecha, expresionDerecha.valor)
                  #-- Si viene -1 o es menor se sale
                CODIGO.insertar_If(tempIzquierda, "==", "-1", labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelDerechaNulo)
                CODIGO.insertar_If(tempIzquierda, ">", tempDerecha, labelMayor)
                CODIGO.insertar_If(tempIzquierda, "<", tempDerecha, labelMenor)
                  #--Se itera hasta que encuentre de los casos anteriores
                CODIGO.insertar_Expresion(expresionIzquierda.valor, expresionIzquierda.valor, "+", "1")
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                #Label Mayor
                CODIGO.insertar_Label(labelMayor)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)

                #Label Menor
                CODIGO.insertar_Label(labelMenor)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)
                
                #Label Izquierdo Nulo
                CODIGO.insertar_Label(labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)

                #Label Derecho Nulo
                CODIGO.insertar_Label(labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)
                
                #--Salida de la operacion
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
            
            else:
                REPORTES.salida += "ERROR: La operacion menor que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion menor que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operacion menor que solo recibe strings o numbers (un solo tipo a la vez).")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.MAYORIG.value:
            CODIGO.insertar_Comentario("////////// INICIA MAYOR IGUAL QUE //////////")

            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, ">=", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)

            
            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                
                #Declarar label
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                labelIzquierdaNulo = CODIGO.nuevoLabel()
                labelDerechaNulo = CODIGO.nuevoLabel()
                labelAmbosNulo = CODIGO.nuevoLabel()
                labelMayor = CODIGO.nuevoLabel()
                labelMenor = CODIGO.nuevoLabel()
                tempIzquierda = CODIGO.nuevoTemporal()
                tempDerecha = CODIGO.nuevoTemporal()

                #Ciclo de comparacion
                CODIGO.insertar_Label(labelCiclo)
                  #--- Leer el caracter del heap
                CODIGO.insertar_ObtenerHeap(tempIzquierda, expresionIzquierda.valor)
                CODIGO.insertar_ObtenerHeap(tempDerecha, expresionDerecha.valor)
                  #-- Si viene -1 o es menor se sale
                CODIGO.insertar_If(tempIzquierda, "==", "-1", labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelDerechaNulo)
                CODIGO.insertar_If(tempIzquierda, ">", tempDerecha, labelMayor)
                CODIGO.insertar_If(tempIzquierda, "<", tempDerecha, labelMenor)
                  #--Se itera hasta que encuentre de los casos anteriores
                CODIGO.insertar_Expresion(expresionIzquierda.valor, expresionIzquierda.valor, "+", "1")
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                #Label Mayor
                CODIGO.insertar_Label(labelMayor)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)

                #Label Menor
                CODIGO.insertar_Label(labelMenor)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)
                
                #Label Izquierdo Nulo
                CODIGO.insertar_Label(labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelAmbosNulo)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)

                #Label Derecho Nulo
                CODIGO.insertar_Label(labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)

                #Label Ambos Nulos. Son iguales.
                CODIGO.insertar_Label(labelAmbosNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)
    
                #--Salida de la operacion
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
            
            else:
                REPORTES.salida += "ERROR: La operacion mayor igual solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion mayor igual solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operacion mayor igual solo recibe strings o numbers (un solo tipo a la vez).")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
        elif self.tipoOperacion == Expresion.MENORIG.value:
            CODIGO.insertar_Comentario("////////// INICIA MENOR IGUAL QUE //////////")

            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "<=", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)

            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                
                #Declarar label
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                labelIzquierdaNulo = CODIGO.nuevoLabel()
                labelDerechaNulo = CODIGO.nuevoLabel()
                labelAmbosNulo = CODIGO.nuevoLabel()
                labelMayor = CODIGO.nuevoLabel()
                labelMenor = CODIGO.nuevoLabel()
                tempIzquierda = CODIGO.nuevoTemporal()
                tempDerecha = CODIGO.nuevoTemporal()

                #Ciclo de comparacion
                CODIGO.insertar_Label(labelCiclo)
                  #--- Leer el caracter del heap
                CODIGO.insertar_ObtenerHeap(tempIzquierda, expresionIzquierda.valor)
                CODIGO.insertar_ObtenerHeap(tempDerecha, expresionDerecha.valor)
                  #-- Si viene -1 o es menor se sale
                CODIGO.insertar_If(tempIzquierda, "==", "-1", labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelDerechaNulo)
                CODIGO.insertar_If(tempIzquierda, "<", tempDerecha, labelMenor)
                CODIGO.insertar_If(tempIzquierda, ">", tempDerecha, labelMayor)
                  #--Se itera hasta que encuentre de los casos anteriores
                CODIGO.insertar_Expresion(expresionIzquierda.valor, expresionIzquierda.valor, "+", "1")
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                #Label Mayor
                CODIGO.insertar_Label(labelMayor)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)

                #Label Menor
                CODIGO.insertar_Label(labelMenor)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)
                
                #Label Izquierdo Nulo
                CODIGO.insertar_Label(labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelAmbosNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)

                #Label Derecho Nulo
                CODIGO.insertar_Label(labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)

                #Label Ambos Nulo
                CODIGO.insertar_Label(labelAmbosNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)
    
                #--Salida de la operacion
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
              
            else:
                REPORTES.salida += "ERROR: La operacion menor igual solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion menor igual que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operacion menor igual solo recibe strings o numbers (un solo tipo a la vez).")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.IGUALACION.value:
            CODIGO.insertar_Comentario("////////// INICIA IGUALACION //////////")

            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "==", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)

            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                
                #Declarar label
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                labelIzquierdaNulo = CODIGO.nuevoLabel()
                labelDerechaNulo = CODIGO.nuevoLabel()
                labelDesigual = CODIGO.nuevoLabel()
                tempIzquierda = CODIGO.nuevoTemporal()
                tempDerecha = CODIGO.nuevoTemporal()

                #Ciclo de comparacion
                CODIGO.insertar_Label(labelCiclo)
                  #--- Leer el caracter del heap
                CODIGO.insertar_ObtenerHeap(tempIzquierda, expresionIzquierda.valor)
                CODIGO.insertar_ObtenerHeap(tempDerecha, expresionDerecha.valor)
                  #-- Si viene -1 o es menor se sale
                CODIGO.insertar_If(tempIzquierda, "==", "-1", labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelDerechaNulo)
                CODIGO.insertar_If(tempIzquierda, "!=", tempDerecha, labelDesigual)
                
                  #--Se itera hasta que encuentre de los casos anteriores
                CODIGO.insertar_Expresion(expresionIzquierda.valor, expresionIzquierda.valor, "+", "1")
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                #Label Desigual
                CODIGO.insertar_Label(labelDesigual)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)
                
                #Label Izquierdo Nulo
                CODIGO.insertar_Label(labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "!=", "-1", labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)

                #Label Derecho Nulo
                CODIGO.insertar_Label(labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)
    
                #--Salida de la operacion
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
            
            elif expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "==", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
            
            else:
                REPORTES.salida += "ERROR: La operacion igualacion que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion igualacion que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operacion igualacion solo recibe strings o numbers (un solo tipo a la vez).")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

        elif self.tipoOperacion == Expresion.DISTINTO.value:
            CODIGO.insertar_Comentario("////////// INICIA DESIGUAL //////////")

            if expresionIzquierda.tipo == Tipo.NUMBER.value and expresionDerecha.tipo == Tipo.NUMBER.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "!=", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)

            elif expresionIzquierda.tipo == Tipo.STRING.value and expresionDerecha.tipo == Tipo.STRING.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                
                #Declarar label
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                labelIzquierdaNulo = CODIGO.nuevoLabel()
                labelDerechaNulo = CODIGO.nuevoLabel()
                labelDesigual = CODIGO.nuevoLabel()
                tempIzquierda = CODIGO.nuevoTemporal()
                tempDerecha = CODIGO.nuevoTemporal()

                #Ciclo de comparacion
                CODIGO.insertar_Label(labelCiclo)
                  #--- Leer el caracter del heap
                CODIGO.insertar_ObtenerHeap(tempIzquierda, expresionIzquierda.valor)
                CODIGO.insertar_ObtenerHeap(tempDerecha, expresionDerecha.valor)
                  #-- Si viene -1 o es menor se sale
                CODIGO.insertar_If(tempIzquierda, "==", "-1", labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "==", "-1", labelDerechaNulo)
                CODIGO.insertar_If(tempIzquierda, "!=", tempDerecha, labelDesigual)
                
                  #--Se itera hasta que encuentre de los casos anteriores
                CODIGO.insertar_Expresion(expresionIzquierda.valor, expresionIzquierda.valor, "+", "1")
                CODIGO.insertar_Expresion(expresionDerecha.valor, expresionDerecha.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                #Label Desigual
                CODIGO.insertar_Label(labelDesigual)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)
                
                #Label Izquierdo Nulo
                CODIGO.insertar_Label(labelIzquierdaNulo)
                CODIGO.insertar_If(tempDerecha, "!=", "-1", labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "0")
                CODIGO.insertar_Goto(labelSalida)

                #Label Derecho Nulo
                CODIGO.insertar_Label(labelDerechaNulo)
                CODIGO.insertar_Asignacion(tempResultado, "1")
                CODIGO.insertar_Goto(labelSalida)
    
                #--Salida de la operacion
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
            
            elif expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "!=", expresionDerecha.valor, labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
            
            else:
                REPORTES.salida += "ERROR: La operacion distinto que solo recibe strings o numbers (un solo tipo a la vez). \n"
                mensaje = "La operacion distinto que solo recibe strings o numbers (un solo tipo a la vez)."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operacion distinto solo recibe strings o numbers (un solo tipo a la vez).")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

        # Logicas -----------------------------------------------------------------------------------
        elif self.tipoOperacion == Expresion.AND.value:
            #Evaluar el caso en que ambos sean boolean
            if expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "==", "0", labelSalida)
                CODIGO.insertar_If(expresionDerecha.valor, "==", "0", labelSalida)
                CODIGO.insertar_Goto(labelVerdadero)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
                
            else:
                REPORTES.salida += "ERROR: La operacion and solo recibe booleanos. \n"
                mensaje = "La operacion and que solo recibe booleanos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operacion and solo recibe booleanos.")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
        elif self.tipoOperacion == Expresion.OR.value:
            #Evaluar el caso en que ambos sean boolean
            if expresionIzquierda.tipo == Tipo.BOOLEAN.value and expresionDerecha.tipo == Tipo.BOOLEAN.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Evaluar
                CODIGO.insertar_If(expresionIzquierda.valor, "==", "1", labelVerdadero)
                CODIGO.insertar_If(expresionDerecha.valor, "==", "1", labelVerdadero)
                CODIGO.insertar_Goto(labelSalida)

                #--Es verdaddera la comparacion
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
                
            else:
                REPORTES.salida += "ERROR: La operacion or solo recibe booleanos. \n"
                mensaje = "La operacion or que solo recibe booleanos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operacion or solo recibe booleanos.")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        

        
        
            

            
