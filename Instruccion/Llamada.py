from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Entorno import entorno
from Ejecucion.Valor import valor

class llamada(instruccion):
    '''
        Obtiene un valor de la tabla de simbolos. Guarda una lista de accesos y el ID de la variable
        - ID: Nombre de la variable
        - ListaAccesos: Lista de objetos de tipo acceso. 
    '''

    def __init__(self, ID, LISTA_ACCESOS, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.listaAccesos = LISTA_ACCESOS

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Llamada\" ];\n"
        REPORTES.cont += 1

        #Declarar ID
        nodoID = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoID + "[ label = \""+ self.id + "\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoID + ";\n"

        #Declarar accesos
        for i in self.listaAccesos:
            nodoAcceso = i.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoAcceso + ";\n"

        return padre
    
    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        access = []
        #Crear la lista de accesos
        for i in self.listaAccesos:
            access.append(i.analisis(SIMBOLOS, REPORTES))

        #Crear el objeto valor y mandarlo a llamar. Si falla, deberia de retornar un Null.
        nuevo = valor()
        nuevo.id = self.id
        nuevo.accesos = access
        nuevo.linea = self.linea
        nuevo.columna = self.columna

        #Llamar al metodo de busqueda estatico
        salida = entorno.getSimbolo(nuevo, SIMBOLOS, REPORTES) 
        return salida
    
    def c3d(self):
        pass

