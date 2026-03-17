import time
import logging
import requests
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
class BaseScraper:

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    def __init__(self, delay: float = 1.0, max_retries: int = 3):
        self.delay = delay
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get(self, url: str):
        for attempt in range(1, self.max_retries + 1):
            try:
                logger.info(f"GET {url[:80]}  (intento {attempt}/{self.max_retries})")
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                time.sleep(self.delay)
                return response

            except requests.exceptions.HTTPError as e:
                logger.warning(f"HTTP error {e.response.status_code}: {url[:60]}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Sin conexión: {url[:60]}")
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout: {url[:60]}")

            if attempt < self.max_retries:
                wait = self.delay * attempt
                logger.info(f"Reintentando en {wait:.1f}s...")
                time.sleep(wait)

        logger.error(f"Falló después de {self.max_retries} intentos: {url[:60]}")
        return None

    def get_json(self, url: str):
        response = self.get(url)
        if response is None:
            return None
        try:
            return response.json()
        except Exception as e:
            logger.error(f"Error parseando JSON: {e}")
            return None

    @staticmethod
    def today() -> str:
        return datetime.today().strftime("%Y-%m-%d")

    @staticmethod
    def today_api() -> str:
        return datetime.today().strftime("%d%m%Y")