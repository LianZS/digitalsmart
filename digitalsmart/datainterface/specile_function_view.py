import uuid
import os
import pickle
from threading import Thread
from multiprocessing import Process
from typing import List
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.http import StreamingHttpResponse, JsonResponse
from .models import PDFFile
from digitalsmart.settings import redis_cache
from datainterface.tasks import NetWorker
from attractions.tool.file_hander import Hander_File
from datainterface.function.analyse import UrlDocAnalyse
from datainterface.function.conversion_file import ConversionFile
from datainterface.function.keyword_weight import KeyWordWeight
from datainterface.function.conversion_file import PageType, FileType
from digitalsmart.celeryconfig import app


class Crack:
    """
    下面是付费音乐下载功能
    """

    @staticmethod
    def get_music_play_list(request):
        """
        下面是针对单核服务器对异步耗时操作吃不消
        :param request:
        :return:
        """
        music_name = request.GET.get("name")  # 音乐名
        soft_type = request.GET.get("type")  # 软件类型，netease：网易云，qq：qq音乐，kugou：酷狗音乐，kuwo：酷我，
        # xiami：虾米，baidu：百度，1ting：一听，migu：咪咕，lizhi：荔枝，
        # qingting：蜻蜓，ximalaya：喜马拉雅，kg：全民K歌，5singyc：5sing原创，
        # 5singfc：5sing翻唱
        page = request.GET.get("page")  # 第几页
        if page is None:
            page = 1
        try:
            page = int(page)
        except Exception:
            return JsonResponse({"status": 0, "message": "error"})

        if not music_name:
            return JsonResponse({"status": 0, "message": "error"})

        net = NetWorker()
        music_list = net.get_music_list(music_name, soft_type, page, cache=False)
        return JsonResponse({"data": music_list})

    @staticmethod
    def get_music(request):
        """
        针对性能比较好的服务器使用异步
        提交搜索音乐列表请求--链接格式：
        http://127.0.0.1:8000/interface/api/getMusicAsy?name=我愿意平凡的陪在你身旁&type=netease
        #netease：网易云，qq：qq音乐，kugou：酷狗音乐，kuwo：酷我，
        # xiami：虾米，baidu：百度，1ting：一听，migu：咪咕，lizhi：荔枝，
        # qingting：蜻蜓，ximalaya：喜马拉雅，kg：全民K歌，5singyc：5sing原创，
        # 5singfc：5sing翻唱
        返回{"result": "success"}
        {'author': '作者', 'url': '下载链接', 'title': '歌名'}
        :param request:
        :return:
        """
        music_name = request.GET.get("name")  # 音乐名
        soft_type = request.GET.get("type")  # 软件类型，netease：网易云，qq：qq音乐，kugou：酷狗音乐，kuwo：酷我，
        # xiami：虾米，baidu：百度，1ting：一听，migu：咪咕，lizhi：荔枝，
        # qingting：蜻蜓，ximalaya：喜马拉雅，kg：全民K歌，5singyc：5sing原创，
        # 5singfc：5sing翻唱
        page = request.GET.get("page")  # 第几页
        if page is None:
            page = 1
        try:
            page = int(page)
        except Exception:
            return JsonResponse({"status": 0, "message": "error"})

        if not music_name:
            return JsonResponse({"status": 0, "message": "error"})

        redis_key = "{soft_type}:{name}:{page}".format(soft_type=soft_type, name=music_name, page=page)
        key_exits = redis_cache.exit_key(key=redis_key)  # 检测是否是否该key，存在就不用再请求一遍了，直接返回
        if key_exits:
            return JsonResponse({"result": "success"})
        else:
            net = NetWorker()
            Thread(target=net.get_music_list, args=(music_name, soft_type, page, True)).start()
            # net.get_music_list.delay(net,music_name, soft_type, page)  # 请求获取所有与之相关的音乐，包括下载链接
            return JsonResponse({"result": "success"})

    @staticmethod
    def get_result_music_list(request):
        """
        获取搜索音乐列表 ---链接格式：
        http://127.0.0.1:8000/interface/api/getMusicResult?name=%E6%8A%A4%E8%8A%B1%E4%BD%BF%E8%80%85&type=netease
        :param request:
        :return:
        """
        music_name = request.GET.get("name")  # 音乐名
        soft_type = request.GET.get("type")  # 软件类型，
        page = request.GET.get("page")  # 第几页
        if page is None:
            page = 1
        try:
            page = int(page)
        except Exception:
            return JsonResponse({"status": 0, "message": "error"})
        redis_key = "{soft_type}:{name}:{page}".format(soft_type=soft_type, name=music_name, page=page)
        response = redis_cache.get(name=redis_key)
        music_list = list(response)[0]
        return JsonResponse({"data": music_list})

    @staticmethod
    def down_music(request):
        """
            下载音乐，根据上面get_result_music_list的链接下载 ---链接格式：
         http://127.0.0.1:8000/interface/api/downMusic?url=下载链接

        :param request:
        :return:
        """
        # 解析获取下载链接
        dowun_url = request.POST.get("url")

        if dowun_url is None:
            return JsonResponse({"status": 0, "message": "error"})

        strem = NetWorker.down_music_content(url=dowun_url)
        response = StreamingHttpResponse(strem)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="example.mp3"'

        return response

    @staticmethod
    def identity_authentication(request):
        """
        身份认证---链接格式：
        # http://127.0.0.1:8000/interface/api/validation?card=440514199804220817
        :param request:
        :return:
        """

        idcard = request.GET.get("card")

        person_info = NetWorker().get_idcard_info(idcard)

        response = {
            "发证地区": person_info.area,
            "电话区号": person_info.phone,
            "出生日期": person_info.bir,
            "农历": person_info.lunar,
            '性别/生肖': person_info.gender,
            '当地经纬度': person_info.latlon
        }
        return JsonResponse(response)

    """
    下面是获取商品历史信息
    """

    @staticmethod
    @csrf_exempt
    def get_goods_price_change(request):
        """
        请求某商品的价格变化情况--链接格式：
        http://127.0.0.1:8000/interface/api/getGoodsPrice?url=目标商品链接&token=bGlhbnpvbmdzaGVuZw==
        支持天猫(detail.tmall.com、detail.m.tmall.com)、淘宝(item.taobao.com、h5.m.taobao.com)、
        京东(item.jd.com、item.m.jd.com)、一号店(item.yhd.com）、苏宁易购(product.suning.com)、
        网易考拉(goods.kaola.com)、当当网(product.dangdang.com)、亚马逊中国(www.amazon.cn)、国美(item.gome.com.cn)等电商
        商品详情的历史价格查询。

        """
        token = request.POST.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})

        url = request.POST.get("url")
        if url is None:
            return JsonResponse({"status": 0, "message": "error"})
        redis_key = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
        check_redis = redis_cache.exit_key(redis_key)  # 检测是否是否该key，存在就不用再请求一遍了，直接返回
        if check_redis:
            return JsonResponse({"result": "success"})
        else:
            net = NetWorker()
            Thread(target=net.get_goods_price_change, args=(url)).start()
            # net.get_goods_price_change.delay(url)  # 获取价格变化情况

            return JsonResponse({"result": "success"})

    @staticmethod
    @csrf_exempt
    def get_goods_price_change_result(request):
        """
        获取取得的请求某商品的价格变化情况结果---链接格式：
        http://127.0.0.1:8000/interface/api/getGoodsPriceResult?url=目标商品链接&token=bGlhbnpvbmdzaGVuZw==
        :param request:
        :return:
        """
        token = request.POST.get("token")
        if token != "bGlhbnpvbmdzaGVuZw==":
            return JsonResponse({"status": 0, "message": "appkey错误"})

        url = request.POST.get("url")
        if url is None:
            return JsonResponse({"status": 0, "message": "error"})
        redis_key = str(uuid.uuid5(uuid.NAMESPACE_URL, url))
        data = redis_cache.get(name=redis_key).__next__()
        return JsonResponse({'data': data})

    @staticmethod
    def get_goods_info(request):
        """
        获取商品卖家画像---链接格式：
        http://127.0.0.1:8000/interface/api/goodsinfo?url=目标商品链接
        支持天猫(detail.tmall.com、detail.m.tmall.com)、淘宝(item.taobao.com、h5.m.taobao.com)、
        京东(item.jd.com、item.m.jd.com)、一号店(item.yhd.com）、苏宁易购(product.suning.com)、
        网易考拉(goods.kaola.com)、当当网(product.dangdang.com)、亚马逊中国(www.amazon.cn)、国美(item.gome.com.cn)等电商
        商品详情的历史价格查询。
        :param request:
        :return:
        """
        pre_path = request.path + "?url="
        href = request.get_full_path()
        url = href.replace(pre_path, "")  # 防止url后带有各类特殊符号导致与目标链接不匹配

        if url is None:
            return JsonResponse({"status": 0, "message": "error"})
        try:
            info = NetWorker.get_goods_info(url)  # 获取商品卖家画像
        except Exception:
            info = []
        response = {
            "data": info
        }
        return JsonResponse(response)

    """
    下面是pdf转为doc功能
    """

    @staticmethod
    @csrf_exempt
    def upload_pdf(request):
        """
        上传pdf文件，将其转为doc格式，并存在pdfdb数据库中--链接格式：
        http://127.0.0.1:8000/interface/api/uploadPDF?pdf=文件&pagetype=页码选择类型&type=转换格式&page=需要转换的页面
        pagetype：   every：转换每一页
                    singular：转换奇数页
                    even：转换偶数页
                    specified：指定页转换,若为此选项，需要分析要转换哪些页，页码或者用逗号分隔的页码范围（例如：1,3-5，8,9表示要转换1,
                                                                                                3,4,5,8,9）
        type转换类型有:  docx,doc
        page   如1,3-5，8,9表示要转换1,3,4,5,8,9这几页

        :param request:
        :return:
        """
        page_type = request.POST.get("pagetype")
        exchange_type = request.POST.get("type")
        page = request.POST.get('page')
        if not page:  # 在非指定页面情况下为，空的时候默认全部转化
            page = '1'
        pdf_file = request.FILES.get('pdf')
        # 预防同一个文件不同操作导致IO出错,只要其中一个参数不同就会导致新文件产生，如果存在了该uuid，则说明解析完了
        filename = pdf_file.name + str(page_type) + str(exchange_type) + str(page)

        # 文件类型是否符合要求
        if pdf_file.content_type == "application/pdf":
            # 产生一个用户访问凭证，并且用来下载解析好的文件

            uid = uuid.uuid5(uuid.NAMESPACE_DNS, filename)
            key_exits: bool = redis_cache.exit_key(str(uid))
            if key_exits:  # 已经存在该文件了
                return JsonResponse({"message": "success", "code": 1, "id": uid})
            else:
                conversion_file = ConversionFile()
                judge_pagetype = PageType.EVERY
                file_type = FileType.DOCX
                if page_type == "every":
                    judge_pagetype = PageType.EVERY
                if page_type == "even":
                    judge_pagetype = PageType.EVEN
                if page_type == "singular":
                    judge_pagetype = PageType.SINGULAR
                if page_type == "specified":
                    judge_pagetype = PageType.SPECIFIED
                if exchange_type == "doc":
                    file_type = FileType.DOC
                if exchange_type == "docx":
                    file_type = FileType.DOCX

                # 解析pdf
                pdf = PDFFile()
                pdf.id = uid
                pdf.create_time = timezone.now()
                pdf.to_file_type = exchange_type
                save_file_name = str(uid) + ".pdf"
                pdf.file.save(save_file_name, pdf_file, save=True)
                pdf.save()
                file_path = pdf.file.path
                plane = 1  # 根据服务器性能选择方案，方案2速度更快，消耗也大
                if plane == 2:

                    conversion_file.pdf_parse_to_docx.delay(conversion_file, file_path, uid, judge_pagetype, file_type,
                                                            page)
                elif plane == 1:
                    command = "python datainterface/function/conversion_file.py  {file_path} {uid} {judge_pagetype}" \
                              " {file_type} {page} ".format(file_path=file_path, uid=uid, judge_pagetype=judge_pagetype,
                                                            file_type=file_type, page=page)
                    Process(target=os.system, args=(command,)).start()
                # Thread(target=conversion_file.pdf_parse_to_docx,
                #        args=(uid, judge_pagetype, file_type, page)).start()

                # code为1表示正常，0表示文件类型有误
                return JsonResponse({"message": "success", "code": 1, "id": uid})
        return JsonResponse({"code": 0, "message": "error"})

    @staticmethod
    def get_doc_down_url(request):
        """获取转后的doc文件---链接格式：
        http://127.0.0.1:8000/interface/api/getDocLink?id=7ca7ab45061b554c928ff45c2f5baa2f"""
        # 只有p为100，且code为1时表示可以下载咯
        uid = request.GET.get("id")
        check_redis = redis_cache.exit_key(key=uid)
        if check_redis:
            return JsonResponse({"code": 1, "p": 100})  # 通知可以下载咯

        else:
            return JsonResponse({"code": 0, "p": 10})  # 只有p为100，且code为1时表示可以下载咯

    @staticmethod
    def down_doc(request):
        """下载doc文件  --链接格式：
        http://127.0.0.1:8000/interface/api/downDocLink?id=7ca7ab45061b554c928ff45c2f5baa2f"""

        uid = request.GET.get("id")
        try:
            file_info = PDFFile.objects.get(id=uid)
        except ValidationError:
            return JsonResponse({"code": 0, "p": "不存在该文件"})  # 只有p为100，且code为1时表示可以下载咯
        doc_type: str = file_info.to_file_type
        pdf_path: str = file_info.file.path
        target_file_path = pdf_path.replace(".pdf", "." + doc_type)
        doc = open(target_file_path, 'rb')

        iter_chuncks = Hander_File().hander_file(doc)
        response = StreamingHttpResponse(iter_chuncks)
        response['Content-Type'] = 'application/octet-stream'

        response['Content-Disposition'] = 'attachment;filename={0}.doc'.format(uid)
        return response

    @staticmethod
    @csrf_exempt
    def analyse_url(request):
        """
        提取中文文本关键词以及频率---链接格式：
        http://127.0.0.1:8000/interface/api/analyse?allowPos=a&url=https://blog.csdn.net/hhtnan/article/details/76586693
         url:请求链接
         allowpos:词性
        :return:
        Ag 形语素
        a 形容词
        m 数词
        n 名词
        nr 人名
        ns 地名
        t 时间词
        v 动词
        z 状态词
        .....
        :param request:
        :return:
        """
        if request.method == "POST":
            pos = request.POST.get("allowPos")  # 获取词性
            url = request.POST.get("url")
            if not (pos and url):
                return JsonResponse({"error": "请求参数有问题"})
            uid = uuid.uuid5(uuid.NAMESPACE_URL, url + pos)  # 作为下载获取数据请求的凭证
            key_exit = redis_cache.exit_key(str(uid))  # 检测是否是否该key，存在就不用再请求一遍了，直接返回
            plan = 1  # 觉得要使用那种异步方案，1表示在内存不够时自定义异步，2表示使用celery异步
            if key_exit:
                return JsonResponse({"code": 1, "p": 1, "id": uid})
            else:

                if url is None or pos is None:
                    return JsonResponse({"p": 0, "id": "", "code": 0})

                if plan == 1:
                    # 下面的url一定要使用单引号扣起来，因为链接里会有一些特殊字符，导致os以为只有单个参数
                    cmd = " python datainterface/function/analyse.py  '{url}'  {allowpos} {uid} ".format(url=url,
                                                                                                         allowpos=pos,
                                                                                                         uid=str(uid))
                    Process(target=os.system, args=(cmd,)).start()
                    # Thread(target=os.system, args=(cmd,)).start()
                elif plan == 2:
                    ad = UrlDocAnalyse()
                    uid = ad.analyse_url_info.delay(url, pos)
                    uid = str(uid)
            return JsonResponse({"code": 1, "p": 1, "id": uid})
        else:
            return JsonResponse({"error": "请求方式有误"})

    @staticmethod
    def get_analyse_result(request):
        """
        获取文本解析结果
        http://127.0.0.1:8000/interface/api/analyseResult?id=68813627-8234-5a1b-8449-4945a1c75bf5
        :param request:
        :return:
        """
        task_uid = request.GET.get("id")
        if task_uid is None:
            return JsonResponse({"code": 0, "p": 10})  # 只有p为100，且code为1时表示可以获取数据，否则继续请求
        redis_data = redis_cache.get(task_uid).__next__()  # 先查看redis里有没有直接缓存数据
        analyse_result = None
        analyse_result_data_list = list()

        if redis_data:  # 有的话获取
            analyse_result: List[KeyWordWeight] = pickle.loads(redis_data)
        else:  # 没有的话说明该key是任务id，而不是数据缓存id，所以应该看看celery里任务是否完成了
            try:
                task_state = app.AsyncResult(task_uid).ready()  # 这个需要启动celery才能用
            except AttributeError:
                task_state = None
            if not task_state:
                return JsonResponse({"code": 0, "p": 10})  # 只有p为100，且code为1时表示可以获取数据，否则继续请求
            else:
                analyse_result = app.AsyncResult(task_uid).result
        for keyword_weight in analyse_result:
            analyse_result_data_list.append([keyword_weight.word, keyword_weight.weight])
        return JsonResponse({"data": analyse_result_data_list})
