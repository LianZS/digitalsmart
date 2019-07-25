from django.urls import path
from .views import citylist, scencelist, scenceflow_data, scenceflow_trend, \
    search_heat, scence_people_distribution, scence_geographic

urlpatterns = {
    path("api/getCitysByProvince", citylist),
    path("api/getRegionsByCity", scencelist),
    path("api/getLocation_pn_percent_new", scenceflow_data),
    path("api/getLocation_trend_percent_new", scenceflow_trend),
    path("api/getLocation_search_rate", search_heat),
    path("api/getLocation_distribution_rate", scence_people_distribution),
    path("api/getLocation_geographic_bounds", scence_geographic),


}
