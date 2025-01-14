from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import yaml
import os

# Load settings from config.yaml file
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
        return config['database']

# Load database configuration
db_config = load_config()

# Create MySQL database connection URL
DATABASE_URL = f"mysql+pymysql://{db_config['username']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database_name']}"

# Create engine for connecting to the database
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, echo=True)

# Check database connection
try:
    with engine.connect() as connection:
        # Execute a simple query to test the connection
        connection.execute(text("SELECT 1"))
    print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed! Error: {e}")
    raise Exception("Database connection failed!") from e

# Create SessionLocal for database interaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create a new session for database interaction
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
