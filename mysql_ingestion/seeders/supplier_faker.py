from mysql_ingestion.seeders.base_faker import BaseFaker


class SupplierFaker(BaseFaker):
    def __init__(self, connection):
        super().__init__(connection)

    def fill_data(self):
        connection = self._connection.get_connection()
        with connection.cursor() as cursor:
            for _ in range(self._size):
                company_name = self._faker.company()
                contact_name = self._faker.name()
                contact_title = self._faker.job()[:50]
                contact_title = (
                    contact_title if len(contact_title) > 50 else contact_title
                )
                address = self._faker.address().replace(
                    "\n", ", "
                )  # Replace newlines with commas for address
                phone = self._faker.phone_number()[:20]
                email = self._faker.email()

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
