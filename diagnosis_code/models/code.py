from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class DiagnosisCode(BaseModel):
    category_code = models.CharField(max_length=50)
    diagnosis_code = models.CharField(max_length=50)
    full_code = models.CharField(max_length=50)
    abbreviated_description = models.CharField(max_length=50)
    full_description = models.CharField(max_length=800)
    category_title = models.CharField(max_length=50)

    def __str__(self):
        return "{}".format(self.id)

