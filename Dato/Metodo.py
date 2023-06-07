class metodo:
    '''
        ALmacena las instrucciones que se ejecutan en un metodo. Ademas, almacena los parametros que recibe, el nombre
        y el tipo de retorno.
        -ID: Nombre del metodo (String)
        -Parametros: Lista de valores que debe de recibir como paraemtros (atributo[])
        -Instrucciones: Lista de instrucciones que se van a ejecutar(intruccion[])
        -Tipo: Tipo de valor que debe de retornar la funcion (int, strimg, bool) (String)
        -Clase: Indica si retorna un primitivo, vector, matriz, etc (String)
    '''

    def __init__(self, ID, PARAMETROS, INSTRUCCIONES, TIPO, CLASE):
        self.id = ID
        self.parametros = PARAMETROS
        self.instrucciones = INSTRUCCIONES
        self.tipo = TIPO
        self.clase = CLASE