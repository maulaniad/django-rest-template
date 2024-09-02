from typing import TypeVar, Generic

from django.db.models import Manager, Model, BigAutoField, CharField, DateTimeField
from django.db.models.query import QuerySet
from django.utils import timezone

from helpers.utils import generate_oid


T = TypeVar('T', bound='BaseModel')

class CustomManager(Manager, Generic[T]):
    def get_queryset(self) -> QuerySet[T]:
        return super().get_queryset().filter(date_deleted__isnull=True)

    def all_with_deleted(self) -> QuerySet[T]:
        """Fetch all objects from the database including soft-deleted ones."""
        return super().get_queryset()

    def deleted_only(self) -> QuerySet[T]:
        """Fetch only soft-deleted objects from the database."""
        return super().get_queryset().filter(date_deleted__isnull=False)


class BaseModel(Model):
    id = BigAutoField(primary_key=True)
    oid = CharField(max_length=21, default=generate_oid)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)
    date_deleted = DateTimeField(null=True)

    objects: CustomManager['BaseModel'] = CustomManager['BaseModel']()  # type: ignore

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Safe deletion through a soft-delete, marked with a deleted date."""
        self.date_deleted = timezone.now()
        self.save()

    def hard_delete(self):
        """The real deletion, wiping data from the database."""
        super().delete()

    def restore(self):
        """Undo a soft-delete, nullifying the deleted date"""
        self.date_deleted = None
        self.save()
