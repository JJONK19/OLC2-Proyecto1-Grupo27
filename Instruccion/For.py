from C3D.Entorno3D import entorno3D
from C3D.Valor3D import valor3D
from Tipos.Tipos import *
from Ejecucion.Entorno import entorno
from Instruccion.Instruccion import instruccion

class cicloFor(instruccion):
    '''
        Ciclo for. Recibe una declaracion/asignacion, condicion, una expresion/asignacion y una serie de instrucciones.
        - Iterador: Instruccion con la declaracion de la variable iterador
        - Expresion: Tercera parte del for. Modifica el iterador.
        - Condicion: Condicion del for 
        - Instrucciones: Array con con las instrucciones a ejecutar
        - TipoInstruccion: Indica que es una instruccion de tipo instruccion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, ITERADOR, CONDICION, EXPRESION, INSTRUCCIONES, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.iterador = ITERADOR
        self.condicion = CONDICION
        self.expresion = EXPRESION
        self.instrucciones = INSTRUCCIONES
        self.tipoInstruccion = Instrucciones.FOR.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        #Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[color = \"brown\", style =\"radial\", fillcolor = \"gold:brown\", gradientangle = \"315\", label = \"For\" ];\n"
        REPORTES.cont += 1

        #Declarar for
        nodoForA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoForA + "[ label = \"For (\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoForA + ";\n"

        #Declarar iterador
        nodoIterador = self.iterador.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoIterador + ";\n"

        #Declarar condicion
        nodoExpresion = self.condicion.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoExpresion + ";\n"

        #Declarar expresion
        nodoExpresion = self.expresion.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoExpresion + ";\n"

        #Declarar while
        nodoForB = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoForB + "[ label = \") {\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoForB + ";\n"

        #Declarar instrucciones
        for instruccion in self.instrucciones:
            nodoInstruccion = instruccion.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoInstruccion + ";\n"
        
        #Declarar while
        nodoForC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoForC + "[ label = \"} ;\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoForC + ";\n"
        return padre    

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        #Crear el entorno local del for y crear la variable iteradora
        nombre = "forGlobal_" + str(SIMBOLOS[0].contador)
        SIMBOLOS[0].contador += 1
        nuevoEntorno = entorno(nombre)
        nuevoEntorno.estructuras = SIMBOLOS[0].estructuras
        SIMBOLOS.append(nuevoEntorno)

        retorno = self.iterador.analisis(SIMBOLOS, REPORTES)

        if retorno == -1:              #Si hay un error en la instruccion, sale
           return -1

        #EL for se maneja como un while
        while True:

            salir = False                #Indica al for si hace un break
            siguiente = False            #Indica al for si viene un continue

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
            nombre = "for_" + str(SIMBOLOS[0].contador)
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
                    break
                elif retorno == -1:             #Es un error. Se sigue arrastrando para detener la ejecucion.
                    #Se hacen dos pops para sacar el Global del For y el for local
                    SIMBOLOS.pop()
                    SIMBOLOS.pop()
                    return -1
                else:
                    if retorno.regreso:         #Algunas funciones retornan valores. Si return no es true, se ignora
                        SIMBOLOS.pop()
                        SIMBOLOS.pop()
                        return retorno   

            #Si pasa por aca es que se aplica el break a la ejecucion.
            if salir:
                SIMBOLOS.pop()
                break 
            
            #Al terminar de ejecutar, si no ha retornado se asume que cumplio las instrucciones. SOlo se saca el entorno.
            SIMBOLOS.pop()

            #Evaluar la expresion de actualizacion
            retorno = self.expresion.analisis(SIMBOLOS, REPORTES)
            if retorno == -1:              #Si hay un error en la instruccion, sale. Se saca el entorno global.
                SIMBOLOS.pop()
                return -1
            
        #Sacar el for Global al terminar
        SIMBOLOS.pop()

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):

        CODIGO.insertar_Comentario("////////// INICIA FOR //////////")

        # Creación de Labels
        labelSiguiente = CODIGO.nuevoLabel()
        labelSalida = CODIGO.nuevoLabel()
        labelInicio = CODIGO.nuevoLabel()
        labelContinue = CODIGO.nuevoLabel()
        listaSalidas = []

        # Mover el entorno al nuevo
        local = SIMBOLOS[-1]
        CODIGO.insertar_MoverStack(local.tamaño)

        nombre = "forGlobal_" + str(SIMBOLOS[0].contador)
        SIMBOLOS[0].contador += 1
        nuevoEntorno = entorno3D(nombre)

        # Heredar labels y contadores
        nuevoEntorno.labelBreak = labelSalida
        nuevoEntorno.contadorBreak += local.tamaño

        nuevoEntorno.labelContinue = labelContinue
        nuevoEntorno.contadorContinue += 0

        nuevoEntorno.labelReturn = local.labelReturn
        nuevoEntorno.contadorReturn += local.contadorReturn + local.tamaño

        SIMBOLOS.append(nuevoEntorno)

        self.iterador.c3d(SIMBOLOS, REPORTES, CODIGO)

        # Inicio
        CODIGO.insertar_Label(labelInicio)

        # Condicion
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
        localInterno = SIMBOLOS[-1]

        CODIGO.insertar_MoverStack(localInterno.tamaño)

        # Crear el entorno nuevo y añadirlo a la lista
        nombre = "for_" + str(SIMBOLOS[0].contador)
        SIMBOLOS[0].contador += 1
        nuevoEntorno = entorno3D(nombre)

        # Heredar labels y contadores
        nuevoEntorno.labelBreak = localInterno.labelBreak
        nuevoEntorno.contadorBreak += local.tamaño + localInterno.tamaño

        nuevoEntorno.labelContinue = localInterno.labelContinue
        nuevoEntorno.contadorContinue += localInterno.tamaño

        nuevoEntorno.labelReturn = localInterno.labelReturn
        nuevoEntorno.contadorReturn += local.contadorReturn + local.tamaño + localInterno.tamaño

        SIMBOLOS.append(nuevoEntorno)

        for instruccion in self.instrucciones:
            instruccion.c3d(SIMBOLOS, REPORTES, CODIGO)

        # Al terminar de traducir, saca el entorno normal
        SIMBOLOS.pop()
        CODIGO.insertar_RegresarStack(localInterno.tamaño)

        #Insertar el goto a la actualizacion (continue llega acá)
        CODIGO.insertar_Goto(labelContinue)
        CODIGO.insertar_Label(labelContinue)
        self.expresion.c3d(SIMBOLOS, REPORTES, CODIGO)
        CODIGO.insertar_Goto(labelInicio)

        for n in listaSalidas:
            CODIGO.insertar_Label(n)

        #Sacar el for global
        CODIGO.insertar_RegresarStack(local.tamaño)
        SIMBOLOS.pop()
