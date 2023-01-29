import json

from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, DeleteView, CreateView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category
from ads.permissions import IsAdOrAuthorStaff
from ads.serializers import AdSerializer, AdDetailSerializer, AdListSerializer

from users.models import User


class AdPagination(PageNumberPagination):
    page_size = 5


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by("-price")
    default_serializer = AdSerializer
    serializer_class = {
        "retrieve": AdDetailSerializer,
        "list": AdListSerializer
    }

    default_permission = [AllowAny()]
    permission_list = {
                       "retrieve": [IsAuthenticated(), IsAdOrAuthorStaff()],
                       "update": [IsAuthenticated(), IsAdOrAuthorStaff],
                       "partial_update": [IsAuthenticated(), IsAdOrAuthorStaff()],
                       "destroy": [IsAuthenticated(), IsAdOrAuthorStaff()]
                       }
    pagination_class = AdPagination

    def get_serializer_class(self):
        return self.serializer_class.get(self.action, self.default_serializer)

    def get_permissions(self):
        return self.permission_list.get(self.action, self.default_permission)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist("cat")
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get("price_from")
        price_to = request.GET.get("price_to")

        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)

        try:
            ad = Ad.objects.create(
                name=ad_data["name"],
                author_id=ad_data["author"],
                price=ad_data["price"],
                description=ad_data["description"],
                is_published=ad_data["is_published"],
                category_id=ad_data["category"],
                image=ad_data["image"]
            )
        except IntegrityError:
            return HttpResponseBadRequest("Bad request, check category or user is available")

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category": ad.category.name,
            "image": ad.image.url if ad.image else None
        }, status=201)


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        self.object.author = get_object_or_404(User, username=ad_data["username"])
        self.object.category = get_object_or_404(Category, name=ad_data["category"])
        self.object.price = ad_data["price"]
        self.object.is_published = ad_data["is_published"]
        self.object.description = ad_data["description"]
        self.object.name = ad_data["name"]

        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author": self.object.author.username,
                "price": self.object.price,
                "description": self.object.description,
                "is_published": self.object.is_published,
                "category": self.object.category.name
            }, safe=False, json_dumps_params={'ensure_ascii': False}
        )

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ad_data = json.loads(request.body)

        if "id" in ad_data:
            self.object.id = ad_data.get("id")
        if "name" in ad_data:
            self.object.name = ad_data.get("name")
        if "author" in ad_data:
            self.object.author = ad_data.get("author")
        if "price" in ad_data:
            self.object.price = ad_data.get("price")
        if "description" in ad_data:
            self.object.description = ad_data.get("description")
        if "is_published" in ad_data:
            self.object.is_published = ad_data.get("is_published")
        if "category" in ad_data:
            self.object.category_id = ad_data.get("category")

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category.name
        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = 'ad/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=204)


@method_decorator(csrf_exempt, name='dispatch')
class ImageUploadView(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
                "author": self.object.author.username,
                "price": self.object.price,
                "description": self.object.description,
                "is_published": self.object.is_published,
                "category": self.object.category.name,
                "image": self.object.image.url
            }
        )
