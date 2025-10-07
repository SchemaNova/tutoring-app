import os
from loguru import logger
from sqlalchemy import create_engine, text

password = os.getenv("MYSQL_ROOT_PASSWORD")
host = os.getenv("HOSTNAME")
url = f"mysql+pymysql://root:{password}@{host}/tutoring_platform"

conn = create_engine(url, echo=True).connect()

logger.debug(f"{conn}")



import os
from sqlalchemy import create_engine, text

password = os.getenv("MYSQL_ROOT_PASSWORD")
host = os.getenv("HOSTNAME")
url = f"mysql+pymysql://root:{password}@{host}/tutoring_platform"  # include DB name
engine = create_engine(url, echo=True)

with engine.begin() as conn:
    total = conn.scalar(text("SELECT COUNT(*) FROM COURSE"))
    rows = conn.execute(text("SELECT course_id, course_name FROM COURSE LIMIT 5")).all()
    print("courses:", total, "sample:", rows)


