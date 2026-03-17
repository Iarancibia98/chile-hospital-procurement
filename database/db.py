import os
import sqlite3
import pandas as pd
import logging

logger = logging.getLogger(__name__)

DB_PATH     = os.path.join(os.path.dirname(__file__), "..", "data", "healthcare_procurement.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")
class DB:

    def __init__(self, db_path=DB_PATH):
        self.db_path = os.path.abspath(db_path)
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_schema()

    def _init_schema(self):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            sql = f.read()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            for statement in sql.split(";"):
                stmt = statement.strip()
                if stmt and not stmt.startswith("--"):
                    try:
                        conn.execute(stmt)
                    except sqlite3.Error as e:
                        logger.debug(f"Schema ignorado: {e}")
            conn.commit()

        logger.info(f"Base de datos lista: {self.db_path}")
    def load_licitaciones(self, df: pd.DataFrame) -> int:
        if df.empty:
            logger.warning("DataFrame vacío, nada que cargar.")
            return 0

        valid_cols = self._get_columns("licitaciones")
        cols       = [c for c in df.columns if c in valid_cols]
        df_clean   = df[cols].copy()

        inserted = 0
        with sqlite3.connect(self.db_path) as conn:
            for _, row in df_clean.iterrows():
                try:
                    conn.execute(
                        f"INSERT OR IGNORE INTO licitaciones ({','.join(cols)}) "
                        f"VALUES ({','.join(['?' for _ in cols])})",
                        tuple(row)
                    )
                    inserted += conn.execute(
                        "SELECT changes()"
                    ).fetchone()[0]
                except sqlite3.Error as e:
                    logger.debug(f"Error insertando licitación: {e}")
            conn.commit()

        logger.info(f"Licitaciones insertadas: {inserted}")
        return inserted
    def load_items(self, codigo_licitacion: str, items: list) -> int:
        if not items:
            return 0

        inserted = 0
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            for item in items:
                try:
                    conn.execute("""
                        INSERT INTO items
                            (codigo_licitacion, nombre_producto, descripcion,
                             categoria, unidad_medida, cantidad)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        codigo_licitacion,
                        item.get("NombreProducto"),
                        item.get("Descripcion"),
                        item.get("Categoria"),
                        item.get("UnidadMedida"),
                        item.get("Cantidad"),
                    ))
                    inserted += 1
                except sqlite3.Error as e:
                    logger.debug(f"Error insertando item: {e}")
            conn.commit()

        return inserted
    def _get_columns(self, table: str) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f"PRAGMA table_info({table})")
            return [row[1] for row in cursor.fetchall()]

    def query(self, sql: str) -> pd.DataFrame:
        with sqlite3.connect(self.db_path) as conn:
            return pd.read_sql_query(sql, conn)

    def count(self, table: str = "licitaciones") -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
            return cursor.fetchone()[0]

    def ya_existe_fecha(self, fecha: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT COUNT(*) FROM licitaciones WHERE date_scraped = ?",
                (fecha,)
            )
            return cursor.fetchone()[0] > 0

if __name__ == "__main__":
    db = DB()
    print(f"✅ Base de datos inicializada")
    print(f"   Licitaciones : {db.count('licitaciones')}")
    print(f"   Items        : {db.count('items')}")