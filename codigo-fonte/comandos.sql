BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "ticket" (
	"id_ticket"	INTEGER NOT NULL,
	"demanda"	TEXT NOT NULL UNIQUE,
	"status"	TEXT,
	"resumo"	TEXT,
	"data"	TEXT,
	PRIMARY KEY("id_ticket" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ticket_filho" (
	"id_ticket"	INTEGER NOT NULL,
	"demanda"	TEXT NOT NULL UNIQUE,
	"data"	TEXT,
	PRIMARY KEY("id_ticket" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "parceiro" (
	"id_parceiro"	INTEGER NOT NULL,
	"id_ticket"	INTEGER NOT NULL,
	"id_ticket_son"	INTEGER NOT NULL,
	"demanda"	TEXT,
	"demanda_son"	TEXT,
	FOREIGN KEY("id_ticket") REFERENCES "ticket"("id_ticket"),
	FOREIGN KEY("id_ticket_son") REFERENCES "ticket_filho"("id_ticket"),
	PRIMARY KEY("id_parceiro" AUTOINCREMENT)
);
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "ticket" (
	"id_ticket"	INTEGER NOT NULL,
	"demanda"	TEXT NOT NULL UNIQUE,
	"status"	TEXT,
	"resumo"	TEXT,
	"data"	TEXT,
	PRIMARY KEY("id_ticket" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ticket_filho" (
	"id_ticket"	INTEGER NOT NULL,
	"demanda"	TEXT NOT NULL UNIQUE,
	"data"	TEXT,
	PRIMARY KEY("id_ticket" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "parceiro" (
	"id_parceiro"	INTEGER NOT NULL,
	"id_ticket"	INTEGER NOT NULL,
	"id_ticket_son"	INTEGER NOT NULL,
	"demanda"	TEXT,
	"demanda_son"	TEXT,
	FOREIGN KEY("id_ticket") REFERENCES "ticket"("id_ticket"),
	FOREIGN KEY("id_ticket_son") REFERENCES "ticket_filho"("id_ticket"),
	PRIMARY KEY("id_parceiro" AUTOINCREMENT)
);
COMMIT;
