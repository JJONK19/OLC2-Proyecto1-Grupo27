from Tipos.Tipos import *
from Ejecucion.Entorno import entorno
from Instruccion.Instruccion import instruccion
from Dato.Primitivo import primitivo

class cicloForOf(instruccion):
    '''
        Ciclo forOf. Recibe una declaracion/asignacion, condicion, una expresion/asignacion y una serie de instrucciones.
        - ID: Nombre de la variable, se usa para asignar y actualizar el valor de la tabla
        - Iterador: Instruccion con la asignacion o declaracion de la variable iterador
        - Expresion: Tercera parte del for. Modifica el iterador.
        - Instrucciones: Array con con las instrucciones a ejecutar
        - TipoInstruccion: Indica que es una instruccion de tipo instruccion
        - Linea: Linea de la instruccion. 
        - Columna: Posicion de la linea donde esta la instruccion.
    '''
    def __init__(self, ITERADOR, EXPRESION, INSTRUCCIONES, LINEA, COLUMNA):
        super().__init__(LINEA, COLUMNA) 
        self.id = ""
        self.iterador = ITERADOR
        self.expresion = EXPRESION
        self.instrucciones = INSTRUCCIONES
        self.tipoInstruccion = Instrucciones.FOROF.value

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
        nodoWhileA = "NODO" + str(REPORTES.cont)
        REPORTES.dot += nodoWhileA + "[ label = \"For (\" ];\n"
        REPORTES.cont += 1
        REPORTES.dot += padre + "->" + nodoWhileA + ";\n"

        #Declarar iterador
        nodoIterador = self.iterador.grafo(REPORTES)
        REPORTES.dot += padre + "->" + nodoIterador + ";\n"

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
        
        self.id = self.iterador.id
        
        #Expresion
        valorCondicion = self.expresion.analisis(SIMBOLOS, REPORTES)

        #Verificar que no sea nulo
        if valorCondicion.tipo == Tipo.NULL.value:
            REPORTES.salida += "ERROR: La expresion del if retorna un NULL. \n"
            mensaje = "La expresion del if retorna un NULL."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return -1

        #Verifivar que no sea struct
        if valorCondicion.clase == Clases.STRUCT.value:
            REPORTES.salida += "ERROR: La expresion del if no recibe structs. \n"
            mensaje = "La expresion del if no recibe structs."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return -1
        
        #Verificar que sea string en caso sea primitivo
        if valorCondicion.tipo != Tipo.STRING.value and valorCondicion.clase == Clases.PRIMITIVO.value:
            REPORTES.salida += "ERROR: La expresion del if solo recibe strings o vectores. \n"
            mensaje = "La expresion del if solo recibe strings o vectores."
            REPORTES.añadirError("Semantico", mensaje, self.linea, self.columna)
            return -1
        
        #Si es string, crear un vector de primitivos en caso sea un string
        iterador = []
        if valorCondicion.tipo == Tipo.STRING.value and valorCondicion.clase == Clases.PRIMITIVO.value:
            for caracter in valorCondicion.valor:
                iterador.append(primitivo("", valorCondicion.tipo, valorCondicion.clase, caracter))  
        else:
            #Si es vector, solo se asigna el vector al iterador
            iterador = valorCondicion.valor

        #EL for se recorre con los valores del iterador
        for i in iterador:

            salir = False                #Indica al for si hace un break
            siguiente = False            #Indica al for si viene un continue

            #Generar el objeto valor, asignarle el ID y actualizar el iterador
            valorActualizar = ""
            if i.clase == Clases.PRIMITIVO.value:
                valorActualizar = i.get()
            elif i.clase == Clases.VECTOR.value:
                valorActualizar = i.get("", REPORTES, self.linea, self.columna)
            elif i.clase == Clases.STRUCT.value:
                valorActualizar = i.get("", REPORTES, self.linea, self.columna)
            elif i.clase == Clases.ANY.value:
                valorActualizar = i.get("", "", REPORTES, self.linea, self.columna)
            
            valorActualizar.id = self.id
            salida = entorno.asignarSimbolo(valorActualizar, SIMBOLOS, REPORTES) 

            if salida == -1:
                SIMBOLOS.pop()
                return -1
            
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
                    siguiente = True
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

        #Sacar el for Global al terminar
        SIMBOLOS.pop()

    def c3d(self, SIMBOLOS, REPORTES, CODIGO):
        pass

