-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS empresa_db;
USE empresa_db;

-- Tabla usuarios (independiente, sin FK)
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    rol ENUM('admin', 'rrhh', 'empleado') NOT NULL
);

-- Tabla departamentos (ahora sin FK a empleados)
CREATE TABLE IF NOT EXISTS departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    gerente_id INT NULL
);

-- Tabla empleados (con FK a departamentos)
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    fecha_inicio DATE,
    salario DECIMAL(10,2),
    departamento_id INT NULL,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id)
);

-- Agregar FK de gerente_id a departamentos después de crear empleados
ALTER TABLE departamentos
ADD CONSTRAINT fk_departamento_gerente
FOREIGN KEY (gerente_id) REFERENCES empleados(id);

-- Tabla proyectos (independiente, sin FK)
CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE
);

-- Tabla registros_tiempo (depende de empleados y proyectos)
CREATE TABLE IF NOT EXISTS registros_tiempo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    proyecto_id INT,
    fecha DATE,
    horas DECIMAL(5,2),
    descripcion TEXT,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id),
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id)
);

-- Insertar usuario admin por defecto (password: admin123)
INSERT INTO usuarios (username, password, rol) 
VALUES ('admin', '$2b$12$QcWxexlekSTXY6fV8eocL.NFw3bx17/traorxdSHV6hUw.MAQhnzW', 'admin');

-- Insertar departamentos de ejemplo
INSERT INTO departamentos (nombre) VALUES 
('Desarrollo Sostenible'),
('Investigación y Desarrollo'),
('Ventas'),
('Recursos Humanos');
