import sqlite3
from src.methods.structures import User

class SQLDb:
    __conn = None

    def connect(self):
        try:
            self.__conn = sqlite3.connect("src/WAITER.db")
        except Exception as e:
            print(e)

    def close_connection(self):
        if self.__conn:
            self.__conn.close()

    def initialise_tables(self):
        self.__create_users_table()
        self.__create_orders_table()
        self.__create_cooks_table()
        self.__create_customers_table()
        self.__create_dishes_table()

    def __get_last_row_id(self):
        self.connect()
        try:
            cur = self.__conn.cursor()
            return cur.lastrowid
        except Exception as e:
            print(e)
        self.close_connection()

    def __execute_command(self, command, do_commit):
        self.connect()
        try:
            cur = self.__conn.cursor()
            cur.execute(command)

            if do_commit:
                self.__conn.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def __execute_insert_command(self, command, data):
        self.connect()
        try:
            cur = self.__conn.cursor()
            cur.execute(command, data)
            self.__conn.commit()
        except Exception as e:
            print(e)
        self.close_connection()

    def __execute_select_command(self, command):
        self.connect()
        try:
            cur = self.__conn.cursor()
            cur.execute(command)

            return cur.fetchall()
        except Exception as e:
            print(e)
        self.close_connection()


    def __create_dishes_table(self):
        create_tasks_command = """ CREATE TABLE IF NOT EXISTS dishes(
                        dish_id INTEGER PRIMARY KEY,
                        name text NOT NULL,
                        cuisine VARCHAR(20) NOT NULL,
                        cooked_by INTEGER NOT NULL, 
                        dish_description text, 
                        image_name text,
                        FOREIGN KEY(cooked_by) REFERENCES cooks(cook_id)
                        );
                        """
        self.__execute_command(create_tasks_command, False)

    def __create_users_table(self):
        create_users_command = """ CREATE TABLE IF NOT EXISTS users(
                                    user_id INTEGER PRIMARY KEY,
                                    first_name text NOT NULL,
                                    last_name text NOT NULL,
                                    email_address text NOT NULL,
                                    password_hash text NOT NULL,
                                    DoB datetime NOT NULL
                                    );
        """

        self.__execute_command(create_users_command, False)

    def __create_customers_table(self):
        create_list_command = """ CREATE TABLE IF NOT EXISTS customers(
                                customer_id integer PRIMARY KEY,
                                allergies text NOT NULL,
                                orders_created INTEGER NOT NULL,
                                user_reference_id INTEGER,
                                FOREIGN KEY(user_reference_id) REFERENCES users(user_id)
                                );
                              """

        self.__execute_command(create_list_command, False)

    def __create_cooks_table(self):
        create_list_command = """ CREATE TABLE IF NOT EXISTS cooks(
                                cook_id integer PRIMARY KEY,
                                dishes_available INTEGER NOT NULL,
                                rating_count INTEGER NOT NULL,
                                rating REAL,
                                user_reference_id INTEGER NOT NULL,
                                FOREIGN KEY(user_reference_id) REFERENCES users(user_id)
                                );
                              """

        self.__execute_command(create_list_command, False)

    def __create_orders_table(self):
        create_list_command = """ CREATE TABLE IF NOT EXISTS orders(
                                order_id integer PRIMARY KEY,
                                user_reference_id INTEGER NOT NULL,
                                dish_reference_id INTEGER NOT NULL,
                                
                                time_ordered datetime NOT NULL,
                                address text NOT NULL,
                                
                                FOREIGN KEY(user_reference_id) REFERENCES users(user_id),
                                FOREIGN KEY(dish_reference_id) REFERENCES dishes(dish_id)
                                );
                              """

        self.__execute_command(create_list_command, False)


    def insert_new_dish(self, dish):
        insert_dish_command = """ INSERT INTO dishes(name, cuisine, cooked_by, dish_description, image_name, price) VALUES (?, ?, ?, ?, ?, ?);"""

        self.__execute_insert_command(insert_dish_command, dish)

    def insert_new_user(self, user):
        insert_command = """INSERT INTO users(first_name, last_name, email_address, password_hash, DoB, username) 
                         VALUES(?, ?, ?, ?, ?, ?);
                         """

        self.__execute_insert_command(insert_command, user)

    def insert_new_customer(self, customer):
        self.insert_new_user(customer)

        user_ref = User(self.get_username(customer[-1]))

        insert_command = """INSERT INTO customers(allergies, orders_created, user_reference_id) 
                         VALUES(?, ?, ?);
                         """

        self.__execute_insert_command(insert_command, ("", 0, user_ref.get_user_id()))

    def insert_new_cook(self, user_data):
        self.insert_new_user(user_data)

        user_ref = User(self.get_username(user_data[-1]))

        insert_command = """INSERT INTO cooks(dishes_available, rating_count, rating, user_reference_id) 
                         VALUES(?, ?, ?, ?);
                         """

        self.__execute_insert_command(insert_command, (0, 0, 0, user_ref.get_user_id()))

    def insert_new_order(self, order):
        insert_order_command = """INSERT INTO orders(user_reference_id, dish_reference_id, time_ordered, address) 
        VALUES (?, ?, ?, ?);"""

        self.__execute_insert_command(insert_order_command, order)


    def update_status(self, name, current_list, status):
        print(f"Task: {name} {status}")
        data = (status, name, current_list)
        update_task_command = """UPDATE tasks SET is_complete = ? WHERE name = ? AND parent_list = ?;"""

        self.__execute_insert_command(update_task_command, data)

    def delete_customer_from_list(self, customer_id):
        delete_command = """DELETE FROM customers WHERE customer_id = ?;
                         """.format(id=customer_id)

        self.__execute_insert_command(delete_command, (customer_id,))

    def delete_cook_from_list(self, cook_id):
        delete_cook_command = """DELETE FROM cooks WHERE cook_id = ?;""".format(id=cook_id)

        self.__execute_insert_command(delete_cook_command, (cook_id,))

    def delete_dish_from_list(self, dish_id):
        delete_dish_command = """DELETE FROM dishes WHERE dish_id = ?;""".format(id=dish_id)

        self.__execute_insert_command(delete_dish_command, (dish_id,))

    def get_customer_from_list(self, customer_id):
        select_tasks_command = """SELECT * FROM customers WHERE customer_id = {id};
                               """.format(id=customer_id)

        return self.__execute_select_command(select_tasks_command)

    def get_username(self, username):
        select_users_command = """SELECT * FROM users WHERE username = "{username}" OR email_address = "{username}";""".format(username=username)

        return self.__execute_select_command(select_users_command)

    def get_all_dishes(self):
        select_dishes_command = """SELECT * FROM dishes;"""

        return self.__execute_select_command(select_dishes_command)

    def get_all_lists(self):
        select_lists_command = """SELECT * FROM lists;
                               """
        return self.__execute_select_command(select_lists_command)

    def is_user_in_cook_table(self, user_id):
        select_cook_command = f"""SELECT user_reference_id FROM cooks WHERE user_reference_id= {user_id}"""
        return True if len(self.__execute_select_command(select_cook_command)) > 0 else False

    def is_user_in_customer_table(self, user_id):
        select_customer_command = f"""SELECT user_reference_id FROM customers WHERE user_reference_id= {user_id}"""
        return True if len(self.__execute_select_command(select_customer_command)) > 0 else False

