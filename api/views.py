from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import DiagnosisCodeSerializer, FileUploadSerializer
from diagnosis_code.models import DiagnosisCode


class CustomPagination(PageNumberPagination):
    page_size = 20


class CreateDiagnosisCodeView(generics.CreateAPIView):
    serializer_class = DiagnosisCodeSerializer


class DiagnosisCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiagnosisCodeSerializer
    queryset = DiagnosisCode.objects.all()
    lookup_url_kwarg = "id"


class DiagnosisCodeListView(generics.ListAPIView):
    serializer_class = DiagnosisCodeSerializer
    pagination_class = CustomPagination
    queryset = DiagnosisCode.objects.all().order_by("-id")


class CreateDiagnosisCodeByFileUploadView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    queryset = DiagnosisCode.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                return Response({
                    "detail": e.get_full_details() if isinstance(e, serializers.ValidationError) else str(e)
                }, status=status.HTTP_403_FORBIDDEN)
            return Response({"detail": "File successfully uploaded"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Uploading file failed", "errors": serializer.errors},
                        status=status.HTTP_403_FORBIDDEN)

