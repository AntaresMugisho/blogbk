from rest_framework import viewsets, permissions
from .models import Project, GalleryImage, Testimonial, Organisation
from .serializers import (
    ProjectSerializer, GalleryImageSerializer, 
    TestimonialSerializer, OrganisationSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = GalleryImage.objects.all()
    serializer_class = GalleryImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Organisation.objects.all()
