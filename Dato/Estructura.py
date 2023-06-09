class atributo:
    '''
        Atributo: Es una clase auxiliar que sirve para describir un valor. Se utliza en los structs y metodos.
        
        Cuando clase es:
        - Primitivo: Valor almacena un string.
        - Struct: Valor almacena un array con instancias de ka clase atributo.
        - Vector: Valor almacena un array con instancias de un tipo o varias 
    '''
    def __init__(self):
        self.id = ""            #Nombre del atributo
        self.tipo = ""          #Tipo de valor que almacena (int, string, bool, etc)
        self.clase = ""         #Indica si el atributo es de una clase primitiva o compuesta(matriz, vector, otro struct, etc)

class estructura:
    '''
        Estructura: La clase estructura sirve como un armazon para almacenar los atributos que debe de tener un struct
        y el orden en el que estos vienen. Sirve nada mas para revisar que al crear un struct se cumpla con esa definicion.
    '''

    def __init__(self, ID, ATRIBUTOS):
        self.id = ID                    #Nombre del struct. Recibe una cadena      
        self.atributos = ATRIBUTOS      #Atributos que conforman la definicion del struct: Recibe variables de la clase atributo. 

