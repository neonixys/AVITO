import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, UpdateView, DeleteView, CreateView

from Avito_DZ28 import settings
from users.models import User, Location


class UserListView(ListView):
    model = User
    queryset = User.objects.annotate(
        total_ads=Count("ad", filter=Q(ad__is_published=True))
    ).order_by('-username').prefetch_related("location")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "first_name": user.first_name,
                "username": user.username,
                "last_name": user.last_name,
                "password": user.password,
                "role": user.role,
                "total_ads": user.total_ads,
                "age": user.age,
                "location": [loc.name for loc in user.location.all()],
            })
        response = {
            "total": page_obj.paginator.count,
            "num_pages": page_obj.paginator.num_pages,
            "items": users
        }

        return JsonResponse(response, safe=False)


class UserDetailView(DetailView):
    model = User

    def get(self, requests, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": [loc.name for loc in user.location.all()]

        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            username=user_data.get("username"),
            password=user_data.get("password"),
            role=user_data.get("role"),
            age=user_data.get("age"))

        locations = user_data.get("locations")

        if locations:
            for loc_name in user_data.get("locations"):
                loc, created = Location.objects.get_or_create(name=loc_name)
                user.location.add(loc)

        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "locations": [loc.name for loc in user.location.all()]

        }, safe=False, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        if "first_name" in user_data:
            self.object.first_name = user_data.get("first_name")
        if "last_name" in user_data:
            self.object.last_name = user_data.get("last_name")
        if "username" in user_data:
            self.object.username = user_data.get("username")
        if "age" in user_data:
            self.object.age = user_data.get("age")

        if "locations" in user_data:
            self.object.location.all().delete()
            for loc_name in user_data.get("locations"):
                loc, created = Location.objects.get_or_create(name=loc_name)
                self.object.location.add(loc)

        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "locations": [loc.name for loc in self.object.location.all()]

        }, safe=False, json_dumps_params={'ensure_ascii': False})

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        user_data = json.loads(request.body)

        self.object.username = user_data["username"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.description = user_data["age"]
        self.object.location.all().delete()
        for loc_name in user_data.get("locations"):
            loc, created = Location.objects.get_or_create(name=loc_name)
            self.object.location.add(loc)

        return JsonResponse(
            {
                "username": self.object.username,
                "first_name": self.object.first_name,
                "last_name": self.object.last_name,
                "age": self.object.age,
                "description": self.object.description,
                "locations": [loc.name for loc in self.object.location.all()]
                }, safe=False, json_dumps_params={'ensure_ascii': False}
        )


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=204)
