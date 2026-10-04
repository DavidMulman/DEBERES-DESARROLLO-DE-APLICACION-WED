-- ==========================================================
-- PROYECTO INTEGRADOR - SEMANA 15
-- BASE DE DATOS POSTGRESQL
-- ==========================================================


-- ==========================================================
-- TABLA USUARIOS
-- ==========================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);


-- ==========================================================
-- TABLA PROVEEDORES
-- ==========================================================

CREATE TABLE IF NOT EXISTS proveedores (
    id_proveedor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    empresa VARCHAR(100),
    email VARCHAR(100),
    telefono VARCHAR(20)
);


-- ==========================================================
-- TABLA PRODUCTOS
-- Relación:
-- productos.id_proveedor -> proveedores.id_proveedor
-- ==========================================================

CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    precio NUMERIC(10,2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0),

    id_proveedor INTEGER,

    CONSTRAINT fk_producto_proveedor
        FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
        ON DELETE SET NULL
);


-- ==========================================================
-- TABLA FACTURAS
-- Relación:
-- facturas.id_producto -> productos.id_producto
-- ==========================================================

CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,

    id_producto INTEGER NOT NULL,

    cantidad INTEGER NOT NULL
        CHECK (cantidad > 0),

    total NUMERIC(10,2) NOT NULL
        CHECK (total >= 0),

    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_factura_producto
        FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
);


-- ==========================================================
-- CONSULTA JOIN
-- PRODUCTOS CON SUS PROVEEDORES
-- ==========================================================

SELECT
    p.id_producto,
    p.nombre AS producto,
    p.categoria,
    p.precio,
    p.stock,
    pr.nombre AS proveedor,
    pr.empresa,
    pr.email,
    pr.telefono
FROM productos p
LEFT JOIN proveedores pr
    ON p.id_proveedor = pr.id_proveedor
ORDER BY p.id_producto;


-- ==========================================================
-- CONSULTA JOIN
-- FACTURAS CON PRODUCTOS
-- ==========================================================

SELECT
    f.id_factura,
    f.cliente,
    p.nombre AS producto,
    f.cantidad,
    f.total,
    f.fecha
FROM facturas f
INNER JOIN productos p
    ON f.id_producto = p.id_producto
ORDER BY f.id_factura;