create DATABASE serviapp_db;
USE serviapp_db;

CREATE TABLE usuarios (
	id_usuario INT PRIMARY KEY auto_increment,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    direccion TEXT,
    contrasena VARCHAR(255),
	fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profesionales (
    id_profesional INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    telefono VARCHAR(20),
    contrasena VARCHAR(255),
    profesion VARCHAR(100),
    habilidades TEXT,
    zona_trabajo VARCHAR(100)
);

CREATE TABLE categoria_servicios (
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    nombre_servicio VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE servicios (
    id_servicio INT AUTO_INCREMENT PRIMARY KEY,
    id_categoria INT,
    nombre_servicio VARCHAR(100) NOT NULL,
    descripcion TEXT,
    FOREIGN KEY (id_categoria) REFERENCES categoria_servicios(id_categoria)
);

CREATE TABLE solicitudes (
    id_solicitud INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_profesional INT,
    id_servicio INT,
    descripcion TEXT,
    direccion_servicio TEXT,
    telefono_contacto VARCHAR(20),
    fecha_servicio DATE,
    hora_servicio TIME,
    presupuesto DECIMAL(10,2),
    estado ENUM('pendiente', 'aceptado', 'completado', 'cancelado', 'reembolsado') DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_profesional) REFERENCES profesionales(id_profesional),
    FOREIGN KEY (id_servicio) REFERENCES servicios(id_servicio)
);

CREATE TABLE pqrs (
    id_pqrs INT AUTO_INCREMENT PRIMARY KEY,
    id_solicitud INT,
    id_usuario INT,
    id_profesional INT,
    tipo ENUM('peticion', 'queja', 'reclamo', 'sugerencia') NOT NULL,
    descripcion TEXT NOT NULL,
    estado ENUM('pendiente', 'en_proceso', 'resuelto') DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_profesional) REFERENCES profesionales(id_profesional)
);

CREATE TABLE evidencias (
    id_evidencia INT AUTO_INCREMENT PRIMARY KEY,
    id_solicitud INT,
    id_usuario INT,
    id_profesional INT,
    tipo_actor ENUM('usuario', 'profesional'),
    archivo_contenido LONGBLOB,
    descripcion TEXT,
    estado ENUM('satisfactorio', 'no_satisfactorio') NOT NULL,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_solicitud) REFERENCES solicitudes(id_solicitud),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_profesional) REFERENCES profesionales(id_profesional)
);