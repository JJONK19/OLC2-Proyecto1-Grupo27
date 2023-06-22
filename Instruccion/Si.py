from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Entorno import entorno
from C3D.Valor3D import valor3D
from C3D.Entorno3D import entorno3D


class si(instruccion):
    '''
        Condicional if
        - Condiciones: Array con las condiciones en orden del if 
        - Instrucciones: Array con arrays de instrucciones en orden del if
        - Sino: Array de instrucciones que se ejecutan en el else
        - TipoInstruccion: Indica que es una instruccion de tipo si
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    def __init__(self, CONDICIONES, INSTRUCCIONES, SINO, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.condiciones = CONDICIONES
        self.instrucciones = INSTRUCCIONES
        self.sino = SINO
        self.tipoInstruccion = Instrucciones.SI.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"If\" ];\n"
        REPORTES.cont += 1

        # Declarar ifs.
        for i in range(len(self.instrucciones)):
            if i == 0:
                nodoIf = "NODO" + str(REPORTES.cont)
                REPORTES.dot += nodoIf + "[ label = \"if (\" ];\n"
                REPORTES.cont += 1
                REPORTES.dot += padre + "->" + nodoIf + ";\n"

                nodoCondicion = self.condiciones[i].grafo(REPORTES)
                REPORTES.dot += padre + "->" + nodoCondicion + ";\n"

                nodoApertura = "NODO" + str(REPORTES.cont)
                REPORTES.dot += nodoApertura + "[ label = \") { \" ];\n"
                REPORTES.cont += 1
                REPORTES.dot += padre + "->" + nodoApertura + ";\n"

                for instruccion in self.instrucciones[i]:
                    nodoInstruccion = instruccion.grafo(REPORTES)
                    REPORTES.dot += padre + "->" + nodoInstruccion + ";\n"

                nodoCierre = "NODO" + str(REPORTES.cont)
                REPORTES.dot += nodoCierre + "[ label = \"} \" ];\n"
                REPORTES.cont += 1
                REPORTES.dot += padre + "->" + nodoCierre + ";\n"
            else:
                nodoIf = "NODO" + str(REPORTES.cont)
                REPORTES.dot += nodoIf + "[ label = \"else if (\" ];\n"
                REPORTES.cont += 1
                REPORTES.dot += padre + "->" + nodoIf + ";\n"

                nodoCondicion = self.condiciones[i].grafo(REPORTES)
                REPORTES.dot += padre + "->" + nodoCondicion + ";\n"

                nodoApertura = "NODO" + str(REPORTES.cont)
                REPORTES.dot += nodoApertura + "[ label = \") { \" ];\n"
                REPORTES.cont += 1
                REPORTES.dot += padre + "->" + nodoApertura + ";\n"

                for instruccion in self.instrucciones[i]:
                    nodoInstruccion = instruccion.grafo(REPORTES)
                    REPORTES.dot += padre + "->" + nodoInstruccion + ";\n"

                nodoCierre = "NODO" + str(REPORTES.cont)
                REPORTES.dot += nodoCierre + "[ label = \"} \" ];\n"
                REPORTES.cont += 1
                REPORTES.dot += padre + "->" + nodoCierre + ";\n"

        # Nodo else
        if len(self.sino) != 0:
            nodoElseA = "NODO" + str(REPORTES.cont)
            REPORTES.dot += nodoElseA + "[ label = \"else {\" ];\n"
            REPORTES.cont += 1
            REPORTES.dot += padre + "->" + nodoElseA + ";\n"

        for instruccion in self.sino:
            nodoElseIns = instruccion.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoElseIns + ";\n"

        if len(self.sino) != 0:
            nodoElseC = "NODO" + str(REPORTES.cont)
            REPORTES.dot += nodoElseC + "[ label = \"}\" ];\n"
            REPORTES.cont += 1
            REPORTES.dot += padre + "->" + nodoElseC + ";\n"

        # Nodo puntocoma
        nodoPtocoma = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoPtocoma + "[ label = \";\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoPtocoma + ";\n"

        return padre

    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion. 
        '''
        # Revisar si la condicion cumple y ejecutar
        for i in range(len(self.instrucciones)):

            # Condicion
            valorCondicion = self.condiciones[i].analisis(SIMBOLOS, REPORTES)

            # Verificar que no sea nulo
            if valorCondicion.tipo == Tipo.NULL.value:
                REPORTES.salida += "ERROR: La condicion retorna un NULL. \n"
                mensaje = "La condicion retorna un NULL."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1

            # VErifivar que sea primitivo
            if valorCondicion.clase != Clases.PRIMITIVO.value:
                REPORTES.salida += "ERROR: La condicion no retorna un primitivo. \n"
                mensaje = "La condicion no retorna un primitivo."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1

            # VErificar que sea boolean
            if valorCondicion.tipo != Tipo.BOOLEAN.value:
                REPORTES.salida += "ERROR: La condicion no retorna un bool. \n"
                mensaje = "La condicion no retorna un bool."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return -1

            # Si es false, se revisa la siguiente condicion
            if valorCondicion.valor == "false":
                continue

            # Crear el entorno nuevo y añadirlo a la lista
            nombre = "if_" + str(SIMBOLOS[0].contador)
            SIMBOLOS[0].contador += 1
            nuevoEntorno = entorno(nombre)
            nuevoEntorno.estructuras = SIMBOLOS[0].estructuras
            SIMBOLOS.append(nuevoEntorno)

            # Ejecutar las instrucciones. Borrar el entorno añadido en cualquier return o al finalizar.
            for instruccion in self.instrucciones[i]:
                retorno = instruccion.analisis(SIMBOLOS, REPORTES)

                if retorno == None:  # Instruccion sin return. Se ignora.
                    pass
                elif retorno == 1:  # Instruccion break. Se regresa para que el que llamo el if lo maneje.
                    SIMBOLOS.pop()
                    return 1
                elif retorno == 0:  # Instruccion continue. Se regresa para que el que llamo el if lo maneje.
                    SIMBOLOS.pop()
                    return 0
                elif retorno == -1:  # Es un error. Se sigue arrastrando para detener la ejecucion.
                    SIMBOLOS.pop()
                    return -1
                else:
                    if retorno.regreso:  # Algunas funciones retornan valores. Si return no es true, se ignora
                        SIMBOLOS.pop()
                        return retorno

                        # Al terminar de ejecutar, si no ha retornado se asume que cumplio las instrucciones
            SIMBOLOS.pop()
            return None

        # Ejecutar el else: Es una lista vacia si no tiene instrucciones asi que se puede correr sin problema
        # Crear el entorno nuevo y añadirlo a la lista
        nombre = "else_" + str(SIMBOLOS[0].contador)
        SIMBOLOS[0].contador += 1
        nuevoEntorno = entorno(nombre)
        nuevoEntorno.estructuras = SIMBOLOS[0].estructuras
        SIMBOLOS.append(nuevoEntorno)

        for instruccion in self.sino:
            # Ejecutar las instrucciones. Borrar el entorno añadido en cualquier return o al finalizar.
            retorno = instruccion.analisis(SIMBOLOS, REPORTES)

            if retorno == None:  # Instruccion sin return. Se ignora.
                pass
            elif retorno == 1:  # Instruccion break. Se regresa para que el que llamo el if lo maneje.
                SIMBOLOS.pop()
                return 1
            elif retorno == 0:  # Instruccion continue. Se regresa para que el que llamo el if lo maneje.
                SIMBOLOS.pop()
                return 0
            elif retorno == -1:  # Es un error. Se sigue arrastrando para detener la ejecucion.
                SIMBOLOS.pop()
                return -1
            else:
                if retorno.regreso:  # Algunas funciones retornan valores. Si return no es true, se ignora
                    SIMBOLOS.pop()
                    return retorno

                    # Al terminar de ejecutar, si no ha retornado se asume que cumplio las instrucciones
        SIMBOLOS.pop()
        return None

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        CODIGO.insertar_Comentario("////////// INICIA IF //////////")
        # Lista que almacena los labels de las salidas verdaderas en la condiciones
        # Se imprimen al terminar el else si es que viene
        listaSalidas = []

        for i in range(len(self.instrucciones)):

            expresion = self.condiciones[i].c3d(SIMBOLOS, REPORTES, CODIGO)

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

            # Creación de Labels
            labelVerdadero = CODIGO.nuevoLabel()
            labelFalso = CODIGO.nuevoLabel()
            labelSalida = CODIGO.nuevoLabel()

            # Evaluar la condicion
            CODIGO.insertar_If(expresion.valor, "==", "1", labelVerdadero)
            CODIGO.insertar_Goto(labelFalso)

            # -- Si es verdadero, se ejecutan todas las instrucciones
            CODIGO.insertar_Label(labelVerdadero)
            
            #Mover el entorno al nuevo
            local = SIMBOLOS[-1]
            CODIGO.insertar_MoverStack(local.tamaño)

            # Crear el entorno nuevo y añadirlo a la lista
            nombre = "if_" + str(SIMBOLOS[0].contador)
            SIMBOLOS[0].contador += 1
            nuevoEntorno = entorno3D(nombre)
            SIMBOLOS.append(nuevoEntorno)

            for instruccion in self.instrucciones[i]:
                retorno = instruccion.c3d(SIMBOLOS, REPORTES, CODIGO)

                if retorno == None:  # Instruccion sin return. Se ignora.
                    pass
                elif retorno == 1:  # Instruccion break. Se regresa para que el que llamo el if lo maneje.
                    SIMBOLOS.pop()
                    CODIGO.insertar_RegresarStack(local.tamaño)
                    # return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

                elif retorno == 0:  # Instruccion continue. Se regresa para que el que llamo el if lo maneje.
                    SIMBOLOS.pop()
                    CODIGO.insertar_RegresarStack(local.tamaño)
                    # return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

                elif retorno == -1:  # Es un error. Se sigue arrastrando para detener la ejecucion.
                    SIMBOLOS.pop()
                    CODIGO.insertar_RegresarStack(local.tamaño)
                    # return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

                else:
                    pass
                    #if retorno.regreso:  # Algunas funciones retornan valores. Si return no es true, se ignora
                    #    SIMBOLOS.pop()
                    #    return retorno

            # Al terminar de traducir, saca el entorno
            SIMBOLOS.pop()
            CODIGO.insertar_RegresarStack(local.tamaño)
            CODIGO.insertar_Goto(labelSalida)
            listaSalidas.append(labelSalida)

            # -- Si es falso solo se imprime el label
            CODIGO.insertar_Label(labelFalso)

        # Ejecución del Else si es falso
        local = SIMBOLOS[-1]
        CODIGO.insertar_MoverStack(local.tamaño)

        nombre = "else_" + str(SIMBOLOS[0].contador)
        SIMBOLOS[0].contador += 1
        nuevoEntorno = entorno3D(nombre)
        SIMBOLOS.append(nuevoEntorno)

        for instruccion in self.sino:
            retorno = instruccion.c3d(SIMBOLOS, REPORTES, CODIGO)

            if retorno == None:  # Instruccion sin return. Se ignora.
                pass
            elif retorno == 1:  # Instruccion break. Se regresa para que el que llamo el if lo maneje.
                SIMBOLOS.pop()
                CODIGO.insertar_RegresarStack(local.tamaño)
                # return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

            elif retorno == 0:  # Instruccion continue. Se regresa para que el que llamo el if lo maneje.
                SIMBOLOS.pop()
                CODIGO.insertar_RegresarStack(local.tamaño)
                # return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

            elif retorno == -1:  # Es un error. Se sigue arrastrando para detener la ejecucion.
                SIMBOLOS.pop()
                CODIGO.insertar_RegresarStack(local.tamaño)
                # return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)

            else:
                pass
                # if retorno.regreso:  # Algunas funciones retornan valores. Si return no es true, se ignora
                #     SIMBOLOS.pop()
                #        return retorno

        # Al terminar de ejecutar, se saca el entorno y se imprimen los labels de salida
        SIMBOLOS.pop()
        CODIGO.insertar_RegresarStack(local.tamaño)

        for n in listaSalidas:
            CODIGO.insertar_Label(n)

        #Aca va el return
