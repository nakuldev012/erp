from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import AddressEmpInfo
from mferp.common.errors import ForbiddenErrors


@receiver(pre_save, sender=AddressEmpInfo)
def validate_address_limit(instance, **kwargs):
    # Check if the employee already has two addresses
    existing_addresses_count = AddressEmpInfo.objects.filter(emp=instance.emp).count()

    if existing_addresses_count > 2:
        raise ForbiddenErrors("Cannot have more than two addresses for an employee")
