from mysql_ingestion.seeders.base_faker import BaseFaker


class EmployeeFaker(BaseFaker):
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
                hire_date = self._faker.date_between(start_date="-5y", end_date="today")
                position = self._faker.job()
                salary = round(
                    self._faker.random_number(digits=5), 2
                )  # Generate a 5 digit salary

                # Insert employee data
                cursor.execute(
                    """
                    INSERT INTO Employee (
                        FirstName, LastName, Email, Phone, HireDate, Position, Salary)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                    (first_name, last_name, email, phone, hire_date, position, salary),
                )

            connection.commit()
        connection.close()
