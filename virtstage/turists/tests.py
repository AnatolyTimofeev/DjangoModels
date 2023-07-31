import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from turists.models import PerevalAdded
from turists.serializers import PerevalAddedSerializer
from turists.views import PerevalAddedAPI


class PerevalApiTests(APITestCase):


    def setUp(self):


        self.data = {
            "raw_data": {
                "beautyTitle": "Testпер. ",
                "title": "Test",
                "other_titles": "222222222",
                "connect": "",
                "add_time": "2021-09-22 13:18:13",

                "coords": {
                    "latitude": "45.3842",
                    "longitude": "7.1525",
                    "height": "1200"
                },
                "level": {
                    "winter": "",
                    "summer": "1А",
                    "autumn": "1А",
                    "spring": ""
                }
            },

            "images":
                [
                    {
                        "id": 1,
                        "title": "1111111111111111111111"
                    },
                    {
                        "id": 2,
                        "title": "2222222222222"
                    }
                ],
            "user": {

                "phone": "79031234567",
                "fam": ":Test",
                "name": "Василий",
                "otc": "Иванович"
            },
            "user_email": "testuser@email.tld"

        }

        PerevalAdded.objects.create(**self.data)

    def test_create_API_Pereval(self):

        response = self.client.post('/api/v1/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_list_email_Api_Pereval(self):
        response = self.client.get('/api/v1/get/?user_email=testuser@email.tld',  format='json')
        obj = PerevalAdded.objects.first()
        serializer = PerevalAddedSerializer(obj)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),[serializer.data])

    def test_detail_Pereval_Api(self):
        obj = PerevalAdded.objects.first()
        serializer = PerevalAddedSerializer(obj)
        id = serializer.data['id']
        response = self.client.get(reverse('detail_api', kwargs={'pk':id}),format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)













