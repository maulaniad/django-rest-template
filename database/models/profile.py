from django.contrib.auth.models import User
from django.db.models import CharField, OneToOneField, CASCADE

from database.models.base import BaseModel


class Profile(BaseModel):
    name = CharField(max_length=50, blank=True, db_index=True)
    email = CharField(max_length=50, blank=True, db_index=True)
    phone = CharField(max_length=15, blank=True)
    user = OneToOneField(User, on_delete=CASCADE, related_name="profile")

    class Meta(BaseModel.Meta):
        db_table = "profile"

    def __str__(self):
        return self.name
