from django.urls import path, include

from .scence_data_view import ScenceData

scence = ScenceData()

urlpatterns = {
    path("api/", include([
        path("getScenceDataByTime", scence.interface_historytime_scence_data),
        path("getScenceDataByDate", scence.interface_historydate_scence_data),
        path("getScenceHeatmapDataByTime", scence.interface_hisroty_scence_distribution_data),

    ])),
}
