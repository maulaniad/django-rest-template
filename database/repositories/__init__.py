"""Centralized place for pre-defined query functions used to retrieve data from the database."""


from database.repositories.profile import ProfileRepo
from database.repositories.user import UserRepo


__all__ = ["ProfileRepo", "UserRepo"]
