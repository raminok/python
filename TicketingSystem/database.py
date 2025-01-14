import os
DATABASE_CONFIG = {
    "api_url": os.getenv("DATABASE_API_URL", "http://127.0.0.1:8001/"),
}


FRONTEND_CONFIG = {
    "base_url": os.getenv("FRONTEND_BASE_URL", "http://127.0.0.1:8000/"),
}
