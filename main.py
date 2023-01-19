import cx_Oracle as sq
import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QLabel, QComboBox, QDateEdit, QTimeEdit, QCheckBox, \
    QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QDate, QTime

login_uiFile = uic.loadUiType("login.ui")
main_uiFile = uic.loadUiType("main.ui")
open_uiFile = uic.loadUiType("open.ui")


def equalDate(date1, date2):
    slist1 = date1.split("/")
    iL1 = list(map(int, slist1))
    slist2 = date2.split("/")
    iL2 = list(map(int, slist2))
    if iL1[2] != iL2[2]: # year
        return 0
    elif iL1[1] != iL2[1]:# month
        return 0
    elif iL1[0] != iL2[0]: # day
        return 0
    return 1


def betterDate(input_string):
    return "/".join(list(reversed(input_string.split(" ")[0].split("-"))))


class OpenGUI(open_uiFile[0], open_uiFile[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.button = self.findChild(QPushButton, "pushButton")
        self.button.clicked.connect(self.buttonCallback)

    def buttonCallback(self):
        self.close()


class LoginGUI(login_uiFile[0], login_uiFile[1]):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.sq_init = 0
        self.success = False
        self.connectB = self.findChild(QPushButton, "ConnectButton")
        self.user = self.findChild(QLineEdit, "UserInput")
        self.password = self.findChild(QLineEdit, "PasswordInput")
        self.connection = None
        self.connectB.clicked.connect(self.connect)
        self.errorLabel = self.findChild(QLabel, "error_label")

    def connect(self):
        """bd154"""
        self.errorLabel.setText(" ")
        if self.sq_init == 0:
            sq.init_oracle_client(lib_dir="D:\Different_tools_and_programs\OracleInstantClient\instantclient_21_8")
            self.sq_init = 1
        try:
            self.connection = sq.connect(self.user.text(), self.password.text(), "bd-dc.cs.tuiasi.ro:1539/orcl")
            self.success = True
            self.close()
        except sq.DatabaseError as e:
            err, = e.args
            self.errorLabel.setText(err.message)
            self.password.setText("")


class MainGUI(main_uiFile[0], main_uiFile[1]):
    def __init__(self, conn):
        super().__init__()
        self.current_modify_row = None
        self.setupUi(self)
        self.connection = conn
        self.emp = self.findChild(QComboBox, "Angajati")
        self.date = self.findChild(QDateEdit, "dateEdit")
        self.time = self.findChild(QTimeEdit, "timeEdit")
        self.interior = self.findChild(QCheckBox, "Interior")
        self.exterior = self.findChild(QCheckBox, "Exterior")
        self.commit = self.findChild(QPushButton, "CommitButton")
        self.oras = self.findChild(QComboBox, "Oras")
        self.matricol = self.findChild(QLineEdit, "NumarInmatriculare")
        self.marca = self.findChild(QLineEdit, "Marca")
        self.errProgramare = self.findChild(QLabel, "Label_Eroare")
        # ================
        self.matricolUD = self.findChild(QLineEdit, "InmatriculareUD")
        self.modify = self.findChild(QPushButton, "Modify")
        self.delete = self.findChild(QPushButton, "Delete")
        self.tabelP = self.findChild(QTableWidget, "TabelaProgramari")
        self.label_oras = self.findChild(QLabel, "Oras_label")
        self.label_angajati = self.findChild(QLabel, "Angajati_label")
        self.label_data = self.findChild(QLabel, "Data_label")
        self.label_ora = self.findChild(QLabel, "Ora_label")
        self.emp_modify = self.findChild(QComboBox, "Angajati_Modify")
        self.date_modify = self.findChild(QDateEdit, "dateEdit_Modify")
        self.time_modify = self.findChild(QTimeEdit, "timeEdit_Modify")
        self.interior_modify = self.findChild(QCheckBox, "Interior_Modify")
        self.exterior_modify = self.findChild(QCheckBox, "Exterior_Modify")
        self.commit_modify = self.findChild(QPushButton, "Commit_Modify")
        self.oras_modify = self.findChild(QComboBox, "Oras_Modify")
        self.cancel_modify = self.findChild(QPushButton, "Cancel_modify")
        self.modify_err_label = self.findChild(QLabel, "Modify_errLabel")
        self.price_label = self.findChild(QLabel, "Price")
        self.setEnabledComponents(False)
        self.cursor = self.connection.cursor()
        self.oras.activated.connect(self.displayEmp)
        self.commit.clicked.connect(self.commitCallback)
        self.matricolUD.textChanged.connect(self.tableUpdate)
        self.delete.clicked.connect(self.stergere)
        self.modify.clicked.connect(self.modifyCallback)
        self.cancel_modify.clicked.connect(self.cancelCallback)
        self.oras_modify.activated.connect(self.displayEmpModify)
        self.commit_modify.clicked.connect(self.commitModifyCallback)
        self.date.setDate(QDate.currentDate())
        self.time.setTime(QTime.currentTime())
        self.tabelP.setEditTriggers(QTableWidget.NoEditTriggers)
        self.displayCity()
    """ INSERT """ # =========================================================================
    def displayEmp(self):
        self.emp.clear()
        self.cursor.execute(f"select a.nume||' '||a.prenume nume  from angajati a, contracte c where a.id_angajat=c.angajati_id_angajat and c.oras_ang='{self.oras.currentText()}'")
        result = self.cursor.fetchall()
        self.emp.addItem("--oricare--")
        for i in range(len(result)):
            self.emp.addItem(result[i][0])

    def displayCity(self):
        self.cursor.execute("select distinct oras_ang from contracte")
        result = self.cursor.fetchall()
        for i in range(len(result)):
            self.oras.addItem(result[i][0])
        self.displayEmp()

    def getPrice(self, data, ora, angID):
        self.cursor.execute(f"select b.pret*(1-0.01*prom.discount) from angajati a,boxe b, programari p,promotii prom\
                                where p.boxe_id_boxa=b.id_boxa\
                                and p.angajati_id_angajat=a.id_angajat\
                                and p.promotii_id_promotie=prom.id_promotie\
                                and p.data=to_date('{data}','DD/MM/YYYY')\
                                and p.ora_incepere_progr=to_date('{ora}','HH24:MI')\
                                and angajati_id_angajat={angID}")
        return int(self.cursor.fetchall()[0][0])

    def existingAppointmentCheck(self, time):
        self.cursor.execute(f"select count(*)\
                                        from masini m,programari p\
                                        where p.masini_id_masina=m.id_masina\
                                        and m.nr_matricol=upper('{self.matricol.text()}')\
                                        and p.data=to_date('{self.date.text()}','DD/MM/YYYY')\
                                        and to_date('{time}','HH24:MI')  between  p.ora_incepere_progr-29/24/60 and p.ora_terminare_progr-1/24/60")
        if self.cursor.fetchall()[0][0] != 0:
            self.cursor.execute(f"select to_char(p.ora_incepere_progr,'hh24:mi')\
                                                    from masini m,programari p\
                                                    where p.masini_id_masina=m.id_masina\
                                                    and m.nr_matricol=upper('{self.matricol.text()}')\
                                                    and p.data=to_date('{self.date.text()}','DD/MM/YYYY')\
                                                    and to_date('{time}','HH24:MI')  between  p.ora_incepere_progr-29/24/60 and p.ora_terminare_progr-1/24/60")
            oltTime = self.cursor.fetchall()
            raise Exception(
                f"Nu va puteti programa la ora {time}\n deoarece aveti o alta programare la ora {oltTime[0][0]}.")

    def programare(self):
        # verificare conexiune baza de date
        if self.cursor is None:
            raise Exception("Cursor is not connected to a database")
    # verificare validitate data
        self.cursor.execute(f"select months_between (to_date('{self.date.text()}','DD/MM/YYYY'), sysdate) from dual")
        diff = self.cursor.fetchall()
        if not(0 <= diff[0][0] <= 6):
            raise Exception("Ati selectat data gresit!\n Verificati ca data sa fie in urmatoarele maxim 6 luni.")
    # verificare validitate ora
        self.cursor.execute("select to_char(sysdate, 'DD/MM/YYYY')zi from dual")
        date = self.cursor.fetchall()
        if equalDate(self.date.text(), date[0][0]) == 1:
            self.cursor.execute(f"select (to_date('{self.time.text()}','hh24:mi')-to_date(to_char(sysdate,'hh24:mi'),'hh24:mi'))*24 from dual")
            timediff = self.cursor.fetchall()
            if timediff[0][0] <= 0:
                raise Exception("Ati selectat ora gresit!\n Verificati ca ora sa fie dupa ora curenta.")
    # verificare client nou
        self.cursor.execute(f"select count(*) from masini where nr_matricol=upper('{self.matricol.text()}')")
        apartine = self.cursor.fetchall()
        if apartine[0][0] == 0:
            self.cursor.execute(f"insert into Masini values(NULL,upper('{self.matricol.text()}'),'{self.marca.text()}')")
    # verifica alegere tip serviciu
        if not (self.interior.isChecked() or self.exterior.isChecked()):
            raise Exception("Nu ati selectat tipul de serviciu dorit!")
    # caz de tratare interior sau exterior
        if self.interior.isChecked() ^ self.exterior.isChecked():
            self.existingAppointmentCheck(self.time.text())
            angId, boxaId = self.chooseEmpBox('interior' if self.interior.isChecked() else 'exterior', self.time.text(), self.emp.currentText(),
                                              self.oras.currentText(), self.date.text(), True)
            self.cursor.execute("commit")
            self.cursor.execute(f"select id_masina from masini where nr_matricol=upper('{self.matricol.text()}')")
            carId = self.cursor.fetchall()[0][0]
            promId = self.promotionId(self.time.text())
            self.cursor.execute(f"insert into Programari values(NULL,TO_DATE('{self.date.text()}','DD/MM/YYYY'),TO_DATE('{self.time.text()}', 'HH24:MI'),\
                                    TO_DATE(to_char(to_date('{self.time.text()}','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),{carId},{angId},{boxaId},{promId})")
            self.cursor.execute("commit")
            self.price_label.setText(f"Pretul: {self.getPrice(self.date.text(), self.time.text(), angId)} lei")

    # caz tratare si interior si exterior
        elif self.interior.isChecked() and self.exterior.isChecked():
            self.existingAppointmentCheck(self.time.text())
            self.existingAppointmentCheck(self.timetravel())
            angIdin, boxaIdin, angIdex, boxaIdex = (None, None, None, None,)
            try:
                angIdin, boxaIdin = self.chooseEmpBox("interior", self.time.text(), self.emp.currentText(), self.oras.currentText(), self.date.text(), True)
                angIdex, boxaIdex = self.chooseEmpBox("exterior", self.timetravel(), self.emp.currentText(), self.oras.currentText(), self.date.text(), True)
                cond = 1
            except Exception as e:
                print(str(e))
                self.errProgramare.setText(str(e))
                try:
                    angIdex, boxaIdex = self.chooseEmpBox("exterior", self.time.text(), self.emp.currentText(), self.oras.currentText(), self.date.text(), True)
                    angIdin, boxaIdin = self.chooseEmpBox("interior", self.timetravel(), self.emp.currentText(), self.oras.currentText(), self.date.text(), True)
                    cond = 0
                except Exception as e:
                    print(str(e))
                    self.errProgramare.setText(str(e))
                    cond = -1
            self.cursor.execute("commit")
            self.cursor.execute(f"select id_masina from masini where nr_matricol=upper('{self.matricol.text()}')")
            carId = self.cursor.fetchall()[0][0]
            promId1 = self.promotionId(self.time.text())
            promId2 = self.promotionId(self.timetravel())
            if cond == -1:
                raise Exception("Alege alta ora!")
            elif cond == 1:
                self.cursor.execute(
                    f"insert into Programari values(NULL,TO_DATE('{self.date.text()}','DD/MM/YYYY'),TO_DATE('{self.time.text()}', 'HH24:MI'),\
                                                    TO_DATE(to_char(to_date('{self.time.text()}','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),{carId},{angIdin},{boxaIdin},{promId1})")
                self.cursor.execute(
                    f"insert into Programari values(NULL,TO_DATE('{self.date.text()}','DD/MM/YYYY'),TO_DATE('{self.timetravel()}', 'HH24:MI'),\
                                                    TO_DATE(to_char(to_date('{self.timetravel()}','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),{carId},{angIdex},{boxaIdex},{promId2})")
                self.cursor.execute("commit")
                pret = self.getPrice(self.date.text(), self.time.text(), angIdin)
                pret += self.getPrice(self.date.text(), self.timetravel(), angIdex)
                self.price_label.setText(f"Pretul: {pret} lei")
            elif cond == 0:
                self.cursor.execute(
                    f"insert into Programari values(NULL,TO_DATE('{self.date.text()}','DD/MM/YYYY'),TO_DATE('{self.time.text()}', 'HH24:MI'),\
                                                    TO_DATE(to_char(to_date('{self.time.text()}','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),{carId},{angIdex},{boxaIdex},{promId1})")
                self.cursor.execute(
                    f"insert into Programari values(NULL,TO_DATE('{self.date.text()}','DD/MM/YYYY'),TO_DATE('{self.timetravel()}', 'HH24:MI'),\
                                                    TO_DATE(to_char(to_date('{self.timetravel()}','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),{carId},{angIdin},{boxaIdin},{promId2})")
                self.cursor.execute("commit")
                pret = self.getPrice(self.date.text(), self.time.text(), angIdex)
                pret += self.getPrice(self.date.text(), self.timetravel(), angIdin)
                self.price_label.setText(f"Pretul: {pret} lei")

    def timetravel(self):
        ilist = list(map(int, self.time.text().split(":")))
        if ilist[1] >= 30:
            ilist[0] += 1
        ilist[1] = (ilist[1] + 30) % 60
        return ":".join(list(map(str, ilist)))

    def commitCallback(self):
        self.errProgramare.setText("")
        self.price_label.setText("")
        try:
            self.programare()
        except sq.DatabaseError as e:
            error, = e.args
            if error.message.split(":")[0] == "ORA-02290" or error.code == "ORA-01013":
                self.errProgramare.setText("Ati introdus gresit numarul de inmatriculare!")
        except Exception as e:
            self.errProgramare.setText(str(e))
        finally:
            pass

    def promotionId(self, time):
        self.cursor.execute(f"select p.id_promotie\
                                from promotii p \
                                where discount = (\
                                    select (max(\
                                        case \
                                            when to_date('{time}','hh24:mi')\
                                                between \
                                                ora_incepere \
                                                and \
                                                ora_terminare-20/24/60 \
                                            then  discount \
                                            else null \
                                        end\
                                                )\
                                    )\
                                    from promotii)")
        return self.cursor.fetchall()[0][0]

    def chooseEmpBox(self, ie, time, emp, oras, date, insert):
        data, ora_s, nume_angajat = ("", "", "")
        if not insert:
            data, ora_s, ora_p, oras_t, tip_serv, nume_angajat, pret = self.getTableUniqueAppointment()
            self.cursor.execute(f"select p.id_programare from programari p\
                                    where p.data=to_date('{data}','DD/MM/YYYY')\
                                    and p.ora_incepere_progr=to_date('{ora_s}','hh24:mi')\
                                    and p.angajati_id_angajat=(select c.id_angajat from angajati c where c.nume||' '||c.prenume like '{nume_angajat}')")
            prog_id_update = self.cursor.fetchall()[0][0]
        self.cursor.execute(f"(select a.id_angajat,b.id_boxa  from  angajati a,contracte c,boxe b,statii s\
                                                where b.statii_id_statie=s.id_statie\
                                                and a.id_angajat=c.angajati_id_angajat\
                                                and c.oras_ang=s.oras_st\
                                                and a.nume||' '||a.prenume like '{'%' if emp == '--oricare--' else emp}'\
                                                and c.oras_ang='{oras}'\
                                                and b.tip='{ie}'\
                                            MINUS(\
                                            select a.id_angajat,b.id_boxa  from  angajati a,contracte c,boxe b,statii s, programari p\
                                                where b.statii_id_statie=s.id_statie\
                                                and b.id_boxa=p.boxe_id_boxa\
                                                and a.id_angajat=c.angajati_id_angajat\
                                                and c.oras_ang=s.oras_st\
                                                and a.nume||' '||a.prenume like '{'%' if emp == '--oricare--' else emp}'\
                                                and s.oras_st='{oras}'\
                                                and b.tip='{ie}'\
                                                {f'and p.id_programare != {prog_id_update}' if not insert else ''}\
                                                and p.data=to_date('{date}','DD/MM/YYYY')\
                                                and to_date('{time}','HH24:MI')  between  p.ora_incepere_progr-29/24/60 and p.ora_terminare_progr-1/24/60\
                                            UNION\
                                            select a.id_angajat,b.id_boxa  from  angajati a,contracte c,boxe b,statii s, programari p\
                                                where b.statii_id_statie=s.id_statie\
                                                and a.id_angajat=p.angajati_id_angajat\
                                                and a.id_angajat=c.angajati_id_angajat\
                                                and c.oras_ang=s.oras_st\
                                                and a.nume||' '||a.prenume like '{'%' if emp == '--oricare--' else emp}'\
                                                {f'and p.id_programare != {prog_id_update}' if not insert else ''}\
                                                and s.oras_st='{oras}'\
                                                and b.tip='{ie}'\
                                                and p.data=to_date('{date}','DD/MM/YYYY')\
                                                and to_date('{time}','HH24:MI')  between  p.ora_incepere_progr-29/24/60 and p.ora_terminare_progr-1/24/60))")
        AngBoxa = self.cursor.fetchall()
        if len(AngBoxa) == 0:
            self.cursor.execute(f"select min(to_char(p.ora_terminare_progr,'hh24:mi'))\
                                                    from angajati a,contracte c,boxe b,statii s, programari p\
                                                    where b.statii_id_statie=s.id_statie\
                                                    and b.id_boxa=p.boxe_id_boxa\
                                                    and a.id_angajat=p.angajati_id_angajat\
                                                    and a.id_angajat=c.angajati_id_angajat\
                                                    and c.oras_ang=s.oras_st\
                                                    and a.nume||' '||a.prenume like '{'%' if emp == '--oricare--' else emp}'\
                                                    and s.oras_st='{oras}'\
                                                    and b.tip='{ie}'\
                                                    and p.data=to_date('{date}','DD/MM/YYYY')\
                                                    and (p.ora_terminare_progr-1/24/60)>to_date('{time}','HH24:MI')")
            ora = self.cursor.fetchall()
            raise Exception(
                f"Din pacate nu se pot face programari la ora {time} \n {'' if emp == '--oricare--' else f'la angajatul {emp} '}.\n {f'Cel mai devreme va puteti programa la ora {ora[0][0]}' if ora[0][0] is not None else ''}")
        return AngBoxa[0 if len(AngBoxa) == 1 else 1]

    def ifSame(self):
        data, ora_s, ora_p, oras, tip_serv, nume_angajat, pret = self.getTableUniqueAppointment()
        return (self.oras_modify, self.emp_modify, self.date_modify, self.time_modify) == (oras, nume_angajat, data, ora_s)

    """ DELETE """ # =========================================================================
    def stergere(self):
        selected_indexes = self.tabelP.selectedIndexes()
        selected_rows = list(set([index.row() for index in selected_indexes]))
        selected_rows.sort(reverse=True)
        for row in selected_rows:
            item_data = self.tabelP.item(row, 0).text()
            item_ora_s = self.tabelP.item(row, 1).text()
            item_nume_angajat = self.tabelP.item(row, 5).text()
            try:
                self.cursor.execute(f"delete from programari where data=to_date('{item_data}','DD/MM/YYYY')\
                                        and ora_incepere_progr=to_date('{item_ora_s}','HH24:MI')\
                                        and angajati_id_angajat=(select c.id_angajat from angajati c where c.nume||' '||c.prenume like '{item_nume_angajat}')")
            except Exception as e:
                self.modify_err_label.setText(str(e))
            self.tabelP.removeRow(row)
        self.cursor.execute("commit")

    def tableUpdate(self):
        self.cursor.execute(f"select p.data,to_char(p.ora_incepere_progr,'hh24:mi')sosire,to_char(p.ora_terminare_progr,'hh24:mi')plecare,\
                                        s.oras_st, b.tip,a.nume||' '||a.prenume nume,b.pret*(1-prom.discount*0.01) pret\
                                from angajati a, contracte c,masini m, boxe b,statii s, programari p,promotii prom\
                                where b.statii_id_statie=s.id_statie\
                                and b.id_boxa=p.boxe_id_boxa\
                                and a.id_angajat=c.angajati_id_angajat\
                                and a.id_angajat=p.angajati_id_angajat\
                                and m.id_masina=p.masini_id_masina\
                                and prom.id_promotie=p.promotii_id_promotie\
                                and c.oras_ang=s.oras_st\
                                and m.nr_matricol like upper('{self.matricolUD.text()}')\
                                order by p.data, p.ora_incepere_progr")
        rows = self.cursor.fetchall()
        self.tabelP.setRowCount(0)
        if len(rows) != 0:
            row_index = 0
            for row in rows:
                self.tabelP.insertRow(row_index)
                data = QTableWidgetItem(betterDate(str(row[0])))
                ora_s = QTableWidgetItem(str(row[1]))
                ora_p = QTableWidgetItem(str(row[2]))
                oras = QTableWidgetItem(str(row[3]))
                tip_serv = QTableWidgetItem(str(row[4]))
                nume_angajat = QTableWidgetItem(str(row[5]))
                pret = QTableWidgetItem(str(row[6]))

                # Insert the items into the table
                self.tabelP.setItem(row_index, 0, data)
                self.tabelP.setItem(row_index, 1, ora_s)
                self.tabelP.setItem(row_index, 2, ora_p)
                self.tabelP.setItem(row_index, 3, oras)
                self.tabelP.setItem(row_index, 4, tip_serv)
                self.tabelP.setItem(row_index, 5, nume_angajat)
                self.tabelP.setItem(row_index, 6, pret)

                row_index += 1
            self.tabelP.update()

    """ UPDATE """  # =========================================================================
    def displayEmpModify(self):
        self.emp_modify.clear()
        self.cursor.execute(f"select a.nume||' '||a.prenume nume  from angajati a, contracte c where a.id_angajat=c.angajati_id_angajat and c.oras_ang='{self.oras_modify.currentText()}'")
        result = self.cursor.fetchall()
        self.emp_modify.addItem("--oricare--")
        for i in range(len(result)):
            self.emp_modify.addItem(result[i][0])
        if self.oras_modify.currentText() == self.tabelP.item(self.current_modify_row, 3).text():
            self.emp_modify.setCurrentIndex(self.emp_modify.findText(self.tabelP.item(self.current_modify_row, 5).text()))

    def displayCityModify(self):
        self.oras_modify.clear()
        self.cursor.execute("select distinct oras_ang from contracte")
        result = self.cursor.fetchall()
        for i in range(len(result)):
            self.oras_modify.addItem(result[i][0])
        self.oras_modify.setCurrentIndex(self.oras_modify.findText(self.tabelP.item(self.current_modify_row, 3).text()))
        self.displayEmpModify()

    def setEnabledComponents(self, boolean):
        self.label_oras.setEnabled(boolean)
        self.label_angajati.setEnabled(boolean)
        self.label_data.setEnabled(boolean)
        self.label_ora.setEnabled(boolean)
        self.emp_modify.setEnabled(boolean)
        self.date_modify.setEnabled(boolean)
        self.time_modify.setEnabled(boolean)
        self.interior_modify.setEnabled(boolean)
        self.exterior_modify.setEnabled(boolean)
        self.commit_modify.setEnabled(boolean)
        self.oras_modify.setEnabled(boolean)
        self.cancel_modify.setEnabled(boolean)

    def modifyCallback(self):
        self.modify_err_label.setText("")
        try:
            selected_index = self.tabelP.selectedIndexes()
            if len(selected_index) != 1:
                raise Exception("Daca se doreste modificarea unei programari\n prima data trebuie selectata doar o programare,\n iar dupa schimbare trebuie apasat butonul Salveaza.")
            self.setEnabledComponents(True)
            self.modify.setEnabled(False)
            self.delete.setEnabled(False)
            self.matricolUD.setEnabled(False)
            self.current_modify_row = selected_index[0].row()
            self.displayCityModify()
            data = betterDate(self.tabelP.item(self.current_modify_row, 0).text())
            ora = self.tabelP.item(self.current_modify_row, 1).text()
            tip_serv = self.tabelP.item(self.current_modify_row, 4).text()

            self.date_modify.setDate(QDate.fromString(data, "dd/MM/yyyy"))
            self.time_modify.setTime(QTime.fromString(ora, "hh:mm"))
            self.interior_modify.setChecked(True) if tip_serv == "interior" else self.exterior_modify.setChecked(True)
        except Exception as e:
            self.modify_err_label.setText(str(e))

    def cancelCallback(self):
        self.setEnabledComponents(False)
        self.modify.setEnabled(True)
        self.delete.setEnabled(True)
        self.matricolUD.setEnabled(True)
        self.interior_modify.setChecked(False)
        self.exterior_modify.setChecked(False)

    def getTableUniqueAppointment(self):
        data = self.tabelP.item(self.current_modify_row, 0).text()
        ora_s = self.tabelP.item(self.current_modify_row, 1).text()
        ora_p = self.tabelP.item(self.current_modify_row, 2).text()
        oras = self.tabelP.item(self.current_modify_row, 3).text()
        tip_serv = self.tabelP.item(self.current_modify_row, 4).text()
        nume_angajat = self.tabelP.item(self.current_modify_row, 5).text()
        pret = self.tabelP.item(self.current_modify_row, 6).text()

        return data, ora_s, ora_p, oras, tip_serv, nume_angajat, pret

    def commitModifyCallback(self):
        self.modify_err_label.setText("")
        try:
            # verificare conexiune baza de date
            if self.cursor is None:
                raise Exception("Cursor is not connected to a database")
            # verificare validitate data
            self.cursor.execute(f"select months_between (to_date('{self.date_modify.text()}','DD/MM/YYYY'), sysdate) from dual")
            diff = self.cursor.fetchall()
            if not (0 <= diff[0][0] <= 6):
                raise Exception("Ati selectat data gresit!\n Verificati ca data sa fie in urmatoarele maxim 6 luni.")
            # verificare validitate ora
            self.cursor.execute("select to_char(sysdate, 'DD/MM/YYYY')zi from dual")
            date = self.cursor.fetchall()
            if equalDate(self.date_modify.text(), date[0][0]) == 1:
                self.cursor.execute(
                    f"select (to_date('{self.time_modify.text()}','hh24:mi')-to_date(to_char(sysdate,'hh24:mi'),'hh24:mi'))*24 from dual")
                timediff = self.cursor.fetchall()
                if timediff[0][0] <= 0:
                    raise Exception("Ati selectat ora gresit!\n Verificati ca ora sa fie dupa ora curenta.")
            # verifica alegere tip serviciu
            if not (self.interior_modify.isChecked() or self.exterior_modify.isChecked()):
                raise Exception("Nu ati selectat tipul de serviciu dorit!")
            # caz de tratare interior sau exterior
            elif self.interior_modify.isChecked() ^ self.exterior_modify.isChecked():
                angId, boxaId = self.chooseEmpBox('interior' if self.interior_modify.isChecked() else 'exterior', self.time_modify.text(), self.emp_modify.currentText(),
                                                  self.oras_modify.currentText(), self.date_modify.text(), False)
                promId = self.promotionId(self.time_modify.text())
                item_data, item_ora_s, _, _, _, item_nume_angajat, _ = self.getTableUniqueAppointment()
                self.cursor.execute(f"update programari\
                                        set data=to_date('{self.date_modify.text()}','DD/MM/YYYY'),\
                                            ora_incepere_progr=to_date('{self.time_modify.text()}','HH24:MI'),\
                                            ora_terminare_progr=to_date('{self.time_modify.text()}','hh24:mi')+30/24/60,\
                                            angajati_id_angajat={angId},\
                                            boxe_id_boxa={boxaId},\
                                            promotii_id_promotie={promId}\
                                                where data=to_date('{item_data}','DD/MM/YYYY')\
                                                and ora_incepere_progr=to_date('{item_ora_s}','HH24:MI')\
                                                and angajati_id_angajat=(select a.id_angajat from angajati a where a.nume||' '||a.prenume like '{item_nume_angajat}')")
                self.cursor.execute("commit")
            elif self.interior_modify.isChecked() and self.exterior_modify.isChecked():
                raise Exception("La modificare trebuie bifat doar un\n singur tip de serviciu: interior sau exterior")
            self.tableUpdate()
            self.cancelCallback()
        except Exception as e:
            self.modify_err_label.setText(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    openWindow = OpenGUI()
    openWindow.show()
    app.exec_()
    login_app = QApplication(sys.argv)
    loginWindow = LoginGUI()
    loginWindow.show()
    login_app.exec_()
    if loginWindow.success:
        Mainapp = QApplication(sys.argv)
        mainWindow = MainGUI(loginWindow.connection)
        mainWindow.show()
        sys.exit(Mainapp.exec_())
