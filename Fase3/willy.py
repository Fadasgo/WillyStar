# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'willy.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime,Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui 
from PyQt5.QtGui import QIcon
import sys
import ply.lex as lex
import lexer
import parser
import logging
import semantic
from time import sleep
import os

counter = [-1]
def main(argv):
    if (len(argv) >= 1):
        try:
            f = open(argv[0], 'r')
        except FileExistsError as e:
            print('Ha ocurrido un error al abrir el archivo:', e)
            sys.exit()
        data = f.read()
        app = QtWidgets.QApplication(sys.argv)
        f.close()

        # tarea
        tarea = argv[1]
        global flag
        # flags
        if (argv[2] == '-a' or argv[2] == '--auto'):
            flag = 'auto'
            if (len(argv) == 4):
                segundos = argv[3]
                # manejo formato segundos
                print(segundos.isdigit())
                if (segundos.isdigit()):
                    segundos = int(segundos)
                else:
                    segundos = None
                    print('Los segundos deben ser numeros')
                    sys.exit()
            else:
                segundos = None
            # print(flag)


        elif (argv[2] == '-m' or argv[2] == '--manual'):
            flag = 'manual'
            if (len(argv) == 4):
                print('Error con operacion manual no es necesario segundos')
                sys.exit()
            else:
                segundos = None

        # Build lexer
        myLexer = lexer.lexer()

        program_tokens, errors = lexer.tokenize(myLexer, data)

        if len(errors) > 0:
            for err in errors:
                print(err)
            sys.exit()

        # Build parser
        log = logging.getLogger()
        myParser = parser.parser()
        result_tree = myParser.parse(data, lex, debug=log)

        global mySemantic
        mySemantic = semantic.semantic(tarea, flag, segundos)
        mySemantic.execute(result_tree)


        # si argv tarea esta en las tareas se abre la interfaz
        if (tarea in mySemantic.tareas):
            # abrir interfaz
            # print(mySemantic.tareas[tarea].__dict__)
            MainWindow = QtWidgets.QMainWindow()
            ui = Ui_MainWindow()
            ui.setupUi(MainWindow, mySemantic)
            MainWindow.show()
            sys.exit(app.exec_())
            #print_node_recursive(result_tree)
    else:
        print('Faltan argumentos')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, mySemantic):
        MainWindow.setObjectName("Willy*")
        MainWindow.resize(1066, 647)
        self.t1 = mySemantic.tareas[mySemantic.tarea]
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 60, 1041, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(self.t1.size[0])
        self.tableWidget.setRowCount(self.t1.size[1])
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(490, 0, 421, 61))
        self.label.setObjectName("label")
        self.Next = QtWidgets.QPushButton(self.centralwidget)
        self.Next.setGeometry(QtCore.QRect(540, 560, 93, 28))
        self.Next.setObjectName("Next")
        
        self.Next.clicked.connect(self.clicked)

        self.segundos = QtWidgets.QLCDNumber(self.centralwidget)
        self.segundos.setGeometry(QtCore.QRect(940, 10, 64, 23))
        self.segundos.setObjectName("segundos")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1066, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionopen_file = QtWidgets.QAction(MainWindow)
        self.actionopen_file.setObjectName("actionopen_file")
        self.loadTable(mySemantic)
        self.menuFile.addAction(self.actionopen_file)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Bienvenido a Willy*"))
        self.Next.setText(_translate("MainWindow", "Next"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionopen_file.setText(_translate("MainWindow", "open file"))

    # Para el caso de auto sin pasarle un argumento de segundos
    def loadTable(self, mySemantic):
        if (mySemantic.flag == 'auto' and mySemantic.segundos == None):
            QMessageBox.about(self.tableWidget,"Inicio", "Para poder visualizar mejor el contenido de las casillas, puede ampliar las filas y columnas acercando el mouse a los bordes de la tabla.\n (cualquier casilla que se vea con ... es necesario ampliarla para ver su contenido)")
            posicion = mySemantic.tareas[mySemantic.tarea].position
            interface = mySemantic.impresion[len(mySemantic.impresion) - 1]
            self.updateTable(interface)
            if (mySemantic.finalGoal == True):
                message = "Se cumplio el final goal!!"
            else:
                message = "Se fallo en cumplir el final goal!"
            QMessageBox.about(self.tableWidget,"Recorrido Culminado", message)
        
        elif (mySemantic.flag == 'auto' and isinstance(mySemantic.segundos, int)):
            self.count = 0
            self.tmr = QtCore.QTimer()
            # tmr.setSingleShot(True)
            self.tmr.timeout.connect(lambda: self.updateTableTimer())
            self.tmr.start(mySemantic.segundos * 1000)
              
    def updateTable(self, interface):
        for fila in range(len(interface.world)):
            for col in range(len(interface.world[fila])):
                willyLocation = (col == interface.willyCol - 1 and fila == mySemantic.willyIndexToMatrixUI(len(interface.world),interface.willyFil) )
                string = ""
                if (willyLocation):
                    string = "willy"
                    self.tableWidget.setItem(fila,col,QTableWidgetItem('willy'))
                if (type(interface.world[fila][col]) == list):
                    for x in interface.world[fila][col]:
                        if (string == 'willy'):
                            string = string + "\n"
                        string = string + x.id +"("+str(x.quantity)+")" + "\n" 
                    self.tableWidget.setItem(fila, col, QTableWidgetItem(string))
                elif (type(interface.world[fila][col]) == str):
                    self.tableWidget.setItem(fila, col, QTableWidgetItem(interface.world[fila][col]))

                elif (type(interface.world[fila][col]) == int and not willyLocation):
                    self.tableWidget.setItem(fila, col, QTableWidgetItem(" "))
        self.tableWidget.update()

    def updateTableTimer(self):
        if (self.count == len(mySemantic.impresion)):
            self.tmr.stop()
            self.tmr.deleteLater()
            if (mySemantic.finalGoal == True):
                message = "Se cumplio el final goal!!"
            else:
                message = "Se fallo en cumplir el final goal!"
            QMessageBox.about(self.tableWidget,"Recorrido Culminado", message)
            # sys.exit()
        else:
            current = mySemantic.impresion[self.count]
            self.label.setText("Instruction: " + current.instruction) # set label to instruction
            self.segundos.display(self.count * mySemantic.segundos) # set segundos box to time pased
            self.updateTable(current)
            self.count = self.count + 1


    # Version manual,por click
    # Se decidio agregar tambien al auto de cuando se le pasan los segundos, por problemas con QTimer
    def clicked(self):
        if flag == 'manual':
            if counter[0] == 0:
                QMessageBox.about(self.tableWidget,"Inicio", "Para poder visualizar mejor el contenido de las casillas, puede ampliar las filas y columnas acercando el mouse a los bordes de la tabla.\n (cualquier casilla que se vea con ... es necesario ampliarla para ver su contenido)")
            counter[0] = counter[0] + 1
            #print(str(counter[0]))
            # Verificar si es el flag con click
            if counter[0] < len(mySemantic.impresion):
                posicion = mySemantic.tareas[mySemantic.tarea].position
                interface = mySemantic.impresion[counter[0]]
                self.label.setText("Instruction: " + interface.instruction) # set label to instruction
                self.updateTable(interface)

            elif len(mySemantic.impresion) + 1 == counter[0]:
                print("Ya se recorrieron todos los pasos \n")
                messageNext = "Si vuelve a presionar Next, se cerrara la ventana"
                if (mySemantic.finalGoal == True):
                    message = "Se cumplio el final goal!! \n" + messageNext
                else:
                    message = "Se fallo en cumplir el final goal! \n" + messageNext
                QMessageBox.about(self.tableWidget,"Recorrido Culminado", message)
            
            elif len(mySemantic.impresion) + 2 == counter[0]:
                sys.exit()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])

