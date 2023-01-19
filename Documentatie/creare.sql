
CREATE TABLE angajati (
    id_angajat NUMBER(3) NOT NULL,
    nume       VARCHAR2(20) NOT NULL,
    prenume    VARCHAR2(20) NOT NULL
);

ALTER TABLE angajati
    ADD CONSTRAINT angajati_nume_ck CHECK ( length(nume) >= 3
                                            AND REGEXP_LIKE ( nume,
                                                              '^[a-zA-Z]*$' ) );

ALTER TABLE angajati
    ADD CONSTRAINT angajati_prenume_ck CHECK ( length(prenume) >= 3
                                               AND REGEXP_LIKE ( prenume,
                                                                 '^[a-zA-Z]*$' ) );

ALTER TABLE angajati ADD CONSTRAINT angajati_pk PRIMARY KEY ( id_angajat );

CREATE TABLE boxe (
    id_boxa          NUMBER(3) NOT NULL,
    tip              VARCHAR2(10) NOT NULL,
    pret             NUMBER(3) NOT NULL,
    statii_id_statie NUMBER(3) NOT NULL
);

ALTER TABLE boxe
    ADD CONSTRAINT boxe_tip_ck CHECK ( tip IN ( 'exterior', 'interior' ) );

ALTER TABLE boxe ADD CONSTRAINT boxe_pret_ck CHECK ( pret >= 20 );

ALTER TABLE boxe ADD CONSTRAINT boxe_pk PRIMARY KEY ( id_boxa );

CREATE TABLE contracte (
    id_contract         NUMBER(3) NOT NULL,
    oras_ang            VARCHAR2(10) NOT NULL,
    angajati_id_angajat NUMBER(3) NOT NULL
);

CREATE UNIQUE INDEX contracte__idx ON
    contracte (
        angajati_id_angajat
    ASC );

ALTER TABLE contracte ADD CONSTRAINT contracte_pk PRIMARY KEY ( id_contract );

CREATE TABLE masini (
    id_masina   NUMBER(3) NOT NULL,
    nr_matricol VARCHAR2(7) NOT NULL,
    marca       VARCHAR2(10)
);

ALTER TABLE masini
    ADD CONSTRAINT masini_nr_matricol_ck CHECK ( ( length(nr_matricol) = 7
                                                   OR length(nr_matricol) = 6 )
                                                 AND ( REGEXP_LIKE ( nr_matricol,
                                                                     '^[A-Z]{2}[0-9]{2}[A-Z]{3}$' )
                                                       OR REGEXP_LIKE ( nr_matricol,
                                                                        '^[A-Z]{1}[0-9]{2}[A-Z]{3}$' )
                                                       OR REGEXP_LIKE ( nr_matricol,
                                                                        '^[A-Z]{1}[0-9]{3}[A-Z]{3}$' ) ) );

ALTER TABLE masini ADD CONSTRAINT masini_pk PRIMARY KEY ( id_masina );

ALTER TABLE masini ADD CONSTRAINT masini_nr_matricol_un UNIQUE ( nr_matricol );

CREATE TABLE programari (
    id_programare        NUMBER(4) NOT NULL,
    data                 DATE NOT NULL,
    ora_incepere_progr   DATE NOT NULL,
    ora_terminare_progr  DATE NOT NULL,
    masini_id_masina     NUMBER(3) NOT NULL,
    angajati_id_angajat  NUMBER(3) NOT NULL,
    boxe_id_boxa         NUMBER(3) NOT NULL,
    promotii_id_promotie NUMBER(3) NOT NULL
);

ALTER TABLE programari
    ADD CONSTRAINT ora_terminare_progr_ck CHECK ( ( ora_terminare_progr - ora_incepere_progr ) * 60 * 24 = 30 );

ALTER TABLE programari
    ADD CONSTRAINT programari_pk PRIMARY KEY ( id_programare,
                                               masini_id_masina,
                                               angajati_id_angajat,
                                               boxe_id_boxa );

