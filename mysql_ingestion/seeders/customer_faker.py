from faker import Faker

from mysql_ingestion.seeders.base_faker import BaseFaker


class CustomerFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)
        self.__connection = connection
        self.__fake = Faker()

    def fill_data(self):
        connection = self.__connection.get_connection()
        with connection.cursor() as cursor:
            for _ in range(self._size):
                first_name = self.__fake.first_name()
                last_name = self.__fake.last_name()
                email = self.__fake.email()
                phone = self.__fake.phone_number()[:20]
                address = self.__fake.address()
                customer_since = self.__fake.date_between(
                    start_date="-5y", end_date="today"
                )
                is_active = self.__fake.boolean()

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
