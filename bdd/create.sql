-- Open
.open scanner.db


-- Clean
DROP TABLE IF EXISTS machines;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS association;


-- Create
CREATE TABLE machines(mid INTEGER NOT NULL, fqdn TEXT NOT NULL, ip TEXT NOT NULL, last_view TEXT NOT NULL, CONSTRAINT mpk PRIMARY KEY (mid));
CREATE TABLE services(sid INTEGER NOT NULL, port INTEGER NOT NULL, proto TEXT NOT NULL, banner TEXT NOT NULL, version TEXT NOT NULL, last_view TEXT NOT NULL, CONSTRAINT spk PRIMARY KEY (sid));
CREATE TABLE association(aid, INTEGER NOT NULL, mid INTEGER NOT NULL, sid INTEGER NOT NULL, CONSTRAINT apk PRIMARY KEY (aid, mid, sid));
