from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from C3D.Valor3D import valor3D
 
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
        retorno.valorClase = retorno.clase
        retorno.valorTipo = retorno.tipo
        return retorno

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
            - Codigo: Generador del C3D 
        '''
        #Crear el temporal del retorno
        temporal = CODIGO.nuevoTemporal()
    
        #Clasificar por tipo
        if self.tipo == Tipo.NUMBER.value:
            #Asignar el numero al temporal
            CODIGO.insertar_Asignacion(temporal, self.valor)
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        elif self.tipo == Tipo.STRING.value:
            #Guardar la posicion del heap en un temporal
            CODIGO.insertar_Asignacion(temporal, "H")

            #Recorrer la cadena y guardar en el heap
            for caracter in str(self.valor):
                CODIGO.insertar_SetearHeap('H', ord(caracter))   
                CODIGO.insertar_MoverHeap()                

            #Guardar el fin de la cadena y mover el heap a una posicion vacia
            CODIGO.insertar_SetearHeap('H', '-1')            
            CODIGO.insertar_MoverHeap()
            return valor3D(temporal, True, Tipo.STRING.value, Clases.PRIMITIVO.value, HEAP=True)
        
        elif self.tipo == Tipo.BOOLEAN.value:
            nuevoLabel = CODIGO.nuevoLabel()
            if self.valor == "true":
                CODIGO.insertar_Asignacion(temporal, "1")
            else:
                CODIGO.insertar_Asignacion(temporal, "0")
            CODIGO.insertar_Goto(nuevoLabel)
            return valor3D(temporal, True, Tipo.BOOLEAN.value, Clases.PRIMITIVO.value, FALSE_LABEL=[nuevoLabel])
        