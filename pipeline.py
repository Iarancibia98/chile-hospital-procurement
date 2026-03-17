import sys
import os
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper.mercadopublico_scraper import MercadoPublicoScraper
from database.db import DB

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

def limpiar_df(df):
    df["nombre"]   = df["nombre"].str.strip().str.upper()
    df["hospital"] = df["hospital"].str.strip().str.upper()
    df["region"]   = df["region"].str.strip()
    df["estado"]   = df["estado"].str.strip()
    df["moneda"]   = df["moneda"].fillna("CLP")
    df             = df.drop_duplicates(subset=["codigo"])
    return df.reset_index(drop=True)
def run(fecha=None):
    logger.info("=" * 55)
    logger.info("  CHILE HOSPITAL PROCUREMENT — PIPELINE")
    logger.info("=" * 55)

    db = DB()

    from datetime import datetime
    hoy = fecha if fecha else datetime.today().strftime("%Y-%m-%d")

    if db.ya_existe_fecha(hoy):
        logger.info(f"Datos del {hoy} ya están en la base de datos.")
        return

    logger.info("\n[1/4] Ejecutando scraper MercadoPublico...")
    scraper = MercadoPublicoScraper()
    df = scraper.scrape(
        fecha=datetime.strptime(hoy, "%Y-%m-%d").strftime("%d%m%Y")
        if fecha else None
    )

    if df.empty:
        logger.error("Sin datos. Abortando pipeline.")
        return

    logger.info("\n[2/4] Limpiando datos...")
    df = limpiar_df(df)

    logger.info("\n[3/4] Guardando CSV de respaldo...")
    csv_path = scraper.save_csv(df)

    logger.info("\n[4/4] Cargando a base de datos...")
    insertadas = db.load_licitaciones(df)

    logger.info("\n" + "=" * 55)
    logger.info("  PIPELINE COMPLETADO")
    logger.info(f"  Licitaciones scrapeadas  : {len(df)}")
    logger.info(f"  Licitaciones insertadas  : {insertadas}")
    logger.info(f"  CSV guardado en          : {csv_path}")
    logger.info(f"  Total en DB              : {db.count()}")
    logger.info("=" * 55)

    print("\n📋 Vista previa:")
    print(df[["codigo", "hospital", "region", "monto_estimado"]].head(10).to_string(index=False))


if __name__ == "__main__":
    run(fecha="2026-03-16")