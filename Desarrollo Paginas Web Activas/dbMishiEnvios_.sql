USE dbMishiEnvios;
GO

INSERT INTO EstadosEnvio (Nombre) VALUES ('Pendiente');
INSERT INTO EstadosEnvio (Nombre) VALUES ('En proceso');
INSERT INTO EstadosEnvio (Nombre) VALUES ('En camino');
INSERT INTO EstadosEnvio (Nombre) VALUES ('Entregado');

INSERT INTO Clientes (Nombre,Telefono,Correo)
VALUES ('Marilyn Arias','77777777','mmarias@correo.com');

INSERT INTO Destinatarios (Nombre,Direccion,Telefono,ClienteId)
VALUES ('Michelle Jimenez','San Salvador','77777777',1);

INSERT INTO Destinatarios (Nombre,Direccion,Telefono,ClienteId)
VALUES ('Michelle J','San Miguel','77777777',2);

INSERT INTO Clientes (Nombre,Telefono,Correo)
VALUES ('Yanira Arias','79779777','arias@correo.com');

INSERT INTO Destinatarios (Nombre,Direccion,Telefono,ClienteId)
VALUES ('Cesar Jimenez','San Salvador','77777777',3);

SELECT * FROM  Auditorias;