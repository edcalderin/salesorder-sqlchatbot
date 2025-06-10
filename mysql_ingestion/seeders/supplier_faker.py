from faker import Faker

from mysql_ingestion.seeders.base_faker import BaseFaker


class SupplierFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)
        self.__connection = connection
        self.__fake = Faker()

    def fill_data(self):
        connection = self.__connection.get_connection()
        with connection.cursor() as cursor:
            for _ in range(self._size):
                company_name = self.__fake.company()
                contact_name = self.__fake.name()
                contact_title = self.__fake.job()[:50]
                contact_title = (
                    contact_title if len(contact_title) > 50 else contact_title
                )
                address = self.__fake.address().replace(
                    "\n", ", "
                )  # Replace newlines with commas for address
                phone = self.__fake.phone_number()[:20]
                email = self.__fake.email()

                # Insert supplier data
                cursor.execute(
                    """
                INSERT INTO Supplier (
                    CompanyName, ContactName, ContactTitle, Address, Phone, Email)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                    (company_name, contact_name, contact_title, address, phone, email),
                )

            connection.commit()
        connection.close()
