import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

required_settings = [
    "PGHOST",
    "PGPORT",
    "PGDATABASE",
    "PGUSER",
    "PGPASSWORD",
]
missing_settings = [
    setting for setting in required_settings if not os.getenv(setting)
]

if missing_settings:
    raise RuntimeError(
        f"Missing settings in .env: {', '.join(missing_settings)}"
    )

tables = ("customers", "orders", "order_items", "products")

with psycopg.connect(
    host=os.environ["PGHOST"],
    port=int(os.environ["PGPORT"]),
    dbname=os.environ["PGDATABASE"],
    user=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
) as connection:
    with connection.cursor() as cursor:
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]
            print(f"{table}: {row_count} rows")
