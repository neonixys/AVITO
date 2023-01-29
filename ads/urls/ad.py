from django.urls import path
from rest_framework.routers import SimpleRouter

from ads.views.ad import *

router = SimpleRouter()
router.register('ad', AdViewSet)

urlpatterns = [

    path('<int:pk>/upload_image/', ImageUploadView.as_view()),
]

router = SimpleRouter()
router.register('', AdViewSet)
urlpatterns += router.urls
