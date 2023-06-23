#--------------IMPORTANDO BIBLIOTECAS------------------------

import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, Event
from random import randint
from tkcalendar import *
from datetime import datetime
import pytz
import os
import time
import openpyxl

#------ USUARIO E SENHA PARA ENTRAR NO SISTEMA -----------------

nome_adm = 'devteam4'
senha_adm = 'devteam4'

#----------- CARREGANDO AS TABELAS DO BANCO DE DADOS---------------

tabela_ferramentas = pd.read_csv(r'lista_ferramentas.csv', sep=';', index_col=0, encoding='UTF-8')
tabela_funcionarios = pd.read_csv(r'lista_funcionarios.csv', sep=',', index_col=0, encoding='UTF-8')
tabela_reservas = pd.read_csv(r'lista_reservas.csv', sep=';', index_col=0, encoding='UTF-8')

#-------------JANELA DE LOGIN------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # TELA DE LOGIN:
        self.iconbitmap('estacio_sem_nome.ico')
        self.title('Sistema de Gerenciamento de Ferramentas')
        self.geometry('1000x700')
        self.config(background='#373435')
        self.bg = PhotoImage(file="TELA BEM VINDO 3.png")
        self.label = Label(self, image=self.bg, width=980, height=690)
        self.label.place(x=0, y=0)

        # LABEL E ENTRY TELA DE LOGIN
        self.lb_usuario = Label(self, text="LOGIN", anchor=W, fg='white', bg='#444244')
        self.lb_usuario.place(x=150, y=190, width=100, height=20)
        self.usuario = Entry(self, bg='white')
        self.usuario.place(x=150, y=220, width=100, height=20)
        self.lb_senha = Label(self, text="PASSWORD", anchor=W, fg='white', bg='#444244')
        self.lb_senha.place(x=150, y=250, width=100, height=20)
        self.senha = Entry(self, show='*', bg='white')
        self.senha.place(x=150, y=280, width=100, height=20)
        # BOTA DE LOGIN
        self.botao3 = Button(self, text="Login", fg='white', bg='#444244', anchor=W, command=self.abrir_jan_cf)
        self.botao3.place(x=150, y=320, width=100, height=20)
        # BOTAO DE MOSTRAR SENHA
        self.botao4 = Button(self, text="Mostrar Senha", fg='white', bg='#444244', anchor=W, command=self.my_show)
        self.botao4.place(x=150, y=350, width=100, height=20)

# FUNÇÃO DE MOSTRAR SENHA
    def my_show(self):
        if (len(self.senha.get()) != 0):
            self.senha.config(show='')
        else:
            messagebox.showinfo(message='Digite sua senha.')

# FUNÇÃO PARA USUARIO E SENHA
    def abrir_jan_cf(self):
        if self.usuario.get() == 'devteam4' and self.senha.get() == 'devteam4':
            self.destroy()
            Jan_Cf()
        else:
            messagebox.showinfo(title='Usuário ou senha inválidos!', message='Usuário ou senha inválidos!')

