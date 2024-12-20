from django.shortcuts import render
from .models import Brand
from django.http import HttpResponse
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

def detail(request, brand_id):
    return HttpResponse("You're looking at brand %s." % brand_id)