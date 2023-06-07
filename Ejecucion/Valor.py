class valor:
    '''
        Valor se usa como un return con la informacion generada por una instruccion (una expresion, un return, etc).
        Se carga con los atributos de todos las clases de valores para que sirva como una clase universal que pueda
        usarse en todo el proyecto, diferenciandose por el atributo clase.

        Cuando clase es:
        - Primitivo: Valor almacena un string.
        - Struct: Valor almacena un array con instancias de la clase simbolo (Primitivo, Struct, Vector).
        - Vector: Valor almacena un array con instancias de Primitivo, Struct o Vector. 
    '''
    def __init__(self):
        self.id = ""                                      #Nombre de la variable
        self.tipo = ""                                    #Int, float, string. etc.
        self.clase = ""                                   #Indica si es primitivo, matriz, etc 
        self.valor = ""                                   #Almacena el contenido. Se usa junto a Clase.
        self.linea = 0                                    #Linea del valor
        self.columna = 0                                  #Columna del valor

        #AUXILIARES 
        self.accesos = []                                 #Arreglo de tipo acceso[]. Se usa para acceder a variables.
        self.claseContenido = ""                          #Usado en vectores. Indica que puede contener.
        self.string = ""                                  #Almacena el valor como string

class acceso:
    '''
        Acceso es una clase con el nombre del atributo o la posicion del vector a la que se quiere acceder. Se utiliza
        para acceder a un vector o un struct sin importar si es para modificarlo o extraer un valor. 
    '''
    def __init__(self, TIPO, VALOR):
        self.tipo = TIPO                                   #Puede ser "atributo" o "posicion"
        self.valor = VALOR                                 #Contiene la posicion de acceso o el nombre del atributo