#!/usr/bin/python3

import sys
import re
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QPen
from pathlib import Path
highttt=0
mod=0


class Paint(QWidget):
	def __init__(self):
		
		super().__init__()
	def paintEvent(self, event):
		global highttt, mod


		
		painter = QPainter(self)
		#painter.translate(0, 30)
		#painter.combinedTransform()
		painter.transform()
		painter.setWindow(5, 0, 100, highttt*10)
		#painter.device(width(100))
		#painter.boundingRect(1, 1, x-1, y-1, 5 ,"gg")
		painter.drawRect(5, 0, 100, highttt*10)
		painter.setBrush(QColor(200, 0, 0))
		painter.drawRect(5, highttt*10, 100, -(mod)*10)
		pen = QPen(Qt.black, 2, Qt.SolidLine)
		painter.setPen(pen)
		for i in range(0,highttt+1):
			
			painter.drawLine(5, (i)*10, 30, (i)*10)
			
		
		
		
class AnotherWindow(QWidget):

	def __init__(self):
		super().__init__()
	
		self.initUI()
	def initUI(self):
		
		hbox = QVBoxLayout(self)
		pixmap = QPixmap('qt.png')
		lbl = QLabel(self)
		lbl1 = QLabel("О программе")
		lbl.setPixmap(pixmap)
		qbtn = QPushButton('Quit', self)
	
		qbtn.clicked.connect(self.close)
		
		qbtn.resize(qbtn.sizeHint())
		
		hbox.addWidget(lbl1)
		hbox.addWidget(lbl)
		hbox.addWidget(qbtn)
		
		
		self.setLayout(hbox)
		self.move(300, 200)
		self.setWindowTitle('About')
		
		
        
class Example(QMainWindow):
	
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		self.p = Paint()
		g=QWidget()
		topr=QWidget()
		hbox = QHBoxLayout()
		vbox = QVBoxLayout()
		grid = QGridLayout()
		#g.setLayout(grid)
		self.setCentralWidget(g)
		#сетка
		self.textEdit1 = QTextEdit()
		self.textEdit2 = QTextEdit()
		self.titleEdit1 = QLineEdit()
		self.titleEdit2 = QLineEdit()
		button1 = QPushButton("...")
		button1.clicked.connect(self.openDialog)
		button2 = QPushButton("OK")
		button2.clicked.connect(self.modules)
		button2.clicked.connect(self._otobrazhenie)
		hbox.addWidget(self.textEdit1)
		hbox.addWidget(topr)
		vbox.addLayout(hbox)
		vbox.addWidget(self.textEdit2)
		
		grid.addWidget(self.titleEdit1, 1, 1)
		grid.addWidget(self.titleEdit2, 5, 1)
		grid.addWidget(button1, 1, 9)
		grid.addWidget(self.p, 2, 1, 2, 9)
		grid.addWidget(button2, 5, 9)
		topr.setLayout(grid)
		#меню
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('File')
		m1 = QAction('Open', self)
		m1.triggered.connect(self.openDialog)
		m2 = QAction('Save', self)
		m2.triggered.connect(self.saveDialog)
		m3 = QAction('Exit', self)
		m3.triggered.connect(self.close)
		m4 = QAction('About', self)
		m4.triggered.connect(self.abouthelp)
		fileMenu.addAction(m1)
		fileMenu.addAction(m2)
		fileMenu.addSeparator()
		fileMenu.addAction(m3)
		fileMenu1 = menubar.addMenu('Help')
		fileMenu1.addAction(m4)
		g.setLayout(vbox)
		#осн окно
		self.setGeometry(300, 300, 850, 820)
		self.setWindowTitle('Cool')
		self.show()
	    	
	def abouthelp(self, checked):

		
		self.textEdit2.insertPlainText("Открытие окна Help\n")
		
		self.w = AnotherWindow()
		self.w.show()
	def openDialog(self):
		self.textEdit2.insertPlainText("__________________________________\nОткрытие нового файла\n")
		self.textEdit1.setText("")
		home_dir = str(Path.home())
		fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "*.v *.sv")
		if fname[0]:
			f = open(fname[0], 'r')
					
			with f:
				data = f.read()
				for line in data.splitlines():
					
					if re.search("//", line):
						newline =re.split(r"//", line)
						
						
						self.textEdit1.insertPlainText("{}\n".format(newline[0]))
						#self.textEdit1.insertPlainText("\n")
					else:
						self.textEdit1.insertPlainText("{}\n".format(line))
						#self.textEdit1.insertPlainText(line)
						#self.textEdit1.insertPlainText("\n")
					
				name=re.search('/((\w+).\w+)$', fname[0])
				self.titleEdit1.setText(name.group(1))
				self.textEdit2.insertPlainText("Выбран файл: {}\n".format(name.group(1)))
				
				
			f.close()	
	def saveDialog(self):
		
		home_dir = str(Path.home())
		fsname = QFileDialog.getSaveFileName(self, 'Save file', home_dir)
		if fsname[0]:
	    		f = open(fsname[0], 'w')
	    		text = self.textEdit1.toPlainText()
	    		f.write(text)
	    		f.close()
	    		self.textEdit2.insertPlainText("Файл сохранен: {}\n".format(fsname[0]))
	    		
	def modules(self):
		global highttt, mod
		text = self.textEdit1.toPlainText().split('\n')
		n=0
		names=[]
		for line in text:
			if (re.match('module\s(\w+)', line)):
				n=0
				name = re.match('module\s(\w+)', line)
				names.append(name.group(1))
				n = 1
				
			
			elif (re.match('endmodule', line)):
				n += 1
				
				names.append(n)
			else:	
				n += 1
								
		print(names)
		highttt=0
		mod=0
		self.textEdit2.insertPlainText("Всего модулей: {} \n".format((len(names))//2))	
		self.textEdit2.insertPlainText("---------------------------\n{}\n---------------------------\n".format(names))
			
		for i in names:
			if type(i)==int and i>highttt:
				highttt=i
				
		self.textEdit2.insertPlainText("Наибольший модуль занимает {} строк\n".format(highttt))				
		module = self.titleEdit2.text()
		if module=="":
			module="модуль не выбран"
			
		self.textEdit2.insertPlainText("Выбран модуль: {} \n".format(module))
		if module in names:
			for i in range(len(names)):
				if names[i]==module:
					mod=names[i+1]
					self.textEdit2.insertPlainText("Выбранный модуль занимает {} строк\n".format(mod))
				
		else:		
			self.textEdit2.insertPlainText("Введенного модуля нет в файле\n")
		
		 
	def _otobrazhenie(self):
		self.resize(850, 822)
		self.resize(850, 820)		
			 	
	
    	


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

