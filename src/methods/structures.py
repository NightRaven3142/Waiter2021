class Rating:
    def __init__(self, rating):
        self.__rating = 0
        self.__rating_count = 0
        self.add_rating(rating)

    def add_rating(self, rating):
        self.__rating_count += 1
        self.__rating = (self.__rating + rating) / self.__rating_count


class User:
    def __init__(self, data):
        self.__user_id = None
        self.first_name = None
        self.last_name = None
        self.email_address = None
        self.password_hash = None
        self.DoB = None
        self.username = None

        if len(data) == 0:
            return

        data = data[0]
        self.__data_as_tuple = data

        self.set_defaults(data)

    def set_defaults(self, data):
        self.__user_id = data[0]
        self.first_name = data[1]
        self.last_name = data[2]
        self.email_address = data[3]
        self.password_hash = data[4]
        self.DoB = data[5]
        self.username = data[6]

    def set_first_name(self, name):
        self.first_name = name

    def set_last_name(self, name):
        self.last_name = name

    def set_email_address(self, address):
        self.email_address = address

    def set_password_hash(self, hash):
        self.password_hash = hash

    def get_password_hash(self):
        return self.password_hash

    def get_user_id(self):
        return self.__user_id

    def get_data_as_tuple(self):
        return self.__data_as_tuple

    def is_empty(self):
        return True if self.__user_id is None else False


class Cook(User):
    def __init__(self, user, user_reference_id):
        self.set_defaults(user)

        self.__rating = Rating(0)
        self.__user_reference_id = user_reference_id

    def set_rating(self, r_value):
        self.__rating = self.__rating.set_rating(r_value)


class Customer(User):
    def __init__(self, user, user_reference_id):
        self.set_defaults(user)

        self.__allergies = []
        self.__orders_created = 0

        self.__user_reference_id = user_reference_id

    def add_allergy(self, allergy):
        self.__allergies.append(allergy)

    def set_orders_created(self):
        self.__orders_created += 1


class Order:
    def __init__(self, data):
        self.order_id = None
        self.__user_reference_id = None
        self.time_ordered = None

        self.set_order_defaults(data)

    def set_order_defaults(self, data):
        self.order_id = data[0]
        self.__user_reference_id = data[1]
        self.time_ordered = data[2]


class Dish:
    def __init__(self, data):
        self.dish_id = None
        self.name = None
        self.cuisine = None
        self.cooked_by = None
        self.description = None
        self.image_name = None
        self.price = None
        self.set_dish_defaults(data)

    def set_dish_defaults(self, data):
        self.dish_id = data[0]
        self.name = data[1]
        self.cuisine = data[2]
        self.cooked_by = data[3]
        self.description = data[4]
        self.image_name = data[5]
        self.price = data[6]