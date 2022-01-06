from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from geo.models import District
from .services import list_district, one_district
from .serializers import DistrictSerializer


class DistrictView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = DistrictSerializer

    def get_object(self, *args, **kwargs):
        try:
            product = District.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('not found district')
        return product

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs and kwargs['pk']:
            result = one_district(request, kwargs['pk'])
        else:
            result = list_district(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(serializer.data)
        result = one_district(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def put(self, request, *args, **kwargs):
        district = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=district, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = one_district(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        self.get_object(*args, **kwargs).delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
