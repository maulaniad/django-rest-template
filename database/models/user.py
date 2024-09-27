from typing import Any
from django.contrib.auth.models import User as _User

from database.models.profile import Profile


class User(_User):
    """This class is not used to define `auth_user` table. It's only here for typehinting purposes."""
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    profile: Profile

    class Meta:
        managed = False
