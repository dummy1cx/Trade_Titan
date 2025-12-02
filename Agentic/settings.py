
try:
    from .config_local import (
        OPENAI_API_KEY,
        ALPHAVANTAGE_API_KEY,
        HF_TOKEN,
        KB_INDEX_PATH,
        KB_PARQUET_PATH,
    )
except ImportError:
    raise RuntimeError("Missing app/config_local.py with local secrets")