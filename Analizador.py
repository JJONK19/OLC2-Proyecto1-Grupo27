from ply import lex, yacc
from Tipos.Tipos import *
from AST.AST import AST
import re

from Instruccion.Dato import dato
from Instruccion.ExpresionBinaria import expresionBinaria
from Instruccion.ExpresionUnaria import expresionUnaria
from Instruccion.Imprimir import imprimir
from Instruccion.NativasConEntrada import nativaConValor
from Instruccion.NativasSinEntrada import nativaSinValor
from Instruccion.NativasVector import nativasVector
from Instruccion.DeclaracionPrimitiva import DeclaracionPrimitiva
from Instruccion.DeclaracionVector import DeclaracionVector
from Instruccion.DeclaracionStruct import DeclaracionStruct
from Instruccion.DefinicionStruct import DefinicionStruct
from Instruccion.DefinicionAtributo import DefinicionAtributo
from Instruccion.DeclaracionAtributo import DeclaracionAtributo
from Instruccion.DeclaracionAny import DeclaracionAny
from Instruccion.DatoVector import datoVector
from Instruccion.Si import si
from Instruccion.Break import sentenciaBreak
from Instruccion.Continue import sentenciaContinue
from Instruccion.Return import sentenciaReturn
from Instruccion.Mientras import sentenciaWhile
from Instruccion.Accesos import accesos
from Instruccion.Llamada import llamada
from Instruccion.Asignacion import asignacion
from Instruccion.For import cicloFor
from Instruccion.ForOf import cicloForOf 
from Instruccion.DeclaracionFunciones import declaracionFuncion
from Instruccion.LlamadaFunciones import llamadaFuncion

