from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("run/", views.run_page, name="run"),
    path("cali/", views.cali_page, name="cali"),
    path("api/action/", views.run_action, name="action"),
    path("api/speed/", views.set_speed, name="speed"),
    path("api/cali/", views.cali_action, name="cali_action"),
    path("api/health/", views.health_check, name="health"),
    re_path(
        r"^static/(?P<path>.*)$",
        serve,
        {"document_root": settings.STATICFILES_DIRS[0]},
    ),
]
