CREATE TABLE IF NOT EXISTS licitaciones (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo              TEXT    NOT NULL UNIQUE,
    nombre              TEXT,
    estado              TEXT,
    tipo                TEXT,
    region              TEXT,
    comuna              TEXT,
    hospital            TEXT,
    monto_estimado      REAL,
    moneda              TEXT    DEFAULT 'CLP',
    fecha_publicacion   TEXT,
    fecha_cierre        TEXT,
    fecha_adjudicacion  TEXT,
    cantidad_items      INTEGER DEFAULT 0,
    date_scraped        TEXT    NOT NULL,
    created_at          TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_region       ON licitaciones (region);
CREATE INDEX IF NOT EXISTS idx_hospital     ON licitaciones (hospital);
CREATE INDEX IF NOT EXISTS idx_estado       ON licitaciones (estado);
CREATE INDEX IF NOT EXISTS idx_date_scraped ON licitaciones (date_scraped);
CREATE TABLE IF NOT EXISTS items (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo_licitacion   TEXT    NOT NULL,
    nombre_producto     TEXT,
    descripcion         TEXT,
    categoria           TEXT,
    unidad_medida       TEXT,
    cantidad            REAL,
    created_at          TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (codigo_licitacion) REFERENCES licitaciones (codigo)
);

CREATE INDEX IF NOT EXISTS idx_codigo_licitacion ON items (codigo_licitacion);
CREATE INDEX IF NOT EXISTS idx_nombre_producto   ON items (nombre_producto);
CREATE INDEX IF NOT EXISTS idx_categoria         ON items (categoria);

-- =============================================================
-- QUERIES DE ANÁLISIS SUPPLY CHAIN
-- =============================================================

-- 1. Total licitaciones y monto por región
-- SELECT
--     region,
--     COUNT(*)                        as total_licitaciones,
--     SUM(monto_estimado)             as monto_total,
--     AVG(monto_estimado)             as monto_promedio
-- FROM licitaciones
-- WHERE monto_estimado IS NOT NULL
-- GROUP BY region
-- ORDER BY monto_total DESC;

-- 2. Top 10 hospitales con mayor gasto
-- SELECT
--     hospital,
--     region,
--     COUNT(*)                        as total_licitaciones,
--     SUM(monto_estimado)             as gasto_total
-- FROM licitaciones
-- WHERE monto_estimado IS NOT NULL
-- GROUP BY hospital
-- ORDER BY gasto_total DESC
-- LIMIT 10;

-- 3. Productos más licitados
-- SELECT
--     nombre_producto,
--     COUNT(*)                        as veces_licitado,
--     COUNT(DISTINCT codigo_licitacion) as en_licitaciones
-- FROM items
-- WHERE nombre_producto IS NOT NULL
-- GROUP BY nombre_producto
-- ORDER BY veces_licitado DESC
-- LIMIT 20;

-- 4. Licitaciones por estado
-- SELECT
--     estado,
--     COUNT(*)                        as total,
--     SUM(monto_estimado)             as monto_total
-- FROM licitaciones
-- GROUP BY estado
-- ORDER BY total DESC;

-- 5. Evolución diaria de licitaciones
-- SELECT
--     date_scraped,
--     COUNT(*)                        as total_licitaciones,
--     SUM(monto_estimado)             as monto_total
-- FROM licitaciones
-- GROUP BY date_scraped
-- ORDER BY date_scraped DESC;

-- 6. Licitaciones de una región específica
-- SELECT codigo, nombre, hospital, monto_estimado, estado
-- FROM licitaciones
-- WHERE region = 'Región de Coquimbo'
-- ORDER BY monto_estimado DESC;