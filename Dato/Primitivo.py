from Dato.Simbolo import simbolo
from Ejecucion.Valor import valor
from Tipos.Tipos import *

class primitivo(simbolo):
    '''
        Se usa para representar los datos primitivos de una clase (int, string, bool, etc).
        - ID: Nombre de la variable (String)
        - Tipo: Tipado de la variable (string, int, bool, etc) (String).
        - Clase: Primitivo (String).
        - Valor: Contenido de la variable 
    '''
    def __init__(self, ID, TIPO, CLASE, VALOR):
        super().__init__(ID, TIPO, CLASE) 
        self.valor = VALOR
    
    def set(self, NUEVO):
        '''
            Asigna un nuevo valor a la variable.
            - Nuevo: Es un string con el contenido de la variable
        '''
        self.valor = NUEVO

    def get(self):
        '''
            Retorna un objeto de tipo Valor, con el valor de la variable como string.
        '''
        retorno = valor()
        retorno.id = self.id
        retorno.tipo = self.tipo
        retorno.valor = self.valor
        retorno.clase = self.clase
        retorno.string = self.valor
        retorno.valorClase = retorno.clase
        retorno.valorTipo = retorno.tipo
        return retorno
    
