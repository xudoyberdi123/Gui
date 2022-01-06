from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound

from geo.models import Region
from .services import list_regions, one_region
from .serializers import RegionSerializer


class RegionView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegionSerializer

    def get_object(self, *args, **kwargs):
        try:
            product = Region.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('not found region')
        return product

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs and kwargs['pk']:
            result = one_region(request, kwargs['pk'])
        else:
            result = list_regions(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(serializer.data)
        result = one_region(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def put(self, request, *args, **kwargs):
        region = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=region, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = one_region(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        self.get_object(*args, **kwargs).delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
