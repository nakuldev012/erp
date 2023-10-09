from django.core.validators import RegexValidator
import re
from rest_framework import status

phone_validator = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
)

validate_zip = RegexValidator(re.compile(r'^[1-9][0-9]{5}$'), ("Invalid pin code."), status.HTTP_400_BAD_REQUEST)