#------------------ JANELA PRINCIPAL/NOTEBOOK -------------------------
class Jan_Cf(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('estacio_sem_nome.ico')
        self.title('Sistema de Gerenciamento de Ferramentas')
        self.config(background='#373435')

        width_value = self.winfo_screenwidth()
        height_value = self.winfo_screenheight()
        self.geometry('%dx%d+0+0' % (width_value, height_value))

        my_note = ttk.Notebook(self)
        my_note.place(x=0, y=0, width=width_value, height=height_value)


# -- FUNÇÕES/BOTÕES/LABELS/ENTRY/COMBOBOX/TREEVIEW DA ABA TECNICOS/FUNCIONARIOS (tb4)----------------------

        tb4 = Frame(my_note, bg='#373435', width=250, height=150, borderwidth=0)
        my_note.add(tb4, text='Gerenciar Técnicos')

        def del_tvbd():
            if not treeTec.selection():
                messagebox.showinfo(title='Atenção!', message='SELECIONE O ELEMENTO A SER DELETADO.')
            else:
                index = treeTec.index(treeTec.selection()[0])
                treeTec.delete(treeTec.selection()[0])
                # print(tabela_funcionarios)
                tabela_funcionarios = pd.read_csv(r'lista_funcionarios.csv', sep=',', index_col=0)
                tabela_funcionarios = tabela_funcionarios.drop([index])
                tabela_funcionarios = tabela_funcionarios.reset_index()
                # print(tabela_funcionarios)
                tabela_funcionarios = tabela_funcionarios.drop(['index'], axis=1)
                tabela_funcionarios.to_csv(r'lista_funcionarios.csv')

        def cpf_validate():
            entrada = vcpf.get()
            #  Obtém os números do CPF e ignora outros caracteres
            cpf = [int(char) for char in entrada if char.isdigit()]
            if cpf == cpf[::-1]:
                return False, 'CPF invalido'

                #  Valida os dois dígitos verificadores
            for i in range(9, 11):
                value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
                digit = ((value * 10) % 11) % 10
                if digit != cpf[i]:
                    return False, 'Digito verificador invalido'
            entrada = entrada.replace(" ", "")
            entrada = entrada.replace("-", "")
            entrada = entrada.replace("-", "")
            entrada = entrada.replace("/", "")
            entrada = entrada.replace(".", "")
            return entrada

        def validation():
            name = vnome.get()
            turno = vturno.get()
            equipe = vequipe.get()
            cpf = cpf_validate()
            fone = vfone.get()
            radio = vradio.get()
            msg = ''

            if len(name) == 0:
                return 'Nome não pode estar vazio'
            if len(turno) == 0:
                return 'Turno vazio'
            if len(equipe) == 0:
                return 'equipe vazio'
            if cpf == (False, 'Digito verificador invalido'):
                return 'Digito verificador do CPF invalido'
            if cpf == (False, 'CPF invalido'):
                return 'CPF invalido'
            if len(cpf) == 0:
                return 'cpf vazio'
            if len(fone) == 0 and len(radio) == 0:
                return 'Celular e radios vazios'
            if len(fone) != 0 and len(fone) != 9:
                return 'Celular deve conter 9 digitos'
            if len(radio) != 0 and len(radio) > 8:
                return 'Radio deve conter até 8 digitos'
            else:
                try:
                    if any(ch.isdigit() for ch in name):
                        return 'Nome nao pode conter numeros'
                    if any(ch.isdigit() for ch in turno):
                        return 'Turno nao pode conter numeros'
                    elif len( name) <= 5: 
                        return 'Nome é muito curto. O nome deve ser entre 05 a 40 caracteres'
                    elif len(name) > 40:
                        return 'Nome é muito longo. O nome deve ser entre 05 a 40 caracteres'
                    elif len(turno) <= 4:  # Podem ser as opções para escolher uma (manha, tarde, noite)
                        return 'Turno deve ser manha, tarde ou noite'
                    elif len(turno) > 5:
                        return 'Turno deve ser manha, tarde ou noite'
                    elif len(equipe) <= 1:
                        return 'Equipe é muito curto. A equipe deve ser entre 02 a 30 caracteres'
                    elif len(equipe) > 30:
                        return 'Equipe é muito longo. Equipe deve ser entre 02 a 30 caracteres'
                    elif len(cpf) != 11:
                        return 'CPF deve conter 11 caracteres. Sem traço nem ponto nem barras'
                    # TEM QUE INSERIR AQUI A FUNÇÃO DE VALIDAR DIGITOS VERIFICADORES DO CPF
                    elif len(radio) == 0 and len(fone) != 9:
                        return 'Fone deve conter 9 caracteres. Sem traço nem ponto nem barras'
                    elif len(fone) == 0 and (len(radio) != 0 and len(radio) > 8):
                        return 'Radio deve conter até 8 caracteres. Sem traço nem ponto nem barras'
                    else:
                        return 'Sucess!'
                except Exception as ep:
                    messagebox.showerror('Error', ep)

        def download():
            tabela_funcionarios = pd.read_csv(r'lista_funcionarios.csv', sep=',', index_col=0)
            tabela_funcionarios.to_excel(r'C:\Users\Public\Downloads\tabela_tecnicos.xlsx')
            messagebox.showinfo(
                message='Download realizado com sucesso. Documento salvo em ' + r'C:\Users\Public\Downloads')            

        def add_tvbd():
            if validation() != 'Sucess!':
                messagebox.showinfo('Atenção!', message=validation())
            else:
                treeTec.insert('', tk.END,
                               values=(
                                   v3.get(), vturno.get(), v4.get(), vcpf.get(), vfone.get(), vradio.get()))
                lista_add = [v3.get(), vturno.get(), v4.get(), vcpf.get(), str(vfone.get()),
                             str(vradio.get())]
                # print(tabela_funcionarios)
                tabela_funcionarios.loc[len(tabela_funcionarios)] = lista_add
                # print(tabela_funcionarios)
                tabela_funcionarios.to_csv(r'lista_funcionarios.csv')
                vnome.delete(0, END),
                # vturno.delete(0, END),
                vequipe.delete(0, END),
                vcpf.delete(0, END),
                vfone.delete(0, END),
                vradio.delete(0, END),
                vnome.focus()

        def caps3(event):
            v3.set(v3.get().upper())
            if len(v3.get()) > 40:
                messagebox.showinfo(message='NOME COMPLETO ULTRAPASSOU O LIMITE DE 40 CARACTERES!')

        v3 = StringVar()
        lbnome_tb4 = Label(tb4, text='NOME', anchor=W, fg='white', bg='#373435')
        vnome = Entry(tb4, textvariable=v3)
        vnome.bind("<KeyRelease>", caps3)

        def caps4(event):
            v4.set(v4.get().upper())
            if len(v4.get()) > 30:
                messagebox.showinfo(message='NOME DA EQUIPE ULTRAPASSOU O LIMITE DE 30 CARACTERES!')

        v4 = StringVar()
        lbequipe_tb4 = Label(tb4, text='EQUIPE', anchor=W, fg='white', bg='#373435')
        vequipe = Entry(tb4, textvariable=v4)
        vequipe.bind("<KeyRelease>", caps4)

        lbturno_tb4 = Label(tb4, text="TURNO", anchor=W, fg='white', bg='#373435')
        vturno = ttk.Combobox(tb4, width=27)
        vturno['values'] = ("MANHÃ",
                            "TARDE", "NOITE")
        vturno.set('Selecione')
        vturno.current()

        lbradio_tb4 = Label(tb4, text='RADIO', anchor=W, fg='white', bg='#373435')
        vradio = Entry(tb4)
        lbcpf_tb4 = Label(tb4, text='CPF', anchor=W, fg='white', bg='#373435')
        vcpf = Entry(tb4)
        lbfone_tb4 = Label(tb4, text='TELEFONE', anchor=W, fg='white', bg='#373435')
        vfone = Entry(tb4)

        btn_adicionar_tb4 = Button(tb4, text='Cadastrar', command=add_tvbd)
        btn_excluir_tb4 = Button(tb4, text='Deletar', command=del_tvbd)
        btn_down_tb4 = Button(tb4, text='Download', command=download)

    #-----------Adicionando o treeview na ABA tb4 -------------------------

        colunas = [item for item in tabela_funcionarios.columns]

        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', background='silver', foreground='black', rowheight=25,
                        fieldbackground='silver')
        style.map('Treeview', background=[('selected', 'red')])

        treeTec = ttk.Treeview(tb4,
                               columns=colunas,
                               show='headings')

        ytreeScroll2 = ttk.Scrollbar(treeTec)
        ytreeScroll2.configure(command=treeTec.yview)

        xtreeScroll2 = ttk.Scrollbar(treeTec, orient='horizontal')
        xtreeScroll2.configure(command=treeTec.xview)

        treeTec.configure(yscrollcommand=ytreeScroll2.set, xscrollcommand=xtreeScroll2.set)

        xtreeScroll2.pack(side=BOTTOM, fill='x')
        ytreeScroll2.pack(side=RIGHT, fill=BOTH)

        for i in colunas:
            treeTec.heading(f"{i}", text=f"{i}")

        for n in tabela_funcionarios.values:
            n[4] = '%.0f' % n[4]
            n[5] = '%.0f' % n[5]
            if n[4] == 'nan':
                n[4] = 'N/A'
            if n[5] == 'nan':
                n[5] = 'N/A'
            treeTec.insert('', tk.END, values=list(n))

        treeTec.place(x=1, y=1, width=width_value - 5, height=290)

    # -----------POSICIONANDO OS ELEMENTOS NA ABA TÉCNICOS/FUNCIONARIOS TB4----------------------

        lbnome_tb4.place(x=10, y=330, width=80, height=20)
        vnome.place(x=100, y=330, width=300, height=20)
        lbturno_tb4.place(x=10, y=390, width=80, height=20)
        vturno.place(x=100, y=390, width=90, height=20)
        lbequipe_tb4.place(x=10, y=360, width=70, height=20)
        vequipe.place(x=100, y=360, width=200, height=20)
        lbcpf_tb4.place(x=10, y=420, width=70, height=20)
        vcpf.place(x=100, y=420, width=90, height=20)
        lbfone_tb4.place(x=10, y=450, width=80, height=20)
        vfone.place(x=100, y=450, width=90, height=20)
        lbradio_tb4.place(x=10, y=480, width=80, height=20)
        vradio.place(x=100, y=480, width=90, height=20)

        btn_adicionar_tb4.place(x=10, y=300, width=80, height=20)
        btn_excluir_tb4.place(x=100, y=300, width=80, height=20)
        btn_down_tb4.place(x=190, y=300, width=80, height=20)

