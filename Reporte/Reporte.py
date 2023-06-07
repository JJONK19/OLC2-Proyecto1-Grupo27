class Error:
    '''
        Se almacena en la variable errores de la clase Reportes. Se utiliza para los reportes.
        - Tipo: Indica si es de sintaxis, semantico o lexico.
        - Descripcion: Caracter o motivo que generó el error.
        - Linea. Linea del archivo de entrada que contiene el error.
        - Columna: Posicion en la linea donde se encontro el error,
    '''
    def __init__(self, TIPO, DESCRIPCION, LINEA, COLUMNA):
        self.tipo = TIPO
        self.descripcion = DESCRIPCION
        self.linea = LINEA
        self.columna = COLUMNA

class rSimbolo:
    '''
        Se almacena en la variable simbolos de la clase Reportes. Se utiliza para los reportes.
        - ID: Nombre de la variable.
        - Tipo: Tipado de la variable (int, string, etc).
        - Valor: Valor que contiene la variable.
        - Entorno: Entorno donde fue declarada la variable-
        - Linea. Linea del archivo de entrada que contiene el error.
        - Columna: Posicion en la linea donde se encontro el error,
    '''
    def __init__(self, ID, TIPO, VALOR, ENTORNO, LINEA, COLUMNA):
        self.id = ID
        self.tipo = TIPO
        self.valor = VALOR
        self.entorno = ENTORNO
        self.linea = LINEA
        self.columna = COLUMNA


class rMetodo:
    '''
        Se almacena en la variable simbolos de la clase Reportes. Se utiliza para los reportes.
        - ID: Nombre del metodo.
        - Tipo: Retorno del metodo (int, string, etc).
        - Linea. Linea del archivo de entrada que contiene el error.
        - Columna: Posicion en la linea donde se encontro el error,
    '''
    def __init__(self, ID, TIPO, LINEA, COLUMNA):
        self.id = ID
        self.tipo = TIPO
        self.linea = LINEA
        self.columna = COLUMNA

class reportes:
    '''
        Contiene las listas de errores, simbolos y metodos para los reportes. Se usa en la clase AST.
        Contiene tambien un string para mostrar en consola.
    '''
    def __init__(self):
        self.errores = []            #Lista de Errores
        self.simbolos = {}           #Lista de Simbolos
        self.metodos = []            #Lista de Metodos
        self.salida = ""             #Cadena con la informacion de la consola
        self.dot = ""                #Contiene el codigo del dot

        #Auxiliares
        self.cont = 0                #Contador de Nodos. Usada en el grafo.

    def limpiar(self):
        '''
            Reinicia las listas de la instancia
        '''
        self.errores = []            #Lista de Errores
        self.simbolos = {}           #Lista de Simbolos
        self.metodos = []            #Lista de Metodos
        self.salida = ""             #Cadena con la informacion de la consola
        self.dot = ""                #Contiene el codigo del dot

        #Auxiliares
        self.cont = 0                #Contador de Nodos. Usada en el grafo.

    
    def añadirSimbolo(self, ID, TIPO, VALOR, ENTORNO, LINEA, COLUMNA):
        '''
            Añade una nueva variable al diccionario de simbolos. Se maneja una tupla con el nombre
            de la variable y el entorno.
        '''
        self.simbolos[(ID, ENTORNO)] = rSimbolo(ID, TIPO, VALOR, ENTORNO, LINEA, COLUMNA)
    
    def añadirMetodo(self, ID, TIPO, LINEA, COLUMNA):
        '''
            Añade una nueva variable a la lista de metodos
        '''
        self.metodos.append(rMetodo(ID, TIPO, LINEA, COLUMNA))
    
    def añadirError(self, TIPO, DESCRIPCION, LINEA, COLUMNA):
        '''
            Añade una nueva variable a la lista de errores
        '''
        self.errores.append(Error(TIPO, DESCRIPCION, LINEA, COLUMNA))
    
    def actualizar(self, ID, ENTORNO, VALOR):
        '''
            Actualiza las variables del reporte de simbolos
        '''
        self.simbolos[(ID, ENTORNO)] = VALOR
    