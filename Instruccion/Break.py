from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from C3D.Valor3D import valor3D
 
class sentenciaBreak(instruccion):
    '''
        No recibe valores. Solo retorna 1 el cual en ejecucion se interpreta como un break.
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.tipoInstruccion = Instrucciones.BREAK.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Break\" ];\n"
        REPORTES.cont += 1

        return padre

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Cuando una instruccion retorna 1, se interpreta como un break
        return 1
    
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        labelBreak = CODIGO.nuevoLabel()
        CODIGO.insertar_Label(labelBreak)

        retorno = valor3D()
        retorno.labelBreak.append(labelBreak)
        retorno.control = 1
        return retorno