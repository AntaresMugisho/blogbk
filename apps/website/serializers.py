from rest_framework import serializers
from .models import Project, Gallery, Testimonial, Organisation, Address

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'address_line', 'city', 'is_principal']

class OrganisationSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = Organisation
        fields = ['id', 'name', 'email', 'phone_number', 'social_links', 'addresses']

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        organisation = Organisation.objects.create(**validated_data)
        for address_data in addresses_data:
            Address.objects.create(organisation=organisation, **address_data)
        return organisation

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', None)
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.social_links = validated_data.get('social_links', instance.social_links)
        instance.save()

        if addresses_data is not None:
            # Simple implementation: replace all addresses
            # For a more robust implementation, one could match by ID
            instance.addresses.all().delete()
            for address_data in addresses_data:
                Address.objects.create(organisation=instance, **address_data)
        
        return instance
