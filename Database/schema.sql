create table membros_pg (
id serial primary key,
Nome varchar Not null,
Data_de_nascimento date not null,
Nome_dos_responsaveis varchar not null,
igreja_id int not null,
foreign key (igreja_id) references Igrejas(Id)
);

create table Igrejas (
Id serial primary key,
Nome Varchar,
Localiza Varchar
);

