
from .settings import Settings

class ProdSettings(Settings):
    DEBUG: bool = False
    DATABASE_URL: str = "postgresql://user:password@prod-db-url:5432/arc_tec_fox"
