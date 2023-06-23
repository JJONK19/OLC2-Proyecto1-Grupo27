from C3D.Entorno3D import entorno3D
from C3D.Valor3D import valor3D
from Tipos.Tipos import *
from Ejecucion.Entorno import entorno
from Instruccion.Instruccion import instruccion

class sentenciaWhile(instruccion):
    '''
        Ciclo while. Recibe una condicion y una serie de instrucciones.
        - Condicion: Condicion del while 
        - Instrucciones: Array con con las instrucciones a ejecutar
        - TipoInstruccion: Indica que es una instruccion de tipo while
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, CONDICION, INSTRUCCIONES, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.condicion = CONDICION
        self.instrucciones = INSTRUCCIONES
        self.tipoInstruccion = Instrucciones.WHILE.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"While\" ];\n"
        REPORTES.cont += 1

        #Declarar while
        nodoWhileA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoWhileA + "[ label = \"While (\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoWhileA + ";\n"

        #Declarar condicion
        nodoCondicion = self.condicion.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoCondicion + ";\n"

        #Declarar while
        nodoWhileB = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoWhileB + "[ label = \") {\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoWhileB + ";\n"

        #Declarar instrucciones
        for instruccion in self.instrucciones:
            nodoInstruccion = instruccion.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoInstruccion + ";\n"
        
        #Declarar while
        nodoWhileC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoWhileC + "[ label = \"} ;\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoWhileC + ";\n"
        return padre    

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
       
        #Crear el while
        while True:

            salir = False                #Indica al while si hace un break
            siguiente = False            #Indica al while si viene un continue
            #Condicion
            valorCondicion = self.condicion.analisis(SIMBOLOS, REPORTES)

           #Verificar que no sea nulo
            if valorCondicion.tipo == Tipo.NULL.value:
                REPORTES.salida += "ERROR: La condicion retorna un NULL. \n"
                mensaje = "La condicion retorna un NULL."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1

            #Verifivar que sea primitivo
            if valorCondicion.clase != Clases.PRIMITIVO.value:
                REPORTES.salida += "ERROR: La condicion no retorna un primitivo. \n"
                mensaje = "La condicion no retorna un primitivo."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Verificar que sea boolean
            if valorCondicion.tipo != Tipo.BOOLEAN.value:
                REPORTES.salida += "ERROR: La condicion no retorna un bool. \n"
                mensaje = "La condicion no retorna un bool."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1
            
            #Si es false, se termina el ciclo
            if valorCondicion.valor == "false":
                break

            #Crear el entorno nuevo y añadirlo a la lista
            nombre = "while_" + str(SIMBOLOS[0].contador)
            SIMBOLOS[0].contador += 1
            nuevoEntorno = entorno(nombre)
            nuevoEntorno.estructuras = SIMBOLOS[0].estructuras
            SIMBOLOS.append(nuevoEntorno)

            #Ejecutar las instrucciones. Borrar el entorno añadido en cualquier return o al finalizar.
            for instruccion in self.instrucciones:
                retorno = instruccion.analisis(SIMBOLOS, REPORTES)

                if retorno == None:             #Instruccion sin return. Se ignora.
                    pass
                elif retorno == 1:              #Instruccion break. Termina la ejecucion y asigna a la variable de salida true.
                    salir = True
                    break
                elif retorno == 0:              #Instruccion continue. El break termina la ejecucion.
                    siguiente = True
                    break
                elif retorno == -1:             #Es un error. Se sigue arrastrando para detener la ejecucion.
                    SIMBOLOS.pop()
                    return -1
                else:
                    if retorno.regreso:         #Algunas funciones retornan valores. Si return no es true, se ignora
                        SIMBOLOS.pop()
                        return retorno   

            #Si pasa por aca es que se aplica el break a la ejecion.
            if salir:
                SIMBOLOS.pop()
                break 
            #Si pasa por aca es que se aplica el continue a la ejecion.
            if siguiente:
                SIMBOLOS.pop()
                continue
            
            #Al terminar de ejecutar, si no ha retornado se asume que cumplio las instrucciones. SOlo se saca el entorno.
            SIMBOLOS.pop()
            
    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        CODIGO.insertar_Comentario("////////// INICIA WHILE //////////")
        # Lista que almacena los labels de las salidas verdaderas en la condiciones
        # Se imprimen al terminar el else si es que viene
        salir = False
        siguiente = False
        listaSalidas = []

        # Creación de Labels
        labelSiguiente = CODIGO.nuevoLabel()
        labelSalida = CODIGO.nuevoLabel()
        labelInicio = CODIGO.nuevoLabel()

        # Inicio
        CODIGO.insertar_Label(labelInicio)

        expresion = self.condicion.c3d(SIMBOLOS, REPORTES, CODIGO)

        # Verificar que sea primitivo
        if expresion.clase != Clases.PRIMITIVO.value:
            CODIGO.insertar_Comentario("ERROR: La condicion no retorna un primitivo.")
            REPORTES.salida += "La condicion no retorna un primitivo. \n"
            mensaje = "La condicion no retorna un primitivo."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

        # Verificar que sea boolean
        if expresion.tipo != Tipo.BOOLEAN.value:
            CODIGO.insertar_Comentario("ERROR: La condicion no retorna un bool.")
            REPORTES.salida += "La condicion no retorna un bool. \n"
            mensaje = "La condicion no retorna un bool."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

        # Evaluar la condicion
        CODIGO.insertar_If(expresion.valor, "==", "1", labelSiguiente)
        CODIGO.insertar_Goto(labelSalida)
        listaSalidas.append(labelSalida)

        # -- Si es verdadero, se ejecutan todas las instrucciones
        CODIGO.insertar_Label(labelSiguiente)

        # Mover el entorno al nuevo
        local = SIMBOLOS[-1]
        CODIGO.insertar_MoverStack(local.tamaño)

        # Crear el entorno nuevo y añadirlo a la lista
        nombre = "while_" + str(SIMBOLOS[0].contador)
        SIMBOLOS[0].contador += 1
        nuevoEntorno = entorno3D(nombre)

        #Heredar labels y contadores
        nuevoEntorno.labelBreak = labelSalida
        nuevoEntorno.contadorBreak += local.tamaño

        nuevoEntorno.labelContinue = labelInicio
        nuevoEntorno.contadorContinue += local.tamaño
        

        nuevoEntorno.labelReturn = local.labelReturn
        nuevoEntorno.contadorReturn += local.contadorReturn

        SIMBOLOS.append(nuevoEntorno)

        for instruccion in self.instrucciones:
            retorno = instruccion.c3d(SIMBOLOS, REPORTES, CODIGO)

        # Al terminar de traducir, saca el entorno normal
        SIMBOLOS.pop()
        CODIGO.insertar_RegresarStack(local.tamaño)

        #Insertar el goto de regreso al inicio del ciclo
        CODIGO.insertar_Goto(labelInicio)

        for n in listaSalidas:
            CODIGO.insertar_Label(n)


