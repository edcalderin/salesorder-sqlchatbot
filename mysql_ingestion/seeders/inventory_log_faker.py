import random

from mysql_ingestion.seeders.base_faker import BaseFaker


class InventoryLogFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)

    def fill_data(self):
        connection = self._connection.get_connection()
        with connection.cursor() as cursor:
            # Fetch Product IDs
            cursor.execute("SELECT ProductID FROM Product")
            product_ids: list = [row[0] for row in cursor.fetchall()]

            for _ in range(self._size):
                product_id = random.choice(product_ids)  # Randomly select a product ID
                change_date = self._faker.date_between(
                    start_date="-1y", end_date="today"
                )
                quantity_change = random.randint(
                    -100, 100
                )  # Assuming inventory can increase or decrease
                notes = "Inventory " + (
                    "increased" if quantity_change > 0 else "decreased"
                )

                # Insert inventory log data
                cursor.execute(
                    """
                    INSERT INTO InventoryLog (
                        ProductID, ChangeDate, QuantityChange, Notes)
                    VALUES (%s, %s, %s, %s)
                """,
                    (product_id, change_date, quantity_change, notes),
                )

            connection.commit()
        connection.close()
