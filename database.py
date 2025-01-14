from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import yaml
import os

# بارگذاری تنظیمات از فایل config.yaml
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        return config['database']

# بارگذاری تنظیمات دیتابیس
db_config = load_config()

# ساخت URL اتصال به دیتابیس MySQL
DATABASE_URL = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database_name']}"

# ایجاد engine برای اتصال به دیتابیس
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=True)

# بررسی اتصال به دیتابیس
try:
    with engine.connect() as connection:
        # اجرای دستور ساده برای تست اتصال
        connection.execute(text("SELECT 1"))
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed! Error: {e}")
    raise Exception("Database connection failed!") from e

# ساخت SessionLocal برای ارتباط با دیتابیس
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# تابع برای ایجاد یک جلسه جدید برای ارتباط با دیتابیس
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
