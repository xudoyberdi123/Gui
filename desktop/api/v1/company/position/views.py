from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.v1.company.position.services import get_one, get_list
from api.v1.company.position.serializer import PositionSerializer
from company.models import Position


class PosView(GenericAPIView):
    serializer_class = PositionSerializer
    permission_classes = (AllowAny, )

    def get_object(self, *args, **kwargs):
        try:
            product = Position.objects.get(id=kwargs['pk'])
        except Exception as e:
            raise NotFound('not found region')
        return product

    def get(self, request, *args, **kwargs):
        if "pk" in kwargs and kwargs['pk']:
            result = get_one(request, kwargs['pk'])
        else:
            result = get_list(request)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.create(serializer.data)
        result = get_one(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def put(self, request, *args, **kwargs):
        region = self.get_object(*args, **kwargs)
        serializer = self.get_serializer(data=request.data, instance=region, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        result = get_one(request, data.pk)
        return Response(result, status=status.HTTP_200_OK, content_type='application/json')

    def delete(self, request, *args, **kwargs):
        self.get_object(*args, **kwargs).delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
