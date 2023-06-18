from Reporte.Reporte import reportes
from Ejecucion.Entorno import entorno
from C3D.Codigo import codigo
from C3D.Entorno3D import entorno3D
from C3D.Valor3D import valor3D
from Tipos.Tipos import Tipo

class AST:
    '''
        La clase AST va a servir como un almacen para la información que se vaya recolectado de la información.
        Se utiliza el patrón Singleton para que exista una sola instacia en la ejecución.
    '''
    #Instancia
    ast = None

    def __new__(cls):
        if not cls.ast:
            cls.ast = super().__new__(cls)
            cls.ast._iniciar()
        else:
            cls.ast._iniciar()
        return cls.ast

    def _iniciar(self):
        '''
            Reinicia cada una de las variables de la instancia.
        '''
        self.reporte = reportes()   #Para los reportes de la interfaz
        self.instrucciones = []      #Lista de Instrucciones
        self.codigo = codigo()
       
    def añadirError(self, TIPO, DESCRIPCION, LINEA, COLUMNA):
        '''
            Añade un nuevo error al reporte
        '''
        self.reporte.añadirError(TIPO, DESCRIPCION, LINEA, COLUMNA)

    def getConsola(self):
        '''
            Regresa el contenido de la consola
        '''
        return self.reporte.salida
    
    def getSimbolos(self):
        '''
            Regresa la lista de simbolos
        '''
        return self.reporte.simbolos
    
    def getErrores(self):
        '''
            Regresa la lista de errores
        '''
        return self.reporte.errores

    def getMetodos(self):
        '''
            Regresa la lista de metodos
        '''
        return self.reporte.metodos
    
    def getDot(self):
        '''
            Regresa el dot del arbol
        '''
        return self.reporte.dot
    
    def getC3D(self):
        '''
            Regresa el codigo del objeto codigo
        '''
        pass

    def Grafo (self):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el codigo de graphviz.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        self.reporte.dot = "digraph G{ rankdir = TB; node[shape = oval];\n"

        #Añadir el padre
        padre = "NODO" + str(self.reporte.cont)
        self.reporte.dot += padre + "[ label = \"Instrucciones\" ];\n"
        self.reporte.cont += 1

        for instruccion in self.instrucciones:
            #Obtener el nombre del hijo (recursivo)
            hijo = instruccion.grafo(self.reporte)

            #Conectar ek padre con el hijo
            self.reporte.dot += padre + "->" + hijo + ";\n"
        self.reporte.dot += "}"
        return self.reporte.dot

    def Ejecucion (self):
        '''
            Se llama el metodo de ejecución y se le manda el arreglo de instrucciones. Este llena las variables 
            con los resulatdos de la ejecución. 
        '''
        #Limpiar reportes
        self.reporte.limpiar()
        
        #Se crea la lista de entornos y se añade el entorno global
        entornos = []
        entornos.append(entorno("Global"))  

        #Se recorre y ejecutan las instrucciones
        for instruccion in self.instrucciones:
            retorno = instruccion.analisis(entornos, self.reporte)

            if retorno == None:             #Instruccion sin return. Se ignora.
                pass
            elif retorno == 1:              #Break
                self.reporte.salida += "ERROR: No se puede usar break fuera de un ciclo. \n"
                mensaje = "No se puede usar break fuera de un ciclo."
                self.reporte.añadirError("Semantico", mensaje, instruccion.linea, instruccion.columna)
                
            elif retorno == 0:              #Continue
                self.reporte.salida += "ERROR: No se puede usar continue fuera de un ciclo. \n"
                mensaje = "No se puede usar continue fuera de un ciclo."
                self.reporte.añadirError("Semantico", mensaje, instruccion.linea, instruccion.columna)
            
            elif retorno == -1:             #Error
                self.reporte.salida += "ERROR: La ejecucion acabo por un error en la linea " + str(instruccion.linea) + ". \n"
               
            else:  
                #Si viene un objeto con regreso = true, es porque se llamo un return en el entorno
                if retorno.regreso:         #Una funcion/metodo retorna el objeto en false para evtar conflictos
                    self.reporte.salida += "ERROR: No se puede usar return fuera de una funcion. \n"
                    mensaje = "No se puede usar return fuera de una funcion."
                    self.reporte.añadirError("Semantico", mensaje, instruccion.linea, instruccion.columna)
                    

    def C3D (self):
        '''
            Recibe las instrucciones y retorna un string con el C3D
        '''
        #Limpiar reportes
        self.reporte.limpiar()
        self.codigo.limpiar()
        
        #Se crea la lista de entornos y se añade el entorno global
        entornos = []
        entornos.append(entorno3D("Global"))  

        #Se recorre y ejecutan las instrucciones
        for instruccion in self.instrucciones:
            retorno = instruccion.c3d(entornos, self.reporte, self.codigo)

            #Verificar retornos
            if isinstance(retorno, valor3D):

                #Si es boolean se insertan las de salida
                if retorno.tipo == Tipo.BOOLEAN.value:
                    #Declarar etiquetas
                    for etiqueta in retorno.trueLabel:
                        self.codigo.insertar_Label(etiqueta)

                    for etiqueta in retorno.falseLabel:
                        self.codigo.insertar_Label(etiqueta)

        return self.codigo.generarCodigo()


