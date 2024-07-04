# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 17:27:45 2021

@author: ABEA

Message of the day code. Escribe un mensaje y lo guarda en una base de datos oculta.

Puedes 

"""
from datetime import datetime
import sqlite3

import sys
from PyQt5 import QtWidgets as qtw, QtCore

class MiApp(qtw.QWidget):
    def __init__(self):
        qtw.QWidget.__init__(self)
        
        lay = qtw.QVBoxLayout()
        self.setLayout(lay)
        self.setWindowTitle("Saludos")
        
        self.l1 = qtw.QLabel("Mensaje del día: Escribe tu mensaje")
        lay.addWidget(self.l1)
        
        self.caja_texto = qtw.QTextEdit()
        lay.addWidget(self.caja_texto)
        
        
        lay_under = qtw.QHBoxLayout()
        self.b3 = qtw.QPushButton("Enviar Mensaje") # confirmacion
        self.b2 = qtw.QPushButton("Leer un mensaje")    # Leer un mensaje aleatorio
        self.b1 = qtw.QSlider()
        
        self.b1.setMinimum(-5)
        self.b1.setMaximum(5)
        self.b1.setValue(0)
        self.b1.setTickPosition(qtw.QSlider.TicksRight)
        self.b1.setTickInterval(1)
        
        lay_under.addWidget(self.b1)
        lay_under.addWidget(self.b2)
        lay_under.addWidget(self.b3)
        lay.addLayout(lay_under)

        self.b2.clicked.connect(self.leer_mensaje)
        self.b3.clicked.connect(self.push_msg)
    # TODO read rating    
        
        #self.dlg.buttonClicked.connect(msgbtn)
    
    def push_msg(self):
        self.caja_texto.setDisabled(True)
        self.b3.setDisabled(True)
        ahora = datetime.today().strftime("%H:%M - %D")
        msg = self.caja_texto.toPlainText()
        rating = self.b1.value()
        a = {'fecha': ahora, 'mensaje': msg, 'rating': rating}
        with conn:
            c.execute("INSERT INTO mensajes VALUES (:fecha, :mensaje, :rating)", a)
        
        self.caja_texto.setText("Mensaje Cargado")
        
        
    def leer_mensaje(self):
        c.execute("SELECT * FROM mensajes ORDER BY RANDOM() LIMIT 1")
        data = c.fetchall() #data = ["1/1/1",'mensaje de prueba',0.5]
        dlg = qtw.QMessageBox()
        # dlg.setIcon(QMessageBox.Information)
        print(data)
        fecha, msg, rating = data[0]
        dlg.setText(f"Mensaje escrito en {fecha}:")
        dlg.setInformativeText(msg)
        dlg.setWindowTitle("MOTD")
        #self.dlg.setDetailedText("The details are as follows:")
        dlg.setStandardButtons(qtw.QMessageBox.Ok | qtw.QMessageBox.Cancel)
        dlg.exec_()
        

conn = sqlite3.connect('motd.db')

c = conn.cursor() # cursor ?

# c.execute("""CREATE TABLE mensajes ( # all caps for sql code
#             fecha text,
#             mensaje text,
#             rating real
#             )""")

# Estas funciones no las uso
def add_msg(msg, rating=-1):
    ahora = datetime.today().strftime("%H:%M - %D")
    a = {'fecha': ahora, 'mensaje': msg, 'rating': rating}
    with conn:
        c.execute("INSERT INTO mensajes VALUES (:fecha :mensaje, :rating)", a)
    #conn.commit()

def retrieve_msg():
    #c.execute("SELECT * FROM mensajes")
    c.execute("SELECT * FROM mensajes ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    print(data)

def update_msg(msg):
    raise NotImplementedError()

def delete_msg(fecha):
    raise NotImplementedError()
    with conn:
        c.execute("DELETE FROM mensajes WHERE fecha = :fecha", {'fecha':fecha})
#conn.commit()
       
app = qtw.QApplication(sys.argv)
window = MiApp()
window.show()

app.exec_()

conn.close()

sys.exit()
    
