import random

from mysql_ingestion.seeders.base_faker import BaseFaker


class SalesOrderLineItemFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)
        self.__connection = connection

    def fill_data(self):
        connection = self.__connection.get_connection()
        with connection.cursor() as cursor:
            # Fetch product IDs
            cursor.execute("SELECT ProductID FROM Product")
            product_ids: list = [id[0] for id in cursor.fetchall()]

            # Fetch sales order IDs
            cursor.execute("SELECT SalesOrderID FROM SalesOrder")
            sales_order_ids: list = [id[0] for id in cursor.fetchall()]

            for _ in range(self._size):
                sales_order_id = random.choice(sales_order_ids)
                product_id = random.choice(product_ids)
                quantity = random.randint(1, 10)
                unit_price = round(
                    random.uniform(10, 100), 2
                )  # Assuming you have this info or fetch it from Product table
                total_price = quantity * unit_price

                cursor.execute(
                    """
                    INSERT INTO LineItem (
                        SalesOrderID, ProductID, Quantity, UnitPrice, TotalPrice)
                    VALUES (%s, %s, %s, %s, %s)
                """,
                    (sales_order_id, product_id, quantity, unit_price, total_price),
                )

            connection.commit()
        connection.close()
