import sqlite3
import datetime
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

class Aplicativo():
    def __init__(self):
        self.status_lista = ["","Em Atendimento", "Aguardando resposta do usuário final", "Fechado", "Aguardando parceiro", "Encaminhado", "Aceito", "Resolvido"]
        self.demanda = ""
        self.status = ""
        self.resumo = ""
        self.parceiro = ""
        
        #self.conexao = sqlite3.connect("demandasdb_teste.sqlite3")
        self.conexao = sqlite3.connect("demandasdb.sqlite3")
        self.cursor = self.conexao.cursor()
        
        self.app = QtWidgets.QApplication([])
        self.telaUnica = uic.loadUi("demandas-tela-unica-tabs.ui")
        #self.tela = uic.loadUi("demandas-cadastro.ui")
        #self.tela2 = uic.loadUi("demandas-lista.ui")
        
        self.telaUnica.status_comboBox.addItems(self.status_lista)
        self.telaUnica.cadastrar_button.clicked.connect(self.cadastro)
        self.telaUnica.pesquisar_button.clicked.connect(self.pesquisa)
        self.telaUnica.atualizar_button.clicked.connect(self.atualiza)
        self.telaUnica.limpar_button.clicked.connect(self.limpa_campos)
        self.telaUnica.atualizar_button_2.clicked.connect(self.listar)
        
        self.atualiza_labels()
        
        self.telaUnica.show()
        self.app.exec()


    def atualiza_labels(self):
        self.qtd_total()
        self.qtd_total_fechado()
        self.qtd_total_usuario()
        self.qtd_total_atendimento()
        self.qtd_total_parceiro()
        
        self.telaUnica.qtd_total_label.setText("  TOTAL:  " + str(self.qtd_total()))
        self.telaUnica.qtd_fechada_label.setText(
            "  FECHADAS:  " + str(self.qtd_total_fechado()))
        self.telaUnica.qtd_aguardando_usuario_label.setText(
            "  AGUARDANDO O USUÁRIO:  " + str(self.qtd_total_usuario()))
        self.telaUnica.qtd_aguardando_parceiro_label.setText(
            "  AGUARDANDO PARCEIRO:  " + str(self.qtd_total_parceiro()))
        self.telaUnica.qtd_atendimento_label.setText(
            "  EM ATENDIMENTO:  " + str(self.qtd_total_atendimento()))


    def qtd_total(self):
        self.cursor.execute(f"SELECT COUNT(demanda) FROM ticket")
        qtd = self.cursor.fetchall()
        return qtd[0][0]
    
    
    def qtd_total_fechado(self):
        self.cursor.execute(f"SELECT COUNT(demanda) FROM ticket WHERE status='Fechado'")
        qtd = self.cursor.fetchall()
        return qtd[0][0]
    
    
    def qtd_total_atendimento(self):
        self.cursor.execute(
            f"SELECT COUNT(demanda) FROM ticket WHERE status='Em Atendimento'")
        qtd = self.cursor.fetchall()
        return qtd[0][0]
    
    
    def qtd_total_usuario(self):
        self.cursor.execute(f"SELECT COUNT(demanda) FROM ticket WHERE status='Aguardando resposta do usuário final'")
        qtd = self.cursor.fetchall()
        return qtd[0][0]
    
    
    def qtd_total_parceiro(self):
        self.cursor.execute(f"SELECT COUNT(demanda) FROM ticket WHERE status='Aguardando parceiro'")
        qtd = self.cursor.fetchall()
        return qtd[0][0]
    
    
    def limpa_campos(self):
        self.telaUnica.demanda_input.setText("")
        self.telaUnica.resumo_input.setText("")
        self.telaUnica.parceiro_input.setText("")
        self.telaUnica.status_comboBox.setCurrentText(self.status_lista[0])
        

    def cadastro(self):
        self.demanda = self.telaUnica.demanda_input.text()
        self.status = self.telaUnica.status_comboBox.currentText()
        self.resumo = self.telaUnica.resumo_input.text()
        self.parceiro = self.telaUnica.parceiro_input.text()
        
        if (self.parceiro == ""):
            self.parceiro = "NULL"
            
        self.data = datetime.date.today()
        if (self.data.day < 10) & (self.data.month < 10):
            self.data_formatada = '{}/0{}/{}'.format(
                self.data.day,     self.data.month, self.data.year)
        else:
            self.data_formatada = '{}/{}/{}'.format(
                self.data.day, self.data.month, self.data.year)
    
        try:
            self.cursor.execute(
                f"INSERT INTO 'ticket' ('demanda', 'status', 'resumo', 'data', 'demanda_son') VALUES('{self.demanda}', '{self.status}', '{self.resumo}', '{self.data_formatada}', {self.parceiro})")
            self.conexao.commit()
        except sqlite3.IntegrityError:
            self.msg = f"  ESSA DEMANDA JÁ ESTÁ CADASTRADA: {self.demanda}"
            self.msg_error_box = QMessageBox()
            self.msg_error_box.warning(self.telaUnica, "Error", self.msg)
        
        self.limpa_campos()
        self.atualiza_labels()

        
        
    def pesquisa(self):
        self.demanda = self.telaUnica.demanda_input.text()

        # lendo os dados
        self.cursor.execute(f"SELECT demanda,status,resumo,demanda_son,data from ticket WHERE demanda = '{self.demanda}'")

        for linha in self.cursor.fetchall():
            _,self.status, self.resumo, self.parceiro,_ = linha
            
        #self.telaUnica.demanda_input.setText("demanda")
        self.telaUnica.resumo_input.setText(self.resumo)
        self.telaUnica.parceiro_input.setText(self.parceiro)
        self.indice = self.telaUnica.status_comboBox.findText(self.status)
        self.telaUnica.status_comboBox.setCurrentText(self.status_lista[self.indice])
        
        self.atualiza_labels()
        
        
    def atualiza(self):
        self.demanda = self.telaUnica.demanda_input.text()
        self.status = self.telaUnica.status_comboBox.currentText()
        self.resumo = self.telaUnica.resumo_input.text()
        self.parceiro = self.telaUnica.parceiro_input.text()

        if (self.parceiro == ""):
            self.cursor.execute(
                f"UPDATE ticket SET status='{self.status}', resumo='{self.  resumo}', demanda_son = NULL WHERE demanda='{self.demanda}'")
        else:
            self.cursor.execute(
                f"UPDATE ticket SET status='{self.status}', resumo='{self.  resumo}', demanda_son='{self.parceiro}' WHERE demanda='{self.demanda}'")
            
        self.conexao.commit()
        
        self.limpa_campos()
        self.atualiza_labels()


    def listar(self):
        #self.tela2.show()
        
        self.cursor.execute(
            "SELECT demanda, status, resumo, demanda_son, data FROM ticket;")
        self.dados_lidos = self.cursor.fetchall()
        
        self.telaUnica.tableWidget.setRowCount(len(self.dados_lidos))
        self.telaUnica.tableWidget.setColumnCount(5)
        
        for i in range(0, len(self.dados_lidos)):
            for j in range(0, 5):
                self.telaUnica.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(self.dados_lidos[i][j])))

    
    
janela = Aplicativo()
janela.conexao.close()
    


