from django.core.files.storage import default_storage
from rest_framework import serializers
from diagnosis_code.models import DiagnosisCode
from .tasks import process_csv_file


class DiagnosisCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisCode
        fields = '__all__'


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True, allow_null=False, allow_empty_file=False,)
    user_email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        file = validated_data['file']
        file_name = default_storage.save(file.name, file)
        if not file_name or str(file_name.split(".")[-1]).lower() != "csv":
            raise serializers.ValidationError("Sorry we support only csv files")
        process_csv_file.delay(file_name=file_name,
                               user_email=validated_data.get('user_email', None))
        return True

    def update(self, instance, validated_data):
        raise NotImplementedError('Not required')
