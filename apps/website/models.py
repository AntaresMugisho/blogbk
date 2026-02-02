from django.db import models
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    name = models.CharField(max_length=255)
    objective = models.TextField()
    expected_results = models.JSONField(help_text=_("List of expected results"))
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50] if self.description else f"Image {self.id}"

class Testimonial(models.Model):
    author_name = models.CharField(max_length=255)
    author_title = models.CharField(max_length=255)
    author_image = models.ImageField(upload_to='testimonials/', null=True, blank=True)
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
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    is_principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.address_line}, {self.city}"

    def save(self, *args, **kwargs):
        if self.is_principal:
            # Set all other addresses for this organisation to not principal
            Address.objects.filter(organisation=self.organisation).update(is_principal=False)
        super().save(*args, **kwargs)
