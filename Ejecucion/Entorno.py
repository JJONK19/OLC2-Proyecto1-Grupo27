from Tipos.Tipos import *
from Ejecucion.Valor import valor
from Dato.Metodo import metodo
from Dato.Primitivo import primitivo
from Dato.Struct import struct
from Dato.Vector import vector
from Dato.Estructura import estructura
from Dato.Any import any

class entorno:
    '''
        Entorno: La clase entorno almacena cada una de las variables en una seccion de la ejecucion.
        - Nombre: Nombre del entorno. Se usa en los reportes.  
    '''

    def __init__(self, NOMBRE):
        self.nombre_entorno = NOMBRE        #Nombre del entorno. Usado en el reporte.
        self.tipo_retorno = ""              #Indica si retorna un string, int, etc.
        self.clase_retorno = ""             #Indica si retorna un tipo primitivo, struct, etc.
        self.variables = {}                 #Almacena variables 
        self.metodos = {}                   #Acceso a los metodos declarados
        self.estructuras = {}               #Guarda la estructura de los structs que se pueden crear
        self.contador = 0                   #Sirve para crear nombres unicos para los entornos 

    #========================================== VARIABLES ===============================================================
    def insertarSimbolo(self, CONTENIDO, REPORTES):
        '''
            Ingresa un simbolo en alguna de los diccionarios del entorno. La variable contenido contiene toda la informacion
            relevante para crear el simbolo.
            Se inserta en el entorno local (el ultimo de la lista de entornos).  
            - CONTENIDO: Variable de la clase Valor.
            - REPORTES: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        #Verificar que no exista
        if self.existeSimbolo(CONTENIDO.id):
            REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " ya existe en este entorno. \n"
            mensaje = "La variable " + CONTENIDO.id + " ya existe en este entorno."
            REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
            return -1
        
        #Separar por clase y crear la variable en el entorno y el reporte
        if CONTENIDO.clase == Clases.PRIMITIVO.value:
            self.variables[CONTENIDO.id] = primitivo(CONTENIDO.id, CONTENIDO.tipo, CONTENIDO.clase, CONTENIDO.valor)
            REPORTES.añadirSimbolo(CONTENIDO.id, CONTENIDO.tipo, CONTENIDO.valor, self.nombre_entorno, CONTENIDO.linea, CONTENIDO.columna)
        
        elif CONTENIDO.clase == Clases.VECTOR.value:
            self.variables[CONTENIDO.id] = vector(CONTENIDO.id, CONTENIDO.tipo, CONTENIDO.clase, CONTENIDO.claseContenido, CONTENIDO.valor)
            var = self.variables[CONTENIDO.id].get("", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
            REPORTES.añadirSimbolo(CONTENIDO.id, CONTENIDO.tipo, var.string, self.nombre_entorno, CONTENIDO.linea, CONTENIDO.columna)
        
        elif CONTENIDO.clase == Clases.STRUCT.value:
            #Buscar si la estructura esta definida
            if not self.existeEstructura(CONTENIDO.tipo):
                REPORTES.salida += "ERROR: La estructura " + CONTENIDO.tipo + " no está definida. \n"
                mensaje = "La estructura " + CONTENIDO.tipo + " no está definida."
                REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                return -1
            
            #Verificar si la variable cumple con la estructura. El tipo de valor determina el tipo de estructura (ej: tipo = carro)
            referencia = self.estructuras[CONTENIDO.tipo]
            if not self.verificarAtributos(CONTENIDO.valor, referencia.atributos):
                REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no cumple con la estructura. \n"
                mensaje = "La variable " + CONTENIDO.id + " no cumple con la estructura."
                REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                return -1
            
            #Crear la variable y añadir a la estructura
            self.variables[CONTENIDO.id] = struct(CONTENIDO.id, CONTENIDO.tipo, CONTENIDO.clase, CONTENIDO.valor)
            var = self.variables[CONTENIDO.id].get("", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
            REPORTES.añadirSimbolo(CONTENIDO.id, CONTENIDO.tipo, var.string, self.nombre_entorno, CONTENIDO.linea, CONTENIDO.columna)
        
        elif CONTENIDO.clase == Clases.ANY.value:
            self.variables[CONTENIDO.id] = any(CONTENIDO.id, CONTENIDO.tipo, CONTENIDO.clase, CONTENIDO.valor, CONTENIDO.valorTipo, CONTENIDO.valorClase, CONTENIDO.claseContenido)
            var = self.variables[CONTENIDO.id].get("", "", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
            REPORTES.añadirSimbolo(CONTENIDO.id, CONTENIDO.tipo, var.string, self.nombre_entorno, CONTENIDO.linea, CONTENIDO.columna)
        
    @staticmethod  
    def asignarSimbolo(CONTENIDO, SIMBOLOS, REPORTES):
        '''
            Modifica una variable en el entorno inmediato. Esta se busca en todos los entornos de un ambito 
            (lista de entornos).
            - Contenido: Variable de tipo valor con los datos de entrada.
            - Simbolos: Lista con los entornos a revisar. Los ambitos se manejan como un arreglo, con el entorno global en la 
                        cabecera y el entorno local actual en la ultima posicion. 
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        #Se empieza a revisar del local inmediato (ultima posicion) al global (primera posicion)
        for i in range(len(SIMBOLOS)):
            entornoTemp = SIMBOLOS[len(SIMBOLOS) - (1 + i)]

            #Si no existe, revisa el siguiente
            if not entornoTemp.existeSimbolo(CONTENIDO.id):
                continue
            temp = entornoTemp.variables[CONTENIDO.id]

            #Recorrer la lista de accesos hasta encontrar el valor indicado
            for j in range(len(CONTENIDO.accesos)):
                tempAcceso = CONTENIDO.accesos[j]

                #Verificar que no sea null
                if temp.tipo == Tipo.NULL.value: 
                    REPORTES.salida += "ERROR: Uno de los accesos retorno NULL. \n"
                    mensaje = "Uno de los accesos retorno NULL."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1

                #Buscar el atributo/posicion 
                if temp.clase == Clases.PRIMITIVO.value:
                    REPORTES.salida += "ERROR: Una variable primitiva no maneja posiciones o atributos. \n"
                    mensaje = "Una variable primitiva no maneja posiciones o atributos."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1

                elif temp.clase == Clases.VECTOR.value:
                    if tempAcceso.tipo == Accesos.ATRIBUTO.value:
                        REPORTES.salida += "ERROR: Una variable vector no maneja atributos. \n"
                        mensaje = "Una variable vector no maneja atributos."
                        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                        return -1

                    temp = temp.get(tempAcceso.valor, REPORTES, CONTENIDO.linea, CONTENIDO.columna)

                elif temp.clase == Clases.STRUCT.value:
                    if tempAcceso.tipo == Accesos.POSICION.value:
                        REPORTES.salida += "ERROR: Una variable struct no maneja posiciones. \n"
                        mensaje = "Una variable struct no maneja posiciones."
                        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                        return -1

                    temp = temp.get(tempAcceso.valor, REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                
                elif temp.clase == Clases.ANY.value:
                    if temp.claseValor == Clases.PRIMITIVO.value:
                        REPORTES.salida += "ERROR: Una variable primitiva no maneja posiciones o atributos. \n"
                        mensaje = "Una variable primitiva no maneja posiciones o atributos."
                        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                        return -1

                    elif temp.claseValor == Clases.VECTOR.value:
                        if tempAcceso.tipo == Accesos.ATRIBUTO.value:
                            REPORTES.salida += "ERROR: Una variable vector no maneja atributos. \n"
                            mensaje = "Una variable vector no maneja atributos."
                            REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                            return -1

                        temp = temp.get(tempAcceso.valor, "", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                    
                    elif temp.clase == Clases.STRUCT.value:
                        if tempAcceso.tipo == Accesos.POSICION.value:
                            REPORTES.salida += "ERROR: Una variable struct no maneja posiciones. \n"
                            mensaje = "Una variable struct no maneja posiciones."
                            REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                            return -1

                        temp = temp.get("", tempAcceso.valor, REPORTES, CONTENIDO.linea, CONTENIDO.columna)

            if temp.clase == Clases.PRIMITIVO.value:
                #Comprobar tipos
                if temp.tipo != CONTENIDO.tipo:
                    REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no es de tipo " + CONTENIDO.tipo + ". \n"
                    mensaje = "La variable " + CONTENIDO.id + " no es de tipo " + CONTENIDO.tipo + "."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1
        
                #Comprobar clases
                if temp.clase != CONTENIDO.clase:
                    REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no es de clase " + CONTENIDO.clase + ". \n"
                    mensaje = "La variable " + CONTENIDO.id + " no es de clase " + CONTENIDO.clase + "."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1
                
                #Modificar valores
                temp.set(CONTENIDO.valor)
                REPORTES.actualizar(CONTENIDO.id, entornoTemp.nombre_entorno, CONTENIDO.valor)
                return None
                
            elif temp.clase == Clases.VECTOR.value:
                #Comprobar tipos
                if temp.tipo != CONTENIDO.tipo:
                    if temp.tipo != Tipo.ANY.value:
                        REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no es de tipo " + CONTENIDO.tipo + ". \n"
                        mensaje = "La variable " + CONTENIDO.id + " no es de tipo " + CONTENIDO.tipo + "."
                        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                        return -1
                
                #Comprobar clases
                if temp.clase != CONTENIDO.clase:
                    REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no es de clase " + CONTENIDO.clase + ". \n"
                    mensaje = "La variable " + CONTENIDO.id + " no es de clase " + CONTENIDO.clase + "."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1
                
                #Modificar valores
                temp.set(CONTENIDO.valor, CONTENIDO.claseContenido)
                var = temp.get("", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                REPORTES.actualizar(CONTENIDO.id, entornoTemp.nombre_entorno, var.string)
                return None
                
            elif temp.clase == Clases.STRUCT.value:
                #Comprobar tipos
                if temp.tipo != CONTENIDO.tipo:
                    REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no es de tipo " + CONTENIDO.tipo + ". \n"
                    mensaje = "La variable " + CONTENIDO.id + " no es de tipo " + CONTENIDO.tipo + "."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1
                
                #Comprobar clases
                if temp.clase != CONTENIDO.clase:
                    REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no es de clase " + CONTENIDO.clase + ". \n"
                    mensaje = "La variable " + CONTENIDO.id + " no es de clase " + CONTENIDO.clase + "."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1
                
                #Buscar si la estructura esta definida
                if not SIMBOLOS[0].existeEstructura(CONTENIDO.tipo):
                    REPORTES.salida += "ERROR: La estructura " + CONTENIDO.tipo + " no está definida. \n"
                    mensaje = "La estructura " + CONTENIDO.tipo + " no está definida."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1
                
                #Verificar si la variable cumple con la estructura. El tipo de valor determina el tipo de estructura (ej: tipo = carro)
                referencia = SIMBOLOS[0].estructuras[CONTENIDO.tipo]
                if not entornoTemp.verificarAtributos(CONTENIDO.valor, referencia.atributos):
                    REPORTES.salida += "ERROR: El nuevo valor no cumple con la estructura. \n"
                    mensaje = "El nuevo valor no cumple con la estructura."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return -1
                
                #Modificar valores
                temp.set(CONTENIDO.valor)
                var = temp.get("", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                REPORTES.actualizar(CONTENIDO.id, entornoTemp.nombre_entorno, var.string)
                return None
            
            elif temp.clase == Clases.ANY.value:
                #Modificar valores
                temp.set(CONTENIDO.valor, CONTENIDO.valorTipo, CONTENIDO.valorClase, CONTENIDO.claseContenido)
                var = temp.get("", "", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                REPORTES.actualizar(CONTENIDO.id, entornoTemp.nombre_entorno, var.string)
                return None
                
        REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no existe en ningun entorno. \n"
        mensaje = "La variable " + CONTENIDO.id + " no existe en ningun entorno."
        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
        return -1
    
    @staticmethod
    def getSimbolo(CONTENIDO, SIMBOLOS, REPORTES):
        '''
            Retorna una instancia de tipo valor con los datos de la variable. Esta se busca en todos los entornos de un ambito 
            (lista de entornos).
            - Contenido: Variable de tipo valor con los datos de entrada.
            - Simbolos: Lista con los entornos a revisar. Los ambitos se manejan como un arreglo, con el entorno global en la 
                        cabecera y el entorno local actual en la ultima posicion. 
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        #Se empieza a revisar del local inmediato (ultima posicion) al global (primera posicion)
        for i in range(len(SIMBOLOS)):
            entornoTemp = SIMBOLOS[len(SIMBOLOS) - (1 + i)]

            #Si no existe, revisa el siguiente
            if not entornoTemp.existeSimbolo(CONTENIDO.id):
                continue
            temp = entornoTemp.variables[CONTENIDO.id]

            #Recorrer la lista de accesos hasta encontrar el valor indicado
            for j in range(len(CONTENIDO.accesos)):
                tempAcceso = CONTENIDO.accesos[j]

                #Verificar que no sea null
                if temp.tipo == Tipo.NULL.value:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: Uno de los accesos retorno NULL. \n"
                    mensaje = "Uno de los accesos retorno NULL."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return retorno

                #Buscar el atributo/posicion 
                if temp.clase == Clases.PRIMITIVO.value:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: Una variable primitiva no maneja posiciones o atributos. \n"
                    mensaje = "Una variable primitiva no maneja posiciones o atributos."
                    REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                    return retorno

                elif temp.clase == Clases.VECTOR.value:
                    if tempAcceso.tipo == Accesos.ATRIBUTO.value:
                        retorno = valor()
                        retorno.id = "NULL"
                        retorno.tipo = Tipo.NULL.value
                        retorno.valor = "NULL"
                        retorno.clase = Clases.NULL.value
                        retorno.string = "NULL"
                        
                        REPORTES.salida += "ERROR: Una variable vector no maneja atributos. \n"
                        mensaje = "Una variable vector no maneja atributos."
                        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                        return retorno

                    temp = temp.get(tempAcceso.valor, REPORTES, CONTENIDO.linea, CONTENIDO.columna)

                elif temp.clase == Clases.STRUCT.value:
                    if tempAcceso.tipo == Accesos.POSICION.value:
                        retorno = valor()
                        retorno.id = "NULL"
                        retorno.tipo = Tipo.NULL.value
                        retorno.valor = "NULL"
                        retorno.clase = Clases.NULL.value
                        retorno.string = "NULL"
                        
                        REPORTES.salida += "ERROR: Una variable struct no maneja posiciones. \n"
                        mensaje = "Una variable struct no maneja posiciones."
                        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                        return retorno

                    temp = temp.get(tempAcceso.valor, REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                
                elif temp.clase == Clases.ANY.value:
                    if temp.claseValor == Clases.PRIMITIVO.value:
                        retorno = valor()
                        retorno.id = "NULL"
                        retorno.tipo = Tipo.NULL.value
                        retorno.valor = "NULL"
                        retorno.clase = Clases.NULL.value
                        retorno.string = "NULL"

                        REPORTES.salida += "ERROR: Una variable primitiva no maneja posiciones o atributos. \n"
                        mensaje = "Una variable primitiva no maneja posiciones o atributos. \n"
                        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                        return retorno

                    elif temp.claseValor == Clases.VECTOR.value:
                        if tempAcceso.tipo == Accesos.ATRIBUTO.value:
                            retorno = valor()
                            retorno.id = "NULL"
                            retorno.tipo = Tipo.NULL.value
                            retorno.valor = "NULL"
                            retorno.clase = Clases.NULL.value
                            retorno.string = "NULL"

                            REPORTES.salida += "ERROR: Una variable vector no maneja atributos. \n"
                            mensaje = "Una variable vector no maneja atributos. \n"
                            REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                            return retorno

                        temp = temp.get(tempAcceso.valor, "", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                    
                    elif temp.clase == Clases.STRUCT.value:
                        if tempAcceso.tipo == Accesos.POSICION.value:
                            retorno = valor()
                            retorno.id = "NULL"
                            retorno.tipo = Tipo.NULL.value
                            retorno.valor = "NULL"
                            retorno.clase = Clases.NULL.value
                            retorno.string = "NULL"
                            
                            REPORTES.salida += "ERROR: Una variable struct no maneja posiciones. \n"
                            mensaje = "Una variable struct no maneja posiciones."
                            REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
                            return retorno

                        temp = temp.get("", tempAcceso.valor, REPORTES, CONTENIDO.linea, CONTENIDO.columna)
                    
            if temp.clase == Clases.PRIMITIVO.value:
                return temp.get()
            elif temp.clase == Clases.VECTOR.value:
                return temp.get("", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
            elif temp.clase == Clases.STRUCT.value:
                return temp.get("", REPORTES, CONTENIDO.linea, CONTENIDO.columna)
            elif temp.clase == Clases.ANY.value:
                return temp.get("", "", REPORTES, CONTENIDO.linea, CONTENIDO.columna)

        #Si termina el for y no lo encuentra, es error y retorna Null
        retorno = valor()
        retorno.id = "NULL"
        retorno.tipo = Tipo.NULL.value
        retorno.valor = "NULL"
        retorno.clase = Clases.NULL.value
        retorno.string = "NULL"
        
        REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no existe en ningun entorno. \n"
        mensaje = "La variable " + CONTENIDO.id + " no existe en ningun entorno."
        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
        return retorno

    #================================================== METODOS ==========================================================
    def insertarMetodo(self, ID, PARAMETROS, INSTRUCCIONES, TIPO, CLASE, REPORTES, LINEA, COLUMNA):
        '''
            Añade un nuevo metodo al diccionario de metodos y a la lista del reporte.
            - ID: Nombre del metodo.
            - Parametros: Lista de parametros que pide el metodo (atributos[])
            - Instrucciones: Lista de instrucciones (instruccion[])
            - Tipo: Tipo de valor que debe de retornar la funcion (int, strimg, bool) (String)
            - Clase: Indica si retorna un primitivo, vector, matriz, etc (String)
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        #Verificar que no exista
        if self.existeMetodo(ID):
            REPORTES.salida += "ERROR: El método " + ID + " ya existe. \n"
            mensaje = "El método " + ID + " ya existe. \n"
            REPORTES.añadirError("Semantico", mensaje, LINEA, COLUMNA)
            return -1

        #Añadir el metodo a los reportes y a la lista de metodos
        REPORTES.añadirMetodo(ID, TIPO, LINEA, COLUMNA)
        self.metodos[ID] = metodo(ID, PARAMETROS, INSTRUCCIONES, TIPO, CLASE)

    def getMetodo(self, ID, REPORTES, LINEA, COLUMNA):
        '''
            Retorna una instancia de metodo.
            - ID: Nombre del metodo.
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
            - Linea: Linea de la instruccion. Para el error.
            - Columna: Columna donde esta el error.
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        if self.existeMetodo(ID):
            retorno = self.metodos[ID]
        else:
            REPORTES.salida += "ERROR: El metodo " + ID + " no existe. \n"
            mensaje = "El metodo " + ID + " no existe."
            REPORTES.añadirError("Semantico", mensaje, LINEA, COLUMNA)
            return -1
        
    #================================================== ESTRUCTURA ==========================================================
    def insertarEstructura(self, ID, ATRIBUTOS, REPORTES, LINEA, COLUMNA):
        '''
            Añade un nuevo metodo al diccionario de metodos y a la lista del reporte.
            - ID: Nombre del struct.
            - Atributos: Lista de atributos que construyen el struct (atributos[])
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
            - Linea: Linea de la instruccion. Para el error.
            - Columna: Columna donde esta el error.
        '''
        #Verificar que no exista
        if self.existeEstructura(ID):
            REPORTES.salida += "ERROR: La estructura " + ID + " ya está definida. \n"
            mensaje = "La estructura " + ID + " ya está definida."
            REPORTES.añadirError("Semantico", mensaje, LINEA, COLUMNA)
            return -1

        #Añadir la estructura a la lista de estructuras
        self.estructuras[ID] = estructura(ID, ATRIBUTOS)
            
    #================================================ AUXILIARES  ================================================================
    def existeSimbolo(self, NOMBRE):
        '''
            Retorna true si existe la variable.
            - Nombre: Nombre de la variable.
        '''
        if NOMBRE in self.variables:
            return True
        else:
            return False
    
    def existeMetodo(self, NOMBRE):
        '''
            Retorna true si existe el metodo.
            - Nombre: Nombre del metodo.
        '''
        if NOMBRE in self.metodos:
            return True
        else:
            return False
    
    def existeEstructura(self, NOMBRE):
        '''
            Retorna true si existe la estructura.
            - Nombre: Nombre de la estructura.
        '''
        if NOMBRE in self.estructuras:
            return True
        else:
            return False
    
    def getClase(self, NOMBRE):
        '''
            Retorna si una variable es primitivo, matriz, vector, etc. Si no existe el simbolo, retorna false.
            - Nombre: Nombre de la variable.
        '''
        if NOMBRE in self.variables:
            temp = self.variables[NOMBRE]
            return temp.clase
        else:
            return False
        
    def verificarAtributos(self, ENTRADA, REFERENCIA):
        '''
            Verifica que se cumpla con la estructura del struct. Toma un vector de atributoss (referencia) y lo compara
            con un vector de tipo Simbolo (Primitivo, Struct, Vector) como entrada.
            - Entrada: Tipo Simbolo[]. Valores a comparar.
            - Referencia: Lista de atributos con la estructura del Struct.
        '''
        #Verifcar que venga la misma cantidad de atributos
        if len(ENTRADA) != len(REFERENCIA):
            return False
        
        #Comprobar los atributos
        for i in range(len(ENTRADA)):
            tempEntrada = ENTRADA[i]
            cumple = False

            for j in range(len(REFERENCIA)):
                tempReferencia = REFERENCIA[j]
                #Buscar si coincide nombre. Si no revisar, el siguiente.
                if tempReferencia.id != tempEntrada.id:
                    continue
                
                #Comprobar tipos. SI no pasa se sale.
                if tempEntrada.tipo != tempReferencia.tipo:
                    if tempReferencia.tipo != Tipo.ANY.value:
                        break
                
                #Comprobar clases. Si no pasa se sale.
                if tempEntrada.clase != tempReferencia.clase:
                    if tempReferencia.clase != Clases.ANY.value:
                        break
                
                
                #Si llega hasta el valor se asume que existe y pasa la prueba 
                cumple = True

            #Si no existe o no pasa la prueba, acaba aca
            if not cumple:
                return False
        
        #Al terminar la comprobacion, retorna true
        return True
