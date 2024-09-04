from django.contrib.auth.models import User
from django.db.models import CharField, DecimalField, OneToOneField, CASCADE

from database.models.base import BaseModel


class Profile(BaseModel):
    name = CharField(max_length=50, blank=True, db_index=True)
    email = CharField(max_length=50, blank=True, db_index=True)
    user = OneToOneField(User, on_delete=CASCADE, related_name="profile")
    profit = DecimalField(max_digits=20, decimal_places=0, null=True)
    asset = DecimalField(max_digits=20, decimal_places=0, null=True)

    class Meta(BaseModel.Meta):
        db_table = "_profile"

    def __str__(self):
        return self.name
