CREATE DATABASE IF NOT EXISTS vet_ai;

USE vet_ai;

CREATE TABLE IF NOT EXISTS Propietario (
    DUI VARCHAR(20) PRIMARY KEY,
    NombrePropietario VARCHAR(255),
    FotoPropietario LONGBLOB,
    Telefono INT(20),
    Direccion VARCHAR(300),
    Correo VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS ExpedienteMascota (
    IDMascota INT PRIMARY KEY AUTO_INCREMENT,
    NombreMascota VARCHAR(255),
    Sexo VARCHAR(10),
    Especie VARCHAR(100),
    Raza VARCHAR(100),
    Edad VARCHAR(250),
    Detalles TEXT,
    FotoMascota LONGBLOB,
    Peso VARCHAR(100),
    Enfermedades TEXT,
    Esterilizado VARCHAR(10),
    Vacunas TEXT,
    Examenes TEXT,
    ObservacionExamenes TEXT,
    Desparasitaciones VARCHAR(300),
    UltimaCita VARCHAR(300),
    ProxCita VARCHAR(300),
    DUI VARCHAR(20),
    FOREIGN KEY (DUI) REFERENCES Propietario(DUI),
    FotoQR LONGBLOB,
    DescUltimaCita TEXT,
    DescProxCita TEXT,
    NombreVeterinario VARCHAR(255)
);