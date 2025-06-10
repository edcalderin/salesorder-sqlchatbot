import random
from datetime import timedelta

from mysql_ingestion.seeders.base_faker import BaseFaker


class SalesOrderFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)

    def fill_data(self):
        connection = self._connection.get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT CustomerID FROM Customer")
            customer_ids: list = [id[0] for id in cursor.fetchall()]
            for _ in range(self._size):
                customer_id = random.choice(customer_ids)
                order_date = self._faker.date_between(
                    start_date="-2y", end_date="today"
                )
                required_date = order_date + timedelta(days=random.randint(1, 30))
                shipped_date = (
                    order_date + timedelta(days=random.randint(1, 30))
                    if random.choice([True, False])
                    else None
                )
                status = random.choice(["Pending", "Completed", "Shipped"])
                is_paid = random.choice([True, False])

                cursor.execute(
                    """
                    INSERT INTO SalesOrder (
                        CustomerID, OrderDate, RequiredDate, ShippedDate, Status,
                        IsPaid)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (
                        customer_id,
                        order_date,
                        required_date,
                        shipped_date,
                        status,
                        is_paid,
                    ),
                )

            connection.commit()
        connection.close()