class Analizador:
    #-----------------------------------------------------------------------------------------

    #                                    VARIABLES

    #-----------------------------------------------------------------------------------------
    arbol = AST()              #Contenedor de la informacion generada en el analisis
    input = ''

    #-----------------------------------------------------------------------------------------

    #                                    ANALISIS LEXICO

    #-----------------------------------------------------------------------------------------
    reserved = {
        'console': 'RCONSOLE',
        'log': 'RLOG',
        'let': 'RLET',
        'null' : "RNULL",
        'any' : "RANY",
        'number' : "RNUMBER",#
        'boolean' : "RBOOLEAN",
        'string' : "RSTRING",
        'true' : "RTRUE",
        'false' : "RFALSE",
        'interface' : "RINTERFACE",
        'toFixed' : 'RFIXED',
        'toExponential' : 'REXPONENTIAL',
        'toString' : 'RTSTRING',
        'toLowerCase' : 'RLC',
        'toUpperCase' : 'RUC',
        'split' : 'RSPLIT',
        'concat' : 'RCONCAT',
        'if' : 'RIF',
        'else': 'RELSE',
        'break': 'RBREAK',
        'continue': 'RCONTINUE',
        'return': 'RRETURN',
        'while': 'RWHILE',
        'for': 'RFOR',
        'of': 'ROF',
        'function': 'RFUNCTION'
    }
    
    tokens = [
                'PT',              # .
                'PTCOMA',          # ;
                'DOSPTS',          # :
                'COMA',            # ,

                'PARENI',          # (
                'PAREND',          # )
                'LLAVEI',          # {
                'LLAVED',          # }
                'CORI',            # [
                'CORD',            # ]

                
                'INCREMENTO',      # ++
                'DECREMENTO',      # --
                'MAS',             # +
                'MENOS',           # -
                'MUL',             # *
                'DIV',             # /
                'POT',             # ^
                'MOD',             # %

                'MAYORIG',         # >=
                'MENORIG',         # <=
                'MAYORQ',          # >
                'MENORQ',          # <
                'IGUALACION',      # ===
                'DISTINTO',        # !==

                'IGUAL',           # =
                'OR',              # ||
                'AND',             # &&
                'NOT',             # !

                'ENTERO',
                'DECIMAL',
                'CADENA',
                'ID'

            ] + list(reserved.values())

    # Tokens
    t_PT = r'\.'
    t_PTCOMA = r'\;'
    t_DOSPTS = r'\:'
    t_COMA = r'\,'

    t_PARENI = r'\('
    t_PAREND = r'\)'
    t_LLAVEI = r'\{'
    t_LLAVED = r'\}'
    t_CORI = r'\['
    t_CORD = r'\]'

    t_INCREMENTO = r'\+\+'
    t_DECREMENTO = r'\-\-'
    t_MAS = r'\+'
    t_MENOS = r'\-'
    t_MUL = r'\*'
    t_DIV = r'\/'
    t_POT = r'\^'
    t_MOD = r'\%'

    t_MAYORIG = r'\>='
    t_MENORIG = r'\<='
    t_MAYORQ = r'\>'
    t_MENORQ = r'\<'
    t_IGUALACION = r'\==='
    t_DISTINTO = r'\!=='

    t_IGUAL = r'\='
    t_OR = r'\|\|'
    t_AND = r'\&&'
    t_NOT = r'\!'

    # Decimal
    def t_DECIMAL(t):
        r'\d+\.\d+'
        try:
            value = float(t.value)
            t.value = str(value)
        except ValueError:
            mensaje = "Float demasiado grande: " + t.value
            Analizador.arbol.añadirError("Lexico", mensaje, t.lexer.lineno, 0)
            t.value = 0
        return t

    # Entero
    def t_ENTERO(n):
        r'\d+'
        try:
            value = 0
            if (n.value != None):
                value = int(n.value)
            else:
                value = 0
            n.value = str(value)
        except ValueError:
            mensaje = "Entero demasiado grande: " + n.value
            Analizador.arbol.añadirError("Lexico", mensaje, n.lexer.lineno, 0)
            n.value = 0
        return n


    # Cadena
    def t_CADENA(t):
        r'(\".*?\")'
        t.value = t.value[1:-1]  # Se remueven las comillas de la entrada
        t.value = t.value.replace('\\t', '\t')
        t.value = t.value.replace('\\n', '\n')
        t.value = t.value.replace('\\"', '\"')
        t.value = t.value.replace("\\'", "\'")
        t.value = t.value.replace('\\\\', '\\')
        return t


    # Identificador
    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9_]*'
        t.type = Analizador.reserved.get(t.value, 'ID')  #Si no encuentra la key, el tipo es ID por defecto
        return t

    # Comentario de Una Linea
    def t_Com_Simple(t):
        r'//.*'
        t.lexer.lineno += 1

    # Comentario Multilinea
    def t_Com_Multiple(t):
        r'[/][*][^*]*[*]+([^/*][^*]*[*]+)*[/]'
        t.lexer.lineno += t.value.count('\n')

    # Nueva Linea
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    # Ignora y hace una accion
    def t_ignorar_salto(t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')


    # Caracteres ignorados
    t_ignore = " \t"


    # Error
    def t_error(t):
        mensaje = f'Caracter no reconocido {t.value[0]!r}.'
        Analizador.arbol.añadirError("Lexico", mensaje, t.lexer.lineno, 0)    
        t.lexer.skip(1)


    def find_column(inp, pos):
        line_start = inp.rfind('\n', 0, pos) + 1
        return (pos - line_start) + 1

    lexer = lex.lex(reflags=re.IGNORECASE)

    #-----------------------------------------------------------------------------------------

    #                           ANALISIS SINTACTICO

    #-----------------------------------------------------------------------------------------


    precedence = (
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('left', 'IGUALACION', 'DISTINTO'),
        ('left', 'MENORQ', 'MAYORQ', 'MAYORIG', 'MENORIG'),
        ('left', 'MAS', 'MENOS', 'COMA'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('left', 'PARENI', 'PAREND'),
        ('left', 'POT'),
        ('right', 'INCREMENTO', 'DECREMENTO'),
        ('right', 'UNARIO')
    )


    # Definicion de la Gramatica
    def p_INICIO(t):
        '''
            inicio : sentencias
        '''
        Analizador.arbol.instrucciones = t[1]       #Añadir las instrucciones al arbol
        t[0] = Analizador.arbol                     #Se retorna la instancia del arbol 


    def p_SENTENCIAS(t):
        '''
            sentencias : sentencias sentencia 
                      | sentencia
        '''
        if(len(t) == 3):
            t[1].append(t[2])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    #Sentencias-------------------------------------------------------------------------------------
    def p_SENTENCIA(t): #QUITAR
        '''
            sentencia : print PTCOMA
                        | expresion PTCOMA
                        | declaracion PTCOMA
                        | if PTCOMA
                        | Sreturn PTCOMA
                        | Scontinue PTCOMA
                        | Sbreak PTCOMA
                        | Swhile PTCOMA
                        | asignacion PTCOMA
                        | for PTCOMA
                        | forOf PTCOMA
                        | declararFuncion PTCOMA
                       
        '''
        t[0] = t[1]

    #Print-------------------------------------------------------------------------------------------
    def p_PRINT_SIMPLE(t):
        """
            print : RCONSOLE PT RLOG PARENI listaExpresiones PAREND
        """
        t[0] = imprimir(t[5], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 
    
    #Sentencias de control-------------------------------------------------------------------------
    def p_BREAK(t):
        """
            Sbreak : RBREAK
        """
        t[0] = sentenciaBreak(t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 
    
    def p_CONTINUE(t):
        """
            Scontinue : RCONTINUE
        """
        t[0] = sentenciaContinue(t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 
    
    def p_RETURN(t):
        """
            Sreturn : RRETURN expresion
                    | RRETURN
        """
        if len(t) == 3:
            t[0] = sentenciaReturn(t[2], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 
        else:
            t[0] = sentenciaReturn(None, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    #If--------------------------------------------------------------------------------------------
    def p_IF(t):
        '''
            if : RIF PARENI expresion PAREND LLAVEI sentencias LLAVED elseif RELSE LLAVEI sentencias LLAVED
                | RIF PARENI expresion PAREND LLAVEI sentencias LLAVED RELSE LLAVEI sentencias LLAVED
                | RIF PARENI expresion PAREND LLAVEI sentencias LLAVED elseif
                | RIF PARENI expresion PAREND LLAVEI sentencias LLAVED
                
        '''
        if(len(t) == 13):
            t[8][0].insert(0, t[3])
            t[8][1].insert(0, t[6])
            t[0] = si(t[8][0], t[8][1], t[11], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

        elif(len(t) == 12):
            t[0] = si([t[3]], [t[6]], t[10], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        
        elif(len(t) == 9):
            t[8][0].insert(0, t[3])
            t[8][1].insert(0, t[6])
            t[0] = si(t[8][0], t[8][1], [], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

        else:
            t[0] = si([t[3]], [t[6]], [], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_IF_ELSE(t):
        '''
            elseif : elseif RELSE RIF PARENI expresion PAREND LLAVEI sentencias LLAVED 
                | RELSE RIF PARENI expresion PAREND LLAVEI sentencias LLAVED
        '''
        if(len(t) == 10):
            t[1][0].append(t[5])
            t[1][1].append(t[8])
            t[0] = t[1]
        else:
            condicion = [t[4]]
            listaSentencia = [t[7]]
            t[0] = [condicion, listaSentencia]

    #While-----------------------------------------------------------------------------------------
    def p_WHILE_A(t):
        """
            Swhile : RWHILE PARENI expresion PAREND LLAVEI sentencias LLAVED
        """
        t[0] = sentenciaWhile(t[3], t[6], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 
    
    #For-----------------------------------------------------------------------------------------
    def p_FOR(t):
        """
            for : RFOR PARENI forDeclaracion PTCOMA expresion PTCOMA expresion PAREND LLAVEI sentencias LLAVED
        """
        t[0] = cicloFor(t[3], t[5], t[7],t[10], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 

    def p_FOR_DECLARACION(t):
        """
            forDeclaracion : asignacion
                            | declaracion
        """
        t[0] = t[1]
    
    #For Of---------------------------------------------------------------------------------------
    def p_FOROF(t):
        """
            forOf : RFOR PARENI declaracion ROF expresion PAREND LLAVEI sentencias LLAVED
        """
        t[0] = cicloForOf(t[3], t[5], t[8], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 

    #Funciones----------------------------------------------------------------------------------
    def p_FUNCIONES_DECLARAR(t):
        """
            declararFuncion : RFUNCTION ID PARENI atributosFuncion PAREND LLAVEI sentencias LLAVED
        """
        t[0] = declaracionFuncion(t[2], t[4], t[7], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 

    def p_FUNCIONES_ATRIBUTOS(t):
        """
            atributosFuncion : atributosFuncion COMA atributoFuncion
                    | atributoFuncion
        """
        if(len(t) == 4):
            t[1].append(t[3])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    def p_FUNCIONES_ATRIBUTOPRIMITVO(t):
        """
            atributoFuncion : ID DOSPTS tiposAny 
        """
        t[0] = DefinicionAtributo(t[1], t[3], Clases.PRIMITIVO.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_FUNCIONES_ATRIBUTOVECTOR(t):
        """
            atributoFuncion : ID DOSPTS tiposAny CORI CORD 
        """
        t[0] = DefinicionAtributo(t[1], t[3], Clases.VECTOR.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_FUNCIONES_ATRIBUTOSTRUCT(t):
        """
            atributoFuncion : ID DOSPTS ID 
        """
        t[0] = DefinicionAtributo(t[1], t[3], Clases.STRUCT.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_FUNCIONES_ANY(t):
        """
            atributoFuncion : ID
        """
        t[0] = DefinicionAtributo(t[1], Tipo.ANY.value, Clases.ANY.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    #Declaraciones----------------------------------------------------------------------------------
    def p_DECLARACION_PRIMITIVA(t):
        '''
            declaracion : RLET ID DOSPTS tiposNoAny IGUAL expresion 
                    | RLET ID DOSPTS tiposNoAny
        '''
        if len(t) == 7:
            t[0] = DeclaracionPrimitiva(t[2],t[4],t[6],t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        else:
            t[0] = DeclaracionPrimitiva(t[2], t[4], None, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_VECTOR(t):
        '''
            declaracion : RLET ID DOSPTS tiposAny CORI CORD IGUAL expresion 
                    | RLET ID DOSPTS tiposAny CORI CORD
        '''
        if len(t) == 9:
            t[0] = DeclaracionVector(t[2],t[4],t[8],t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        else:
            t[0] = DeclaracionVector(t[2], t[4], None, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_ANY_TIPADO(t):
        '''
            declaracion : RLET ID DOSPTS RANY IGUAL expresion
                    | RLET ID DOSPTS RANY  
        '''
        if len(t) == 7:
            t[0] = DeclaracionAny(t[2], t[6],t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        else:
            t[0] = DeclaracionAny(t[2], None, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
    
    def p_DECLARACION_ANY_NOTIPADO(t):
        '''
            declaracion : RLET ID IGUAL expresion
                    | RLET ID
        '''
        if len(t) == 5:
            t[0] = DeclaracionAny(t[2],t[4],t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        else:
            t[0] = DeclaracionAny(t[2], None, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_INTERFACE(t):
        """
            declaracion : RINTERFACE ID LLAVEI atributos LLAVED
        """
        t[0] = DefinicionStruct(t[2], t[4], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_INTERFACE_ATRIBUTOS(t):
        """
            atributos : atributos atributo
                    | atributo
        """
        if(len(t) == 3):
            t[1].append(t[2])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    def p_DECLARACION_INTERFACE_ATRIBUTOPRIMITVO(t):
        """
            atributo : ID DOSPTS tiposAny PTCOMA 
        """
        t[0] = DefinicionAtributo(t[1], t[3], Clases.PRIMITIVO.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_INTERFACE_ATRIBUTOVECTOR(t):
        """
            atributo : ID DOSPTS tiposAny CORI CORD PTCOMA 
        """
        t[0] = DefinicionAtributo(t[1], t[3], Clases.VECTOR.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_INTERFACE_ATRIBUTOSTRUCT(t):
        """
            atributo : ID DOSPTS ID PTCOMA
        """
        t[0] = DefinicionAtributo(t[1], t[3], Clases.STRUCT.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_STRUCT(t):
        """
            declaracion : RLET ID DOSPTS ID IGUAL LLAVEI valoresStruct LLAVED 
        """
        t[0] = DeclaracionStruct(t[2], t[4], t[7], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
    
    def p_DECLARACION_STRUCT_VALORES(t):
        """
            valoresStruct : valoresStruct COMA valorStruct 
                    | valorStruct
        """
        if(len(t) == 4):
            t[1].append(t[3])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    def p_DECLARACION_STRUCT_VALOR(t):
        """
            valorStruct : ID DOSPTS expresion
        """
        t[0] = DeclaracionAtributo(t[1], t[3], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    #Asignacion----------------------------------------------------------------------------------
    def p_ASIGNACION(t):
        '''
            asignacion : ID listaAccesos IGUAL expresion
                        | ID IGUAL expresion 
        '''
        if(len(t) == 5):
             t[0] = asignacion(t[1],t[2],t[4],t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        else:
             t[0] = asignacion(t[1],[],t[3],t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    #Tipo ----------------------------------------------------------------------------------
    def p_TIPOS_NOANY(t):
        '''
            tiposNoAny : tipoString
                        | tipoNumber
                        | tipoBoolean
        '''
        t[0] = t[1]

    def p_TIPOS_ANY(t):
        '''
            tiposAny : tipoString
                        | tipoNumber
                        | tipoBoolean
                        | tipoAny
        '''
        t[0] = t[1]
        
    def p_TIPO_STRING(t):
        '''
            tipoString : RSTRING
        '''

        t[0] = Tipo.STRING.value

    def p_TIPO_ANY(t):
        '''
            tipoAny : RANY
        '''

        t[0] = Tipo.ANY.value

    def p_TIPO_NUMBER(t):
        '''
            tipoNumber : RNUMBER
        '''

        t[0] = Tipo.NUMBER.value

    def p_TIPO_BOOLEAN(t):
        '''
            tipoBoolean : RBOOLEAN
        '''

        t[0] = Tipo.BOOLEAN.value

    #Lista de Accesos----------------------------------------------------------------------------
    def p_LISTA_ACCESOS(t):
        """
            listaAccesos : listaAccesos acceso  
                            | acceso
        """
        if(len(t) == 3):
            t[1].append(t[2])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    def p_ACCESOS(t):
        """
            acceso : CORI expresion CORD
                    | PT ID
        """
        if(len(t) == 4):
            t[0] = accesos(Accesos.POSICION.value, t[2], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        else:
            t[0] = accesos(Accesos.ATRIBUTO.value, t[2], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    #Lista de Expresiones----------------------------------------------------------------------------
    def p_LISTA_EXPRESIONES(t):
        """
            listaExpresiones : listaExpresiones COMA expresion  
                            | expresion 
        """
        if(len(t) == 4):
            t[1].append(t[3])
            t[0] = t[1]
        else:
            t[0] = [t[1]]

    #Expresiones-------------------------------------------------------------------------------------
    def p_EXPRESION_SUMA(p):
        """
            expresion : expresion MAS expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.SUMA.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_RESTA(p):
        """
            expresion : expresion MENOS expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.RESTA.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_MULTIPLICACION(p):
        """
            expresion : expresion MUL expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.MULTIPLICACION.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_DIVISION(p):
        """
            expresion : expresion DIV expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.DIVISION.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_MOD(p):
        """
            expresion : expresion MOD expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.MOD.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_POTENCIA(p):
        """
            expresion : expresion POT expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.POT.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_NOT(p):
        """
            expresion : NOT expresion
        """
        p[0] = expresionUnaria(p[2], Expresion.NOT.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_IGUALACION(p):
        """
            expresion : expresion IGUALACION expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.IGUALACION.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_DISTINTO(p):
        """
            expresion : expresion DISTINTO expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.DISTINTO.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_MAYORQ(p):
        """
            expresion : expresion MAYORQ expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.MAYORQ.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_MENORQ(p):
        """
            expresion : expresion MENORQ expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.MENORQ.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_MAYORIG(p):
        """
            expresion : expresion MAYORIG expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.MAYORIG.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_MENORIG(p):
        """
            expresion : expresion MENORIG expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.MENORIG.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_OR(p):
        """
            expresion : expresion OR expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.OR.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_AND(p):
        """
            expresion : expresion AND expresion
        """
        p[0] = expresionBinaria(p[1], p[3], Expresion.AND.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_UNARIO(p):
        """
            expresion : MENOS expresion %prec UNARIO
        """
        p[0] = expresionUnaria(p[2], Expresion.UNARIO.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_INCREMENTO(p):
        """
            expresion : llamada INCREMENTO
        """
        p[0] = expresionUnaria(p[1], Expresion.INCREMENTO.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))

    def p_EXPRESION_DECREMENTO(p):
        """
            expresion : llamada DECREMENTO
        """
        p[0] = expresionUnaria(p[1], Expresion.DECREMENTO.value, p.lineno(1), Analizador.find_column(Analizador.input, p.lexpos(1)))


    def p_EXPRESION_PARENTESIS(p):
        """
            expresion : PARENI expresion PAREND
        """
        p[0] = p[2]

    def p_EXPRESION_BOOLEAN(t):
        """
            expresion : RTRUE
                     | RFALSE
        """
        t[0] = dato(t[1], Tipo.BOOLEAN.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_EXPRESION_NULL(t):
        """
            expresion : RNULL
        """
        t[0] = dato(t[1], Tipo.NULL.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_EXPRESION_NUMBER(t):
        """
            expresion : ENTERO
                    | DECIMAL
        """
        t[0] = dato(t[1], Tipo.NUMBER.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 

    def p_EXPRESION_CADENA(t):
        """
            expresion : CADENA
        """
        t[0] = dato(t[1], Tipo.STRING.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
    
    def p_EXPRESION_NATIVAS(t):
        '''
            expresion : nativa
        '''
        t[0] = t[1]

    def p_EXPRESION_ARRAY(t):
        """
            expresion : CORI listaExpresiones CORD
        """
        t[0] = datoVector(t[2], Tipo.ANY.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
    
    def p_EXPRESION_LLAMADAS(t):
        '''
            expresion : llamada
        '''
        t[0] = t[1]
    
    def p_EXPRESION_LLAMADAFUNCION(t):
        '''
            expresion : llamadaFuncion
        '''
        t[0] = t[1]
    
    #Llamada Funcion----------------------------------------------------------------------------------------
    def p_LLAMADAFUNCION(t):
        """
            llamadaFuncion : ID PARENI listaExpresiones PAREND
        """
        t[0] = llamadaFuncion(t[1], t[3], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
    
    #Llamada----------------------------------------------------------------------------------------
    def p_LLAMADAS(t):
        '''
            llamada : ID listaAccesos PT nativa
                    | ID listaAccesos
                    | ID PT nativa
                    | ID
        '''

        if len(t) == 5:
            temp_llamada = llamada(t[1], t[2], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
            t[4].modificar = temp_llamada
            t[0] = t[4]
        elif len(t) == 3:
            t[0] = llamada(t[1], t[2], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
        elif len(t) == 4:
            temp_llamada = llamada(t[1], [], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))
            t[3].modificar = temp_llamada
            t[0] = t[3]
        else:
            t[0] = llamada(t[1], [], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    #Nativas-----------------------------------------------------------------------------------------
    def p_NATIVA(t):
        '''
            nativa : tofixed
                    | toexponential
                    | tostring
                    | tolowercase
                    | touppercase
                    | split
                    | concat
        '''
        t[0] = t[1]

    def p_NATIVA_TOFIXED(t):
        '''
            tofixed : RFIXED PARENI expresion PAREND
        '''
        t[0] = nativaConValor(None, t[3], Expresion.TOFIXED.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOEXPONENTIAL(t):
        '''
            toexponential : REXPONENTIAL PARENI expresion PAREND
        '''
        t[0] = nativaConValor(None, t[3], Expresion.TOEXPONENTIAL.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOSTRING(t):
        '''
            tostring : RTSTRING PARENI PAREND
        '''
        t[0] = nativaSinValor(None, Expresion.TOSTRING.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOLOWERCASE(t):
        '''
            tolowercase : RLC PARENI PAREND
        '''
        t[0] = nativaSinValor(None, Expresion.TOLOWERCASE.value , t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOUPPERCASE(t):
        '''
            touppercase : RUC PARENI PAREND
        '''
        t[0] = nativaSinValor(None, Expresion.TOUPPERCASE.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_SPLIT(t):
        '''
            split : RSPLIT PARENI expresion PAREND
        '''
        t[0] = nativasVector(None, t[3], Expresion.SPLIT.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_CONCAT(t):
        '''
            concat : RCONCAT PARENI listaExpresiones PAREND
        '''
        t[0] = nativasVector(None, t[3], Expresion.CONCAT.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))



    #Errores Sintaxis--------------------------------------------------------------------------------
    def p_error(t):

        if t is not None:
            if t.type == 'error':
                mensaje = "Token Inesperado: " + t.value
                tipo = "Lexico"
            else:
                mensaje = "Token Inesperado: " + t.value
                tipo = "Sintactico"

            Analizador.arbol.añadirError(tipo, mensaje, t.lineno, t.lexpos)
            Analizador.parser.errok()
        else:
            mensaje = "Token Inesperado: " + t.value
            tipo = "Sintactico"
            Analizador.arbol.añadirError(tipo, mensaje, t.lineno, t.lexpos)

    parser = yacc.yacc(debug=True)

    def analizar(self, Entrada):
        Analizador.lexer.lineno = 1
        Analizador.input = Entrada

        if len(Entrada) == 0:
            mensaje = "La Cadena está vacía"
            Analizador.arbol.añadirError("Lexico", mensaje, 0, 0)
            return Analizador.arbol

        return Analizador.parser.parse(Entrada)


