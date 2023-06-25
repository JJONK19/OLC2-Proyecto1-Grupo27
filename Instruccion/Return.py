from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from C3D.Valor3D import valor3D
from C3D.Entorno3D import entorno3D

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

        #Si la expresion no es vacia, evaluar el valor y asignarlo al stack
        if self.expresion != None:
            #Obtener la variable de la tabla de simbolos
            nuevo =  valor3D("return", True, "", "")
            nuevo.id = self.id
            nuevo.linea = self.linea
            nuevo.columna = self.columna 

            salida = entorno3D.getSimbolo(nuevo, SIMBOLOS, REPORTES, CODIGO)
            
            #Obtener posicion de la variable
            posicion = entorno3D.getPosicion(nuevo, SIMBOLOS, REPORTES, CODIGO)

            #Evaluar el contenido
            expresion = self.expresion.c3d(SIMBOLOS, REPORTES, CODIGO)

            #Separar por clases
            if salida.clase == Clases.PRIMITIVO.value:
                #Comprobar tipos
                if salida.tipo != expresion.tipo:
                    REPORTES.salida += "ERROR: La variable " + salida.id + " no es de tipo " + expresion.tipo + ". \n"
                    mensaje = "La variable " + salida.id + " no es de tipo " + expresion.tipo + "."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    CODIGO.insertar_Comentario("ERROR: La variable " + salida.id + " no es de tipo " + expresion.tipo + ".")
                    return 
        
                #Comprobar clases
                if salida.clase != expresion.clase:
                    REPORTES.salida += "ERROR: La variable " + salida.id + " no es de clase " + expresion.clase + ". \n"
                    mensaje = "La variable " + salida.id + " no es de clase " + expresion.clase + "."
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    CODIGO.insertar_Comentario("ERROR: La variable " + salida.id + " no es de tipo " + expresion.tipo + ".")
                    return 
                
                tempStack = CODIGO.nuevoTemporal()

                #Guardar en un temporal del valor del stack
                CODIGO.insertar_Expresion(tempStack, "P", "+", str(posicion))
                CODIGO.insertar_SetearStack(tempStack, expresion.valor)
            
            elif salida.clase == Clases.VECTOR.value:
                pass

            elif salida.clase == Clases.STRUCT.value:
                pass

            elif salida.clase == Clases.ANY.value:
                #Asignar en el stack
                tempStack = CODIGO.nuevoTemporal()
                CODIGO.insertar_Expresion(tempStack, "P", "+", str(posicion))
                CODIGO.insertar_SetearStack(tempStack, expresion.valor)

                #Cambiar el tipo del any
                salida.claseValor = expresion.clase
                salida.tipoValor = expresion.tipo
                salida.claseContenido = expresion.claseContenido

        CODIGO.insertar_RegresarStack(local.contadorReturn)
        CODIGO.insertar_Goto(local.labelReturn)
