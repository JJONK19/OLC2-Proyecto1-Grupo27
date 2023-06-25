class simbolo3D:
    '''
        Almacena la informacion relevante de una variable en la traduccion del codigo.
        - ID : Nombre de la variable.
        - Tipo : Tipo de la variable
        - Clase : Clase de la variable (Primitivo, Struct, Vector o Any)
        - Tipo Valor: Variable con el tipo del contenido. Sirve para Any.
        - Clase Valor: Variable con la clase del contenido. Sirve para Any.
        - Clase Contenido: Auxiliar en vectores: Indica que es lo que guarda.
        - Posicion Stack: Indica la posicion de la variable en el stack. Es su posicion relativa en el entorno.
        - Esta en heap: Indica si la variable esta en el heap (o sea, si es un vector,un struct o string).
        -esReeferencia: Indica si la variable es un puntero a otra variable. EN conjunto con la variable heap,
         se sabe si al usar el valor se extrae el valor del stack de la referencia o se va al heap.
    '''
    def __init__(self, ID, TIPO, CLASE, POSICION, HEAP, TIPO_VALOR = "", CLASE_VALOR = "", CLASE_CONTENIDO = "", REFERENCIA = False):
        self.id = ID
        self.tipo = TIPO        
        self.clase = CLASE          
        self.tipoValor = TIPO_VALOR
        self.claseValor = CLASE_VALOR
        self.claseContenido = CLASE_CONTENIDO
        self.posicionStack = POSICION
        self.estaEnHeap = HEAP
        self.esReferencia = REFERENCIA 

        #Para el return se crea una variable en la tabla de simbolos. 
        self.returnAsignado = False
