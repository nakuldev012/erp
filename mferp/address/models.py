
from django.db import models
from mferp.common.choices import ADDRESS_TYPE
from mferp.common.validators import validate_zip


class Country(models.Model):
    name = models.CharField(max_length=256)
    iso3 = models.CharField(max_length=3)
    iso2 = models.CharField(max_length=2)
    phone_code = models.CharField(null=True, blank=True, max_length=24)
  
    def __str__(self):
        return self.name


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="state_country")
    name = models.CharField(max_length=256)
    state_code = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}, {self.country.name}"
    
# class District(models.Model):
#     name = models.CharField(max_length=512)
#     state = models.ForeignKey(State, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.name}, {self.state.name}, {self.state.country.name}"


class City(models.Model):
    name = models.CharField(max_length=512)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="city_state")

    def __str__(self):
        return f"{self.name}, {self.state.name}, {self.state.country.name}"


class BaseAddress(models.Model):
	type = models.CharField(choices=ADDRESS_TYPE, max_length=250,
        default="permanent",)
	address = models.TextField()
	landmark = models.CharField(max_length=400, null=True, blank=True)
	city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="baseadress_city")
	zip = models.PositiveIntegerField(validators=[validate_zip])
    
	class Meta:
		abstract = True