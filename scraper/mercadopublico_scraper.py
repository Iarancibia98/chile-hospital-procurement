import sys
import os
import pandas as pd
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scraper.base_scraper import BaseScraper, logger
from dotenv import load_dotenv

load_dotenv()

TICKET = os.getenv("MERCADOPUBLICO_TICKET", "F8537A18-6766-4DEF-9E59-426B4FEE2844")
BASE_URL = "https://api.mercadopublico.cl/servicios/v1/Publico"
OUTPUT_DIR = "data"

PALABRAS_CLAVE = [
    "hospital", "salud", "médico", "medico",
    "farmac", "clínica", "clinica", "insumo",
    "quirúrgico", "quirurgico", "sanitario",
    "servicio de salud"
]

PALABRAS_EXCLUIR = [
    "tabiquería", "construcción", "infraestructura",
    "pintura", "aseo", "limpieza", "vigilancia",
    "seguridad", "alimentación", "cocina"
]

class MercadoPublicoScraper(BaseScraper):

    def __init__(self):
        super().__init__(delay=1.0, max_retries=3)

    def es_hospitalaria(self, nombre: str) -> bool:
        nombre = nombre.lower()
        tiene_clave   = any(p in nombre for p in PALABRAS_CLAVE)
        esta_excluida = any(p in nombre for p in PALABRAS_EXCLUIR)
        return tiene_clave and not esta_excluida
    def obtener_licitaciones_dia(self, fecha: str = None) -> list:
        if fecha is None:
            fecha = self.today_api()

        url = f"{BASE_URL}/Licitaciones.json?fecha={fecha}&ticket={TICKET}"
        data = self.get_json(url)

        if data is None or "Listado" not in data:
            logger.warning(f"Sin datos para la fecha {fecha}")
            return []

        total = data["Cantidad"]
        listado = data["Listado"]
        logger.info(f"Total licitaciones del día: {total}")

        hospitalarias = [
            l for l in listado
            if self.es_hospitalaria(l.get("Nombre", ""))
        ]
        logger.info(f"Licitaciones hospitalarias: {len(hospitalarias)}")

        return hospitalarias
    def obtener_detalle(self, codigo: str) -> dict | None:
        url = f"{BASE_URL}/Licitaciones.json?codigo={codigo}&ticket={TICKET}"
        data = self.get_json(url)

        if data is None or "Listado" not in data or not data["Listado"]:
            logger.warning(f"Sin detalle para licitación {codigo}")
            return None

        return data["Listado"][0]
    def extraer_campos(self, detalle: dict) -> dict:
        comprador = detalle.get("Comprador", {})
        fechas    = detalle.get("Fechas", {})

        return {
            "codigo":             detalle.get("CodigoExterno"),
            "nombre":             detalle.get("Nombre", "").strip(),
            "estado":             detalle.get("Estado"),
            "tipo":               detalle.get("Tipo"),
            "region":             comprador.get("RegionUnidad"),
            "comuna":             comprador.get("ComunaUnidad"),
            "hospital":           comprador.get("NombreOrganismo"),
            "monto_estimado":     detalle.get("MontoEstimado"),
            "moneda":             detalle.get("Moneda"),
            "fecha_publicacion":  fechas.get("FechaPublicacion", "")[:10],
            "fecha_cierre":       fechas.get("FechaCierre", "")[:10],
            "fecha_adjudicacion": fechas.get("FechaAdjudicacion", "")[:10],
            "cantidad_items":     detalle.get("Items", {}).get("Cantidad", 0),
            "date_scraped":       self.today(),
        }
    def scrape(self, fecha: str = None) -> pd.DataFrame:
        logger.info("=== Iniciando MercadoPublico Scraper ===")

        licitaciones = self.obtener_licitaciones_dia(fecha)

        if not licitaciones:
            logger.warning("Sin licitaciones hospitalarias para procesar.")
            return pd.DataFrame()

        registros = []

        for i, lic in enumerate(licitaciones, 1):
            codigo = lic.get("CodigoExterno")
            logger.info(f"[{i}/{len(licitaciones)}] Procesando {codigo}")

            detalle = self.obtener_detalle(codigo)
            if detalle is None:
                continue

            campos = self.extraer_campos(detalle)
            registros.append(campos)

        df = pd.DataFrame(registros)
        logger.info(f"Total registros extraídos: {len(df)}")
        return df

    def save_csv(self, df: pd.DataFrame) -> str:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = f"{OUTPUT_DIR}/licitaciones_{self.today()}.csv"
        df.to_csv(filename, index=False, encoding="utf-8")
        logger.info(f"Datos guardados en: {filename}")
        return filename
    
if __name__ == "__main__":
    scraper = MercadoPublicoScraper()
    df = scraper.scrape(fecha="16032026")

    if not df.empty:
        path = scraper.save_csv(df)
        print(f"\n✅ Scraping completado: {len(df)} licitaciones")
        print(f"📁 Archivo guardado: {path}")
        print("\n📋 Primeras 5 filas:")
        print(df[["codigo", "hospital", "region", "monto_estimado"]].head())
    else:
        print("\n❌ No se obtuvieron datos.")