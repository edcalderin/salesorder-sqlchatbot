import random

from mysql_ingestion.seeders.base_faker import BaseFaker


class ProductFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)

    def fill_data(self):
        connection = self._connection.get_connection()
        with connection.cursor() as cursor:
            for _ in range(self._size):
                product_name = f"{self._faker.word().capitalize()}"
                f" {self._faker.word().capitalize()}"

                description = self._faker.sentence(nb_words=10)
                unit_price = round(
                    random.uniform(10, 500), 2
                )  # Random price between $10 and $500
                stock_quantity = random.randint(
                    10, 1000
                )  # Random stock quantity between 10 and 1000
                reorder_level = random.randint(
                    5, 50
                )  # Random reorder level between 5 and 50
                discontinued = random.choice(
                    [0, 1]
                )  # Randomly choose between 0 (false) and 1 (true)

                # Insert product data
                cursor.execute(
                    """
                    INSERT INTO Product (
                        ProductName, Description, UnitPrice, StockQuantity,
                        ReorderLevel, Discontinued)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (
                        product_name,
                        description,
                        unit_price,
                        stock_quantity,
                        reorder_level,
                        discontinued,
                    ),
                )

            connection.commit()
        connection.close()
