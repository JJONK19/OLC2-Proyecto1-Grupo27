class simbolo:
    '''
        Sirve como padre para heredar a los distintos tipos de datos que pueden ser encontrados en el lenguaje.
        - ID: Nombre de la variable (String)
        - Tipo: Tipado de la variable (string, int, bool, etc) (String).
        - Clase: Si el dato es primitivo, struct, matriz, clase, etc (String).
    '''

    def __init__(self, ID, TIPO, CLASE):
        self.id = ID           
        self.tipo = TIPO        
        self.clase = CLASE      
