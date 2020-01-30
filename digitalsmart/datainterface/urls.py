from django.urls import path, include

from .scenic_data_view import ScenicDataDetail
from .traffic_data_view import CityTrafficDetail
from .mobile_data_view import MobileDataDetail
# from .specile_function_view import Crack
from .weather_data_view import WeatherData

# crack = Crack()
weather = WeatherData()
urlpatterns = {
    path("api/", include([
        path("getScenceDataByTime", ScenicDataDetail.interface_get_historytime_scence_queryset),  # 获取景区某时刻人流
        path("getScenceDataByDate", ScenicDataDetail.interface_get_historydate_scence_queryset),  # 获取景区某天人流
        path("getScenceHeatmapDataByTime", ScenicDataDetail.interface_get_hisroty_distribution_queryset),  # 获取景区某时刻人流分布情况
        # path("getMusic", crack.get_music_play_list),  # 搜索音乐
        # path("getMusicAsy", crack.get_music),  # 搜索音乐
        #
        # path("getMusicResult", crack.get_result_music_list),  # 搜索音乐
        #
        # path("downMusic", crack.down_music),  # 下载音乐
        # path("validation", crack.identity_authentication),  # 身份认证
        # # path("baidudoc", crack.down_baidu_doc),  # 百度文档下载
        # path("getGoodsPrice", crack.get_goods_price_change),  # 提交获取商品价格变化请求
        # path("getGoodsPriceResult", crack.get_goods_price_change_result),  # 获取商品价格变化结果
        #
        # path("goodsinfo", crack.get_goods_info),  # 获取商品卖家画像
        # path("uploadPDF", crack.upload_pdf),  # 上传pdf文件，解析成doc
        # path("getDocLink", crack.get_doc_down_url),  # 获取转换后的doc下载链接
        # path("downDocLink", crack.down_doc),  # 获取转换后的doc下载链接
        # path("analyse", crack.analyse_url),  # 请求分析链接里的中文文本关键词以及频率
        # path("analyseResult", crack.get_analyse_result),  # 文本分析结果
        path("getCitydailyIndex", CityTrafficDetail.get_daily_traffic_index_queryset),  # 城市交通延迟指数
        path("getCityRoadlist", CityTrafficDetail.get_road_list__queryset),  # 城市实时拥堵道路前10名
        path("getCityMonthsTraffic", CityTrafficDetail.get_city_year_traffic__queryset),  # 城市实时拥堵道路前10名
        path("getCityAirState", CityTrafficDetail.get_city_air_queryset),  # 城市空气指标
        path("getBrandShare", MobileDataDetail.get_public_brand_share_queryset),  # 获取固定的公开品牌占有率数据
        path("getMobileSystemShare", MobileDataDetail.get_mobile_system_rate_queryset),  # 获取手机系统占有率数据
        path("getOperatorShare", MobileDataDetail.get_operator_rate_queryset),  # 获取运营商占有率数据
        path("getNetShare", MobileDataDetail.get_network_rate__queryset),  # 获取网络占有率数据
        path("getWeather", weather.get_hisroty_day_weather),  # 获取某天历史天气数据
        path("getMonthWeather", weather.get_hisroty_month_weather),  # 获取某月历史天气数据
        # path("getUrlKeyword", crack.get_keyword),  # 获取链接关键词

    ])),
}
