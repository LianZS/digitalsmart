from django.urls import path, include
from .app_view import AppInfoView

appinfo = AppInfoView()

urlpatterns = {
    path("api/", include([
        path("app/", include([
            path("applist", appinfo.get_app_list),
            path("appinfo", appinfo.get_page_all_data)

        ])),

    ])),

}
