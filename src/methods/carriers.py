class navbar_data:
    left = None
    right_a = None
    right_b = None

    def set_left(self, val):
        self.left = val

    def set_right_a(self, val):
        self.right_a = val

    def set_right_b(self, val):
        self.right_b = val

    def populate_no_user(self):
        self.set_left("Order")
        self.set_right_a("Login")
        self.set_right_b("Signup")

    def populate_logged_in_user(self):
        self.set_left("Order")
        self.set_right_a("View Account")
        self.set_right_b("Logout")