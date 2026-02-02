from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, GalleryViewSet, 
    TestimonialViewSet, OrganisationViewSet
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'gallery', GalleryViewSet, basename='gallery')
router.register(r'testimonials', TestimonialViewSet, basename='testimonial')
router.register(r'organisation', OrganisationViewSet, basename='organisation')

urlpatterns = [
    path('', include(router.urls)),
]
