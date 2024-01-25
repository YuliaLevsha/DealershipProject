from django.db import models
from django_countries import Countries


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class G8Countries(Countries):
    only = ['CA', 'FR', 'DE', 'IT', 'JP', 'RU', 'GB', 'CN']
