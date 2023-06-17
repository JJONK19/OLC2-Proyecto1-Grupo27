from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Entorno import entorno
from Ejecucion.Valor import valor

class asignacion(instruccion):
    '''
        Asigna nuevo contenido a un valor de la tabla de simbolos. Guarda una lista de accesos y el ID de la variable
        - ID: Nombre de la variable
        - ListaAccesos: Lista de objetos de tipo acceso.
        - Expresion: Valor nuevo a asignar. 
    '''

    def __init__(self, ID, LISTA_ACCESOS, EXPRESION, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.listaAccesos = LISTA_ACCESOS
        self.expresion = EXPRESION

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Asignacion\" ];\n"
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

        nodoIgual = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoIgual + "[ label = \"=\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoIgual + ";\n"

        nodoExp = self.expresion.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoExp + ";\n"

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

        #Extraer valores
        valorEnviado = self.expresion.analisis(SIMBOLOS, REPORTES)
        
        #Asignar ID y valores al valor. Si falla, deberia de retornar -1.
        valorEnviado.id = self.id
        valorEnviado.accesos = access
        valorEnviado.linea = self.linea
        valorEnviado.columna = self.columna

        #Llamar al metodo de busqueda estatico
        salida = entorno.asignarSimbolo(valorEnviado, SIMBOLOS, REPORTES) 

        if salida == -1:
            return -1
        else:
            return None
        
        return salida
    
    def c3d(self):
        pass



