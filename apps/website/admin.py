from django.contrib import admin
from .models import Project, GalleryImage, Testimonial, Organisation, Address

# @admin.register(Project)
# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('name', 'location', 'created_at')
#     search_fields = ('name', 'objective', 'location')

# @admin.register(GalleryImage)
# class GalleryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'description', 'created_at')

# @admin.register(Testimonial)
# class TestimonialAdmin(admin.ModelAdmin):
#     list_display = ('author_name', 'author_title', 'created_at')
#     search_fields = ('author_name', 'author_title')

# class AddressInline(admin.TabularInline):
#     model = Address
#     extra = 1

# @admin.register(Organisation)
# class OrganisationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'phone_number')
#     inlines = [AddressInline]
