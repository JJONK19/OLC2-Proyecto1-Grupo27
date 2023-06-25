from Instruccion.Instruccion import instruccion
from Tipos.Tipos import *
from Ejecucion.Valor import valor
from Ejecucion.Entorno import entorno
from C3D.Valor3D import valor3D
from C3D.Entorno3D import entorno3D

class llamadaFuncion(instruccion):
    '''
        LLama una funcion. Devuelve un valor NULL si no regresa nada.
        - ID: Nombre de la funcion 
        - ListaExpresiones: Parametros que se pasan a la variable
        - TipoInstruccion: Indica que es una instruccion de tipo declaracion primitiva
        - Linea: Linea de la instruccion.
        - Columna: Posicion de la linea donde esta la instruccion.
    '''

    #todo cambiar constructores
    def __init__(self, ID, LISTA_EXPRESIONES, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA)
        self.id = ID
        self.listaExpresiones = LISTA_EXPRESIONES
        self.tipoInstruccion = Instrucciones.LLAMADA_FUNCION.value

    def grafo(self, REPORTES):
        '''
            Se llama al metodo para graficar las instrucciones, retorna el ID del nodo raiz de la instruccion.
            - Reportes: Variable de tipo reportes. Contene la variable con el dot.
        '''
        # Declarar el padre
        padre = "NODO" + str(REPORTES.cont)
        REPORTES.dot += padre + "[ label = \"Llamada Funciones\" ];\n"
        REPORTES.cont += 1

        nodoID = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoID + "[ label = \""+self.id+"\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoID + ";\n"

        #Nodo complementario :
        nodoLlA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlA + "[ label = \"(\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlA + ";\n"

        #Declarar atributos
        for i in self.listaExpresiones:
            nodoExpresion = i.grafo(REPORTES)
            REPORTES.dot += padre + "->" + nodoExpresion + ";\n"

        #Nodo complementario :
        nodoLlC = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoLlC + "[ label = \")\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoLlC + ";\n"

        # Nodo complementario ;
        nodoPtcoma = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoPtcoma + "[ label = \";\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoPtcoma + ";\n"

        return padre
    
    def analisis(self, SIMBOLOS, REPORTES):
        '''
            Se encarga de ejecutar la instruccion.
            - Simbolos: Lista con los entornos de la ejecucion.
            - Reportes: Almacena un resumen de la ejecucion.
        '''
        #Crear la lista de parametros 
        parametros = []
        for i in self.listaExpresiones:
            parametros.append(i.analisis(SIMBOLOS, REPORTES))
        
        #Buscar el metodo en el entorno global
        entornoGlobal = SIMBOLOS[0]
        funcion = entornoGlobal.getMetodo(self.id, REPORTES,self.linea, self.columna)

        if funcion == -1:
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            return retorno

        #Evaluar si la entrada cumple. Se va a ir añadiendo el ID a las entradas en el proceso.
        atributos = funcion.parametros
      
        if len(atributos) != len(parametros):
            retorno = valor()
            retorno.id = "NULL"
            retorno.tipo = Tipo.NULL.value
            retorno.valor = "NULL"
            retorno.clase = Clases.NULL.value
            retorno.string = "NULL"
            
            REPORTES.salida += "ERROR: La cantidad de valores de entrada en la funcion es incorrecta. \n"
            mensaje = "La cantidad de valores de entrada en la funcion es incorrecta."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return retorno

            
        for i in range(len(atributos)):
            tempAtributo = atributos[i]
            tempParametro = parametros[i]

            #Comprobar tipos. SI no pasa se sale.
            if tempParametro.tipo != tempAtributo.tipo:
                if tempAtributo.tipo != Tipo.ANY.value:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: El tipo de la entrada no coincide con el atributo " + tempAtributo.id + ".\n"
                    mensaje = "El tipo de la entrada no coincide con el atributo " + tempAtributo.id + ".\n"
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    return retorno
            
            #Comprobar clases. Si no pasa se sale.
            if tempParametro.clase != tempAtributo.clase:
                if tempAtributo.clase != Clases.ANY.value:
                    retorno = valor()
                    retorno.id = "NULL"
                    retorno.tipo = Tipo.NULL.value
                    retorno.valor = "NULL"
                    retorno.clase = Clases.NULL.value
                    retorno.string = "NULL"
                    
                    REPORTES.salida += "ERROR: El tipo de la entrada no coincide con el atributo " + tempAtributo.id + ".\n"
                    mensaje = "El tipo de la entrada no coincide con el atributo " + tempAtributo.id + ".\n"
                    REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                    return retorno

            tempParametro.id = tempAtributo.id

        #Crear nueva lista de simbolo y añadir el entorno de la llamada
        Simbolos = [SIMBOLOS[0]]
        
        #Crear el entorno nuevo y añadirlo a la lista
        nombre = "llamada_" + str(SIMBOLOS[0].contador)
        SIMBOLOS[0].contador += 1
        nuevoEntorno = entorno(nombre)
        nuevoEntorno.estructuras = SIMBOLOS[0].estructuras
        Simbolos.append(nuevoEntorno)

        #Recorrer las expresiones y añadirlas al nuevo ambiente
        for parametro in parametros:
            #Enviar al entorno local
            local = Simbolos[-1]
            salida = local.insertarSimbolo(parametro, REPORTES)

            if salida == -1:
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                return retorno

        #Recorrer las instrucciones
        instrucciones = funcion.instrucciones

        for instruccion in instrucciones:
            #Ejecutar las instrucciones. Borrar el entorno añadido en cualquier return o al finalizar.
            retorno = instruccion.analisis(Simbolos, REPORTES)

            if retorno == None:             #Instruccion sin return. Se ignora.
                pass

            elif retorno == 1:              #Instruccion break. 
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: No se puede usar break fuera de un ciclo."
                mensaje = "No se puede usar break fuera de un ciclo."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            elif retorno == 0:              #Instruccion continue. 
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                REPORTES.salida += "ERROR: No se puede usar continue fuera de un ciclo."
                mensaje = "No se puede usar continue fuera de un ciclo."
                REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                return retorno
            
            elif retorno == -1:             #Es un error. Se sigue arrastrando para detener la ejecucion.
                retorno = valor()
                retorno.id = "NULL"
                retorno.tipo = Tipo.NULL.value
                retorno.valor = "NULL"
                retorno.clase = Clases.NULL.value
                retorno.string = "NULL"
                
                return retorno
            else:
                if retorno.regreso:         #Algunas funciones retornan valores. Se asigna false para que no arroje error de return.
                    #Verificar si el retorno cumple el tipo y clase
                    if retorno.valorTipo != funcion.tipo:         
                        retorno.id = "NULL"
                        retorno.tipo = Tipo.NULL.value
                        retorno.valor = "NULL"
                        retorno.clase = Clases.NULL.value
                        retorno.string = "NULL"

                        REPORTES.salida += "ERROR: El retorno no cumple con el tipo."
                        mensaje = "El retorno no cumple con el tipo."
                        REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                        return retorno

                    #Verificar si el retorno cumple el tipo
                    if retorno.valorClase != funcion.claseReturn:         
                        retorno.id = "NULL"
                        retorno.tipo = Tipo.NULL.value
                        retorno.valor = "NULL"
                        retorno.clase = Clases.NULL.value
                        retorno.string = "NULL"

                        REPORTES.salida += "ERROR: El retorno no cumple con la clase."
                        mensaje = "El retorno no cumple con la clase."
                        REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
                        return retorno
                    
                    retorno.regreso = False
                    return retorno          
        
        #Si no ha retornado, regresar una instancia de valor en Null. Esto es porque las llamadas son una expresion.
        retorno = valor()
        retorno.id = "NULL"
        retorno.tipo = Tipo.NULL.value
        retorno.valor = "NULL"
        retorno.clase = Clases.NULL.value
        retorno.string = "NULL"
        return retorno

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass
        
        #Buscar si existe la funcion
        metodo = CODIGO.getMetodo(self.id, REPORTES,self.linea, self.columna)

        if metodo == -1:
            CODIGO.insertar_Comentario("ERROR: La funcion no existe.")
            REPORTES.salida += "ERROR: La funcion no existe. \n"
            mensaje = "La funcion no existe."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)

            temporal = CODIGO.nuevoTemporal()
            CODIGO.insertar_Asignacion(temporal, "0")
            return valor3D(temporal, True, Tipo.NUMBER.value, Clases.PRIMITIVO.value)
        
        #Extraer los atributos de la funcion y comparar con las expresiones de entrada
        #Ir asignando en el stack
        

        #Si todo salio bien llamar a la funcion

        #Retornar el stack a su posicion original

 