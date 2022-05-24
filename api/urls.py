from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'api'

urlpatterns = [
    path('create/', csrf_exempt(views.CreateDiagnosisCodeView.as_view()), name="create_code"),
    path('csv/upload/', csrf_exempt(views.CreateDiagnosisCodeByFileUploadView.as_view()), name="file_upload"),
    path('<int:id>/', csrf_exempt(views.DiagnosisCodeDetailView.as_view()), name="diagnosis_code"),
    path('list/', csrf_exempt(views.DiagnosisCodeListView.as_view()), name="code_list")
]
