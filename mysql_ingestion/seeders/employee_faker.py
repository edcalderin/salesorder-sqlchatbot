from faker import Faker

from mysql_ingestion.seeders.base_faker import BaseFaker


class EmployeeFaker(BaseFaker):
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
                hire_date = self.__fake.date_between(start_date="-5y", end_date="today")
                position = self.__fake.job()
                salary = round(
                    self.__fake.random_number(digits=5), 2
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
