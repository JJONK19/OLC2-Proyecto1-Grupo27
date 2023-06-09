from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor

class expresionUnaria(instruccion):
    '''
        Almacena el contenido de una operacion con dos valores (suma, mayor que, igual, etc).
        Siempre retorna un primitivo al ejecutarse.
        - Expresion: Contiene una instruccion que puede ser otra operacion o un valor.
        - TipoOperacion: Contiene un string que indica que operacion se va a realizar (suma, resta, potencia, etc)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    
    def __init__(self, EXPRESION, TIPO_OPERACION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.expresion = EXPRESION
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

        #Declarar operador
        nodoOperador = "NODO" + str(REPORTES.cont)
        operador = ""
        if self.tipoOperacion == Expresion.UNARIO.value:
            operador = "-"
        elif self.tipoOperacion == Expresion.NOT.value:
            operador = "!"
        REPORTES.dot += nodoOperador + "[ label = \"" +  operador + "\" ];\n"
        REPORTES.cont += 1

        #Declarar operacion
        nodoExpresion = self.expresion.grafo(REPORTES)

        #Conectar con el padre
        REPORTES.dot += padre + "->" + nodoOperador + ";\n"
        REPORTES.dot += padre + "->" + nodoExpresion + ";\n"
        return padre    

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Obtener el valor de la expresion
        expresion = self.expresion.analisis(SIMBOLOS, REPORTES)

        #Comprobar que no sea NUll
        if expresion.tipo == Tipo.NULL.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: No se puede operar un valor de tipo Null (1). \n"
            mensaje = "No se puede operar un valor de tipo Null (1)."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno

        #Comprobar que sea primitivo
        if expresion.clase != Clases.PRIMITIVO.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: Se esperaba un valor de tipo primitivo (1). \n"
            mensaje = "ERROR: Se esperaba un valor de tipo primitivo (1)."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno
        
        #Separacion de instruccion
        if self.tipoOperacion == Expresion.NOT.value:
            #Evaluar que el valor sea booleano
            if expresion.tipo != Tipo.BOOLEAN.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La operación not solo recibe booleanos. \n"
                mensaje = "La operación not solo recibe booleanos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            #Retorno
            retorno = valor()
            retorno.id = expresion.id
            retorno.tipo = expresion.tipo
            if expresion.valor == "true":
                retorno.valor = "false"
            else:
                retorno.valor = "true"
            retorno.clase = expresion.clase
            retorno.string = retorno.valor
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo
            return retorno
            
        elif self.tipoOperacion == Expresion.UNARIO.value:
            #Evaluar que el valor sea booleano
            if expresion.tipo != Tipo.NUMBER.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La negacion unaria solo recibe numbers. \n"
                mensaje = "La negacion unaria solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            #Convertir el numero
            numero = float(expresion.valor) * -1
            
            #Retorno
            retorno = valor()
            retorno.id = expresion.id
            retorno.tipo = expresion.tipo
            retorno.valor = str(numero)
            retorno.clase = expresion.clase
            retorno.string = retorno.valor
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno

    def c3d(self):
        pass
