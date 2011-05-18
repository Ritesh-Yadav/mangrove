# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from django.contrib.auth.models import User
from django.db import models


class Organization(models.Model):
    name = models.TextField()
    sector = models.TextField()
    addressline1 = models.TextField()
    addressline2 = models.TextField()
    city = models.TextField()
    state = models.TextField()
    country = models.TextField()
    zipcode = models.TextField()
    office_phone = models.TextField()
    website = models.TextField()
    org_id = models.TextField()


class NGOUserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    title = models.TextField()
    org_id = models.TextField()

class OrganizationSettings(models.Model):
    organization = models.ForeignKey(Organization)
    document_store = models.TextField()