# ------------- FIM DA ABA DE TECNICOS/FUNCIONARIOS (tb4)------------------------------

# ------ FUNÇÕES/BOTÕES/LABELS/ENTRY/COMBOBOX/treeview DA ABA FERRAMENTAS (tb2)----------------------

        tb2 = Frame(my_note, width=250, height=150, bg='#373435', borderwidth=0)
        my_note.add(tb2, text='Gerenciar Ferramentas')

        def del_tvbd2():
            if not treeFer.selection():
                messagebox.showinfo(title='Atenção!', message='SELECIONE O ELEMENTO A SER DELETADO.')
            else:
                index = treeFer.index(treeFer.selection()[0])
                # print(index)
                treeFer.delete(treeFer.selection()[0])
                tabela_ferramentas = pd.read_csv(r'lista_ferramentas.csv', sep=';', index_col=0)
                # print(tabela_ferramentas)
                tabela_ferramentas = tabela_ferramentas.drop([index])
                tabela_ferramentas = tabela_ferramentas.reset_index()
                # print(tabela_ferramentas)
                tabela_ferramentas = tabela_ferramentas.drop(['index'], axis=1)
                # print(tabela_ferramentas)
                tabela_ferramentas.to_csv(r'lista_ferramentas.csv', sep=';')

        def val_fer():
            descricao = v.get()
            fabricante = v2.get()
            voltagem = vvolt.get()
            pnumber = vpn.get()
            tamanho = vtam.get()
            unidade = vuni.get()
            tipofer = vtipo.get()
            matfer = vmat.get()
            tmr = vtmr.get()
            if len(tmr) == 0:
                return 'TEMPO MÁXIMO DE RESERVA NÃO PODE ESTAR VAZIO!'
            if len(descricao) == 0:
                return 'DESCRIÇÃO NÃO PODE ESTAR VAZIO!'
            if len(fabricante) == 0:
                return 'FABRICANTE NÃO PODE ESTAR VAZIO!'
            if len(voltagem) == 0:
                return 'VOLTAGEM NÃO PODE ESTAR VAZIO!'
            if len(pnumber) == 0:
                return 'PART NUMBER NÃO PODE ESTAR VAZIO!'
            if len(tamanho) == 0:
                return 'TAMANHO NÃO PODE ESTAR VAZIO!'
            if len(unidade) == 0:
                return 'UNIDADE NÃO PODE ESTAR VAZIO!'
            if len(tipofer) == 0:
                return 'TIPO NÃO PODE ESTAR VAZIO!'
            if len(matfer) == 0:
                return 'MATERIAL NÃO PODE ESTAR VAZIO!'
            else:
                try:
                    if len(descricao) > 60: 
                        return 'DESCRIÇÃO: LIMITE DE 60 CARACTERES!'
                    if len(fabricante) > 30:
                        return 'FABRICANTE: LIMITE DE ATÉ 30 CARACTERES!'
                    if len(voltagem) > 15:
                        return 'VOLTAGEM: LIMITE DE 15 CARACTERES!'
                    if len(pnumber) > 25:
                        return 'PART NUMBER: LIMITE DE 25 CARACTERES!'
                    if len(tamanho) > 20:
                        return 'TAMANHO: LIMITE DE 20 CARACTERES!'
                    if len(unidade) > 15:
                        return 'UNIDADE: LIMITE DE 15 CARACTERES!'
                    if len(tipofer) > 15:
                        return 'TIPO: LIMITE DE 15 CARACTERES!'
                    if len(matfer) > 15:
                        return 'MATERIAL: LIMITE DE 15 CARACTERES!'
                    else:
                        return 'Sucess!'
                except Exception as ep:
                    messagebox.showerror('Error', ep)

        def add_tvbd2():
            if val_fer() != 'Sucess!':
                # or vturno.get() =='' or vequipe.get() =='' or vcpf.get() =='' or vfone.get() =='':
                messagebox.showinfo('Atenção!', message=val_fer())
            # if vdesc.get() =='' or vfab.get() =='' or vvolt.get() =='' \
            #         or vtam.get() =='' or vuni.get() =='' or vtipo.get() =='' or vmat.get() ==''\
            #         or vpn.get() =='':
            #     messagebox.showinfo('erro', message='Preencha todos os campos')
            else:
                id_fer = gerar_id()
                treeFer.insert('', tk.END,
                               values=(id_fer, v.get(), v2.get(), vvolt.get(), vtam.get(), vuni.get(),
                                       vtipo.get(), vmat.get(), vpn.get(),vtmr.get()))
                lista_add = [id_fer, v.get(), v2.get(), vvolt.get(), vtam.get(), vuni.get(),
                             vtipo.get(), vmat.get(), vpn.get(), vtmr.get()]
                # print(Bd.tabela_ferramentas)
                tabela_ferramentas.loc[len(tabela_ferramentas)] = lista_add
                # print(Bd.tabela_ferramentas)
                tabela_ferramentas.to_csv(r'lista_ferramentas.csv', sep=';')
                # vid.delete(0, END),
                vdesc.delete(0, END),
                vfab.delete(0, END),
                vvolt.delete(0, END),
                vtam.delete(0, END),
                vuni.delete(0, END),
                vtipo.delete(0, END),
                vmat.delete(0, END),
                vpn.delete(0, END),
                vnome.focus()

        def gerar_id():
            bd_fer = pd.read_csv(r'lista_ferramentas.csv', sep=';', index_col=0)
            lista_ids_existentes = bd_fer['ID']
            id = randint(1, 100000)
            while id in lista_ids_existentes:
                id = randint(1, 100000)
            else:
                return id

        def download2():
            tabela_ferramentas = pd.read_csv(r'lista_ferramentas.csv', sep=';', index_col=0)
            tabela_ferramentas.to_excel(r'C:\Users\Public\Downloads\tabela_ferramentas.xlsx')
            messagebox.showinfo(
                message='Download realizado com sucesso. Documento salvo em ' + r'C:\Users\Public\Downloads')

        lbtmr = Label(tb2, text="TMR", anchor=W, fg='white', bg='#373435')
        vtmr = ttk.Combobox(tb2, width=27)
        vtmr['values'] = ("12:00", "24:00", "36:00","48:00","60:00", "72:00")
        vtmr.set('Selecione')
        vtmr.current()

        lbhoras = Label(tb2, text="TEMPO MÁXIMO DE RESERVA.", anchor=W, fg='white', bg='#373435')

        def caps2(event):
            v2.set(v2.get().upper())
            if len(v2.get()) > 30:
                messagebox.showinfo(message='FABRICAÇÃO ULTRAPASSOU O LIMITE DE 30 CARACTERES!')

        v2 = StringVar()
        lbfab = Label(tb2, anchor=W, text="FABRICANTE", fg='white', bg='#373435')
        vfab = Entry(tb2, textvariable=v2)
        vfab.bind("<KeyRelease>", caps2)

        lbvolt = Label(tb2, text="VOLTAGEM", fg='white', anchor=W, bg='#373435')
        vvolt = ttk.Combobox(tb2, width=27)
        vvolt['values'] = ("127V",
                           "220V",
                           'BIVOLT',
                           'NÃO SE APLICA')
        vvolt.set('Selecione')
        vvolt.current()

        lbuni = Label(tb2, text="UNIDADE", anchor=W, fg='white', bg='#373435')
        vuni = ttk.Combobox(tb2, width=27)
        vuni['values'] = ("CM",
                          "POLEGADA", "METROS")
        vuni.set('Selecione')
        vuni.current()

        lbmat = Label(tb2, text='MATERIAL', anchor=W, fg='white', bg='#373435')
        vmat = ttk.Combobox(tb2, width=27)
        vmat['values'] = ("PLASTICO",
                          "AÇO", "MADEIRA", "VIDRO")
        vmat.set('Selecione')
        vmat.current()

        lbtipo = Label(tb2, text='TIPO', anchor=W, fg='white', bg='#373435')
        vtipo = ttk.Combobox(tb2, width=27)
        vtipo['values'] = ("ELÉTRICO",
                           "MECÂNICA", "SEGURANÇA")
        vtipo.set('Selecione')
        vtipo.current()

        lbtam_tb2 = Label(tb2, text='TAMANHO', anchor=W, fg='white', bg='#373435')
        vtam = Entry(tb2)

        def caps(event):
            v.set(v.get().upper())
            if len(v.get()) > 60:
                messagebox.showinfo(message='DESCRIÇÃO ULTRAPASSOU O LIMITE DE 60 CARACTERES!')

        v = StringVar()

        lbdesc_tb2 = Label(tb2, text='DESCRIÇÃO', anchor=W, fg='white', bg='#373435')
        vdesc = Entry(tb2, textvariable=v)
        vdesc.bind("<KeyRelease>", caps)

        lbpn_tb2 = Label(tb2, text='PART NUMBER', anchor=W, fg='white', bg='#373435')
        vpn = Entry(tb2)

        btn_adicionar_tb2 = Button(tb2, text='Cadastrar', command=add_tvbd2)
        btn_excluir_tb2 = Button(tb2, text='Deletar', command=del_tvbd2)
        btn_down_tb2 = Button(tb2, text='Download', command=download2)

    # -----------Treeview da aba de ferramentas --------------

        dadosColunas2 = [item2 for item2 in tabela_ferramentas.columns]
        style = ttk.Style()
        style.configure('Treeview', background='#444244', rowheight=25, foreground="white", fieldbackground='#444244')

        treeFer = ttk.Treeview(tb2, columns=dadosColunas2, show='headings')

        ytreeScroll = ttk.Scrollbar(treeFer)
        ytreeScroll.configure(command=treeFer.yview)

        xtreeScroll = ttk.Scrollbar(treeFer, orient='horizontal')
        xtreeScroll.configure(command=treeFer.xview)

        treeFer.configure(yscrollcommand=ytreeScroll.set, xscrollcommand=xtreeScroll.set)

        xtreeScroll.pack(side=BOTTOM, fill='x')
        ytreeScroll.pack(side=RIGHT, fill=BOTH)

        for i2 in dadosColunas2:

            if i2 == 'ID':
                treeFer.column(i2, width=70, minwidth=50, stretch=NO)
                treeFer.heading(f"{i2}", text=f"{i2}")
            elif i2 == 'DESCRIÇÃO':
                treeFer.column(i2, width=420, minwidth=50, stretch=NO)
                treeFer.heading(f"{i2}", text=f"{i2}")
            else:
                treeFer.column(i2, width=200, minwidth=50, stretch=NO)
                treeFer.heading(f"{i2}", text=f"{i2}")

        for n2 in tabela_ferramentas.values:
            treeFer.insert('', tk.END, values=list(n2))

        treeFer.place(x=1, y=1, width=width_value - 5, height=290)

    #-------------POSICIONANDO OS ELEMENTOS NA ABA FERRAMENTAS TB2----------------------------

        lbpn_tb2.place(x=10, y=390, width=90, height=20)
        vpn.place(x=100, y=390, width=150, height=20)

        lbdesc_tb2.place(x=10, y=330, width=100, height=20)
        vdesc.place(x=100, y=330, width=500, height=20)

        lbfab.place(x=10, y=360, width=100, height=20)
        vfab.place(x=100, y=360, width=250, height=20)

        lbtam_tb2.place(x=10, y=420, width=70, height=20)
        vtam.place(x=100, y=420, width=90, height=20)

        lbuni.place(x=10, y=450, width=70, height=20)
        vuni.place(x=100, y=450, width=90, height=20)

        lbtipo.place(x=10, y=480, width=70, height=20)
        vtipo.place(x=100, y=480, width=90, height=20)

        lbmat.place(x=10, y=510, width=70, height=20)
        vmat.place(x=100, y=510, width=90, height=20)

        lbvolt.place(x=10, y=540, width=100, height=20)
        vvolt.place(x=100, y=540, width=100, height=20)

        lbtmr.place(x=10, y=570, width=70, height=20)
        vtmr.place(x=100, y=570, width=90, height=20)
        lbhoras.place(x=200, y=570, width=300, height=20)

        btn_adicionar_tb2.place(x=10, y=300, width=80, height=20)
        btn_excluir_tb2.place(x=100, y=300, width=80, height=20)
        btn_down_tb2.place(x=190, y=300, width=80, height=20)

