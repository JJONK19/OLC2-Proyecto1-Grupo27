class metodo:
    '''
        ALmacena las instrucciones que se ejecutan en un metodo. Ademas, almacena los parametros que recibe, el nombre
        y el tipo de retorno.
        -ID: Nombre del metodo (String)
        -Parametros: Lista de valores que debe de recibir como paraemtros (atributo[])
        -Instrucciones: Lista de instrucciones que se van a ejecutar(intruccion[])
    '''

    def __init__(self, ID, PARAMETROS, INSTRUCCIONES):
        self.id = ID
        self.parametros = PARAMETROS
        self.instrucciones = INSTRUCCIONES