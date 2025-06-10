from mysql_ingestion.seeders.base_faker import BaseFaker


class CustomerFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)

    def fill_data(self):
        connection = self._connection.get_connection()
        with connection.cursor() as cursor:
            for _ in range(self._size):
                first_name = self._faker.first_name()
                last_name = self._faker.last_name()
                email = self._faker.email()
                phone = self._faker.phone_number()[:20]
                address = self._faker.address()
                customer_since = self._faker.date_between(
                    start_date="-5y", end_date="today"
                )
                is_active = self._faker.boolean()

                cursor.execute(
                    """
                        INSERT INTO Customer (
                            FirstName, LastName, Email, Phone, BillingAddress,
                            ShippingAddress, CustomerSince, IsActive)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        first_name,
                        last_name,
                        email,
                        phone,
                        address,
                        address,
                        customer_since,
                        is_active,
                    ),
                )

            connection.commit()
        connection.close()
