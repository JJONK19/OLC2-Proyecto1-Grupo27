from enum import Enum

class Clases(Enum):
    '''
        Indica el tipo de datos que se maneja en el lenguaje. Puede ser primitivo, vector, struct, objeto, etc.
    '''
    PRIMITIVO = "PRIMITIVO"
    VECTOR = "VECTOR"
    STRUCT = "STRUCT"
    ANY = "ANY"
    NULL = "NULL"

class Tipo(Enum):
    '''
        Indica el tipado que se maneja en el lenguaje. Puede ser string, int, bool, etc.
    '''
    NULL = "NULL"
    ANY = "ANY"
    NUMBER = "NUMBER"
    BOOLEAN = "BOOLEAN"
    STRING = "STRING"

class Accesos(Enum):
    '''
        Se usa como auxiliar para determinar si la clase acceso es una posicion o un atributo.
    '''
    ATRIBUTO = "ATRIBUTO"
    POSICION = "POSICION"

class Instrucciones(Enum):
    '''
        Indica y separa los tipos de instruccion que pueden venir en la ejecucion.
    '''
    PRINT = "PRINT"
    OPERACION = "OPERACION"
    DATO = "DATO"
    DECLARACION_PRIMITIVA = "DECLARACION_PRIMITIVA"
    DECLARACION_VECTOR = "DECLARACION_VECTOR"
    DECLARACION_ANY = "DEFINICION_ANY"
    DEFINICION_STRUCT = "DEFINICION_STRUCT"
    DEFINICION_ATRIBUTO = "DEFINICION_ATRIBUTO"
    DECLARACION_STRUCT = "DECLARACION_STRUCT"
    DECLARACION_ATRIBUTO = "DECLARACION_ATRIBUTO"
    SI = "SI"
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    RETURN = "RETURN"
    WHILE = "WHILE"
    FOR = "FOR"
    FOROF = "FOROF"
    LLAMADA_FUNCION = "LLAMADA_FUNCION"
    DECLARACION_FUNCION = "DECLARACION_FUNCION"
    


class Expresion(Enum):
    '''
        Indica y separa los tipos de expresion que pueden venir en la ejecucion.
    '''
    SUMA = "SUMA"
    RESTA = "RESTA"
    MULTIPLICACION = "MULTIPLICACION"
    DIVISION = "DIVISION"
    UNARIO = "UNARIO"
    MOD = "MOD"
    POT = "POT"
    NOT = "NOT"
    IGUALACION = "IGUALACION"
    DISTINTO = "DISTINTO"
    MAYORQ = "MAYORQ"
    MENORQ = "MENORQ"
    MAYORIG = "MAYORIG"
    MENORIG = "MENORIG"
    OR = "OR"
    AND = "AND"
    TOFIXED = "TOFIXED"
    TOEXPONENTIAL = "TOEXPONENTIAL"
    TOSTRING = "TOSTRING"
    TOLOWERCASE = "TOLOWERCASE"
    TOUPPERCASE = "TOUPPERCASE"
    SPLIT = "SPLIT"
    CONCAT = "CONCAT"
    INCREMENTO = "INCREMENTO"
    DECREMENTO = "DECREEMENTO"
    PUSH = "PUSH"
    LENGTH = "LENGTH"
    TYPEOF = "TYPEOF"