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
from Instruccion.DatoVector import datoVector

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
        'concat' : 'RCONCAT'
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
        ('left', 'COMA'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('right', 'NOT'),
        ('left', 'IGUALACION', 'DISTINTO'),
        ('left', 'MENORQ', 'MAYORQ', 'MAYORIG', 'MENORIG'),
        ('left', 'MAS', 'MENOS'),
        ('left', 'MUL', 'DIV', 'MOD'),
        ('left', 'PARENI', 'PAREND'),
        ('left', 'POT'),
        ('right', 'UNARIO'),
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
    def p_SENTENCIAS_PRINT(t): #QUITAR
        '''
            sentencia : print PTCOMA
                        | expresion PTCOMA
        '''
        t[0] = t[1]

    def p_SENTENCIAS_DECLARACIONES(t): #QUITAR
        '''
            sentencia : declaraciones PTCOMA
        '''
        t[0] = t[1]

    #Declaraciones----------------------------------------------------------------------------------
    def p_DECLARACION_PRIMITIVA1(t):
        '''
            declaraciones : RLET ID DOSPTS tipo IGUAL expresion 
                    | RLET ID 
        '''
        if len(t) == 8:
            t[0] = DeclaracionPrimitiva(t[2],t[4],t[6],t.lineno(1),
                                        Analizador.find_column(Analizador.input, t.lexpos(1)))
        else:
            t[0] = DeclaracionPrimitiva(t[2], Tipo.ANY.value, "None", t.lineno(1),
                                        Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_DECLARACION_PRIMITIVA2(t):
        '''
            declaraciones : RLET ID IGUAL expresion 
        '''
        t[0] = t[1]

    def p_DECLARACION_PRIMITIVA3(t):
        '''
            declaraciones : RLET ID DOSPTS tipo 
        '''
        t[0] = t[1]

    def p_DECLARACION_INTERFACE(t):
        """
            declaraciones : RINTERFACE ID LLAVEI atributos LLAVED
        """
        t[0] = t[2]

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

    def p_DECLARACION_INTERFACE_ATRIBUTO(t):
        """
            atributo : ID DOSPTS tipo PTCOMA 
        """
        t[0] = t[1]

    #Tipo ----------------------------------------------------------------------------------
    def p_TIPO_STRING(t):
        '''
            tipo : RSTRING
        '''

        t[0] = Tipo.STRING.value

    def p_TIPO_ANY(t):
        '''
            tipo : RANY
        '''

        t[0] = Tipo.ANY.value

    def p_TIPO_NUMBER(t):
        '''
            tipo : RNUMBER
        '''

        t[0] = Tipo.NUMBER.value

    def p_TIPO_BOOLEAN(t):
        '''
            tipo : RBOOLEAN
        '''

        t[0] = Tipo.BOOLEAN.value

    #Print-------------------------------------------------------------------------------------------
    def p_PRINT_SIMPLE(t):
        """
            print : RCONSOLE PT RLOG PARENI listaExpresiones PAREND
        """
        t[0] = imprimir(t[5], t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1))) 
    
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
            tofixed : expresion PT RFIXED PARENI expresion PAREND 
        '''
        t[0] = nativaConValor(t[1], t[5], Expresion.TOFIXED.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOEXPONENTIAL(t):
        '''
            toexponential : expresion PT REXPONENTIAL PARENI expresion PAREND 
        '''
        t[0] = nativaConValor(t[1], t[5], Expresion.TOEXPONENTIAL.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOSTRING(t):
        '''
            tostring : expresion PT RTSTRING PARENI PAREND 
        '''
        t[0] = nativaSinValor(t[1], Expresion.TOSTRING.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOLOWERCASE(t):
        '''
            tolowercase : expresion PT RLC PARENI PAREND 
        '''
        t[0] = nativaSinValor(t[1], Expresion.TOLOWERCASE.value , t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_TOUPPERCASE(t):
        '''
            touppercase : expresion PT RUC PARENI PAREND 
        '''
        t[0] = nativaSinValor(t[1], Expresion.TOUPPERCASE.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_SPLIT(t):
        '''
            split : expresion PT RSPLIT PARENI expresion PAREND 
        '''
        t[0] = nativasVector(t[1], t[5], Expresion.SPLIT.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))

    def p_NATIVA_CONCAT(t):
        '''
            concat : expresion PT RCONCAT PARENI listaExpresiones PAREND
        '''
        t[0] = nativasVector(t[1], t[5], Expresion.CONCAT.value, t.lineno(1), Analizador.find_column(Analizador.input, t.lexpos(1)))



    #Errores Sintaxis--------------------------------------------------------------------------------
    def p_error(t):
        mensaje = "Token Inesperado: " + t.value
        Analizador.arbol.añadirError("Sintaxis", mensaje, t.lineno, t.lexpos)    
        
        #Verficar que el archivo no ha acabado
        if not t:
            return Analizador.arbol
 
        while True:
            nextToken = Analizador.parser.token()            
            if not nextToken or nextToken.type == 'PTCOMA':
                break
        Analizador.parser.restart()

    parser = yacc.yacc()

    def analizar(self, Entrada):
        Analizador.lexer.lineno = 1
        Analizador.input = Entrada

        if len(Entrada) == 0:
            mensaje = "La Cadena está vacía"
            Analizador.arbol.añadirError("Lexico", mensaje, 0, 0)
            return Analizador.arbol

        return Analizador.parser.parse(Entrada)


