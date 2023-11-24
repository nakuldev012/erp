from rest_framework import serializers
from .models import HrConfig


class HrConfigSerializer( serializers.ModelSerializer,):
    class Meta:
        model = HrConfig
        fields = "__all__"