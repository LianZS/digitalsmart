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
            path("brand", share.get_brand_list),  # # 获取品牌数据

            path("brandshare", share.get_brand_share),  # 获取某品牌占有率

            path("mobiletype", share.get_mobile_type),  # 获取机型数据

            path("mobileshare", share.get_mobiletype_share),  # 获取某机型占有率

            path("publicBrandshare", share.get_public_brand_share),  # 公开的品牌数据接口

        ])),

    ])),

}
