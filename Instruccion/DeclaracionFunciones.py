from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from C3D.Valor3D import valor3D

class declaracionFuncion(instruccion):
    '''
        Define como viene una funcion.
        - ID: Nombre de la funcion
        - ListaAtributos: Lista de atributos de la funcion. Se reusa la clase atributo de los structs. 
        - Instrucciones: Lista de instrucciones de la funcion. 
        - TipoInstruccion: Indica que es una instruccion de declaracion de funcion
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    def __init__(self, ID, LISTA_ATRIBUTOS, RETURN, CLASE_RETURN, INSTRUCCIONES, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.listaAtributos = LISTA_ATRIBUTOS
        self.instrucciones = INSTRUCCIONES
        self.tipo = RETURN
        self.claseReturn = CLASE_RETURN
        self.tipoInstruccion = Instrucciones.DECLARACION_FUNCION.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Definicion Funcion\" ];\n"
        REPORTES.cont += 1

        #Declarar palabra reservada function
        nodoFunction = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunction + "[ label = \"function\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunction + ";\n"

        nodoID = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoID + "[ label = \""+self.id+"\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoID + ";\n"

        #Nodo complementario :
        nodoLlA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlA + "[ label = \"{\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlA + ";\n"

        #Declarar atributos
        for i in self.listaAtributos:
            nodoAtributo = i.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoAtributo + ";\n"

        #Declarar instrucciones
        nodoFunctionB = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunctionB + "[ label = \") {\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunctionB + ";\n"

        #Declarar return
        #Declarar instrucciones
        nodoFunctionB = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunctionB + "[ label = \": " + self.tipo + "\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunctionB + ";\n"

        #Declarar instrucciones
        nodoFunctionB = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunctionB + "[ label = \"{\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunctionB + ";\n"

        #Declarar instrucciones
        for instruccion in self.instrucciones:
            nodoInstruccion = instruccion.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoInstruccion + ";\n"
        
        #Declarar while
        nodoFunctionC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoFunctionC + "[ label = \"} ;\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoFunctionC + ";\n"
        return padre    

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        atributos = []
        #Crear la lista de atributos
        for i in self.listaAtributos:
            atributos.append(i.analisis(SIMBOLOS, REPORTES))
        
        #Enviar al entorno global la estructura
        entornoGlobal = SIMBOLOS[0]
        salida = entornoGlobal.insertarMetodo(self.id, atributos, self.tipo, self.claseReturn, self.instrucciones,  REPORTES, self.linea, self.columna)
        
        if salida == -1:
            return -1
        else:
            return None
 
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        #Se van a reutilizar la ejecucion de los atributos para tener un comprobante de los tipos de la funcion
        SIMBOLOS = []
        atributos = []
        #Crear la lista de atributos
        for i in self.listaAtributos:
            atributos.append(i.analisis(SIMBOLOS, REPORTES))

        #Crear el metodo en el generador
        salida = CODIGO.insertarMetodo(self.id, atributos, self.tipo, self.claseReturn, self.instrucciones,  REPORTES, self.linea, self.columna)
        
        if salida == -1:
            return 
        
        metodo = CODIGO.getMetodo(self.id, REPORTES,self.linea, self.columna)

        #Crear los atributos en la tabla de simbolos
        local = SIMBOLOS[-1]

        #-- Declarar return en la tabla 
        nuevo =  valor3D("", True, self.tipo, self.claseReturn, ID="return")
        nuevo.linea = 0
        nuevo.columna = 0

        for atributo in metodo.parametros:
            nuevo = ""
            if atributo.tipo == Tipo.ANY.value:
                nuevo =  valor3D("", True, atributo.tipo, atributo.clase, TIPO_VALOR=Tipo.NUMBER,
                                CLASE_VALOR=Clases.PRIMITIVO.value)
            else:
                nuevo =  valor3D("", True, atributo.tipo, atributo.clase)

            
            #Añadir el id de la variable a valor
            nuevo.id = atributo.id
            nuevo.linea = 0
            nuevo.columna = 0

            salida = local.insertarSimbolo(nuevo, REPORTES, CODIGO)

        
        
                




 