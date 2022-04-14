from django.db import models
from shortuuid.django_fields import ShortUUIDField
from appchance.settings import SHORTENED_LINK_LENGTH
from django.core.validators import URLValidator, validate_ipv4_address

validate_url = URLValidator()


class Link(models.Model):
    shortened_link = ShortUUIDField(length=SHORTENED_LINK_LENGTH, primary_key=True)
    link = models.CharField(unique=True, max_length=30, validators=[validate_url])
    visits_count = models.IntegerField(default=0)
    user_ip = models.CharField(max_length=18, validators=[validate_ipv4_address], null=True)
    user_agent = models.CharField(max_length=30, null=True)

    def __str__(self) -> str:
        return self.link
