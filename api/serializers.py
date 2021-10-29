from rest_framework import serializers

from .models import Check, Printer


class CreateChecksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Printer
        fields = ('point_id', )

    def to_representation(self, instance):
        serializer = ChecksSerializer(instance, context=self.context)
        return serializer.data


class ChecksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Check
        fields = ('id', )
