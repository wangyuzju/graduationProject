drop table train;
create table train(
id int auto_increment primary key,

g0 INT,
g1 INT,
g2 varchar(8),
g3 INT,
g4 INT,
g5 INT,
g6 varchar(8),
g7 INT,
g8 INT,
g9 INT,

atp0 INT,
atp1 INT,
atp2 INT,
atp3 INT,
atp4 INT,
atp5 INT,
atp6 INT,
atp7 INT,
atp8 INT,
atp9 INT,
atp10 varchar(8),
atp11 INT,
atp12 varchar(8),
atp13 INT,
atp14 varchar(8),
atp15 INT,
atp16 varchar(8),
atp17 INT,
atp18 varchar(8),
atp19 INT,
atp20 INT,
atp21 INT,
atp22 varchar(8),
atp23 INT,
atp24 INT,
atp25 INT,
atp26 varchar(8),
atp27 INT,
atp28 INT,
atp29 INT,
atp30 INT,
atp31 varchar(8),
atp32 varchar(8),
atp33 varchar(8),
atp34 varchar(8),
atp35 varchar(8),
atp36 varchar(8),
atp37 varchar(8),
atp38 varchar(1),
atp39 INT,
atp40 INT,
atp41 INT,
atp42 varchar(8),
atp43 INT,
atp44 INT,
atp45 INT,
atp46 varchar(8),
atp47 INT,
atp48 INT,
atp49 INT,
atp50 INT,
atp51 INT,
atp52 INT,
atp53 INT,
atp54 INT,
atp55 INT,
atp56 INT,

ats0 INT,
ats1 INT,
ats2 varchar(8),
ats3 INT,
ats4 INT,
ats5 INT,
ats6 INT,
ats7 INT,
ats8 INT,
ats9 INT,
ats10 INT,
ats11 varchar(12),
ats12 varchar(8),
ats13 varchar(8),
ats14 INT,
ats15 INT,
ats16 varchar(8),
ats17 INT,
ats18 INT,
ats19 INT,
ats20 varchar(8),
ats21 INT,
ats22 INT,
ats23 INT,
ats24 INT,
ats25 INT,
ats26 INT,
ats27 INT,
ats28 varchar(8),
ats29 INT,
ats30 INT,
ats31 INT,
ats32 INT,
ats33 varchar(2),
ats34 varchar(8),
ats35 varchar(8),
ats36 varchar(2),
ats37 INT,
ats38 varchar(2),
ats39 INT,
ats40 INT,
ats41 INT,
ats42 INT,
ats43 INT,
ats44 INT,
ats45 INT,
ats46 INT,
ats47 varchar(2),
ats48 varchar(2),
ats49 varchar(2),

opg0 varchar(2),
opg1 INT,
opg2 INT,
opg3 INT,
opg4 INT,
opg5 varchar(2),
opg6 INT,
opg7 INT,
opg8 INT,
opg9 INT,
opg10 varchar(2),
opg11 INT,
opg12 INT,
opg13 INT,
opg14 varchar(20),
opg15 INT,
opg16 INT,
opg17 INT,
opg18 INT,
 
io0 varchar(2),
io1 varchar(2),
io2 varchar(2),
io3 varchar(2),
io4 varchar(2),
io5 varchar(2),
io6 varchar(2),
io7 varchar(2),
io8 varchar(2),
io9 varchar(2),
io10 varchar(8),
io11 varchar(8),
io12 varchar(8),
io13 varchar(1),
io14 varchar(8),
io15 varchar(8),
io16 varchar(8),
io17 varchar(1),
 
zc0 INT,
zc1 varchar(8),
zc2 INT,
zc3 varchar(8),
zc4 varchar(40),
zc5 varchar(60),

pf0 varchar(2),
pf1 varchar(2),
pf2 varchar(2),
pf3 varchar(2),
pf4 varchar(2),
pf5 varchar(2),
pf6 INT,
pf7 varchar(2),
pf8 INT,
pf9 INT,
pf10 varchar(8),
pf11 varchar(8),
pf12 varchar(8),
pf13 varchar(8),
pf14 varchar(8),
pf15 varchar(8),
pf16 varchar(8),
pf17 varchar(8),
pf18 varchar(8),
pf19 varchar(8),
pf20 varchar(8),
pf21 varchar(8),
pf22 varchar(8),
pf23 varchar(8),
pf24 varchar(8),
pf25 varchar(8),
pf26 varchar(8),
pf27 varchar(8),
pf28 varchar(8),
pf29 varchar(8),
pf30 INT,
pf31 varchar(8),
pf32 varchar(8),
pf33 varchar(8),
pf34 varchar(8),
pf35 varchar(8),
pf36 varchar(8),
pf37 varchar(8),
pf38 varchar(8),
pf39 varchar(8),
pf40 varchar(8),

tms0 INT,
tms1 INT,
tms2 varchar(2),
tms3 varchar(2),
tms4 varchar(4),
tms5 INT,
tms6 INT,
tms7 INT,
tms8 varchar(4),
tms9 varchar(2),
tms10 varchar(2),
tms11 varchar(2),
tms12 varchar(2),
tms13 varchar(4),
tms14 varchar(4),
tms15 varchar(4),
tms16 INT,
tms17 INT,
tms18 INT,
tms19 INT,
tms20 INT,
tms21 INT,
tms22 INT,
tms23 INT,
tms24 INT,
tms25 varchar(4),
tms26 INT,

debug0 INT,
debug1 INT,
debug2 INT,
debug3 INT,
debug4 INT,
debug5 INT,
debug6 INT,
debug7 INT,
debug8 varchar(8),
debug9 varchar(8),
debug10 varchar(8),
debug11 varchar(8),
debug12 INT,
debug13 varchar(8),
debug14 varchar(8),
debug15 INT,
debug16 varchar(8),
debug17 INT,
debug18 INT,
debug19 INT,
debug20 INT,
debug21 varchar(16),
debug22 varchar(16),
debug23 INT,
debug24 INT,
debug25 varchar(8),
debug26 varchar(4),
debug27 varchar(4),
debug28 INT,
debug29 INT,
debug30 INT,
debug31 INT,
debug32 INT,
debug33 varchar(40),
debug34 INT,
debug35 varchar(2)
)CHARSET=utf8;
