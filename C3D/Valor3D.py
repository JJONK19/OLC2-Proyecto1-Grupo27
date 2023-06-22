class valor3D:
    '''
        Maneja los retornos en la ejecucion. Al ir ascendiendo, maneja informacion como las listas de etiquetas
        o los tipos.
        - Valor: Contenido del retorno.
        - Tipo : Tipo del retorno.
        - Clase : Clase del retorno.
        - True Label : Lista de true labels en una operacion
        - False Label : Lista de false labels en una operacion
        - Es temporal : Indica si el retorno tiene como variable un temporal.
        - Label break: Es lo que retorna un break
        - Control: Replica lo que se hace en analisis de tener un numero para indicar que es.
    '''
    def __init__(self, VALOR, TEMP, TIPO, CLASE, ID = "", TIPO_VALOR = "", CLASE_VALOR = "", 
                 CLASE_CONTENIDO = "", HEAP = False, REFERENCIA = False, TRUE_LABEL = [], FALSE_LABEL = []):
        #Informacion de variable
        self.id = ID
        self.valor = VALOR
        self.tipo = TIPO
        self.clase = CLASE
        self.tipoValor = TIPO_VALOR
        self.claseValor = CLASE_VALOR
        self.claseContenido = CLASE_CONTENIDO
        self.estaEnHeap = HEAP
        self.referencia = REFERENCIA
        self.linea = 0                                    #Linea del valor
        self.columna = 0                                  #Columna del valor

        #Retorno de lables e informacion adicional
        self.trueLabel = TRUE_LABEL
        self.falseLabel = FALSE_LABEL
        self.esTemporal = TEMP

        self.control = None
        self.labelBreak = []