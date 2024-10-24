####################################################################################################
# Aplicación sencilla para recuadrar texto monoespaciado con opciones de centrado, ajuste de ancho #
# y caracteres personalizados.                                                                     #
#                                                                                                  #
# Autor: Angelo Gallardi (angelogallardi@gmail.com)                                                #
####################################################################################################


from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtCore import QRegExp, QTimer
from PyQt5.QtGui import QRegExpValidator, QIcon
from PyQt5 import uic
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi('recuadrator.ui', self) # Cargo el archivo .ui

        self.setWindowTitle('Recuadrador de texto para código') # Pongo título a la ventana

        self.setWindowIcon(QIcon('icono.ico')) # Establezco el ícono de la ventana

        self.label_copiado.hide() # Oculto inicialmente el QLabel de texto copiado

        # Restrinjo los QLineEdit a un solo caracter
        regex = QRegExp(r'.{1}')
        validator = QRegExpValidator(regex)
        self.lineEdit_inicio.setValidator(validator)
        self.lineEdit_medio.setValidator(validator)
        self.lineEdit_final.setValidator(validator)

        self.pushButton.clicked.connect(self.recuadrarTexto)


    def recuadrarTexto(self):
        """Se encarga de construir el texto recuadrado."""

        # Obtengo el texto del QPlainTextEdit y lo paso a una lista de líneas
        texto = self.plainTextEdit_entrada.toPlainText().splitlines()

        if texto:
            # Defino variables para recuadro
            pipe = '|'
            num = '#'
            lineas = '¯', '_'

            # Selección de radio buttons para el carácter de inicio
            inicio = (
                pipe if self.radioButton_inicio_pipe.isChecked() else
                num if self.radioButton_inicio_num.isChecked() else
                self.obtenerTexto(self.lineEdit_inicio, 'Debe ingresar algo para el caracter de inicio.')
            )
            if not inicio:
                return # Salgo si falta el dato

            # Selección de radio buttons para el carácter del medio
            if self.radioButton_medio_linea.isChecked():
                medioInicio, medioFinal = lineas
            elif self.radioButton_medio_num.isChecked():
                medioInicio, medioFinal = num, num
            else:
                medio = self.obtenerTexto(self.lineEdit_medio, 'Debe ingresar algo para los caracteres del medio.')
                if not medio:
                    return # Salgo si falta el dato
                medioInicio, medioFinal = medio, medio

            # Selección de radio buttons para el carácter de fin
            fin = (
                pipe if self.radioButton_final_pipe.isChecked() else
                num if self.radioButton_final_num.isChecked() else
                self.obtenerTexto(self.lineEdit_final, 'Debe ingresar algo para el caracter de fin.')
            )
            if not fin:
                return  # Salir si falta el dato

            # Calculo el ancho de las líneas
            lenMax = max(len(string) for string in texto)
            espacioEnElMedio = self.spinBox_ancho.value() if not self.radioButton_ancho.isChecked() else lenMax + 2
            if espacioEnElMedio < lenMax:
                QMessageBox.warning(self, 'Ancho muy pequeño', 'El ancho ingresado es menor al de su texto, por favor ingrese un ancho mayor.')
                return                

            # Construyo el texto recuadrado
            espacioArribaAbajo = f'\n{inicio}{' ' * espacioEnElMedio}{fin}' if self.checkBox_espacios.isChecked() else ''
            primeraLinea = f'{inicio}{medioInicio * espacioEnElMedio}{fin}{espacioArribaAbajo}'
            ultimaLinea = f'{espacioArribaAbajo}\n{inicio}{medioFinal * espacioEnElMedio}{fin}'

            textoMod = primeraLinea
            for linea in texto: # Líneas del medio
                if self.checkBox_centrar.isChecked():
                    textoMod += f'\n{inicio}{linea.center(espacioEnElMedio)}{fin}'
                else:
                    textoMod += f'\n{inicio} {linea}{' '*(espacioEnElMedio-1-len(linea))}{fin}'
            textoMod += ultimaLinea

            # Lo muestro en la salida
            self.plainTextEdit_salida.setPlainText(textoMod)

             # Copio el texto al portapapeles
            clipboard = QApplication.clipboard()
            clipboard.setText(self.plainTextEdit_salida.toPlainText())

            # Muestro la etiqueta de texto copiado por 2 segundos
            self.mostrarEtiqueta()


    def obtenerTexto(self, lineEdit, mensaje):
        """Valida y obtiene el texto de los QLineEdit de caracteres."""

        texto = lineEdit.text().strip() # Elimino espacios
        if texto:
            return texto
        else:
            QMessageBox.warning(self, 'Falta un dato', mensaje)
            return None


    def mostrarEtiqueta(self):
        """Muestra el QLabel de copiado y lo oculta después de 2 segundos."""

        self.label_copiado.show()
        QTimer.singleShot(2000, self.label_copiado.hide)


# Inicializo la app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())