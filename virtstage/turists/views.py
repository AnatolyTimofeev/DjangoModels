from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from .models import *
from .serializers import PerevalAddedSerializer


class PerevalAddedAPI(generics.ListCreateAPIView):
    queryset = PerevalAdded.objects.all()
    serializer_class = PerevalAddedSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        id = serializer.data['id']
        return Response(f'status 201 - успех, id = {id}', status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        try:
            data = self.list(request, *args, **kwargs)
            return data
        except Exception as e:
            response_data = {
                'status': 'error -500 :Ошибка подключения к базе',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            response_data = {

                'status': 'error -400 :Bad Request',
                'message': str(e),
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



