from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from C3D.Valor3D import valor3D

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
        if self.tipoInstruccion == Expresion.TOSTRING.value or self.tipoInstruccion == Expresion.TOLOWERCASE.value or self.tipoInstruccion == Expresion.TOUPPERCASE.value:
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
            
        elif self.tipoInstruccion == Expresion.LENGTH.value:
            if expresionEvaluar.clase == Clases.STRUCT.value:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre tipos Strings o Vectores. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo opera sobre tipos String o Vectores."
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
        
        elif self.tipoInstruccion == Expresion.TYPEOF.value:
            #Ejecutar la funcion. Solo se retorna el tipo del objeto del valor.
            cadena = ""
            if expresionEvaluar.tipo == Tipo.STRING.value:
                cadena = "string"
            elif expresionEvaluar.tipo == Tipo.NUMBER.value:
                cadena = "number"
            elif expresionEvaluar.tipo == Tipo.BOOLEAN.value:
                cadena = "boolean"
            elif expresionEvaluar.tipo == Tipo.ANY.value:
                cadena = "any"
            else:
                cadena = expresionEvaluar.tipo

            retorno = valor()
            retorno.id = expresionEvaluar.id
            retorno.tipo = Tipo.STRING.value
            retorno.valor = cadena
            retorno.clase = Clases.PRIMITIVO.value
            retorno.string = cadena
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno

        elif self.tipoInstruccion == Expresion.LENGTH.value:
            #Verificar que reciba un string en la entrada y el parametro
            if expresionEvaluar.tipo != Tipo.STRING.value:
                if expresionEvaluar.clase != Clases.VECTOR.value:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings o vectores. \n"
                    mensaje = "La funcion " + self.tipoInstruccion + " solo maneja strings o vectores."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    return retorno

            #Ejecutar la funcion. El numero de decimales es contenido y el valor que se trabaja es modificar
            cadena = expresionEvaluar.valor
            longitud = str(len(cadena))

            retorno = valor()
            retorno.id = expresionEvaluar.id
            retorno.tipo = Tipo.NUMBER.value
            retorno.valor = longitud
            retorno.clase = Clases.PRIMITIVO.value
            retorno.string = longitud
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno
        
        
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        #Extraer valores
        expresionEvaluar = self.modificar.c3d(SIMBOLOS, REPORTES, CODIGO)

        #VErificar que no sea nulo
        if expresionEvaluar.tipo == Tipo.NULL.value:
            REPORTES.salida += "ERROR: La funcion nativa se esta ejecutando sobre un NULL. \n"
            mensaje = "La funcion nativa se esta ejecutando sobre un NULL."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            CODIGO.insertar_Comentario("ERROR: La funcion nativa se esta ejecutando sobre un NULL.")
  
            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        #Comprobar que sea primitivo
        if self.tipoInstruccion == Expresion.TOSTRING.value or self.tipoInstruccion == Expresion.TOLOWERCASE.value or self.tipoInstruccion == Expresion.TOUPPERCASE.value:
            if expresionEvaluar.clase != Clases.PRIMITIVO.value:
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre tipos Primitivos. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo opera sobre tipos Primitivos."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre tipos Primitivos.")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
        elif self.tipoInstruccion == Expresion.LENGTH.value:
            if expresionEvaluar.clase == Clases.STRUCT.value:
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre tipos Strings o Vectores. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo opera sobre tipos String o Vectores."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre tipos Strings o Vectores.")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        #Clasificar por tipo de operacion y ejecutar
        if self.tipoInstruccion == Expresion.TOSTRING.value:
            #Separar por tipos. 
            CODIGO.insertar_Comentario("////////// INICIA TOSTRING //////////")
            
            #Por divisiones sucesivas se busca extraer cada digito del numero y añadirlo al heap como string
            if expresionEvaluar.tipo == Tipo.NUMBER:
                #Crear el temporal y guardar la posicion del heap
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "H")
                
                #Declaracion de Labels y temporales
                labelNoEsNegativo = CODIGO.nuevoLabel()
                labelEntero = CODIGO.nuevoLabel()
                labelEnteroSalida = CODIGO.nuevoLabel()
                labelDecimal = CODIGO.nuevoLabel()
                labelDecimalSalida = CODIGO.nuevoLabel()
                tempEntero = CODIGO.nuevoTemporal()
                tempDecimal = CODIGO.nuevoTemporal()
                tempAlmacen = CODIGO.nuevoTemporal()
                tempTemporal = CODIGO.nuevoTemporal()
                tempTemporal2 = CODIGO.nuevoTemporal()

                #Si es negativo, añadir al heap el signo y obtener el valor absoluto
                CODIGO.insertar_If(expresionEvaluar.valor, "<", "0", labelNoEsNegativo)
                CODIGO.insertar_SetearHeap('H', "45")
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_Abs(expresionEvaluar.valor, expresionEvaluar.valor)

                CODIGO.insertar_Label(labelNoEsNegativo)

                #Separar enteros de decimales
                CODIGO.insertar_Floor(tempEntero, expresionEvaluar.valor)
                CODIGO.insertar_Expresion(tempDecimal, expresionEvaluar.valor, "-", tempEntero)

                #Iniciar un ciclo para crear los enteros
                CODIGO.insertar_Label(labelEntero)
                CODIGO.insertar_If(tempEntero, "<", "0", labelEnteroSalida)
                CODIGO.insertar(f'{tempAlmacen} = int({tempEntero}) % 10')
                CODIGO.insertar_Expresion(tempAlmacen, tempAlmacen, "+", "48")
                CODIGO.insertar_SetearHeap('H', tempAlmacen)   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_Expresion(tempTemporal, tempEntero, "/", "10")
                CODIGO.insertar_Floor(tempEntero, tempTemporal)
                CODIGO.insertar_Goto(labelEntero)
                CODIGO.insertar_Label(labelEnteroSalida)
                
                #Iniciar un ciclo para crear los Decimales
                CODIGO.insertar_Label(labelDecimal)
                CODIGO.insertar_If(tempDecimal, "<", "0", labelDecimalSalida)
                CODIGO.insertar(f'{tempAlmacen} = int({tempEntero}) * 10')
                CODIGO.insertar_Expresion(tempAlmacen, tempAlmacen, "+", "48")
                CODIGO.insertar_SetearHeap('H', tempAlmacen)   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_Expresion(tempTemporal, tempDecimal, "*", "10")
                CODIGO.insertar_Floor(tempTemporal2, tempTemporal)
                CODIGO.insertar_Expresion(tempDecimal, tempTemporal, "-", tempTemporal2)
                CODIGO.insertar_Goto(labelDecimal)
                CODIGO.insertar_Label(labelDecimalSalida)

                #Guardar el fin de la cadena y mover el heap a una posicion vacia
                CODIGO.insertar_SetearHeap('H', '-1')            
                CODIGO.insertar_MoverHeap()

                return valor3D(tempResultado, True, Tipo.STRING.value, Clases.PRIMITIVO.value)

            elif expresionEvaluar.tipo == Tipo.STRING.value:
                #Solo retorna el apuntador.
                return valor3D(expresionEvaluar.value, True, Tipo.STRING.value, Clases.PRIMITIVO.value)
            
            elif expresionEvaluar.tipo == Tipo.BOOLEAN.value:
                #Crear el temporal y guardar la posicion del heap
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "H")
                
                #Labels del if
                labelTrue = CODIGO.nuevoLabel()
                labelFalse = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                
                #If
                CODIGO.insertar_If(expresionEvaluar.valor, "==", "1", labelTrue)
                CODIGO.insertar_Goto(labelFalse)
                
                #Imprimir true
                CODIGO.insertar_Label(labelTrue)
                CODIGO.insertar_SetearHeap('H', "116")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "114")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "117")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "101")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_Goto(labelSalida)
                
                #Imprimir false
                CODIGO.insertar_Label(labelFalse)
                CODIGO.insertar_SetearHeap('H', "102")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "97")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "108")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "115")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "101")   
                CODIGO.insertar_MoverHeap()
                
                #Salida
                CODIGO.insertar_Label(labelSalida)
                CODIGO.insertar_SetearHeap('H', '-1')            
                CODIGO.insertar_MoverHeap()
                return valor3D(tempResultado, True, Tipo.STRING.value, Clases.PRIMITIVO.value)
            
        elif self.tipoInstruccion == Expresion.TOLOWERCASE.value:
            CODIGO.insertar_Comentario("////////// INICIA LOWERCASE //////////")
            #Verificar que reciba un string en la entrada y el parametro
            if expresionEvaluar.tipo != Tipo.STRING.value:
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo maneja strings."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings.")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
            #Crear el temporal y guardar la posicion del heap
            tempResultado = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(tempResultado, "H")

            #Declarar label
            labelCiclo = CODIGO.nuevoLabel()
            labelSalida = CODIGO.nuevoLabel()
            labelConvertir = CODIGO.nuevoLabel()
            labelAñadir = CODIGO.nuevoLabel()
            tempAlmacen = CODIGO.nuevoTemporal()
            
            #Ciclo de comparacion
            CODIGO.insertar_Label(labelCiclo)
                #--- Leer el caracter del heap
            CODIGO.insertar_ObtenerHeap(tempAlmacen, expresionEvaluar.valor)
                #-- Si viene -1 se sale
            CODIGO.insertar_If(tempAlmacen, "==", "-1", labelSalida)
            CODIGO.insertar_If(tempAlmacen, "<=", "90", labelConvertir)
                #-- Insertar
            CODIGO.insertar_SetearHeap('H', tempAlmacen)   
            CODIGO.insertar_MoverHeap()    
                #--Se itera hasta que encuentre un menor
            CODIGO.insertar_Expresion(expresionEvaluar.valor, expresionEvaluar.valor, "+", "1")
            CODIGO.insertar_Goto(labelCiclo)

            #Label Convertir. Convierte y añade al heap para regresar al ciclo
             #-- Si son numeros o cualquier otra cosa regresa
            CODIGO.insertar_Label(labelConvertir)
            CODIGO.insertar_If(tempAlmacen, "<=", "64", labelAñadir)
            CODIGO.insertar_Expresion(tempAlmacen, tempAlmacen, "+", "32")
            CODIGO.insertar_SetearHeap('H', tempAlmacen)   
            CODIGO.insertar_MoverHeap()  
            CODIGO.insertar_Expresion(expresionEvaluar.valor, expresionEvaluar.valor, "+", "1")
            CODIGO.insertar_Goto(labelCiclo)

            #Label Añadir. Si no son letras, solo las agrega
            CODIGO.insertar_Label(labelAñadir)
            CODIGO.insertar_SetearHeap('H', tempAlmacen)   
            CODIGO.insertar_MoverHeap()  
            CODIGO.insertar_Expresion(expresionEvaluar.valor, expresionEvaluar.valor, "+", "1")
            CODIGO.insertar_Goto(labelCiclo)

            #Guardar el fin de la cadena y mover el heap a una posicion vacia
            #--Salida de la operacion
            CODIGO.insertar_Label(labelSalida)
            CODIGO.insertar_SetearHeap('H', '-1')            
            CODIGO.insertar_MoverHeap()
            return valor3D(tempResultado, True, Tipo.STRING.value, Clases.PRIMITIVO.value)

        elif self.tipoInstruccion == Expresion.TOUPPERCASE.value:
            CODIGO.insertar_Comentario("////////// INICIA TOUPPERCASE //////////")
            #Verificar que reciba un string en la entrada y el parametro
            if expresionEvaluar.tipo != Tipo.STRING.value:
                REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings. \n"
                mensaje = "La funcion " + self.tipoInstruccion + " solo maneja strings."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                CODIGO.insertar_Comentario("ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings.")

                temporal = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(temporal, "0")
                return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
            #Crear el temporal y guardar la posicion del heap
            tempResultado = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(tempResultado, "H")

            #Declarar label
            labelCiclo = CODIGO.nuevoLabel()
            labelSalida = CODIGO.nuevoLabel()
            labelConvertir = CODIGO.nuevoLabel()
            tempAlmacen = CODIGO.nuevoTemporal()
            
            #Ciclo de comparacion
            CODIGO.insertar_Label(labelCiclo)
                #--- Leer el caracter del heap
            CODIGO.insertar_ObtenerHeap(tempAlmacen, expresionEvaluar.valor)
                #-- Si viene -1 se sale
            CODIGO.insertar_If(tempAlmacen, "==", "-1", labelSalida)
            CODIGO.insertar_If(tempAlmacen, ">=", "97", labelConvertir)
                #-- Insertar
            CODIGO.insertar_SetearHeap('H', tempAlmacen)   
            CODIGO.insertar_MoverHeap()    
                #--Se itera hasta que encuentre un menor
            CODIGO.insertar_Expresion(expresionEvaluar.valor, expresionEvaluar.valor, "+", "1")
            CODIGO.insertar_Goto(labelCiclo)

            #Label Convertir. Convierte y añade al heap para regresar al ciclo
             #-- Si son numeros o cualquier otra cosa regresa
            CODIGO.insertar_Label(labelConvertir)
            CODIGO.insertar_Expresion(tempAlmacen, tempAlmacen, "-", "32")
            CODIGO.insertar_SetearHeap('H', tempAlmacen)   
            CODIGO.insertar_MoverHeap()  
            CODIGO.insertar_Expresion(expresionEvaluar.valor, expresionEvaluar.valor, "+", "1")
            CODIGO.insertar_Goto(labelCiclo)

            #Guardar el fin de la cadena y mover el heap a una posicion vacia
            #--Salida de la operacion
            CODIGO.insertar_Label(labelSalida)
            CODIGO.insertar_SetearHeap('H', '-1')            
            CODIGO.insertar_MoverHeap()
            return valor3D(tempResultado, True, Tipo.STRING.value, Clases.PRIMITIVO.value)
        
        elif self.tipoInstruccion == Expresion.TYPEOF.value:
            CODIGO.insertar_Comentario("////////// INICIA TYPEOF //////////")
            #Crear el temporal y guardar la posicion del heap
            tempResultado = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(tempResultado, "H")

            if expresionEvaluar.tipo == Tipo.STRING.value:
                CODIGO.insertar_SetearHeap('H', "115")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "116")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "114")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "105")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "110")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "103")   
                CODIGO.insertar_MoverHeap()

            elif expresionEvaluar.tipo == Tipo.NUMBER.value:
                CODIGO.insertar_SetearHeap('H', "110")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "117")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "109")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "98")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "101")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "114")   
                CODIGO.insertar_MoverHeap()

            elif expresionEvaluar.tipo == Tipo.BOOLEAN.value:
                CODIGO.insertar_SetearHeap('H', "98")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "111")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "111")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "108")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "101")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "97")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "110")   
                CODIGO.insertar_MoverHeap()

            elif expresionEvaluar.tipo == Tipo.ANY.value:
                CODIGO.insertar_SetearHeap('H', "97")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "110")   
                CODIGO.insertar_MoverHeap()
                CODIGO.insertar_SetearHeap('H', "121")   
                CODIGO.insertar_MoverHeap()
                
            else:
                #Recorrer la cadena y guardar en el heap
                for caracter in str(expresionEvaluar.tipo):
                    CODIGO.insertar_SetearHeap('H', ord(caracter))   
                    CODIGO.insertar_MoverHeap()     

            CODIGO.insertar_SetearHeap('H', '-1')            
            CODIGO.insertar_MoverHeap()
            return valor3D(tempResultado, True, Tipo.STRING.value, Clases.PRIMITIVO.value)
        
        elif self.tipoInstruccion == Expresion.LENGTH.value:
            CODIGO.insertar_Comentario("////////// INICIA LENGTH //////////")
            #Verificar que reciba un string en la entrada y el parametro
            if expresionEvaluar.tipo != Tipo.STRING.value:
                if expresionEvaluar.clase != Clases.VECTOR.value:
                    REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings o vectores. \n"
                    mensaje = "La funcion " + self.tipoInstruccion + " solo maneja strings o vectores."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    CODIGO.insertar_Comentario("ERROR: La funcion " + self.tipoInstruccion + " solo maneja strings o vectores.")

                    temporal = CODIGO.nuevoTemporal()
                    CODIGO.insertar_Asignacion(temporal, "0")
                    return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
            
            if expresionEvaluar.tipo == Tipo.STRING.value and expresionEvaluar.clase == Clases.PRIMITIVO:
                tempResultado = CODIGO.nuevoTemporal()
                CODIGO.insertar_Asignacion(tempResultado, "0")

                #Expresion retorna la posicion en el heap en un temporal
                #Crear temporal contenedor, label del ciclo y salida
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                tempComparar = CODIGO.nuevoTemporal()

                #Comenzar ciclo 
                CODIGO.insertar_Label(labelCiclo)
                CODIGO.insertar_ObtenerHeap(tempComparar, expresionEvaluar.valor)
                CODIGO.insertar_If(tempComparar, "==", "-1", labelSalida)
                CODIGO.insertar_Expresion(tempResultado, tempResultado, "+", "1")
                CODIGO.insertar_Expresion(expresionEvaluar.valor, expresionEvaluar.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                #-- La condicion es falsa o acabo la verdadera
                CODIGO.insertar_Label(labelSalida)
                return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

            elif expresionEvaluar.clase == Clases.VECTOR:
                pass
           
