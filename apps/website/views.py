from rest_framework import viewsets, permissions
from .models import Project, Gallery, Testimonial, Organisation
from .serializers import (
    ProjectSerializer, GallerySerializer, 
    TestimonialSerializer, OrganisationSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
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
        # Allow only one organisation config? Or multiple? 
        # Usually it's just one, but ViewSet allows multiple.
        return Organisation.objects.all()
