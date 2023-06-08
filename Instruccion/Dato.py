from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
 
class dato(instruccion):
    '''
        Almacena los datos para crear un valor de tipo primitivo (string, bool, number).
        Siempre retorna un primitivo al ejecutarse.
        - Valor: Contiene el valor (5, true, false, etc). Siempre es un string.
        - Tipo: Contiene el tipo del valor (number, string, bool)
        - TipoInstruccion: Indica que es una instruccion de tipo operacion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, VALOR, TIPO, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.valor = VALOR
        self.tipo = TIPO
        self.clase = Clases.PRIMITIVO.value
        self.tipoInstruccion = Instrucciones.DATO.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Valor\" ];\n"
        REPORTES.cont += 1

        #Declarar los nodos hijos
        nodoValor = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoValor + "[ label = \"" +  self.valor + "\" ];\n"
        REPORTES.cont += 1

        #Conectar con el padre
        REPORTES.dot += padre + "->" + nodoValor + ";\n"
        return padre

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Armar el objeto de tipo Valor y retornarlo
        retorno = valor()
        retorno.valor = self.valor
        retorno.tipo = self.tipo
        retorno.clase = self.clase
        retorno.string = self.valor
        return retorno

    def c3d(self):
        pass


