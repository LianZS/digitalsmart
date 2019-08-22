from django.urls import path, include

from .views import interface_scence_data

urlpatterns = {
    path("api/", include([
       path("getScenceDataByTime",interface_scence_data),

    ])),



}
