import logging
import os

from dotenv import load_dotenv

from mysql_ingestion.db.connection import Connection
from mysql_ingestion.seeders import (
    CustomerFaker,
    EmployeeFaker,
    InventoryLogFaker,
    ProductFaker,
    SalesOrderFaker,
    SalesOrderLineItemFaker,
    SupplierFaker,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

load_dotenv()

connection = Connection(
    host=os.getenv("MYSQL_HOST"),
    port=os.getenv("MYSQL_PORT"),
    database=os.getenv("MYSQL_DATABASE"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
)

fakers: list = [
    CustomerFaker,
    EmployeeFaker,
    ProductFaker,
    InventoryLogFaker,
    SupplierFaker,
    SalesOrderFaker,
    SalesOrderLineItemFaker,
]

if __name__ == "__main__":
    for faker in fakers:
        logging.info(f"Inserting data into {faker.__name__.removesuffix('Faker')}")
        faker(connection).fill_data()
