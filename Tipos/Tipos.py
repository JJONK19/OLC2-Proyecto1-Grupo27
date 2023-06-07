from enum import Enum

class Clases(Enum):
    '''
        Indica el tipo de datos que se maneja en el lenguaje. Puede ser primitivo, vector, struct, objeto, etc.
    '''
    PRIMITIVO = "PRIMITIVO"
    VECTOR = "VECTOR"
    STRUCT = "STRUCT"
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