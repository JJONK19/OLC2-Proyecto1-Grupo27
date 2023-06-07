from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
import sys
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
from Analizador import Analizador

class ventana (QtWidgets.QMainWindow):

    def __init__(self):
        super(ventana, self).__init__()
        uic.loadUi('Ventana.ui', self)
        self.BEditor.clicked.connect(lambda: self.Vistas.setCurrentIndex(0))
        self.BSimbolos.clicked.connect(lambda: self.Vistas.setCurrentIndex(1))
        self.BErrores.clicked.connect(lambda: self.Vistas.setCurrentIndex(2))
        self.BAST.clicked.connect(lambda: self.Vistas.setCurrentIndex(3))
        self.BInfo.clicked.connect(lambda: self.Vistas.setCurrentIndex(4))
        self.BAnalizar.clicked.connect(self.analizar)
        self.BAbrir.clicked.connect(self.abrir)
        self.BGuardar.clicked.connect(self.guardar)
        self.BGuardarComo.clicked.connect(self.guardarComo)
        self.BLimpiar.clicked.connect(self.limpiar)

        #Manejo de los editores
        font = QFont()
        font.setPointSize(12)
        font.setFamily('Courier')
        font.setFixedPitch(True)
        self.Consola.setReadOnly(True)
        self.Consola.setFont(font)
        self.Entrada.setFont(font)

        #Variables de la aplicación
        self.ENTRADA = ""                #Texto ubicado en el espacio de entrada
        self.SALIDA = ""                 #Texto a colocar en la consola
        self.RUTA = ""                   #Ruta del archivo que se leyo
        self.show()

    def analizar(self):
        """
        analizar toma el texto ubicado en Entrada y lo manda a analizar. Este metodo prepara
        y distribuye la información por toda la aplicación.

        """
        #--- Recopilar el texto
        self.ENTRADA = self.Entrada.toPlainText()
        print("//////////////////////////////////////////////////")
        print(self.ENTRADA)
        print("//////////////////////////////////////////////////")

        #--- Limpiar la tabla de simbolos
        self.TSimbolos.clearContents()
        self.TSimbolos.setRowCount(0)

        #--- /Limpiar la tabla de errores
        self.TErrores.clearContents()
        self.TErrores.setRowCount(0)

        #--- Analizar cadena
        Interprete = Analizador()
        Salida = Interprete.analizar(self.ENTRADA)

        #Errores
        for i in Salida.getErrores(): 
            print(i.descripcion)

        for i in Salida.instrucciones: 
            print(i)

        #--- MOSTRAR EL CONTENIDO EN LA CONSOLA
        self.Consola.setPlainText(Salida.getConsola())

        """
        #--- Añadir los simbolos encontrados
        for temp in Interprete.Simbolos:
            col = 0
            fila = self.TSimbolos.rowCount()
            self.TSimbolos.setRowCount(fila + 1)

            id = QTableWidgetItem()
            tipo = QTableWidgetItem()
            dato = QTableWidgetItem()
            entorno = QTableWidgetItem()
            linea = QTableWidgetItem()
            columna = QTableWidgetItem()

            id.setText(temp.id)
            tipo.setText("Variable")
            dato.setText(temp.tipo)
            entorno.setText(temp.entorno)
            linea.setText(str(temp.linea))
            columna.setText(str(temp.columna))

            self.TSimbolos.setItem(fila, 0, id)
            self.TSimbolos.setItem(fila, 1, tipo)
            self.TSimbolos.setItem(fila, 2, dato)
            self.TSimbolos.setItem(fila, 3, entorno)
            self.TSimbolos.setItem(fila, 4, linea)
            self.TSimbolos.setItem(fila, 5, columna)

        #--- Añadir los metodos
        for temp in Interprete.Metodos:
            col = 0
            fila = self.TSimbolos.rowCount()
            self.TSimbolos.setRowCount(fila + 1)

            id = QTableWidgetItem()
            tipo = QTableWidgetItem()
            dato = QTableWidgetItem()
            entorno = QTableWidgetItem()
            linea = QTableWidgetItem()
            columna = QTableWidgetItem()

            id.setText(temp.id)
            tipo.setText("Metodo")
            dato.setText(temp.tipo)
            entorno.setText("")
            linea.setText(str(temp.linea))
            columna.setText(str(temp.columna))

            self.TSimbolos.setItem(fila, 0, id)
            self.TSimbolos.setItem(fila, 1, tipo)
            self.TSimbolos.setItem(fila, 2, dato)
            self.TSimbolos.setItem(fila, 3, entorno)
            self.TSimbolos.setItem(fila, 4, linea)
            self.TSimbolos.setItem(fila, 5, columna)

        #--- Aañdir los errores
        for temp in analizador.Errores:
            fila = self.TErrores.rowCount()
            self.TErrores.setRowCount(fila + 1)

            tipo = QTableWidgetItem()
            descripcion = QTableWidgetItem()
            linea = QTableWidgetItem()
            columna = QTableWidgetItem()

            tipo.setText(temp.tipo)
            descripcion.setText(temp.descripcion)
            linea.setText(str(temp.linea))
            columna.setText(str(temp.columna))

            self.TErrores.setItem(fila, 0, tipo)
            self.TErrores.setItem(fila, 1, descripcion)
            self.TErrores.setItem(fila, 2, linea)
            self.TErrores.setItem(fila, 3, columna)

        #--- Añadir el grafo
        pixmap = QPixmap("arbol.png");
        self.ImagenLabel.setPixmap(pixmap);
        self.ImagenLabel.setMask(pixmap.mask());

        """

    def limpiar(self):
        """
        limpiar borra toda la información almacenada en la consola y en las tablas.

        """
        self.Entrada.setPlainText("")
        self.Consola.setPlainText("")

    def abrir(self):
        """
        abrir: Abre un archivo y lo coloca en el editor de texto. Utiliza leerArchivos como auxiliar.

        """
        file_dialog = QFileDialog(self)
        file_dialog.fileSelected.connect(self.leerArchivos)
        file_dialog.exec_()

    def leerArchivos(self, ruta):
        self.RUTA = ruta
        with open(ruta, 'r') as f:
            texto = f.read()
            self.Entrada.setPlainText(texto)

    def guardar(self):
        """
        guardar: Guarda el contenido del editor. Si el texto se extrajo de un archivo, se sobreescribe. 
        Si no, crea un nuevo archivo. 

        """
        contenido = self.Entrada.toPlainText()

        if self.RUTA != "":
            with open(self.RUTA, 'w') as archivo:
                archivo.write(contenido)        
        else:
            ruta, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", "", "Archivo de texto (*.txt)")
            if ruta:
                self.RUTA = ruta
                with open(ruta, 'w') as file:
                    file.write(contenido)    

    def guardarComo(self):
        """
        guardarComo: Guarda el contenido del editor. Crea un nuevo archivo. 

        """
        contenido = self.Entrada.toPlainText()
        ruta, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", "", "Archivo de texto (*.txt)")
        if ruta:
            self.RUTA = ruta
            with open(ruta, 'w') as file:
                file.write(contenido)    

app = QtWidgets.QApplication(sys.argv)
main = ventana()
sys.exit(app.exec_())

