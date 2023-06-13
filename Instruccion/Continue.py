from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
 
class sentenciaContinue(instruccion):
    '''
        No recibe valores. Solo retorna 0 el cual en ejecucion se interpreta como un continue.
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.tipoInstruccion = Instrucciones.CONTINUE.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Continue\" ];\n"
        REPORTES.cont += 1

        return padre

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Cuando una instruccion retorna 0, se interpreta como un continue
        return 0
    
    def c3d(self):
        pass