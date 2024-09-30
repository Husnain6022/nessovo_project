from bson import ObjectId
from django.db import models

class Item(models.Model):
    id = models.CharField(primary_key=True, default=str(ObjectId()), editable=False, max_length=24)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name