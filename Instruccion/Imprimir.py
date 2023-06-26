from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
 
class imprimir(instruccion):
    '''
        Añade texto a la variable "salida" de los reportes.
        Siempre retorna un primitivo al ejecutarse.
        - Expresion: Contiene una lista de instrucciones de tipo expresion
        - TipoInstruccion: Indica que es una instruccion de tipo print
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.expresion = EXPRESION
        self.tipoInstruccion = Instrucciones.PRINT.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[color = \"brown\", style =\"radial\", fillcolor = \"gold:brown\", gradientangle = \"315\", label = \"Impresion\" ];\n"
        REPORTES.cont += 1
    
        #Declarar funcion
        nodoFuncionA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncionA + "[ label = \"Console.log (\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFuncionA + ";\n"

        #Declarar operaciones
        for i in self.expresion:
            nodoExpresion = i.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoExpresion + ";\n"

        #Declarar cierre de funcion
        nodoFuncionC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFuncionC + "[ label = \")\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFuncionC + ";\n"
        return padre    

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Obtener el valor de la expresion
        for i in self.expresion:
            expresion = i.analisis(SIMBOLOS, REPORTES)

            #Añadirlo al string de la consola (Salida)
            REPORTES.salida += expresion.string + " "
   
        REPORTES.salida += "\n"
        

        #Retornar none porque la instruccion no retorna nada
        return None     

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        #Crear el temporal del retorno
        for i in self.expresion:
            expresion = i.c3d(SIMBOLOS, REPORTES, CODIGO)
        
            #Clasificar por tipo
            if expresion.tipo == Tipo.NUMBER.value and expresion.clase == Clases.PRIMITIVO.value:
                #Comentario
                CODIGO.insertar_Comentario("////////// IMPRIMIR NUMBER //////////")
                #Asignar el numero al temporal
                CODIGO.insertar_Print("f", expresion.valor)
                CODIGO.insertar_Print("c", 32, "int")       #Espacio en blanco
            
            elif expresion.tipo == Tipo.STRING.value and expresion.clase == Clases.PRIMITIVO.value:
                #Comentario
                CODIGO.insertar_Comentario("////////// IMPRIMIR STRING //////////")
                
                #Expresion retorna la posicion en el heap en un temporal
                #Crear temporal contenedor, label del ciclo y salida
                labelCiclo = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                tempComparar = CODIGO.nuevoTemporal()

                #Comenzar ciclo 
                CODIGO.insertar_Label(labelCiclo)
                CODIGO.insertar_ObtenerHeap(tempComparar, expresion.valor)
                CODIGO.insertar_If(tempComparar, "==", "-1", labelSalida)
                CODIGO.insertar_Print("c", tempComparar, "int")
                CODIGO.insertar_Expresion(expresion.valor, expresion.valor, "+", "1")
                CODIGO.insertar_Goto(labelCiclo)

                CODIGO.insertar_Label(labelSalida)
                CODIGO.insertar_Print("c", 32, "int")       #Espacio en blanco
                
            elif expresion.tipo == Tipo.BOOLEAN.value and expresion.clase == Clases.PRIMITIVO.value:
                #Comentario
                CODIGO.insertar_Comentario("////////// IMPRIMIR BOOLEAN //////////")

                #Labels del if
                labelTrue = CODIGO.nuevoLabel()
                labelFalse = CODIGO.nuevoLabel()
                labelSalida = CODIGO.nuevoLabel()
                
                #If
                CODIGO.insertar_If(expresion.valor, "==", "1", labelTrue)
                CODIGO.insertar_Goto(labelFalse)
                
                #Imprimir true
                CODIGO.insertar_Label(labelTrue)
                CODIGO.insertar_Print("c", 116, "int")
                CODIGO.insertar_Print("c", 114, "int")
                CODIGO.insertar_Print("c", 117, "int")
                CODIGO.insertar_Print("c", 101, "int")
                CODIGO.insertar_Print("c", 32, "int")       #Espacio en blanco
                CODIGO.insertar_Goto(labelSalida)
                
                #Imprimir false
                CODIGO.insertar_Label(labelFalse)
                CODIGO.insertar_Print("c", 102, "int")
                CODIGO.insertar_Print("c", 97, "int")
                CODIGO.insertar_Print("c", 108, "int")
                CODIGO.insertar_Print("c", 115, "int")
                CODIGO.insertar_Print("c", 101, "int")
                CODIGO.insertar_Print("c", 32, "int")      #Espacio en blanco
                
                #Salida
                CODIGO.insertar_Label(labelSalida)
                
        CODIGO.insertar_Print("c", 10, "int")       #Salto de linea despues del print
                
                
        

