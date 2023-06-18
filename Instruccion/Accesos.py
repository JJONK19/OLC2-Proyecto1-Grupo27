from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Dato.Estructura import acceso

class accesos(instruccion):
    '''
        Almacena la informacion para crear un objeto de tipo acceso. Esto va contenido en la llamada a variables.
        - Tipo: Posicion / Atributo
        - Valor: Un numero / Nombre del atributo
    '''

    def __init__(self, ID, VALOR, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.valor = VALOR

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Acceso\" ];\n"
        REPORTES.cont += 1

        #Declarar palabra reservada Let
        nodoAcceso = "NODO" + str(REPORTES.cont)
        if self.id == Accesos.ATRIBUTO.value:
            REPORTES.dot += nodoAcceso + "[ label = \""+ self.valor + "\" ];\n"
            REPORTES.cont += 1
            REPORTES.dot += padre + "->" + nodoAcceso + ";\n"
        else:
            nodoExp = self.valor.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoExp + ";\n"

        return padre
    
    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        #TRABAJAR CON LA EXPRESION Y CREAR EL VALOR
        nuevo = ""
        if self.id == Accesos.ATRIBUTO.value:
            nuevo = acceso(self.id, self.valor)

        elif self.id == Accesos.POSICION.value:
            #Extraer valores
            expresionEvaluar = self.valor.analisis(SIMBOLOS, REPORTES)
            
            #Verificar que no sea nulo
            if expresionEvaluar.tipo == Tipo.NULL.value:
                REPORTES.salida += "ERROR: La posicion de un array no puede ser NULL. \n"
                mensaje = "La posicion de un array no puede ser NULL."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Comprobar que sea primitivo
            if expresionEvaluar.clase != Clases.PRIMITIVO.value:
                REPORTES.salida += "ERROR: La posicion del array debe de ser un primitivo. \n"
                mensaje = "La posicion del array debe de ser un primitivo."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Comprobar que el tipo sea number
            if expresionEvaluar.tipo != Tipo.NUMBER.value:
                REPORTES.salida += "ERROR: La posicion del array debe de ser un numero. \n"
                mensaje = "ERROR: La posicion del array debe de ser un numero."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            nuevo = acceso(self.id, int(expresionEvaluar.valor))
            
        return nuevo
    
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

