from django.urls import reverse
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


