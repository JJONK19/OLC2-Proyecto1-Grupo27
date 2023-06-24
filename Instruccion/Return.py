from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
 
class sentenciaReturn(instruccion):
    '''
        Recibe o no una instruccion. Retorna un objeto de tipo valor con el retorno setteado en true. 
        Si el retorno es un Null o no viene, siempre se retorna un objeto con un Null. 
        - Expresion: Instruccion expresion con el valor a retornar
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.tipoInstruccion = Instrucciones.RETURN.value
        self.expresion = EXPRESION

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Return\" ];\n"
        REPORTES.cont += 1

        #Declarar operador
        nodoReturn = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoReturn + "[ label = \"return\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoReturn + ";\n"

        #Declarar operacion
        if self.expresion != None:
            nodoExpresion = self.expresion.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoExpresion + ";\n"
        return padre
    
    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Verificar si viene la expresion. Operar o retornar null en caso no venga
        if self.expresion == None:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            retorno.regreso = True
            return  retorno
        
        else:
            retorno = self.expresion.analisis(SIMBOLOS, REPORTES)
            retorno.regreso = True
            return retorno
            
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        # Si labelReturn es igual a "" significa que no esta en un ciclo
        local = SIMBOLOS[-1]
        if local.labelReturn == "":
            CODIGO.insertar_Comentario("ERROR: Se encontró un return fuera de una función.")
            return

        CODIGO.insertar_Comentario("////////// RETURN //////////")
        CODIGO.insertar_RegresarStack(local.contadorReturn)
        CODIGO.insertar_Goto(local.labelReturn)
