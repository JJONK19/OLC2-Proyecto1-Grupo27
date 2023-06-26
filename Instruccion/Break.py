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
        REPORTES.dot += padre + "[ color= \"brown\", style =\"radial\", fillcolor = \"gold:brown\", gradientangle = \"315\" , label = \"Break\" ];\n"
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

        # Si labelBreak es igual a "" significa que no esta en un ciclo
        local = SIMBOLOS[-1]
        if local.labelBreak == "":
            CODIGO.insertar_Comentario("ERROR: Se encontró un break fuera de ciclo.")
            return

        CODIGO.insertar_Comentario("////////// BREAK //////////")
        CODIGO.insertar_RegresarStack(local.contadorBreak)
        CODIGO.insertar_Goto(local.labelBreak)