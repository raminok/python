from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as routes_app
from database.models
import Base
from database.database import engine

# Create Tables
Base.metadata.create_all(bind=engine)

# Running FastAPI
app = FastAPI()

# CORS Setting
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # All Client can access
    allow_credentials=True,
    allow_methods=["*"],  # All Methodes (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # All Headers
)

# Adding Endpoints
app.include_router(routes_app)

# Run Program
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
