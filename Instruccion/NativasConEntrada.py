from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from C3D.Valor3D import valor3D

class nativaConValor(instruccion):
    '''
        Funciones nativas que retornan un primitivo. Reciben un parametro.
        - Modificar: Contiene una expresion (llamada a variable, un string, etc).
        - Contenido: Contiene una expresion usada en la funcion nativa (una variable, un string, etc)
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

        # Declarar funcion
        nodoFuncion = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncion + "[ label = \"." + self.tipoInstruccion +" (\" ];\n"
        REPORTES.cont += 1

        # Declarar operacion
        nodoContenido = self.contenido.grafo(REPORTES)

        # Declarar cierre de funcion
        nodoFuncionC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncionC + "[ label = \")\" ];\n"
        REPORTES.cont += 1

        # Conectar con el padre
        REPORTES.dot += padre + "->" + nodoModificar + ";\n"
        REPORTES.dot += padre + "->" + nodoFuncion + ";\n"
        REPORTES.dot += padre + "->" + nodoContenido + ";\n"
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
        expresionContenido = self.contenido.analisis(SIMBOLOS, REPORTES)

        #Verificar que no sea nulo
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
        
        #Verificar que reciba un number en la entrada y el parametro
        if expresionEvaluar.tipo != Tipo.NUMBER.value or expresionContenido.tipo != Tipo.NUMBER.value:
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
    
        #Clasificar por tipo de operacion y ejecutar
        if self.tipoInstruccion == Expresion.TOFIXED.value:
            #Ejecutar la funcion. El numero de decimales es contenido y el valor que se trabaja es modificar
            numero = float(expresionEvaluar.valor)
            cifras = int(float(expresionContenido.valor))
            aproximar = f"{numero:.{cifras}f}"

            retorno = valor()
            retorno.id = expresionEvaluar.id
            retorno.tipo = expresionEvaluar.tipo
            retorno.valor = expresionEvaluar.valor
            retorno.clase = expresionEvaluar.clase
            retorno.string = aproximar
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno
        
        elif self.tipoInstruccion == Expresion.TOEXPONENTIAL.value:
            #Ejecutar la funcion. El numero de decimales es contenido y el valor que se trabaja es modificar
            numero = float(expresionEvaluar.valor)
            cifras = int(float(expresionContenido.valor))
            exponencial = format(numero, f".{cifras}e")

            retorno = valor()
            retorno.id = expresionEvaluar.id
            retorno.tipo = expresionEvaluar.tipo
            retorno.valor = expresionEvaluar.valor
            retorno.clase = expresionEvaluar.clase
            retorno.string = exponencial
            retorno.valorClase = retorno.clase
            retorno.valorTipo = retorno.tipo    
            return retorno
        
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        #Extraer valores
        expresionEvaluar = self.modificar.c3d(SIMBOLOS, REPORTES, CODIGO)
        expresionContenido = self.contenido.c3d(SIMBOLOS, REPORTES, CODIGO)

        #Comprobar que sea primitivo
        if expresionEvaluar.clase != Clases.PRIMITIVO.value:
            REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo opera sobre tipos Primitivos. \n"
            mensaje = "La funcion " + self.tipoInstruccion + " solo opera sobre tipos Primitivos."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            CODIGO.insertar_Comentario("ERROR: La funcion nativa se esta ejecutando sobre un NULL.")
  
            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
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
            CODIGO.insertar_Comentario("ERROR: La funcion " + self.tipoInstruccion + " solo recibe sobre tipos Primitivos.")
  
            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        #Verificar que reciba un number en la entrada y el parametro
        if expresionEvaluar.tipo != Tipo.NUMBER.value or expresionContenido.tipo != Tipo.NUMBER.value:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: La funcion " + self.tipoInstruccion + " solo maneja numbers. \n"
            mensaje = "La funcion " + self.tipoInstruccion + " solo maneja numbers."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            CODIGO.insertar_Comentario("ERROR: La funcion " + self.tipoInstruccion + " solo maneja numbers.")
  
            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        #Clasificar por tipo de operacion y ejecutar
        if self.tipoInstruccion == Expresion.TOFIXED.value:
            CODIGO.insertar_Comentario("////////// FUNCION TO FIXED //////////")

            #Crear el temporal y guardar la posicion del heap
            tempResultado = CODIGO.nuevoTemporal()

            #Declaracion de Labels y temporales
            tempPotencia = CODIGO.nuevoTemporal()
            tempOperacion = CODIGO.nuevoTemporal()
            
            #Primero se eleva 10 ^ decimales
            CODIGO.insertar_Pow(tempPotencia, "10", expresionContenido.valor) #potencia = math.Pow(10, decimales)
            CODIGO.insertar_Expresion(tempOperacion, expresionEvaluar.valor, "*", tempPotencia)
            CODIGO.insertar_Round(tempResultado, tempOperacion)
            CODIGO.insertar_Expresion(tempResultado, tempResultado, "/", tempPotencia) #res = math.Round(numero*potencia) / potencia

            #Retornar el valor
            return valor3D(tempResultado, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipoInstruccion == Expresion.TOEXPONENTIAL.value:
            #Ejecutar la funcion. El numero de decimales es contenido y el valor que se trabaja es modificar
            CODIGO.insertar_Comentario("////////// FUNCION TO EXPONENTAL //////////")
            
            #Crear el temporal y guardar la posicion del heap
            tempResultado = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(tempResultado, "H")

            #Declaracion de Labels y temporales
            tempPotencia = CODIGO.nuevoTemporal()

            #Tomar el numero de decimales y convertirlo a potencia de 10
            CODIGO.insertar_Pow(tempPotencia, "10", expresionContenido.valor) #potencia = math.Pow(10, decimales)
            
            #Dividir ese numero entre la potencia
            CODIGO.insertar_Expresion(expresionEvaluar.valor, expresionEvaluar.valor, "/", tempPotencia)

            #Convertir el resultado a string ===================================================================
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
            CODIGO.insertar_If(tempEntero, ">", "0", labelEnteroSalida)
            CODIGO.insertar_Mod(tempAlmacen, tempEntero, "10")
            CODIGO.insertar_Expresion(tempTemporal, tempAlmacen, "+", "48")
            CODIGO.insertar_SetearHeap('H', tempTemporal)   
            CODIGO.insertar_MoverHeap()
            CODIGO.insertar_Expresion(tempEntero, tempEntero, "/", "10")
            CODIGO.insertar_Goto(labelEntero)
            CODIGO.insertar_Label(labelEnteroSalida)
            
            #Añadir punto
            CODIGO.insertar_SetearHeap('H', '46')            
            CODIGO.insertar_MoverHeap()

            #Iniciar un ciclo para crear los Decimales
            CODIGO.insertar_Label(labelDecimal)
            CODIGO.insertar_If(tempDecimal, ">", "0", labelDecimalSalida)
            CODIGO.insertar(f'{tempDecimal} = {tempDecimal} * 10\n')
            CODIGO.insertar(f'{tempAlmacen} = math.Floor({tempDecimal})\n')
            CODIGO.insertar_Expresion(tempTemporal, tempAlmacen, "+", "48")
            CODIGO.insertar_SetearHeap('H', tempTemporal)   
            CODIGO.insertar_MoverHeap()
            CODIGO.insertar_Expresion(tempDecimal, tempDecimal, "-", tempAlmacen)
            CODIGO.insertar_Goto(labelDecimal)
            CODIGO.insertar_Label(labelDecimalSalida)
            
            #Añadir la e y el + 
            CODIGO.insertar_SetearHeap('H', '101')            
            CODIGO.insertar_MoverHeap()
            CODIGO.insertar_SetearHeap('H', '43')            
            CODIGO.insertar_MoverHeap()

            #Añadir el numero de posiciones al heap ===========================================================
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
            CODIGO.insertar_If(tempEntero, ">", "0", labelEnteroSalida)
            CODIGO.insertar(f'{tempTemporal} = int({tempEntero}) % 10\n')
            CODIGO.insertar_Asignacion(tempAlmacen, tempTemporal)
            CODIGO.insertar_Expresion(tempAlmacen, tempAlmacen, "+", "48")
            CODIGO.insertar_SetearHeap('H', tempAlmacen)   
            CODIGO.insertar_MoverHeap()
            CODIGO.insertar_Expresion(tempEntero, tempEntero, "/", "10")
            CODIGO.insertar_Goto(labelEntero)
            CODIGO.insertar_Label(labelEnteroSalida)
            
            #Iniciar un ciclo para crear los Decimales
            CODIGO.insertar_Label(labelDecimal)
            CODIGO.insertar_If(tempDecimal, ">", "0", labelDecimalSalida)
            CODIGO.insertar(f'{tempDecimal} = {tempDecimal} * 10\n')
            CODIGO.insertar(f'{tempAlmacen} = math.Floor({tempDecimal})\n')
            CODIGO.insertar_Expresion(tempAlmacen, tempAlmacen, "+", "48")
            CODIGO.insertar_SetearHeap('H', tempAlmacen)   
            CODIGO.insertar_MoverHeap()
            CODIGO.insertar_Floor(tempTemporal, tempAlmacen)
            CODIGO.insertar_Expresion(tempDecimal, tempDecimal, "-", tempTemporal)
            CODIGO.insertar_Goto(labelDecimal)
            CODIGO.insertar_Label(labelDecimalSalida)

            #--Salida de la operacion
            CODIGO.insertar_SetearHeap('H', '-1')            
            CODIGO.insertar_MoverHeap()
            return valor3D(tempResultado, True, Tipo.STRING.value, Clases.PRIMITIVO.value)
