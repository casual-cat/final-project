import os

DB_HOST = os.getenv('DB_HOST', '44.211.155.253')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'a1a2a3')
DB_NAME = os.getenv('DB_NAME', 'final_project_db')

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

