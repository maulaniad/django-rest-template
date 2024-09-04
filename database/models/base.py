from typing import Any, Generic, Iterable, Optional, Self, Sequence, TypeVar

from django.db.models import Manager, Model, QuerySet, BigAutoField, CharField, DateTimeField
from django.utils import timezone

from helpers.utils import generate_oid


T = TypeVar('T', bound='BaseModel')

class CustomQuerySet(QuerySet, Generic[T]):
    def first(self) -> Optional[Self]:
        return super().first()

    def get(self, *args: Any, **kwargs: Any) -> Self:
        return super().get(*args, **kwargs)


class CustomManager(Manager, Generic[T]):
    def get_queryset(self) -> QuerySet[T] | CustomQuerySet[T]:
        return super().get_queryset().filter(date_deleted__isnull=True)

    def all_with_deleted(self) -> QuerySet[T]:
        """Fetch all objects from the database including soft-deleted ones."""
        return super().get_queryset()

    def deleted_only(self) -> QuerySet[T]:
        """Fetch only soft-deleted objects from the database."""
        return super().get_queryset().filter(date_deleted__isnull=False)

    def create(self, **kwargs: Any) -> T:
        """Create a new object and save it to the database."""
        return super().create(**kwargs)

    def bulk_create(self, objects: Iterable[Any], batch_size: int | Any = ..., ignore_conflicts: bool | Any = ..., update_conflicts: bool | Any = ..., update_fields: Sequence[str] | Any = ..., unique_fields: Sequence[str] | Any = ...) -> list[T]:
        """Bulk create objects and save them to the database."""
        return super().bulk_create(objects, batch_size, ignore_conflicts, update_conflicts, update_fields, unique_fields)

    def bulk_update(self, objects: Iterable[Any], fields: Sequence[str], batch_size: int | Any = ...) -> int:
        """Bulk update objects and save them to the database."""
        return super().bulk_update(objects, fields, batch_size)


class BaseModel(Model):
    id = BigAutoField(primary_key=True)
    oid = CharField(max_length=21, default=generate_oid)
    date_created = DateTimeField(auto_now_add=True)
    date_updated = DateTimeField(auto_now=True)
    date_deleted = DateTimeField(null=True)

    objects: CustomManager[Self] = CustomManager()  # type: ignore

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