# ------------- FIM DA ABA DE FERRAMENTAS (tb2)------------------------------

# ------ FUNÇÕES/BOTÕES/LABELS/ENTRY/COMBOBOX/TREEVIEW DA ABA RESERVAS (tb5)----------------------

        tb5 = Frame(my_note, bg='#373435', width=250, height=150, borderwidth=0)
        my_note.add(tb5, text='Gerenciar Reservas')

        def reservar():
            lista_idfer = tabela_ferramentas['ID'].tolist()
            if int(vidfer.get()) not in lista_idfer or len(vidfer.get()) == 0:
                return messagebox.showinfo('Atenção!',
                                           message='REVISE O ID NA TABELA FERRAMENTAS!')
            if len(vdescres.get()) == 0 or len(vdescres.get()) <= 15:
                return messagebox.showinfo('Atenção!',
                                           message='DESCRIÇÃO DEVE TER NO MINIMO 15 CARACTERES!')
            if len(vdtret.get()) == 0:
                return messagebox.showinfo('Atenção!', message='Selecione a data de retirada')
            if len(vhrret.get()) == 0 or vhrret.get() == 'Selecione':
                return messagebox.showinfo('Atenção!', message='Selecione a hora de retirada')
            if len(vdtdev.get()) == 0:
                return messagebox.showinfo('Atenção!', message='Selecione a data de devolução')
            if len(vhrdev.get()) == 0 or vhrdev.get() == 'Selecione':
                return messagebox.showinfo('Atenção!', message='Selecione a hora da devolução')
            if len(vnmtec.get()) == 0 or len(vnmtec.get()) <= 5:
                return messagebox.showinfo('Atenção!', message='Por favor insira o nome completo (MAIOR QUE 10 CARACTERES)')
            else:
                id_res = gerar_idres()
                treeRes.insert('', tk.END,
                               values=(id_res, vidfer.get(), vdescres.get(), vdtret.get(), vhrret.get(),
                                       vdtdev.get(), vhrdev.get(), vnmtec.get(), 'PENDENTE', data_hora()))
                lista_add = [id_res, vidfer.get(), vdescres.get(), vdtret.get(), vhrret.get(), vdtdev.get(),
                             vhrdev.get(), vnmtec.get(), 'PENDENTE', data_hora()]
                tabela_reservas.loc[len(tabela_reservas)] = lista_add
                tabela_reservas.to_csv(r'lista_reservas.csv', sep=';')
                vidfer.delete(0, END),
                vdescres.delete(0, END),
                vdtret.delete(0, END),
                vhrret.delete(0, END),
                vdtdev.delete(0, END),
                vhrdev.delete(0, END),
                vnmtec.delete(0, END),
                vidfer.focus()

        def gerar_idres():
            lista_ids_existentes = tabela_reservas['ID FERRAMENTA'].tolist()
            id = randint(1, 100000)
            while id in lista_ids_existentes:
                id = randint(1, 100000)
            else:
                return id

        def data_hora():
            current_dateTime = datetime.now(pytz.timezone('America/Recife'))
            current_dateTime = current_dateTime.strftime('%d/%m/%Y %H:%M')
            return current_dateTime

        def devolucao():
            if not treeRes.selection():
                messagebox.showinfo(title='Atenção!', message='Selecione o elemento a ser atualizado')
            else:
                index = treeRes.index(treeRes.selection()[0])

                # Grab the record number
                selected = treeRes.focus()

                # Grab record values
                values = treeRes.item(selected, 'values')
                vdthrres = values[9]
                # (selected)
                # id_reserva = treeRes.item(selected)['values'][0]
                # print(id_reserva)

                vidres.delete(0, END)
                vidfer.delete(0, END),
                vdescres.delete(0, END),
                vdtret.delete(0, END),
                vhrret.delete(0, END),
                vdtdev.delete(0, END),
                vhrdev.delete(0, END),
                vnmtec.delete(0, END),
                # vdthrres.delete(0, END)

                # outpus to entry boxes
                vidres.insert(0, values[0])
                vidfer.insert(0, values[1])
                vdescres.insert(0, values[2])
                vdtret.insert(0, values[3])
                vhrret.insert(0, values[4])
                vdtdev.insert(0, values[5])
                vhrdev.insert(0, values[6])
                vnmtec.insert(0, values[7])
                vstatus.insert(0, values[8])
                # vdthrres.insert(0, values[9])

                # Update record
                treeRes.item(selected, text="", values=(
                    vidres.get(), vidfer.get(), vdescres.get(), vdtret.get(), vhrret.get(), vdtdev.get(),
                    vhrdev.get(), vnmtec.get(), 'finalizado', vdthrres))
                lista_add = [vidres.get(), vidfer.get(), vdescres.get(), vdtret.get(), vhrret.get(), vdtdev.get(),
                             vhrdev.get(), vnmtec.get(), 'finalizado', vdthrres]
                tabela_reservas = pd.read_csv('lista_reservas.csv', sep=';', index_col=0)
                # print(tabela_reservas.values[0])
                tabela_reservas = tabela_reservas.drop([index])
                tabela_reservas = tabela_reservas.reset_index()
                tabela_reservas = tabela_reservas.drop(['index'], axis=1)
                # print(tabela_ferramentas)
                tabela_reservas.loc[len(tabela_reservas)] = lista_add
                # print(tabela_reservas)
                tabela_reservas.to_csv(r'lista_reservas.csv', sep=';')
                vidfer.delete(0, END),
                vdescres.delete(0, END),
                vdtret.delete(0, END),
                vhrret.delete(0, END),
                vdtdev.delete(0, END),
                vhrdev.delete(0, END),
                vnmtec.delete(0, END),
                vidfer.focus()

        def download3():
            tabela_reservas = pd.read_csv('lista_reservas.csv', sep=';', index_col=0)
            tabela_reservas.to_excel(r'C:\Users\Public\Downloads\lista_reservas.xlsx')
            messagebox.showinfo(
                message='Download realizado com sucesso. Documento salvo em ' + r'C:\Users\Public\Downloads')
        
        def imprimir():
            df = pd.read_csv(r'lista_reservas.csv', sep=';', index_col=0, encoding='UTF-8')
            df2 = df[['ID RESERVA','ID FERRAMENTA','NOME TÉCNICO','DATA DEVOLUÇÃO',
                        'HORA DEVOLUÇÃO','DT E HR RESERVA','STATUS']]
            df2 = df2.sort_values(by=['DT E HR RESERVA'])
            df2.to_excel(r'C:\Users\Public\Downloads\tabela_reservas.xlsx')

            # Call a Workbook() function of openpyxl 
            # to create a new blank Workbook object
            wb_obj = openpyxl.load_workbook(r"C:\Users\Public\Downloads\tabela_reservas.xlsx")

            # Get workbook active sheet  
            # from the active attribute. 
            sheet_obj = wb_obj.active 

            # set the width of the column 
            sheet_obj.column_dimensions['A'].width = 2
            sheet_obj.column_dimensions['B'].width = 12
            sheet_obj.column_dimensions['C'].width = 15
            sheet_obj.column_dimensions['D'].width = 19
            sheet_obj.column_dimensions['E'].width = 17
            sheet_obj.column_dimensions['F'].width = 17
            sheet_obj.column_dimensions['G'].width = 17

            sheet_obj.page_setup.orientation = sheet_obj.ORIENTATION_LANDSCAPE

            wb_obj.save(r"C:\Users\Public\Downloads\tabela_reservas.xlsx")
            

            # Insert the directory path in here
            path = r'C:\Users\Public\Downloads'
            
            # Extracting all the contents in the directory corresponding to path
            l_files = os.listdir(path)
            file = 'tabela_reservas.xlsx'
            file_path = f'{path}\\{file}'
            # Checking whether the given file is a directory or not
            if os.path.isfile(file_path):
                try:
                    # Printing the file pertaining to file_path
                    os.startfile(file_path, 'print')
                    print(f'Imprimindo {file}')
            
                    # Sleeping the program for 5 seconds so as to account the
                    #steady processing of the print operation.
                    time.sleep(3)
                except:
                    #Catching if any error occurs and alerting the user
                    print(f'ALERTA: {file} NÃO PODE SER IMPRESSA! POR FAVOR\
                    VERIFIQUE O TIPO DO ARQUIVO.')
            else:
                print(f'ALERTA: {file} NÃO É UM ARQUIVO E NÃO PODE SER IMPRESSO!')

        def descriUp(event):
            desc.set(desc.get().upper())

        desc = StringVar()

        lbdesc_tb5 = Label(tb5, text='DESCRIÇÃO', anchor=W, fg='white', bg='#373435')
        vdescres = Entry(tb5, textvariable=desc)
        vdescres.bind('<KeyRelease>', descriUp)

        lbidfer_tb5 = Label(tb5, text='ID FERRAMENTA', anchor=W, fg='white', bg='#373435')
        vidfer = Entry(tb5)

        vidfer = ttk.Combobox(tb5)
        listaId = [item for item in tabela_ferramentas['ID']]
        vidfer['values'] = listaId
        vidfer.set('Selecione')
        vidfer.current()
        vidres = Entry(tb5)
        vstatus = Entry(tb5)
        lbdtret_tb5 = Label(tb5, text='DATA RETIRADA', anchor=W, fg='white', bg='#373435')
        vdtret = DateEntry(tb5)
        lbhrret_tb5 = Label(tb5, text='HORA RETIRADA', anchor=W, fg='white', bg='#373435')
        vhrret = ttk.Combobox(tb5, width=27)
        vhrret['values'] = (
        "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
        "12:00",
        "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00")
        vhrret.set('Selecione')
        vhrret.current()

        lbdtdev_tb5 = Label(tb5, text='DATA DEVOLUÇAO', anchor=W, fg='white', bg='#373435')
        vdtdev = DateEntry(tb5)

        lbhrdev_tb5 = Label(tb5, text='HORA DEVOLUÇÃO', anchor=W, fg='white', bg='#373435')

        vhrdev = ttk.Combobox(tb5, width=27)
        vhrdev['values'] = (
        "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
        "12:00",
        "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00")
        vhrdev.set('Selecione')
        vhrdev.current()

        lbnmtec_tb5 = Label(tb5, text='TÉCNICO', anchor=W, fg='white', bg='#373435')

        vnmtec = ttk.Combobox(tb5)
        listaNomes = [item for item in tabela_funcionarios['NOME']]
        vnmtec['values'] = listaNomes
        vnmtec.set('Selecione')
        vnmtec.current()

        btn_adicionar_tb5 = Button(tb5, text='Reservar', command=reservar)

        btn_imp_tb5 = Button(tb5, text='Imprimir', command=imprimir) 

        btn_down_tb5 = Button(tb5, text='Download', command=download3)

        btn_devol_tb5 = Button(tb5, text='Devolução', command=devolucao)

    # -----------Treeview da aba de RESERVAS TB5 ---------------------

        dadosColunas3 = [item3 for item3 in tabela_reservas.columns]

        treeRes = ttk.Treeview(tb5, columns=dadosColunas3, show='headings')

        ytreeScroll = ttk.Scrollbar(treeRes)
        ytreeScroll.configure(command=treeRes.yview)

        xtreeScroll = ttk.Scrollbar(treeRes, orient='horizontal')
        xtreeScroll.configure(command=treeRes.xview)

        treeRes.configure(yscrollcommand=ytreeScroll.set, xscrollcommand=xtreeScroll.set)

        xtreeScroll.pack(side=BOTTOM, fill='x')
        ytreeScroll.pack(side=RIGHT, fill=BOTH)

        for i3 in dadosColunas3:
            if 'ID' in i3:
                treeRes.column(i3, width=100, minwidth=50, stretch=NO)
                treeRes.heading(f"{i3}", text=f"{i3}")
            elif i3 == 'DESCRIÇÃO':
                treeRes.column(i3, width=400, minwidth=50, stretch=NO)
                treeRes.heading(f"{i3}", text=f"{i3}")
            else:
                treeRes.heading(f"{i3}", text=f"{i3}")

        for n3 in tabela_reservas.values:
            # print(n3[8]) #Chegando a coluna status da tabela que e igual ao item 8 da lista n3.
            if n3[8] == 'PENDENTE':
                treeRes.insert('', tk.END, values=list(n3))

        treeRes.place(x=1, y=1, width=width_value - 5, height=290)

    # -------Posicionando os elementos na aba RESERVAS tb5 ---------------------

        btn_devol_tb5.place(x=100, y=300, width=80, height=20)
        btn_adicionar_tb5.place(x=10, y=300, width=80, height=20)
        btn_down_tb5.place(x=190, y=300, width=80, height=20)
        btn_imp_tb5.place(x=280, y=300, width=80, height=20)

        lbidfer_tb5.place(x=10, y=330, width=100, height=20)
        vidfer.place(x=130, y=330, width=80, height=20)

        lbdesc_tb5.place(x=10, y=360, width=150, height=20)
        vdescres.place(x=130, y=360, width=300, height=20)

        lbdtret_tb5.place(x=10, y=390, width=100, height=20)
        vdtret.place(x=130, y=390, width=80, height=20)

        lbhrret_tb5.place(x=220, y=390, width=100, height=20)
        vhrret.place(x=340, y=390, width=90, height=20)

        lbdtdev_tb5.place(x=10, y=420, width=110, height=20)
        vdtdev.place(x=130, y=420, width=80, height=20)

        lbhrdev_tb5.place(x=220, y=420, width=110, height=20)
        vhrdev.place(x=340, y=420, width=90, height=20)

        lbnmtec_tb5.place(x=10, y=450, width=100, height=20)
        vnmtec.place(x=130, y=450, width=200, height=20)

# ------------- FIM DA ABA DE RESERVAS (tb5)------------------------------

if __name__ == "__main__":
    root = App()
    root.mainloop()