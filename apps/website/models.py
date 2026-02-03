from django.db import models
from django.utils.translation import gettext_lazy as _
from utils import random_filename

class Project(models.Model):
    name = models.CharField(max_length=255)
    objective = models.TextField()
    expected_results = models.JSONField(help_text=_("List of expected results"))
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=random_filename, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    src = models.ImageField(upload_to=random_filename)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50] if self.description else f"Image {self.id}"

class Testimonial(models.Model):
    author_name = models.CharField(max_length=255)
    author_role = models.CharField(max_length=255, null=True, blank=True)
    author_image = models.ImageField(upload_to=random_filename, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Testimonial by {self.author_name}"

class Organisation(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    social_links = models.JSONField(default=dict, help_text=_("Social media links (e.g. {'facebook': '...', 'twitter': '...'})"))
    
    def __str__(self):
        return self.name

class Address(models.Model):
    organisation = models.ForeignKey(Organisation, related_name='addresses', on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20, null=True)
    is_principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.street}, {self.city}"

    def save(self, *args, **kwargs):
        if self.is_principal:
            # Set all other addresses for this organisation to not principal
            Address.objects.filter(organisation=self.organisation).update(is_principal=False)
        super().save(*args, **kwargs)
