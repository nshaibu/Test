from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from model_mommy import mommy
from diagnosis_code.models import DiagnosisCode


class DiagnosisCodeAPITest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.code1 = mommy.make(DiagnosisCode)

    def tearDown(self):
        DiagnosisCode.objects.all().delete()

    def test_api_can_create_a_record(self):
        url = reverse('api:create_code')
        response = self.client.post(url, data={
            "category_code": "1111",
            "diagnosis_code": "1111",
            "full_code": "1111",
            "abbreviated_description": "1111",
            "full_description": "1111",
            "category_title": "1111"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_can_return_detail_of_a_record(self):
        url = reverse('api:diagnosis_code', args=(self.code1.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["id"], self.code1.id)

    def test_api_can_update_a_record(self):
        url = reverse('api:diagnosis_code', args=(self.code1.id,))
        response = self.client.put(url, data={
            "category_code": "3232",
            "diagnosis_code": "ewqwee",
            "full_code": "eqweqwe",
            "abbreviated_description": "eqweqw",
            "full_description": "eqwewe",
            "category_title": "eqweqwe"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.code1.refresh_from_db()
        data = response.json()
        self.assertEqual(data['category_code'], self.code1.category_code)
        self.assertEqual(data['diagnosis_code'], self.code1.diagnosis_code)
        self.assertEqual(data["full_code"], self.code1.full_code)
        self.assertEqual(data['abbreviated_description'], self.code1.abbreviated_description)
        self.assertEqual(data['full_description'], self.code1.full_description)
        self.assertEqual(data['category_title'], self.code1.category_title)

    def test_api_can_delete_a_record(self):
        mommy.make(DiagnosisCode)
        code = mommy.make(DiagnosisCode)
        count = DiagnosisCode.objects.count()
        url = reverse('api:diagnosis_code', args=(code.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertGreater(count, DiagnosisCode.objects.count())

    def test_api_returns_all_records(self):
        url = reverse('api:code_list')
        for _ in range(1, 40):
            mommy.make(DiagnosisCode)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['count'], 40)
        self.assertEqual(len(data['results']), 20)

    def test_api_is_able_to_upload_csv_file(self):
        url = reverse('api:file_upload')
        content = b"""
        A00,0,A000,"Cholera due to Vibrio cholerae 01, biovar cholerae","Cholera due to Vibrio cholerae 01, biovar cholerae","Cholera"\n
        A00,1,A001,"Cholera due to Vibrio cholerae 01, biovar eltor","Cholera due to Vibrio cholerae 01, biovar eltor","Cholera"\n
        A010,0,A0100,"Typhoid fever, unspecified","Typhoid fever, unspecified","Typhoid fever"\n
        A010,1,A0101,"Typhoid meningitis","Typhoid meningitis","Typhoid fever"\n
        A010,2,A0102,"Typhoid fever with heart involvement","Typhoid fever with heart involvement","Typhoid fever"\n
        A010,3,A0103,"Typhoid pneumonia","Typhoid pneumonia","Typhoid fever"\n
        A010,4,A0104,"Typhoid arthritis","Typhoid arthritis","Typhoid fever"\n
        A010,5,A0105,"Typhoid osteomyelitis","Typhoid osteomyelitis","Typhoid fever"\n
        A010,9,A0109,"Typhoid fever with other complications","Typhoid fever with other complications","Typhoid fever"
        """
        file = SimpleUploadedFile("file.csv", content, content_type="text/plain")
        response = self.client.post(url, {"file": file, 'user_email': "som@example.com"}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_for_file_upload_does_not_accept_non_csv_file(self):
        url = reverse('api:file_upload')
        file = SimpleUploadedFile("file.txt", b'sdas', content_type="text/plain")
        response = self.client.post(url, {"file": file, 'user_email': "som@example.com"}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

