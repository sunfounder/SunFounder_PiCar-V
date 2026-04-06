from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("run/", views.run_page, name="run"),
    path("cali/", views.cali_page, name="cali"),
    path("api/action/", views.run_action, name="action"),
    path("api/speed/", views.set_speed, name="speed"),
    path("api/cali/", views.cali_action, name="cali_action"),
    path("api/health/", views.health_check, name="health"),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
