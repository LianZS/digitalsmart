from django.urls import path
from .views import cityList, scenceList, scenceflowData

urlpatterns = {
    path("api/getCitysByProvince", cityList),
    path("api/getRegionsByCity", scenceList),
    path("api/getLocation_uv_percent_new", scenceflowData),
}
