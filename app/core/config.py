from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import pydantic_settings

base_dir = Path(__file__).resolve().parent.parent
data_dir: Path = base_dir / "data"
class Settings(pydantic_settings.BaseSettings):
    """Application settings."""
    embeddings_model: str = "all-MiniLM-L6-v2"
    cross_encoder_model:str ="cross-encoder/ms-marco-MiniLM-L-6-v2"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k: int = 5
    data_dir: Path = data_dir
    index_dir: Path = data_dir / "index"
    debug: bool = False
    model_config = SettingsConfigDict(env_file=".env")
    GROQ_API_KEY:str
    
settings = Settings()