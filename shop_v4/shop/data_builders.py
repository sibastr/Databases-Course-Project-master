from .models import Color, Category
from users.models import MyUser


class ColorBuilder():
    name = None

    def with_name(self, name: str):
        self.name = name

    def build(self):
        return Color(name = self.name)

class CategoryBuilder():
    name = None

    def with_name(self, name: str):
        self.name = name

    def build(self):
        return Category(name=self.name)

class UserBuilder():
    email = None
    password = None

    def with_email(self, email: str):
        self.email = email

    def with_password(self, password: str):
        self.password = password

    def build(self):
        return MyUser(email =self.email,password =self.password)