from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router as routes_app
from database.models
import Base
from database.database import engine

# ایجاد جداول دیتابیس
Base.metadata.create_all(bind=engine)

# ایجاد برنامه اصلی FastAPI
app = FastAPI()

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # اجازه دسترسی به همه کلاینت‌ها
    allow_credentials=True,
    allow_methods=["*"],  # اجازه همه متدها (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # اجازه همه هدرها
)

# اضافه کردن اندپوینت‌ها
app.include_router(routes_app)

# اجرای برنامه
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