CREATE TABLE promotii (
    id_promotie   NUMBER(3) NOT NULL,
    ora_incepere  DATE NOT NULL,
    ora_terminare DATE NOT NULL,
    discount      NUMBER(2) NOT NULL
);

ALTER TABLE promotii ADD CONSTRAINT promotii_ora_terminare_ck CHECK ( ora_terminare > ora_incepere );

ALTER TABLE promotii ADD CONSTRAINT promotii_pk PRIMARY KEY ( id_promotie );

CREATE TABLE statii (
    id_statie        NUMBER(3) NOT NULL,
    nr_boxe_interior NUMBER(2) NOT NULL,
    nr_boxe_exterior NUMBER(2) NOT NULL,
    oras_st          VARCHAR2(10) NOT NULL
);

ALTER TABLE statii ADD CONSTRAINT statii_pk PRIMARY KEY ( id_statie );

ALTER TABLE boxe
    ADD CONSTRAINT boxe_statii_fk FOREIGN KEY ( statii_id_statie )
        REFERENCES statii ( id_statie );

ALTER TABLE contracte
    ADD CONSTRAINT contracte_angajati_fk FOREIGN KEY ( angajati_id_angajat )
        REFERENCES angajati ( id_angajat );

ALTER TABLE programari
    ADD CONSTRAINT programari_angajati_fk FOREIGN KEY ( angajati_id_angajat )
        REFERENCES angajati ( id_angajat );

ALTER TABLE programari
    ADD CONSTRAINT programari_boxe_fk FOREIGN KEY ( boxe_id_boxa )
        REFERENCES boxe ( id_boxa );

ALTER TABLE programari
    ADD CONSTRAINT programari_masini_fk FOREIGN KEY ( masini_id_masina )
        REFERENCES masini ( id_masina );

ALTER TABLE programari
    ADD CONSTRAINT programari_promotii_fk FOREIGN KEY ( promotii_id_promotie )
        REFERENCES promotii ( id_promotie );

CREATE SEQUENCE angajati_id_angajat_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER angajati_id_angajat_trg BEFORE
    INSERT ON angajati
    FOR EACH ROW
    WHEN ( new.id_angajat IS NULL )
BEGIN
    :new.id_angajat := angajati_id_angajat_seq.nextval;
END;
/

CREATE SEQUENCE boxe_id_boxa_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER boxe_id_boxa_trg BEFORE
    INSERT ON boxe
    FOR EACH ROW
    WHEN ( new.id_boxa IS NULL )
BEGIN
    :new.id_boxa := boxe_id_boxa_seq.nextval;
END;
/

CREATE SEQUENCE contracte_id_contract_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER contracte_id_contract_trg BEFORE
    INSERT ON contracte
    FOR EACH ROW
    WHEN ( new.id_contract IS NULL )
BEGIN
    :new.id_contract := contracte_id_contract_seq.nextval;
END;
/

CREATE SEQUENCE masini_id_masina_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER masini_id_masina_trg BEFORE
    INSERT ON masini
    FOR EACH ROW
    WHEN ( new.id_masina IS NULL )
BEGIN
    :new.id_masina := masini_id_masina_seq.nextval;
END;
/

CREATE SEQUENCE programari_id_programare_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER programari_id_programare_trg BEFORE
    INSERT ON programari
    FOR EACH ROW
    WHEN ( new.id_programare IS NULL )
BEGIN
    :new.id_programare := programari_id_programare_seq.nextval;
END;
/

CREATE SEQUENCE promotii_id_promotie_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER promotii_id_promotie_trg BEFORE
    INSERT ON promotii
    FOR EACH ROW
    WHEN ( new.id_promotie IS NULL )
BEGIN
    :new.id_promotie := promotii_id_promotie_seq.nextval;
END;
/

CREATE SEQUENCE statii_id_statie_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER statii_id_statie_trg BEFORE
    INSERT ON statii
    FOR EACH ROW
    WHEN ( new.id_statie IS NULL )
BEGIN
    :new.id_statie := statii_id_statie_seq.nextval;
END;
/


