import datetime
import json
import os

import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ops.settings.settings')
application = get_wsgi_application()
django.setup()

from django.conf import settings

from mferp.address.models import City, Country, State
import ipdb;
ipdb.set_trace()
with open("erp_backend/countries-states-cities.json", "r") as handle:
    data = json.load(handle)

for country in data:
    country_instance = Country.objects.create(
        name=country["name"],
        iso3=country["iso3"],
        iso2=country["iso2"],
        phone_code=country["phone_code"],
    )

    states = country["states"]

    for state in states:
        state_instance = State.objects.create(
            country=country_instance, name=state["name"], state_code=state["state_code"]
        )

        cities = state["cities"]

        for city in cities:
            City.objects.create(name=city["name"], state=state_instance)
