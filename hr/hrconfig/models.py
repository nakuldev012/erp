from django.db import models
from mferp.mastertableconfig.models import AbstractTime



class HrConfig(AbstractTime):
    label = models.CharField(max_length=100)
    max_subcategory_level = models.PositiveIntegerField(default=5)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.label