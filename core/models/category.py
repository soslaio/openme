
from django.db import models
from .base import Base


class Category(Base):
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    @property
    def is_root(self):
        return not self.parent_category

    def __str__(self):
        return self.name
