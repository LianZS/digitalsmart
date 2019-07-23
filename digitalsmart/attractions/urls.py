from django.urls import path
from .views import scencelist

urlpatterns = {
    path("test/", scencelist),
}
