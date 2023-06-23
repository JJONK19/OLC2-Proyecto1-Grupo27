from C3D.Simbolo3D import simbolo3D
class entorno3D:
    '''
        Tabla de simbolos para la traduccion del codigo. Guarda objetos de simbolo 3D y tiene metodos para acceder a
        ellos.
    '''
    def __init__(self, NOMBRE):
        self.nombre_entorno = NOMBRE        #Nombre del entorno. Usado en el reporte.
        self.variables = {}                 #Almacena variables 
        self.contador = 0                   #Sirve para crear nombres unicos para los entornos 
        self.tamaño = 0                     #Numero de variables declaradas en el entorno

        #Labels de Control
        self.labelBreak = ""
        self.labelContinue = ""
        self.labelReturn = ""

        #Contadores de retorno 
        self.contadorBreak = 0
        self.contadorContinue = 0
        self.contadorReturn = 0

    #========================================== VARIABLES ===============================================================
    def insertarSimbolo(self, CONTENIDO, REPORTES, CODIGO):
        '''
            Ingresa un simbolo en el diccionario del entorno. La variable contenido contiene toda la informacion
            relevante para crear el simbolo.
            Se inserta en el entorno local (el ultimo de la lista de entornos).  
            - CONTENIDO: Variable de la clase Valor3D.
            - REPORTES: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        #Verificar que no exista
        if self.existeSimbolo(CONTENIDO.id):
            CODIGO.insertar_Comentario("ERROR: La variable " + CONTENIDO.id + " ya existe en este entorno.")
            REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " ya existe en este entorno. \n"
            mensaje = "La variable " + CONTENIDO.id + " ya existe en este entorno."
            REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
            return -1
        
        #Añadir la variable en el entorno y el reporte
        self.variables[CONTENIDO.id] = simbolo3D(CONTENIDO.id, CONTENIDO.tipo, CONTENIDO.clase, self.tamaño, CONTENIDO.estaEnHeap,
                                                 TIPO_VALOR= CONTENIDO.tipoValor, CLASE_VALOR= CONTENIDO.claseValor, 
                                                 CLASE_CONTENIDO= CONTENIDO.claseContenido, REFERENCIA = CONTENIDO.referencia)
        REPORTES.añadirSimbolo(CONTENIDO.id, CONTENIDO.tipo, "", self.nombre_entorno, CONTENIDO.linea, CONTENIDO.columna)
        self.tamaño += 1
        return self.variables[CONTENIDO.id]
    
    
    @staticmethod
    def getSimbolo(CONTENIDO, SIMBOLOS, REPORTES, CODIGO):
        '''
            Retorna una instancia de tipo Simbolo3D con los datos de la variable. Esta se busca en todos los entornos de un ambito 
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
            return temp
            
        #Si termina el for y no lo encuentra, es error y retorna Null
        CODIGO.insertar_Comentario("ERROR: La variable " + CONTENIDO.id + " no existe en ningun entorno.")
        REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no existe en ningun entorno. \n"
        mensaje = "La variable " + CONTENIDO.id + " no existe en ningun entorno."
        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
        return -1
    
    @staticmethod
    def getPosicion(CONTENIDO, SIMBOLOS, REPORTES, CODIGO):
        '''
            Retorna el numero de posiciones que debe moverse el stack para acceder a una variable.
            - Contenido: Variable de tipo valor con los datos de entrada.
            - Simbolos: Lista con los entornos a revisar. Los ambitos se manejan como un arreglo, con el entorno global en la 
                        cabecera y el entorno local actual en la ultima posicion. 
            - Reportes: Variable con las listas para los reportes de la ejecucion y la consola
        '''
        #Se empieza a revisar del local inmediato (ultima posicion) al global (primera posicion)
        retroceso = 0
        for i in range(len(SIMBOLOS)):
            entornoTemp = SIMBOLOS[len(SIMBOLOS) - (1 + i)]

            #Si no existe, revisa el siguiente. Suma al retroceso el tamaño del entorno.
            if not entornoTemp.existeSimbolo(CONTENIDO.id):
                #Extraer el entorno anterior de la lista
                if (len(SIMBOLOS) - (2 + i)) < -1:
                    break

                entornoAnterior = SIMBOLOS[len(SIMBOLOS) - (2 + i)]
                retroceso += entornoAnterior.tamaño
                continue
            temp = entornoTemp.variables[CONTENIDO.id]
            posicionLocal = temp.posicionStack
            posicion = posicionLocal - retroceso
            return posicion
            
        #Si termina el for y no lo encuentra, es error y retorna Null
        CODIGO.insertar_Comentario("ERROR: La variable " + CONTENIDO.id + " no existe en ningun entorno.")
        REPORTES.salida += "ERROR: La variable " + CONTENIDO.id + " no existe en ningun entorno. \n"
        mensaje = "La variable " + CONTENIDO.id + " no existe en ningun entorno."
        REPORTES.añadirError("Semantico", mensaje, CONTENIDO.linea, CONTENIDO.columna)
        return -1
    
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

