from django.urls import path, include
from .app_view import AppInfoView
from .views import MobileShare
appinfo = AppInfoView()
share = MobileShare()
urlpatterns = {
    path("api/", include([
        path("app/", include([
            path("applist", appinfo.get_app_list),
            path("appinfo", appinfo.get_page_all_data)

        ])),
        path("mobile/", include([
            path("brand", share.get_brand_list),
            path("brandshare",share.get_brand_share),
            path("mobiletype",share.get_mobile_type),
            path("mobileshare",share.get_mobiletype_share),

        ])),

    ])),

}
