from django.db import models
import re

# Create your models here.

class AttendeeManager(models.Manager):
    def attendee_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Confirmation does not match password."
        return errors

class Attendee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_organizer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=AttendeeManager()

class OrganizerManager(models.Manager):
    def organizer_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['org_name']) < 2:
            errors['org_name'] = "Organization Name must be at least 2 characters."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be valid."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Confirmation does not match password."
        return errors

class Organizer(models.Model):
    org_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_organizer = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects=OrganizerManager()

class ConManager(models.Manager):
    def con_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors['name'] = "Name must be at least 3 characters."
        if len(postData['description']) < 8:
            errors['description'] = "Description must be at least 8 characters."
        if len(postData['date']) < 1:
            errors['description'] = "Date required."
        if len(postData['location']) < 1:
            errors['description'] = "Location required."
        return errors

class Convention(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    con_type = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    created_by = models.ForeignKey(Organizer, related_name="cons", on_delete=models.CASCADE)
    likes = models.ManyToManyField(Attendee,related_name="likes")
    rsvps = models.ManyToManyField(Attendee,related_name="rsvps")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ConManager()