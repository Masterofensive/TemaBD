--------inserare tabela Angajati---------
insert into Angajati values(NULL,'Ionescu','Andrei');
insert into Angajati values(NULL,'Popescu','Vasile');
insert into Angajati values(NULL,'Marinescu','Ionel');
insert into Angajati values(NULL,'Popa','Paul');
insert into Angajati values(NULL,'Dumitra','Lucia');
insert into Angajati values(NULL,'Lazar','Cosmin');
insert into Angajati values(NULL,'Golescu','Marian');
insert into Angajati values(NULL,'Dan','Ion');
insert into Angajati values(NULL,'Dumitu','Lazar');
insert into Angajati values(NULL,'Pop','Cosmina');
insert into Angajati values(NULL,'Vlase','Andreea');
insert into Angajati values(NULL,'Tudose','Mihaela');
insert into Angajati values(NULL,'Toader','Vasile');
insert into Angajati values(NULL,'Mihai','Daniela');
insert into Angajati values(NULL,'Noru','Larisa');
insert into Angajati values(NULL,'Visina','Alex');
select * from Angajati;



--------inserare tabela Contracte--------
insert into Contracte values(NULL,'Iasi',104);
insert into Contracte values(NULL,'Iasi',105);
insert into Contracte values(NULL,'Iasi',106);
insert into Contracte values(NULL,'Iasi',107);
insert into Contracte values(NULL,'Galati',108);
insert into Contracte values(NULL,'Galati',109);
insert into Contracte values(NULL,'Bacau',110);
insert into Contracte values(NULL,'Bacau',111);
insert into Contracte values(NULL,'Bacau',112);
insert into Contracte values(NULL,'Arad',113);
insert into Contracte values(NULL,'Arad',114);
insert into Contracte values(NULL,'Bucuresti',115);
insert into Contracte values(NULL,'Bucuresti',116);
insert into Contracte values(NULL,'Bucuresti',117);
insert into Contracte values(NULL,'Bucuresti',118);
insert into Contracte values(NULL,'Bucuresti',119);
select * from Contracte;


--------inserare tabela Masini---------
insert into Masini values(NULL,'IS07BDB','BMW');
insert into Masini values(NULL,'BC43GRT','BMW');
insert into Masini values(NULL,'IS63HDG','Audi');
insert into Masini values(NULL,'B65HTD','Audi');
insert into Masini values(NULL,'B168JFG','Ford');
insert into Masini values(NULL,'GL12ASD',null);
insert into Masini values(NULL,'B123ABC','BMW');
select * from Masini;


--------inserare tabela Statii---------
insert into Statii values(NULL,1,1,'Galati');
insert into Statii values(NULL,2,2,'Iasi');
insert into Statii values(NULL,1,2,'Bacau');
insert into Statii values(NULL,2,3,'Bucuresti');
insert into Statii values(NULL,2,1,'Arad');
select * from Statii;



--------inserare tabela Boxe---------
insert into Boxe values(NULL,'interior',40,47);
insert into Boxe values(NULL,'exterior',40,47);
insert into Boxe values(NULL,'interior',50,48);
insert into Boxe values(NULL,'interior',50,48);
insert into Boxe values(NULL,'exterior',50,48);
insert into Boxe values(NULL,'exterior',50,48);
insert into Boxe values(NULL,'interior',30,49);
insert into Boxe values(NULL,'exterior',30,49);
insert into Boxe values(NULL,'exterior',30,49);
insert into Boxe values(NULL,'interior',60,50);
insert into Boxe values(NULL,'interior',60,50);
insert into Boxe values(NULL,'exterior',60,50);
insert into Boxe values(NULL,'exterior',60,50);
insert into Boxe values(NULL,'exterior',60,50);
insert into Boxe values(NULL,'interior',35,51);
insert into Boxe values(NULL,'interior',35,51);
insert into Boxe values(NULL,'exterior',35,51);
select * from Boxe;


--------inserare tabela Promotii---------
insert into Promotii values(NULL,TO_DATE('20:00', 'HH24:MI'),TO_DATE('21:00', 'HH24:MI'),10);
insert into Promotii values(NULL,TO_DATE('15:30', 'HH24:MI'),TO_DATE('17:00', 'HH24:MI'),15);
insert into Promotii values(NULL,TO_DATE('11:30', 'HH24:MI'),TO_DATE('12:30', 'HH24:MI'),20);
insert into Promotii values(NULL,TO_DATE('08:00', 'HH24:MI'),TO_DATE('09:00', 'HH24:MI'),30);
insert into Promotii values(NULL,TO_DATE('00:00', 'HH24:MI'),TO_DATE('23:59', 'HH24:MI'),0);
select * from Promotii;



--------inserare tabela Programari---------
insert into Programari values(NULL,TO_DATE('12/1/2023','DD/MM/YYYY'),TO_DATE('08:00', 'HH24:MI'), 
TO_DATE(to_char(to_date('08:00','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),117,104,57,32);
insert into Programari values(NULL,TO_DATE('12/1/2023','DD/MM/YYYY'),TO_DATE('8:30', 'HH24:MI'), 
TO_DATE(to_char(to_date('8:30','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),117,104,59,32);
insert into Programari values(NULL,TO_DATE('12/1/2023','DD/MM/YYYY'),TO_DATE('10:00', 'HH24:MI'), 
TO_DATE(to_char(to_date('10:00','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),118,104,57,33);
insert into Programari values(NULL,TO_DATE('12/1/2023','DD/MM/YYYY'),TO_DATE('10:00', 'HH24:MI'), 
TO_DATE(to_char(to_date('10:00','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),123,115,64,33);
insert into Programari values(NULL,TO_DATE('12/1/2023','DD/MM/YYYY'),TO_DATE('10:30', 'HH24:MI'), 
TO_DATE(to_char(to_date('10:30','hh24:mi')+30/24/60,'hh24:mi'), 'HH24:MI'),123,115,66,33);
select * from Programari;
select id_programare,data,to_char(ora_incepere_progr,'hh24:mi')sosire,to_char(ora_terminare_progr,'hh24:mi')plecare,
masini_id_masina,angajati_id_angajat,boxe_id_boxa,promotii_id_promotie from programari order by masini_id_masina,data;

delete  from programari  ;

commit;
