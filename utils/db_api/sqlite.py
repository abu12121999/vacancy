import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            telegram_id int NOT NULL,
            first_name varchar(64) NOT NULL,
            last_name varchar(64) NOT NULL,
            username varchar(64) NULL,
            phone varchar(13) NOT NULL,
            PRIMARY KEY (telegram_id)
            );
"""
        self.execute(sql, commit=True)

    def create_table_category(self):
        sql = """
        CREATE TABLE Category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name varchar(255) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    def create_table_village(self):
        sql = """
        CREATE TABLE Village (
            village_id INTEGER PRIMARY KEY AUTOINCREMENT,
            village_name varchar(64) NOT NULL,
            reg_id varchar(64) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    def create_table_vacancy(self):

        sql = """
        CREATE TABLE Vacancy (
            vacancy_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location varchar(128) NOT NULL,
            category varchar(128) NOT NULL,
            name varchar(128) NOT NULL,
            author_id varchar(31) NOT NULL,
            salary varchar(255) NOT NULL,
            status varchar(31) NOT NULL,
            deadline varchar(31) NOT NULL,
            file_id varchar(255) NOT NULL,
            description TEXT NOT NULL,
            uuid varchar(128) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())
# INSERT information to db
    def add_user(self, telegram_id: int, first_name: str, last_name: str, username: str = None, phone: str=None):
        # SQL_EXAMPLE = "INSERT INTO Users(telegram_id, first_name, last_name, username, phone) VALUES(123456, 'John', 'adam', '@salom' '+998930756606')"

        sql = """
        INSERT INTO Users(telegram_id, first_name, last_name, username, phone) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(telegram_id, first_name, last_name, username, phone), commit=True)

    def add_vacancy(self, location, category, name, author_id, salary, status, deadline, file_id, description, uuid):
        sql = """INSERT INTO Vacancy (location, category, name, author_id, salary, status, deadline, file_id, description, uuid) 
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute(sql, parameters=(location, category, name, author_id, salary, status, deadline, file_id, description, uuid), fetchone=True, commit=True)

    def add_category(self, category_name):
        sql = """INSERT INTO Category(category_name) 
        VALUES(?)
        """
        return self.execute(sql, parameters=(category_name,), fetchone=True, commit=True)

    def add_village(self, village_name, reg_id):
        sql = """INSERT INTO Village(village_name, reg_id) 
        VALUES(?,?)
        """
        return self.execute(sql, parameters=(village_name, reg_id), fetchone=True, commit=True)

# SELECT
    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_all_village(self):
        sql = """
        SELECT * FROM Village
        """
        return self.execute(sql, fetchall=True)

    def select_all_category(self):
        sql = """
        SELECT * FROM Category
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def get_village_name(self, village_id):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT village_name FROM Village WHERE village_id == ?"
        return self.execute(sql, parameters=(village_id,), fetchone=True)

    def select_village(self, reg_id):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT village_id, village_name FROM Village WHERE reg_id == ?"
        return self.execute(sql, parameters=(reg_id,), fetchall=True)

    def select_vacancy(self, uuid):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM Vacancy WHERE uuid == ?"
        return self.execute(sql, parameters=(uuid,), fetchone=True)

    def select_active_vacancy(self):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT category, name, salary, location, description, deadline, author_id, file_id FROM Vacancy WHERE status == 'active' "
        return self.execute(sql, fetchall=True)

    def select_category(self, category_id):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT category_name FROM Category WHERE category_id == ?"
        return self.execute(sql, parameters=(category_id,), fetchone=True)

    def numbers_active_vacancy(self):
        sql = """
        SELECT COUNT(*) FROM Vacancy WHERE status == "active"
        """
        return self.execute(sql, fetchone=True)

    def edit_vacancy_status(self, status, uuid):

        sql = f"""
        UPDATE Vacancy SET status = ? WHERE uuid == ?
        """
        return self.execute(sql, parameters=(status, uuid), commit=True)










    def select_all_id_tests(self):
        return self.execute("SELECT test_id FROM Tests ", fetchall=True)

    def select_participiant(self, a_test_id):
        sql = """SELECT a_member_id FROM Answers WHERE a_test_id== ?"""
        return self.execute(sql, parameters=(a_test_id,), fetchall=True)

    def select_test(self, **kwargs):
        sql = "SELECT * FROM Tests WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def active_tests(self):
        sql = "SELECT test_author, test_name, test_answers, test_id FROM Tests WHERE test_status=='Faol' "
        return self.execute(sql, fetchall=True)

    def select_answer(self, a_test_id, a_member_id):
        sql = f"""SELECT * FROM Answers WHERE a_test_id == ? AND a_member_id == ?"""
        return self.execute(sql, parameters=(a_test_id, a_member_id,), fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def count_tests(self):
        return self.execute("SELECT COUNT(*) FROM Tests;", fetchone=True)

    def edit_user_info(self, first_name, last_name, telegram_id):

        sql = f"""
        UPDATE Users SET first_name=?, last_name=? WHERE telegram_id ==?
        """
        return self.execute(sql, parameters=(first_name, last_name, telegram_id), commit=True)

    def test_end(self, test_id):
        sql = f"""UPDATE Tests SET test_status="Yakunlangan" WHERE test_id == ?"""
        return self.execute(sql, parameters=(test_id,), commit=True)

    def select_result(self, a_test_id):
        sql = """SELECT a_name_surname, a_ball, a_time FROM Answers WHERE a_test_id == ? ORDER BY a_ball DESC"""
        return self.execute(sql, parameters=(a_test_id,), fetchall=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)




def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")