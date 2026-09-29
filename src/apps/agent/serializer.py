from rest_framework import serializers

from .models import Document
from .worker import document_upload_to_vector


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        fields = "__all__"

    def create(self, validated_data):
        document = super().create(validated_data)

        document_upload_to_vector.delay(
            document.id
        )

        return document