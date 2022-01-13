from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from education.models import GroupStudent
from .serializer import GrSerializer
from .services import get_one, get_list


class GrView(GenericAPIView):
    serializer_class = GrSerializer
    permission_classes = (AllowAny, )

    def get_object(self, *args, **kwargs):
        try:
            product = GroupStudent.objects.get(id=kwargs['pk'])
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
