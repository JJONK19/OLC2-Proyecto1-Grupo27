from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from Ejecucion.Entorno import entorno
from C3D.Valor3D import valor3D

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
        elif self.tipoOperacion == Expresion.DECREMENTO.value:
            operador = "--"
        elif self.tipoOperacion == Expresion.INCREMENTO.value:
            operador = "++"
        REPORTES.dot += nodoOperador + "[ label = \"" +  operador + "\" ];\n"
        REPORTES.cont += 1

        #Declarar operacion
        nodoExpresion = self.expresion.grafo(REPORTES)

        if self.tipoOperacion == Expresion.UNARIO.value or self.tipoOperacion == Expresion.NOT.value:
            #Conectar con el padre
            REPORTES.dot += padre + "->" + nodoOperador + ";\n"
            REPORTES.dot += padre + "->" + nodoExpresion + ";\n"
        else: 
            #Conectar con el padre
            REPORTES.dot += padre + "->" + nodoExpresion + ";\n"
            REPORTES.dot += padre + "->" + nodoOperador + ";\n"
            
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
            numero = float(expresion.valor) * - 1

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
            
        elif self.tipoOperacion == Expresion.INCREMENTO.value:
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
            numero = float(expresion.valor) + 1

            #Retorno
            retorno = valor()
            retorno.id = expresion.id
            retorno.tipo = expresion.tipo
            retorno.valor = str(numero)
            retorno.clase = expresion.clase
            retorno.string = retorno.valor
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            
            #Actualizar en la tabla de simbolos
            salida = entorno.asignarSimbolo(retorno, SIMBOLOS, REPORTES) 

            if salida == -1:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: Ocurrio un error al reasignar la variable. \n"
                mensaje = "Ocurrio un error al reasignar la variable."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            return retorno
        
        elif self.tipoOperacion == Expresion.DECREMENTO.value:
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
            numero = float(expresion.valor) - 1

            #Retorno
            retorno = valor()
            retorno.id = expresion.id
            retorno.tipo = expresion.tipo
            retorno.valor = str(numero)
            retorno.clase = expresion.clase
            retorno.string = retorno.valor
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            
            #Actualizar en la tabla de simbolos
            salida = entorno.asignarSimbolo(retorno, SIMBOLOS, REPORTES) 

            if salida == -1:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: Ocurrio un error al reasignar la variable. \n"
                mensaje = "Ocurrio un error al reasignar la variable."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            return retorno

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        #Obtener el valor de las expresiones
        expresion = self.expresion.c3d(SIMBOLOS, REPORTES, CODIGO)

        #Comprobar que sea primitivo
        if expresion.clase != Clases.PRIMITIVO.value:
            CODIGO.insertar_Comentario("ERROR: El operador izquierdo no es de tipo Primitivo")
            REPORTES.salida += "ERROR: El operador izquierdo no es de tipo Primitivo. \n"
            mensaje = "El operador izquierdo no es de tipo Primitivo."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        #Separacion de instruccion
        if self.tipoOperacion == Expresion.NOT.value:
            #Evaluar el caso en que ambos sean boolean
            if expresion.tipo == Tipo.BOOLEAN.value:
                #Crear el temporal. Resulatdo almacena el resultado de la comparacion. 1 en el true, 0 en el false.
                #Se le asigna 0 de una vez para que vaya al label de salida si no cumple
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Declarar lables de entrada y salida
                labelVerdadero = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()

                #---Como se inicializa en 0, si es verdadero el valor de salida ya va a tener 0
                CODIGO.insertar_If(expresion.valor, "==", "1", labelSalida)
                CODIGO.insertar_Goto(labelVerdadero)

                #--Si es 0 entra aca y cambia a 1
                CODIGO.insertar_Label(labelVerdadero)
                CODIGO.insertar_Asignacion(tempResultado, "1")

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value)
                
            else:
                REPORTES.salida += "ERROR: La operación not solo recibe booleanos. \n"
                mensaje = "La operación not solo recibe booleanos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La operación not solo recibe booleanos.")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoOperacion == Expresion.UNARIO.value:
            CODIGO.insertar_Comentario("////////// INICIA RESTA //////////")
            #Evaluar el caso en que ambos sean number
            if expresion.tipo == Tipo.NUMBER.value:
                #Crear el temporal y añadirle la resta de los temporales
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Expresion(tempResultado, "0", "-", expresion.valor)

                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
    
            else:
                CODIGO.insertar_Comentario("ERROR: La negacion unaria solo recibe numbers.")
                REPORTES.salida += "ERROR: La negacion unaria solo recibe numbers. \n"
                mensaje = "La negacion unaria solo recibe numbers."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
        
        
        
