from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Brand
from django.http import HttpResponse
from .serializers import BrandSerializer
# from app.mixins import ModelViewSet #soit on le crée soit ça tej

# from rest_framework import mixins

#résoudre import


# class BrandViewSet(ModelViewSet):
#     serializer_class = None
#     permission_classes = (None,)
#     queryset = Brand.objects.all()

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         return queryset

# def brands(request):
#     brands = Brand.objects.all()
#     return render(request, 'app/brands.html', {'brands': brands})

class BrandListView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)